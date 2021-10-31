import logging
import helpers.metadata as metadata
import helpers.log_helper as log_helper

log = logging.getLogger(__name__)

log_helper.setup_logger(is_debug=True, log_path="/tmp/fileorg", app_name="exif_tester")

# filename = "/Volumes/pictures/IMG_6267.JPG"
# files = [
#     "/Volumes/mobile/erwyn6s Camera Roll Backup/IMG_C896D1500B23-1.JPEG",
#     "/Volumes/mobile/erwyn6s Camera Roll Backup/IMG_3878.JPG",
# ]

files = [
    "/Volumes/mobile/Agnes iphone 11 Camera Roll Backup/v09044g40000c43qmn3c77u740mea7a0.MP4",
    "/Volumes/mobile/Agnes iphone 11 Camera Roll Backup/IMG_6261.JPG",
]
for filename in files:
    create_date = metadata.get_create_date(filename)
    log.info(f"{filename}:create_date: {create_date}")

    stat = metadata.get_file_stat(filename)
    log.info(f"{filename}:stat: {stat}")

    ts = metadata.get_create_timestamp(filename)
    log.info(f"{filename}:get_create_timestamp: {ts}")

    from datetime import datetime

    timestamp_str = datetime.fromtimestamp(stat.st_ctime)

    print(type(timestamp_str))
    log.info(f"{filename}:timestamp_str: {timestamp_str}")

import os

dir_name = "/tmp/fileorg"
# Get list of all files only in the given directory
list_of_files = filter(
    lambda x: os.path.isfile(os.path.join(dir_name, x)), os.listdir(dir_name)
)

# print(list(list_of_files))

# Sort list of files based on last modification time in ascending order
list_of_files = sorted(
    list_of_files,
    key=lambda x: os.path.getctime(os.path.join(dir_name, x)),
    reverse=True,
)
print("-----")
print(list_of_files)
