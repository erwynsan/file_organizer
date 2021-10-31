import argparse
from filecmp import dircmp
import os
import shutil
from os.path import isfile, join
from datetime import datetime
import os.path
import helpers.log_helper as log_helper
import logging

log = logging.getLogger(__name__)

# add comment for checkin


class Xdiff:

    dryrun = True
    dryrun_info = ""
    remove_file = False
    diff_out_file = "compare_files.txt"

    def __init__(self, dryrun, remove_file=None, diff_out_file=None) -> None:
        self.dryrun = dryrun
        if dryrun:
            self.dryrun_info = "exec dryrun: "
        self.remove_file = remove_file

        if not diff_out_file:
            now = datetime.now()
            dt_string = now.strftime("%Y%m%d%H%M%S")
            self.diff_out_file = f"compare_files_{dt_string}.txt"
        else:
            self.diff_out_file = diff_out_file

    def get_create_timestamp(self, filename):
        t = os.path.getctime(filename)
        return datetime.fromtimestamp(t).date().strftime("%Y-%m-%d")

    def get_strdate(self, t):
        return datetime.fromtimestamp(t).date().strftime("%Y-%m-%d")

    def get_file_stat(self, filename):
        stat = os.stat(filename)
        return stat

    def compare_file_size(self, msg_info, left_fname, right_fname):
        match = False
        r_fname = os.path.basename(right_fname)
        l_fname = os.path.basename(left_fname)

        right_fname_stat = self.get_file_stat(right_fname)
        left_fname_stat = self.get_file_stat(left_fname)

        log.info(
            f"right_fname_stat:{right_fname_stat};left_fname_stat={left_fname_stat}"
        )

        if left_fname_stat.st_size == right_fname_stat.st_size:
            match = True
            msg = f"SameFile{msg_info}-Delete:{l_fname}/{r_fname};LEFT:{left_fname_stat.st_size};RIGHT:{right_fname_stat.st_size} \n"
            log.info(msg)

        return match

    def compare_dir(self, left_dir, right_dir):
        dcmp = dircmp(left_dir, right_dir)
        self.remove_dups(dcmp)
        return None

    def remove_dups(self, dcmp):
        log.info(
            "========comparing: left: {} == right: {} ======".format(
                dcmp.left, dcmp.right
            )
        )
        log.info("remove_file:{}".format(self.remove_file is True))

        for fname in dcmp.common_files:
            left_fname = join(dcmp.left, fname)
            left_fname_stat = self.get_file_stat(left_fname)

            right_fname = join(dcmp.right, fname)
            right_fname_stat = self.get_file_stat(right_fname)

            log.info(f"dcmp:{left_fname}=={right_fname}")
            log.info(f"dcmp:{left_fname_stat}=={right_fname_stat}")

            if left_fname_stat.st_size == right_fname_stat.st_size and self.get_strdate(
                left_fname_stat.st_ctime
            ) == self.get_strdate(right_fname_stat.st_ctime):
                log.info(
                    f"SameFile-Delete:{fname};LEFT:{left_fname_stat.st_size};RIGHT:{right_fname_stat.st_size}"
                )
                if self.remove_file:
                    log.info(f"{self.dryrun_info} deleting {right_fname}")
                    if not self.dryrun:
                        os.remove(right_fname)
            else:
                file_date = self.get_create_timestamp(right_fname)
                log.info(f"Keep: {fname},{file_date}")

        for fname in dcmp.right_only:
            chk_file = False
            filename, file_ext = os.path.splitext(fname)

            right_fname = join(dcmp.right, fname)
            left_fname = join(dcmp.left, f"{filename}{file_ext.lower()}")
            if os.path.exists(left_fname):
                msg_info = "CAP"
                chk_file = True

            elif "(" in fname:
                # get string before (  and the extension
                fname = fname[: fname.index("(")]
                left_fname = join(dcmp.left, fname + file_ext)
                lower_left_fname = join(dcmp.left, fname + file_ext.lower())
                if os.path.exists(left_fname):
                    msg_info = "VER"
                    chk_file = True
                elif os.path.exists(lower_left_fname):
                    msg_info = "CAP_VER"
                    left_fname = lower_left_fname
                    chk_file = True

            if chk_file:
                match = self.compare_file_size(msg_info, left_fname, right_fname)
                if match and self.remove_file:
                    log.info(f"{self.dryrun_info} deleting {right_fname}")
                    if not self.dryrun:
                        os.remove(right_fname)
            else:
                file_date = self.get_create_timestamp(right_fname)
                log.info(f"RightOnly: {fname},{file_date} ")


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-l", "--left", type=str, help="left path", default=None)
    arg_parser.add_argument("-r", "--right", type=str, help="right path", default=None)
    arg_parser.add_argument(
        "-rm", "--remove_file", action="store_true", help="rm_file mode"
    )
    arg_parser.add_argument("--debug", action="store_true", help="debug mode")
    arg_parser.add_argument("-d", "--dryrun", action="store_true", help="dry run mode")

    return arg_parser.parse_args()


args = get_args()
log_helper.setup_logger(args.debug, log_path="/tmp/fileorg", app_name="dir_cmp")
log.info(args)

differ = Xdiff(dryrun=args.dryrun, remove_file=args.remove_file)
# dcmp = differ.compare_dir(
#     "/Volumes/library/mobile/erwynsan", "/Volumes/library/mobile/erwynSE"
# )

dcmp = differ.compare_dir(
    "/Volumes/library/mobile/erwynSE", "/Volumes/library/mobile/erwynsan"
)
