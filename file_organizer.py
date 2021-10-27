from filecmp import dircmp
import os
import shutil
import datetime
import exiftool
import json

from os import listdir
from os.path import isfile, join

max=200
def get_metadata(filename: str):
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
            if not create_date:
                #remove -
                create_date = str.split(metadata.get("File:FileInodeChangeDate"), '-')[0]

        try:
            date_obj = datetime.datetime.strptime(create_date, '%Y:%m:%d %H:%M:%S')
        except:
            print(f"{filename}:metadata: {json.dumps(metadata)}")
        print(f"{filename}:create_date: {date_obj}")

def get_create_timestamp(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t).date()


def walk_files(path):
    files = []
    for (dirpath, _, filenames) in os.walk(path):
        for fname in filenames:
            files.append(join(dirpath, fname))


def parse_path(path, target_path, yr_limit=None, tag=None):
    global fcount
    print("--organizing path=" + path + " ;target_path=" +
          target_path + ' ;yr_limit=' + str(yr_limit) + ' ;tag=' + tag)

    # if yr_limit:
    #     target_path = join(target_path, str(yr_limit.year))
    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True)

    for (dirpath, _, filenames) in os.walk(path):
        for fname in filenames:
            src_file = join(dirpath, fname)

            print(src_file)
            try: 
                get_metadata(src_file)
            except Exception as ex:
                print("exception {} {}".format(ex, src_file))                
            # parse filename, separator _;
            target_dt = None
            try:
                target_dt = get_create_timestamp(src_file)
            except Exception as ex:
                print("exception {} {}".format(ex, src_file))
                continue

            # if yr_limit:
            #     if str(target_dt.year) != yr_limit:
            #         continue

            # target_dir = join(target_path, target_dt.isoformat())
            # # and not os.path.exists(target_dir):
            # if not os.path.exists(target_dir):
            #     os.makedirs(target_dir, exist_ok=True)

            # checkFile = join(target_dir, os.path.basename(src_file))
            # # print("check file: " + checkFile)

            # if tag:
            #     full_target_path = join(
            #         target_dir, tag + '_' + os.path.basename(src_file))
            # else:
            #     full_target_path = join(
            #         target_dir, os.path.basename(src_file))

            fcount += 1

            # check if file already exists in target directory, skip
            # if not os.path.exists(full_target_path):
            #     fcount += 1

            #     try:
            #         print("copying " + src_file + " to " + full_target_path)
            #         shutil.copy2(src_file, full_target_path)
            #     except Exception as ex:
            #         print("Error copying " + src_file + ".  Retrying..")
            #         shutil.copy2(src_file, full_target_path)
            # else:
            #     print(src_file + " already exists in " + full_target_path)
            print("file count: {} ".format(fcount))

            if fcount >= max:
                break

        if fcount >= max:
            break
        # ************
        # main


def get_tag(path):
    if 'mobile' in path:
        return path.split('/')[-1]
    else:
        return None


fcount = 0

yr_limit = '2020'
target_path = f'/Volumes/pictures/2021/wdmycloud'

# source_path = '/Volumes/library/mobile/agnes-x'
# tag = get_tag(source_path)
# parse_path(source_path,
#            target_path=target_path,
#            yr_limit=yr_limit,
#            tag=tag)

# source_path = '/Volumes/library/mobile/sofia'
# tag = get_tag(source_path)
# parse_path(source_path,
#            target_path=target_path,
#            yr_limit=yr_limit,
#            tag=tag)

source_path = '/Volumes/mobile/erwyn6s Camera Roll Backup'
tag = 'erwyn6s' #get_tag(source_path)
parse_path(source_path,
           target_path=target_path,
           yr_limit=yr_limit,
           tag=tag)

print("copied {} files".format(fcount))

print("end")
