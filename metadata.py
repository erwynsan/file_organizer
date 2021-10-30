import datetime
import exiftool
import logging
import json
import os

log = logging.getLogger(__name__)


def get_create_date(filename: str):
    log.debug(f"get_create_date for {filename}")
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(filename)

        file_ext = os.path.splitext(filename)[1]
        if file_ext in [".PNG"]:
            create_date = metadata.get("EXIF:DateTimeOriginal")
        elif file_ext in [".JPEG"]:
            create_date = metadata.get("ICC_Profile:ProfileDateTime")
        elif file_ext in [".MOV", ".MP4"]:
            create_date = metadata.get("QuickTime:TrackCreateDate")
        else:
            create_date = metadata.get("EXIF:CreateDate")

        # if create date is None, use a default date/default folder "unknown"
        try:
            date_obj = datetime.datetime.strptime(create_date, "%Y:%m:%d %H:%M:%S")
            return date_obj.date()
        except Exception as ex:
            log.error(
                f"{filename}: Create date metadata not found: {json.dumps(metadata)}"
            )
            return None
