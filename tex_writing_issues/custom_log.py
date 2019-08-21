import logging
from typing import List, Union
logging.basicConfig(
    level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


def log(s: Union[List, str]):
    if type(s).__name__ == 'str':
        logging.debug(s)
    else:
        temp = ""
        for i in s:
            temp += i + " "
        logging.debug(temp)


def disable():
    logging.disable(logging.CRITICAL)
