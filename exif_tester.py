import json
import exiftool
import os
import datetime
import metadata
import logging
import sys

print("hello")

log = logging.getLogger(__name__)

def setup_logger(is_debug=None):
    logfile = "./log/app.log"
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


setup_logger(is_debug=True)

# filename = "/Volumes/pictures/IMG_6267.JPG"
# files = [
#     "/Volumes/mobile/erwyn6s Camera Roll Backup/IMG_C896D1500B23-1.JPEG",
#     "/Volumes/mobile/erwyn6s Camera Roll Backup/IMG_3878.JPG",
# ]

files = ['/Volumes/mobile/Agnes iphone 11 Camera Roll Backup/v09044g40000c43qmn3c77u740mea7a0.MP4', '/Volumes/mobile/Agnes iphone 11 Camera Roll Backup/IMG_6261.JPG', '/Volumes/mobile/Agnes iphone 11 Camera Roll Backup/IMG_0399.JPG', '/Volumes/mobile/Agnes iphone 11 Camera Roll Backup/IMG_0398.JPG', '/Volumes/mobile/Agnes iphone 11 Camera Roll Backup/IMG_0397.JPG', '/Volumes/mobile/Agnes iphone 11 Camera Roll Backup/IMG_6322.JPG']
for filename in files:
    create_date = metadata.get_create_date(filename)
    log.info(f"{filename}:create_date: {create_date}")
