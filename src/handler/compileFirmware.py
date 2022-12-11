import copy
import tempfile
import os
import shlex
import subprocess



def compileFirmware(mainFile, headerFile, device_name):
  res = None
  #deletes everything automatically at end of with
  with tempfile.TemporaryDirectory() as tempdir:
    dir = 'src'
    path = os.path.join(tempdir, dir)
    os.mkdir(path)
    #copy files into tempdir
    tmpdir_name = os.path.basename(os.path.normpath(tempdir))
    with open(f'{tempdir}/{tmpdir_name}.ino', "a+") as main_write:
      main_write.write(mainFile)
    with open(f'{tempdir}/src/header_cpp.hpp', "a+") as header_write:
      header_write.write(headerFile) 
    
    success = compile(tempdir, tmpdir_name, device_name)
    if success:
      with open(f'{tempdir}/{tmpdir_name}.ino.bin', "rb") as createdBinary_read:
        binaryFirmwareRead = createdBinary_read.read()
        binaryFirmware = copy.deepcopy(binaryFirmwareRead)
      res = binaryFirmware
  return res    

def createArduinoCliCall(tmpdir, tmpdir_name, device_name):
  if device_name == 'nicla':
    return f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b arduino:mbed_nicla:nicla_sense {tmpdir}/{tmpdir_name}.ino'
  elif device_name == 'nano':
     return f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b arduino:mbed_nano:nano33ble {tmpdir}/{tmpdir_name}.ino'
  elif device_name == 'xiao':
    return f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b Seeeduino:mbed:xiaonRF52840Sense  {tmpdir}/{tmpdir_name}.ino' 

    

def compile(tempdir, tmpdir_name, device_name):
  arduino_cli_cmd = shlex.split(createArduinoCliCall(tempdir, tmpdir_name, device_name))
  process = subprocess.Popen(arduino_cli_cmd)
  #busy loop (non-blocking) implementation with subprocess.wait()
  process.wait()
  success = process.returncode == 0
  return success
