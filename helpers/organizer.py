import os
import shutil
import logging
import helpers.metadata as metadata
from datetime import datetime

from os.path import isfile, join

log = logging.getLogger(__name__)


class Organizer:
    dryrun = True
    fcount = 0
    files_copied = 0
    files_no_metadata = 0
    max_cnt = 10
    list_unknown_date = list()
    dryrun_info = ""
    min_sync_date = None

    def __init__(self, dryrun, max_cnt=None, min_sync_date=None) -> None:
        self.max_cnt = max_cnt
        self.dryrun = dryrun
        if self.dryrun:
            self.dryrun_info = "exec dryrun:"
        if min_sync_date:
            try:
                self.min_sync_date = datetime.strptime(min_sync_date, "%Y-%m-%d")
            except:
                pass

    def rollback_file(self, full_target_path):
        # exception encountered, delete the target file since it might be corrupted
        if os.path.exists(full_target_path):
            os.remove(full_target_path)
            log.info(f"File ({full_target_path}) deleted.")
        else:
            log.info(f"The file ({full_target_path}) does not exist")

    def copy_file(self, src_file, full_target_path):
        # check if file already exists in target directory, skip
        if not os.path.exists(full_target_path):
            try:
                log.info(f"{self.dryrun_info} copying {src_file} to {full_target_path}")
                if not self.dryrun:
                    shutil.copy2(src_file, full_target_path)
                self.files_copied += 1
            except Exception as ex:
                log.error(
                    f"Error copying {src_file} to {full_target_path}. Error message: {ex}"
                )
                self.rollback_file(full_target_path)
                raise ex
        else:
            log.info(
                f"{self.dryrun_info} {src_file} already exists in {full_target_path}"
            )

    def update_status(self):
        if self.fcount % 2 == 0:
            log.info(
                f"--- : fcount:{self.fcount};files_copied:{self.files_copied};files_no_metadata:{self.files_no_metadata}"
            )

    def parse_path(self, source_path, target_path, yr_limit=None, tag=None):
        log.info(
            f"--organizing source_path={source_path};target_path={target_path} ;yr_limit={str(yr_limit)};tag={tag}"
        )

        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)

        for (dirpath, _, filenames) in os.walk(source_path):

            # list_of_files = filter(
            #     lambda x: os.path.isfile(os.path.join(dirpath, x)), os.listdir(dirpath)
            # )
            # Sort list of files based on last modification time in ascending order
            filenames = sorted(
                filenames,
                key=lambda x: os.path.getctime(os.path.join(dirpath, x)),
                reverse=True,
            )
            for fname in filenames:
                if self.max_cnt and self.fcount >= self.max_cnt:
                    break
                self.fcount += 1

                src_file = join(dirpath, fname)
                log.info(src_file)

                # get file timestamp
                if self.min_sync_date:
                    src_file_date = datetime.fromtimestamp(
                        metadata.get_file_stat(src_file).st_ctime
                    )
                    if src_file_date < self.min_sync_date:
                        log.info(f"Too old to sync: {src_file}:{src_file_date}")
                        break

                try:
                    target_dt = metadata.get_create_date(src_file)
                    log.info(f"Created date: {str(target_dt)}")
                    if not target_dt:
                        log.info(f"No create date.  Add to unknown list:{src_file}")
                        self.files_no_metadata = +1
                        self.list_unknown_date.append(src_file)
                except Exception as ex:
                    log.error("Unable to get metadata {} {}".format(ex, src_file))
                    raise ex

                if target_dt:
                    if yr_limit:
                        if str(target_dt.year) < yr_limit:
                            continue

                    target_dir = join(target_path, target_dt.isoformat())
                else:
                    target_dir = join(target_path, f"unknown_date/{tag}")

                # and not os.path.exists(target_dir):
                if not os.path.exists(target_dir):
                    if not self.dryrun:
                        os.makedirs(target_dir, exist_ok=True)

                checkFile = join(target_dir, os.path.basename(src_file))
                log.info("check file: " + checkFile)

                if tag:
                    full_target_path = join(
                        target_dir, tag + "_" + os.path.basename(src_file)
                    )
                else:
                    full_target_path = join(target_dir, os.path.basename(src_file))

                self.copy_file(src_file, full_target_path)
                log.info("file count: {} ".format(self.fcount))

                self.update_status()
            if self.max_cnt and self.fcount >= self.max_cnt:
                break
        # end of for walk

    # end of parse
