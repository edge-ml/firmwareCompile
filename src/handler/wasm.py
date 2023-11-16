import os
from contextlib import ExitStack
from src.utils.zipfile import zipFiles

def create_emscripten_call(tmpdir, device_name):
    if device_name == 'WASM-single-file':
        return f'emcc {tmpdir}/model.cpp -o {tmpdir}/model.js -sMODULARIZE -sSINGLE_FILE -s EXPORTED_FUNCTIONS="[\'_predict\', \'_add_datapoint\']" -s EXPORTED_RUNTIME_METHODS="[\'cwrap\']"'
    elif device_name == 'WASM':
        return f'emcc {tmpdir}/model.cpp -o {tmpdir}/model.js -sMODULARIZE -s EXPORTED_FUNCTIONS="[\'_predict\', \'_add_datapoint\']" -s EXPORTED_RUNTIME_METHODS="[\'cwrap\']"'
    
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
