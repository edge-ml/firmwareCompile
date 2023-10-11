import os

def createArduinoCliCall(tmpdir, device_name):
    if device_name == 'nicla':
        cmd = f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b arduino:mbed_nicla:nicla_sense {tmpdir}/main.ino'
    elif device_name == 'nano':
        cmd = f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b arduino:mbed_nano:nano33ble {tmpdir}/main.ino'
    elif device_name == 'xiao':
        cmd = f'arduino-cli compile --export-binaries --output-dir {tmpdir} -b Seeeduino:mbed:xiaonRF52840Sense  {tmpdir}/main.ino' 
    print("Arduino CLI command:", cmd)
    return cmd

def read_ino(tmpdir):
    with open(os.path.join(tmpdir, "main.ino.hex"), "rb") as f:
        firmware = f.read()
    return firmware