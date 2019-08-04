import argparse
import custom_log as l

_file_path: str = None
_ignore_keyword: str = None


def get_path() -> str:
    global _file_path
    if _file_path:
        return _file_path
    else:
        _get_arguments()
        return _file_path


def get_ignore_word() -> str:
    global _ignore_keyword
    if _ignore_keyword:
        return _ignore_keyword
    else:
        _get_arguments()
        return _ignore_keyword


def _get_arguments():
    l.log("parsing arguments")
    global _file_path
    global _ignore_keyword

    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore', type=str, help='keywords to be ignored while parsing files')
    parser.add_argument('--path', type=str, help='address from where images will be pursed', required=True)
    args = parser.parse_args()
    _file_path = args.path
    if args.ignore:
        _ignore_keyword = args.ignore
