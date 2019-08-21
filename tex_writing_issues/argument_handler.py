import argparse
import custom_log as l

_dir_path: str = None
_file_path: str = None


def get_dir_path() -> str:
    global _dir_path
    if _dir_path:
        return _dir_path
    else:
        _get_arguments()
        return _dir_path


def get_file_path() -> str:
    global _file_path
    if _file_path:
        return _file_path
    else:
        _get_arguments()
        return _file_path


def _get_arguments():
    l.log("parsing arguments")
    global _dir_path
    global _file_path
    parser = argparse.ArgumentParser()

    parser.add_argument('--path',
                        type=str, help='address from where tex files will be scanned')
    parser.add_argument('--file',
                        type=str, help='address of tex file')

    args = parser.parse_args()
    if args.path:
        _dir_path = args.path
        l.log("dir path: " + _dir_path)
    if args.file:
        _file_path = args.file
        l.log("file path: " + _file_path)


