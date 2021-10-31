import logging
import sys
from datetime import datetime

log = logging.getLogger(__name__)


def setup_logger(is_debug=None, log_path="/tmp", app_name="app"):
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d%H%M%S")

    logfile = f"{log_path}/{app_name}_{dt_string}.log"
    log_level = logging.INFO
    if is_debug:
        log_level = logging.DEBUG
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s",
        level=log_level,
        handlers=[
            logging.FileHandler(logfile, mode="w+"),
            logging.StreamHandler(sys.stdout),
        ],
    )
