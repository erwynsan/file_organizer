from filecmp import dircmp
import os
import shutil
import datetime

from os import listdir
from os.path import isfile, join


def get_create_timestamp(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t).date()


def walk_files(path):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for fname in filenames:
            files.append(join(dirpath, fname))


def parse_path(path, target_path=None):
    global fcount
    print("--organizing " + path + " ...")
    for (dirpath, dirnames, filenames) in os.walk(path):

        for fname in filenames:
            fcount += 1
            src_file = join(dirpath, fname)

            # parse filename, separator _;
            try:
                fprefix, oth = fname.split("_", 1)
                if len(fprefix) == 8:
                    datetime_obj = datetime.datetime.strptime(
                        fprefix, "%Y%m%d")
                    target_dt = datetime_obj.date()
                elif fprefix == "IMG" or fprefix == "WP":
                    fprefix, oth = oth.split("_", 1)
                    if len(fprefix) == 8:
                        datetime_obj = datetime.datetime.strptime(
                            fprefix, "%Y%m%d")
                        target_dt = datetime_obj.date()
                else:
                    target_dt = get_create_timestamp(src_file)
            except ValueError as identifier:
                target_dt = get_create_timestamp(src_file)
            finally:
                pass

            target_dir = join(target_path, target_dt.isoformat())
            # and not os.path.exists(target_dir):
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)

            checkFile = join(target_dir, os.path.basename(src_file))
            print("check file: " + checkFile)

            # check if file already exists in target directory, skip
            if not os.path.exists(join(target_dir, os.path.basename(src_file))):
                try:
                    print("copying " + src_file + " to " + target_dir)
                    shutil.copy2(src_file, target_dir)
                except OSError as identifier:
                    print("Error copying " + src_file + ".  Retrying..")
                    shutil.copy2(src_file, target_dir)
                finally:
                    pass
            else:
                print(src_file + " already exists in " + target_dir)
            print("file count: {} ".format(fcount))

            # if fcount >= 10:
            #    break

# ************
# main


fcount = 0

#TARGET_PATH = "/Volumes/pictures/OneDrive_reorg"
#TARGET_PATH = "/Volumes/library/file_organizer/erwynSE"

# parse_path("/Volumes/pictures/OneDrive/2011")
# parse_path("/Volumes/pictures/OneDrive/2012")
# parse_path("/Volumes/pictures/OneDrive/2013")
# parse_path("/Volumes/pictures/OneDrive/2014")
# parse_path("/Volumes/pictures/OneDrive/2015")
# parse_path("/Volumes/pictures/OneDrive/2016")
# parse_path("/Volumes/pictures/OneDrive/0000_UnknownDate")

parse_path("/Volumes/library/mobile/erwynSE",
           "/Volumes/library/file_organizer/erwynSE")


print("copied {} files".format(fcount))

print("end")
