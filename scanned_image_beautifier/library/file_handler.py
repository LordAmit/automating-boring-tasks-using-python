import os.path as path
import os


def extract_filename_wo_ext(address: str) -> str:
    return path.splitext(path.basename(address))[0]


def extract_dir(address: str) -> str:
    return str(path.abspath(address).split(path.basename(address))[0])


def filepath_modified_suffix(address: str, suffix: str= "_modified")-> str:
    address_dir: str = extract_dir(address)
    filename = extract_filename_wo_ext(address)
    ext = extract_ext(address)
    return str(address_dir + filename + suffix + ext)


def extract_ext(address: str):
    return str(path.splitext(path.basename(address))[1])


def check_ext(ext: str):
    extensions = [".bmp", ".jpg", ".png", ".jpeg"]
    return ext in extensions


def remove_file(address: str):
    os.remove(address)


def change_path_extension(absolute_path_image: str, extension: str) ->str:
    address_dir: str = extract_dir(absolute_path_image)
    filename: str = extract_filename_wo_ext(absolute_path_image)
    return str(address_dir+filename + extension)
