import os.path as path
import os

def extract_filename_wo_ext(address: str) -> str:
    basename = path.basename(address)
    return path.splitext(path.basename(address))[0]

def extract_dir(address: str) -> str:
    return str(path.abspath(address).split(path.basename(address))[0])

def filepath_modified_prefix(address: str, prefix: str= "modified_")-> str:
    address_dir: str = extract_dir(address)
    basename: str = path.basename(address)
    return str(address_dir + prefix + basename)

def extract_ext(address: str):
    return str(path.splitext(path.basename(address))[1])

def check_ext(ext: str):
    extensions = [".bmp", ".jpg", ".png", ".jpeg"]
    return ext in extensions

def remove_file(address: str):
    os.remove(address)