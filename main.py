#!/usr/bin/env python3
import uvicorn 
import multiprocessing as mp
from fastapi import FastAPI, Request, HTTPException, Path, UploadFile, File
from fastapi.responses import PlainTextResponse, Response
from src.handler.compileFirmware import compileFirmware
import zipfile
import os
import shlex
import subprocess
import uuid
import traceback
from io import BytesIO
import shutil

BASE_DIR = "TEMP_COMPILE_FILES"


app = FastAPI()

@app.post("/compileFirmware/{device_name}")
async def postCompileFirmware(request: Request, device_name: str = Path(...)):
    data = await request.json()
    binaryFile = compileFirmware(data["main"], data["header"], device_name)
    if binaryFile == None:
        raise HTTPException(status_code=500, detail="Server could not compile binary from supplied files")

    return Response(binaryFile)


def createArduinoCliCall(tmpdir, device_name):
    if device_name == 'nicla':
        cmd = f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b arduino:mbed_nicla:nicla_sense {tmpdir}/main.ino'
    elif device_name == 'nano':
        cmd = f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b arduino:mbed_nano:nano33ble {tmpdir}/main.ino'
    elif device_name == 'xiao':
        cmd = f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b Seeeduino:mbed:xiaonRF52840Sense  {tmpdir}/main.ino' 
    print("Arduino CLI command:", cmd)
    return cmd


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
            arduino_cli_cmd = shlex.split(createArduinoCliCall(folder, device_name))
            process = subprocess.Popen(arduino_cli_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while True:
                output = process.stdout.readline().decode().strip()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output)
            process.wait()
            if process.returncode != 0:
                raise Exception("Compilation failed")
            with open(os.path.join(folder, "main.ino.hex"), "rb") as f:
                firmware = f.read()
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