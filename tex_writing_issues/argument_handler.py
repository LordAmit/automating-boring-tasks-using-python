import argparse
import custom_log as l

_file_path: str = None
_keyword: str = None

def get_path() -> str:
    global _file_path
    if _file_path:
        return _file_path
    else:
        _get_arguments()
        return _file_path


def get_keyword() -> str:
    global _keyword
    if _keyword:
        return _keyword
    else:
        _get_arguments()
        return _keyword


def get_print_line() -> bool:
    global _print_line
    if _print_line:
        return _print_line
    else:
        _get_arguments()
        return _print_line


def _get_arguments():
    l.log("parsing arguments")
    global _file_path
    global _keyword
    global _ext
    global _print_line

    parser = argparse.ArgumentParser()

    parser.add_argument('--path',
                        type=str, help='address from where tex files will be scanned',
                        required=True)

    args = parser.parse_args()

    _file_path = args.path
    l.log("path: "+_file_path)
