from filecmp import dircmp
import os
import shutil
import logging
import metadata
import sys

from os.path import isfile, join

max=10
files_copied = 0
files_no_metadata = 0
list_unknown_date = list()

logfile='./app.log'
logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s', 
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler(sys.stdout),
    ])

log = logging.getLogger(__name__)

def parse_path(path, target_path, yr_limit=None, tag=None, dryrun=False):
    global fcount
    global files_copied
    global files_no_metadata

    log.info("--organizing path=" + path + " ;target_path=" +
          target_path + ' ;yr_limit=' + str(yr_limit) + ' ;tag=' + tag)

    if not os.path.exists(target_path):
        os.makedirs(target_path, exist_ok=True)

    for (dirpath, _, filenames) in os.walk(path):
        for fname in filenames:
            src_file = join(dirpath, fname)

            log.info(src_file)
            try: 
                target_dt = metadata.get_create_date(src_file)
                log.info(str(target_dt))
            except Exception as ex:
                log.info("exception {} {}".format(ex, src_file))
                break   

            dryrun_info = ""
            if dryrun:
                dryrun_info = "exec dryrun:"

            fcount += 1
            if target_dt:
                if yr_limit:
                    if str(target_dt.year) != yr_limit:
                        continue
            
                target_dir = join(target_path, target_dt.isoformat())
            else:
                target_dir = join(target_path, "unknown_date")
                files_no_metadata =+ 1
                list_unknown_date.append(src_file)
                
            # and not os.path.exists(target_dir):
            if not os.path.exists(target_dir):
                if not dryrun:
                    os.makedirs(target_dir, exist_ok=True)

            checkFile = join(target_dir, os.path.basename(src_file))
            log.info("check file: " + checkFile)

            if tag:
                full_target_path = join(
                    target_dir, tag + '_' + os.path.basename(src_file))
            else:
                full_target_path = join(
                    target_dir, os.path.basename(src_file))

            # check if file already exists in target directory, skip
            if not os.path.exists(full_target_path):
                try:
                    log.info(f"{dryrun_info} copying {src_file} to {full_target_path}")
                    if not dryrun:
                        shutil.copy2(src_file, full_target_path)                    
                except Exception as ex:
                    log.info("{dryrun_info} Error copying {src_file} Retrying..")
                    if not dryrun:
                        shutil.copy2(src_file, full_target_path)
                files_copied += 1
            else:
                log.info(f"{dryrun_info} {src_file} already exists in {full_target_path}")
            log.info("file count: {} ".format(fcount))

            if max and fcount >= max:
                break

        if max and fcount >= max:
            break
        # ************
        # main




def get_tag(path):
    if 'mobile' in path:
        return path.split('/')[-1]
    else:
        return None


fcount = 0

yr_limit = '2021'
target_path = f'/Volumes/pictures/{yr_limit}/mobile'

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
           tag=tag,
           dryrun=False)

log.info(f"Files read: {fcount}")
log.info(f"Files copied: {files_copied}")
log.info(f"Unknown date list: {list_unknown_date}")

log.info("end")
