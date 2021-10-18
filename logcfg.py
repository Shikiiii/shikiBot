import sys
from datetime import datetime
from logging import *

name = datetime.utcnow().strftime("logs/%Y-%m-%d_%H-%M.log")
c_handler = StreamHandler(sys.stdout)
f_handler = FileHandler(name, 'a', 'utf-8')
c_handler.setLevel(15)
f_handler.setLevel(5)


f_format = Formatter('%(asctime)s\t%(name)s\t%(levelname)s: %(message)s')
f_handler.setFormatter(f_format)


def gLogr(*names: str):
    res = []
    for name in names:
        new_logger = getLogger(name)
        if len(new_logger.handlers) < 2:
            new_logger.setLevel(1)
            new_logger.addHandler(f_handler)
            new_logger.addHandler(c_handler)
        res.append(new_logger)
    if len(res) == 1:
        return res[0]
    return res


discord_client_logger = gLogr('guilded.client')  # hidden by default?

__all__ = ["gLogr"]
