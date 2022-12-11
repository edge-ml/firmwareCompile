#!/usr/bin/env python3
import uvicorn 
import multiprocessing as mp
from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import PlainTextResponse, Response
from src.handler.compileFirmware import compileFirmware

app = FastAPI()

@app.post("/compileFirmware/{device_name}")
async def postCompileFirmware(request: Request, device_name: str = Path(...)):
    data = await request.json()
    binaryFile = compileFirmware(data["main"], data["header"], device_name)
    if binaryFile == None:
        raise HTTPException(status_code=500, detail="Server could not compile binary from supplied files")

    return Response(binaryFile)

mp.set_start_method("forkserver", force=True)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3004)