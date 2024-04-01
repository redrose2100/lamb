import os
import logging
import platform
from pathlib import Path
from concurrent_log_handler import ConcurrentRotatingFileHandler


def get_logger(name, level=logging.INFO, log_path=None):
    sys_name = platform.system()
    if not log_path:
        if sys_name == "Linux":
            os.system(f"mkdir -p /var/log/{name}")
            log_path = f"/var/log/{name}/lambkid.log"
        else:
            log_path = Path(__file__).parent / "lambkid.log"
    handler = ConcurrentRotatingFileHandler(log_path, "a", 512 * 1024, 30)
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'))
    logger = logging.getLogger(name)
    logger.addHandler(console_handler)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger


log = get_logger("lambkid")

if __name__ == "__main__":
    log = get_logger("redrose2100")
    log.debug("test debug log")
    log.info("test info log")
    log.warning("test warning log")
    log.error("test error log")
