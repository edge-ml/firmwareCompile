import os
from contextlib import ExitStack
from src.utils.zipfile import zipFiles

def create_emscripten_call_and_preprocess(tmpdir, device_name):
    os.rename(os.path.join(tmpdir, 'model.hpp'), os.path.join(tmpdir, 'model.cpp'))
    if device_name == 'WASM-single-file':
        return f'em++ {tmpdir}/model.cpp -o {tmpdir}/model.js -sMODULARIZE -sSINGLE_FILE --bind'
    elif device_name == 'WASM':
        return f'em++ {tmpdir}/model.cpp -o {tmpdir}/model.js -sMODULARIZE --bind'
    
def read_output(tmpdir, device_name):
    if device_name == 'WASM':
        return zip_outputs(tmpdir)
    elif device_name == 'WASM-single-file':
        return read_single_file(tmpdir)
    
def read_single_file(tmpdir, filename='model.js'):
    with open(os.path.join(tmpdir, filename), 'rb') as file:
        binary = file.read()
    return binary
    
def zip_outputs(tmpdir, filenames=['model.wasm', 'model.js']):
    with ExitStack() as stack:
        files = [
            stack.enter_context(open(os.path.join(tmpdir, filename), 'rb'))
            for filename in filenames
        ]
        zipped = zipFiles(files)
    return zipped
