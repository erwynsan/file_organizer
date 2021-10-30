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
        create_date = None
        file_ext = os.path.splitext(filename)[1]

        if file_ext in [".MOV", ".MP4"]:
            create_date = metadata.get("QuickTime:TrackCreateDate")
        
        if not create_date:        
            create_date = metadata.get("EXIF:DateTimeOriginal")
        if not create_date:
            create_date = metadata.get("EXIF:CreateDate")
        if not create_date:
            create_date = metadata.get("ICC_Profile:ProfileDateTime")
            log.info(f"No DateTimeOriginal, using ProfileDateTime instead {create_date}")
        if not create_date:
            create_date = metadata.get("EXIF:ModifyDate")
            log.info(f"No CreateDate, using ModifyDate instead {create_date}")
        # if create date is None, use a default date/default folder "unknown"
        try:
            date_obj = datetime.datetime.strptime(create_date, "%Y:%m:%d %H:%M:%S")
            return date_obj.date()
        except Exception as ex:
            log.error(
                f"{filename}: Create date metadata not found: {json.dumps(metadata)}"
            )
            return None
