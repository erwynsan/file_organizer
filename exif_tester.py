import json
import exiftool
import os
import datetime


print("hello")

# filename = "/Volumes/pictures/IMG_6267.JPG"
files = [
    "/Volumes/mobile/erwyn6s Camera Roll Backup/IMG_C896D1500B23-1.JPEG",
    "/Volumes/mobile/erwyn6s Camera Roll Backup/IMG_3878.JPG",
]
for filename in files:
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(filename)
        # print(metadata)
        file_ext = os.path.splitext(filename)[1]
        print(file_ext)
        if file_ext in [".PNG"]:
            create_date = metadata.get("EXIF:DateTimeOriginal")
        elif file_ext in [".JPEG"]:
            create_date = metadata.get("ICC_Profile:ProfileDateTime")
        elif file_ext in [".MOV", ".MP4"]:
            create_date = metadata.get("QuickTime:TrackCreateDate")
        else:
            create_date = metadata.get("EXIF:CreateDate")
            if not create_date:
                create_date = metadata.get("File:FileInodeChangeDate")
                # remove -
                create_date = str.split(create_date, "-")[0]

        print(f"{filename}:create_date: {create_date}")
        try:
            date_obj = datetime.datetime.strptime(create_date, "%Y:%m:%d %H:%M:%S")
            print(f"{filename}:date_obj: {date_obj}")
        except:
            print(f"{filename}:metadata: {json.dumps(metadata)}")
            print(f"{filename}:metadata: {metadata.get('SourceFile')}")

# for d in metadata:
#     print("{:20.20} {:20.20}".format(d["SourceFile"],
#                                      d["EXIF:DateTimeOriginal"]))
