import subprocess
import copy
import tempfile
import os
import shlex



def compileFirmware(mainFile, headerFile):
  binaryFirmware = None
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
    process = subprocess.Popen(shlex.split(createArduinoCliCall(tempdir, tmpdir_name)), stdout=subprocess.PIPE, bufsize=1)
    for line in iter(process.stdout.readline, b''):
      print(line)    
    process.stdout.close()
    process.wait()

    #success
    with open(f'{tempdir}/{tmpdir_name}.ino.bin', "rb") as createdBinary_read:
      binaryFirmwareRead = createdBinary_read.read()
      binaryFirmware = copy.deepcopy(binaryFirmwareRead)
  return binaryFirmware

def createArduinoCliCall(tmpdir, tmpdir_name):
  return f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b arduino:mbed_nicla:nicla_sense {tmpdir}/{tmpdir_name}.ino'