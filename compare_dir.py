from filecmp import dircmp
import os
import shutil
from os.path import isfile, join
import datetime


def get_create_timestamp(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t).date().strftime("%Y-%m-%d")


def print_diff_files(filename, dcmp, remove_file=None):
    print("========comparing: left: {} == right: {} ======".format(
        dcmp.left, dcmp.right))
    print("remove_file:{}".format(remove_file is True))

    file = open(filename, "w")
    for fname in dcmp.common_files:
        full_fname = join(dcmp.right, fname)
        file_date = get_create_timestamp(full_fname)
        if file_date == '2018-12-27' or file_date == '2018-12-28':
            msg = f"Delete: {fname},{file_date} \n"
            if remove_file is True:
                os.remove(full_fname)
        else:
            msg = f"Keep: {fname},{file_date} \n"
        file.write(msg)

    # for name in dcmp.diff_files:
    #     print("diff_file {} found in {} and {}".format(
    #         name, dcmp.left, dcmp.right))

    #     for name in dcmp.left_only:
    #         # print "diff_file %s found in left only %s" % (name, dcmp.left)
    #         src_filename = dcmp.left + "/" + name
    #         dest_dir = dcmp.right + "/" + name
    #         print("copying file {} to {}".format(src_filename, dest_dir))
    #         if os.path.isdir(src_filename) and not os.path.exists(dest_dir):
    #             shutil.copytree(src_filename, dest_dir)
    #         else:
    #             shutil.copy2(src_filename, dest_dir)

    for fname in dcmp.right_only:
        file_date = get_create_timestamp(join(dcmp.right, fname))
        msg = f"RightOnly: {fname},{file_date} \n"
        file.write(msg)

    #     for sub_dcmp in dcmp.subdirs.values():
    #         print_diff_files(sub_dcmp)
    file.close()


dcmp = dircmp('/Volumes/library/mobile/agnes',
              '/Volumes/library/mobile/erwynsan')
print_diff_files("compare_files.txt", dcmp)
