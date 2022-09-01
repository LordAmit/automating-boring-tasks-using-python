import argparse
import custom_log as l

_file_path: str = None
_ignore_keyword: str = None
_backup_path: str = None

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


def get_backup()->str:
    global _backup_path
    if not _backup_path:
        _get_arguments()
    return _backup_path


def _get_arguments():
    l.log("parsing arguments")
    global _file_path
    global _ignore_keyword
    global _backup_path

    parser = argparse.ArgumentParser()
    parser.add_argument('--ignore', type=str, help='keywords to be ignored while parsing files')
    parser.add_argument('--path', type=str, help='address from where images will be pursed', required=True)
    parser.add_argument('--backup', type=str, help='directory path for backing up non-compressed images')
    args = parser.parse_args()
    _file_path = args.path
    _backup_path = args.backup
    if args.ignore:
        _ignore_keyword = args.ignore
