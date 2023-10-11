#!/usr/bin/env python3
import uvicorn 
import multiprocessing as mp
from fastapi import FastAPI, Request, HTTPException, Path, UploadFile, File
from fastapi.responses import PlainTextResponse, Response
import zipfile
import os
import shlex
import subprocess
import uuid
import traceback
from io import BytesIO
import shutil

import src.handler.wasm as wasm
import src.handler.arduino as arduino

BASE_DIR = "TEMP_COMPILE_FILES"

app = FastAPI()

# TODO we could make this better with classes sometime
def createShellCall(tmpdir, device_name):
    if device_name == "WASM" or \
        device_name == "WASM-single-file":
        return wasm.create_emscripten_call(tmpdir, device_name)
    elif device_name == "nicla" or \
        device_name == "nano" or \
        device_name == "xiao":
        return arduino.createArduinoCliCall(tmpdir, device_name)
    else:
        raise Exception(f'Unknown device: {device_name}')
    
def post_call_read_binary(tmpdir, device_name):
    if device_name == "WASM" or \
        device_name == "WASM-single-file":
        return wasm.read_output(tmpdir, device_name)
    elif device_name == "nicla" or \
        device_name == "nano" or \
        device_name == "xiao":
        return arduino.read_ino(tmpdir)
    else:
        raise Exception(f'Unknown device: {device_name}')

@app.post("/compileFirmware/{device_name}")
async def postCompileFirmware(request: Request, device_name: str = Path(...)):
    data = await request.json()
    binaryFile = compileFirmware(data["main"], data["header"], device_name)
    if binaryFile == None:
        raise HTTPException(status_code=500, detail="Server could not compile binary from supplied files")

    return Response(binaryFile)

@app.post("/compile/{device_name}")
async def compileFirmware(device_name: str, file: UploadFile = File(...)):
    compile_id = str(uuid.uuid4())
    folder = os.path.join(BASE_DIR, compile_id, "main")
    deleteFolder = os.path.join(BASE_DIR, compile_id)
    try:
        content = await file.read()
        with zipfile.ZipFile(BytesIO(content)) as zip_file:
            if not os.path.exists(folder):
                os.makedirs(folder)
            zip_file.extractall(folder)
            shell_cmd = shlex.split(createShellCall(folder, device_name))
            process = subprocess.Popen(shell_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while True:
                output = process.stdout.readline().decode().strip()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output)
            process.wait()
            if process.returncode != 0:
                raise Exception("Compilation failed")
            firmware = post_call_read_binary(folder, device_name)
            response = Response(content=firmware, media_type="application/octet-stream")
            if os.path.exists(folder):
                shutil.rmtree(deleteFolder)
            return response
    except Exception as e:
        if os.path.exists(folder):
            shutil.rmtree(deleteFolder)
        print(e)
        print(traceback.format_exc())
        raise e


mp.set_start_method("forkserver", force=True)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3005)