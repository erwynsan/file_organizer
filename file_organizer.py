import argparse
import logging
from organizer import Organizer
import sys


log = logging.getLogger(__name__)


def setup_logger(is_debug=None):
    logfile = "./log/app.log"
    log_level = logging.INFO
    if is_debug:
        log_level = logging.DEBUG
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s",
        level=log_level,
        handlers=[
            logging.FileHandler(logfile, mode="w+"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-a","--agnes", action="store_true", help="agnes")
    arg_parser.add_argument("-e","--erwyn", action="store_true", help="erwyn")
    arg_parser.add_argument("-s","--sofia", action="store_true", help="sofia")
    arg_parser.add_argument("--debug", action="store_true", help="debug mode")
    arg_parser.add_argument("-d", "--dryrun", action="store_true", help="dry run mode")
    arg_parser.add_argument(
        "-m", "--max_count", type=int, help="maximum file count", default=None
    )
    return arg_parser.parse_args()


args = get_args()
setup_logger(args.debug)

log.info(f"dryrun: {args.dryrun}")
log.info(f"max_count: {args.max_count}")
log.info(f"debug: {args.debug}")

yr_limit = "2021"

organizer = Organizer(dryrun=args.dryrun, max_cnt=args.max_count)

if args.erwyn:
    organizer.parse_path(
        source_path="/Volumes/mobile/erwyn6s Camera Roll Backup",
        target_path=f"/Volumes/pictures/{yr_limit}/mobile",
        yr_limit=yr_limit,
        tag="erwyn6s",
    )

if args.agnes:
    organizer.parse_path(
        source_path="/Volumes/mobile/Agnes iphone 11 Camera Roll Backup",
        target_path=f"/Volumes/pictures/{yr_limit}/mobile",
        yr_limit=yr_limit,
        tag="agnes11",
    )

if args.sofia:
    organizer.parse_path(
        source_path="/Volumes/mobile/Sofia's iPad Camera Roll Backup",
        target_path=f"/Volumes/pictures/{yr_limit}/mobile",
        yr_limit=yr_limit,
        tag="sofia",
    )


log.info(f"Files read: {organizer.fcount}")
log.info(f"Files copied: {organizer.files_copied}")
log.info(f"Unknown date list: {organizer.list_unknown_date}")

log.info("end")
