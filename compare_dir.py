from filecmp import dircmp
import os
import shutil
from os.path import isfile, join
import datetime


def get_create_timestamp(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t).date().strftime("%Y-%m-%d")


def get_strdate(t):
    return datetime.datetime.fromtimestamp(t).date().strftime("%Y-%m-%d")


def get_file_stat(filename):
    stat = os.stat(filename)
    return stat


def print_diff_files(filename, dcmp, remove_file=None):
    print("========comparing: left: {} == right: {} ======".format(
        dcmp.left, dcmp.right))
    print("remove_file:{}".format(remove_file is True))

    file = open(filename, "w")
    for fname in dcmp.common_files:
        left_fname = join(dcmp.left, fname)
        left_fname_stat = get_file_stat(left_fname)

        right_fname = join(dcmp.right, fname)
        right_fname_stat = get_file_stat(right_fname)

        file_date = get_create_timestamp(right_fname)

        print("rightfile:{};{}".format(file_date,
                                       get_strdate(right_fname_stat.st_ctime)))

        # if file_date == '2018-12-27' or file_date == '2018-12-28':
        #     msg = f"Delete: {fname};LEFT:{left_fname_stat.st_size};RIGHT:{left_fname_stat.st_size} \n"
        #     if remove_file is True:
        #         os.remove(right_fname)
        if left_fname_stat.st_size == right_fname_stat.st_size and get_strdate(left_fname_stat.st_ctime) == get_strdate(right_fname_stat.st_ctime):
            msg = f"SameFile-Delete:{fname};LEFT:{left_fname_stat.st_size};RIGHT:{right_fname_stat.st_size} \n"
            if remove_file is True:
                os.remove(right_fname)
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
              '/Volumes/library/mobile/agnes-iphone-6s')
print_diff_files("compare_files.txt", dcmp, remove_file=False)
