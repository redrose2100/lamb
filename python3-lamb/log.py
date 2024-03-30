import logging
import platform
from pathlib import Path
from concurrent_log_handler import ConcurrentRotatingFileHandler

def get_logger(name,level=logging.INFO,log_path=None):
    sys_name=platform.system()
    if not log_path:
        if sys_name == "Linux":
            log_path=f"/var/log/{name}/python3-lamb.log"
        else:
            log_path = Path(__file__).parent / "python3-lamb.log"
    handler = ConcurrentRotatingFileHandler(log_path, "a", 512 * 1024, 30)
    handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(message)s'))
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger

log=get_logger("python3-lamb")

if __name__=="__main__":
    log=get_logger("redrose2100")
    log.debug("test debug log")
    log.info("test info log")
    log.warning("test warning log")
    log.error("test error log")