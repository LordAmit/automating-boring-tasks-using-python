import argparse
import custom_log as l

_force_run: bool = False
_prefix: str = ''


def force_run() -> bool:
    global _force_run
    if _force_run:
        return _force_run
    else:
        _get_arguments()
        return _force_run


def prefix()->str:
    global _prefix
    if _prefix:
        return _prefix
    else:
        _get_arguments()
        return _prefix


def _get_arguments():
    l.log("parsing arguments")

    global _force_run
    global _prefix
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str,
                        help='specifies the prefix to be used while renaming')
    parser.add_argument(
        '-f', action='store_true', help='force run, will output list of changes while making changes, without this will only output changes')

    args = parser.parse_args()
    _prefix = args.name
    # _file_path = args.path
    _force_run = args.f

    l.log(_prefix)
    l.log(_force_run)
