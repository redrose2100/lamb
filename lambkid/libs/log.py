import os
import logging
import platform
from pathlib import Path
from datetime import datetime
from concurrent_log_handler import ConcurrentRotatingFileHandler


def get_logger(name, level=logging.INFO, log_path=None,open_console=True):
    sys_name = platform.system()
    timestamp = datetime.now().strftime("%Y%m%d")
    if not log_path:
        if sys_name == "Linux":
            os.system(f"mkdir -p /var/log/{name}")
            log_path = f"/var/log/{name}/lambkid_{timestamp}.log"
        else:
            log_path = Path(__file__).parent / f"lambkid_{timestamp}.log"
    handler = ConcurrentRotatingFileHandler(log_path, "a", 1024 * 1024 * 1024, 200)
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'))
    handler.setLevel(level)
    logger = logging.getLogger(name)
    if open_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'))
        logger.addHandler(console_handler)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


log = get_logger("lambkid")

if __name__ == "__main__":
    log = get_logger("redrose2100")
    log.debug("test debug log")
    log.info("test info log")
    log.warning("test warning log")
    log.error("test error log")
