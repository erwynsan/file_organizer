import argparse
import logging
from helpers.organizer import Organizer
import helpers.log_helper as log_helper
import sys

log = logging.getLogger(__name__)


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-a", "--agnes", action="store_true", help="agnes")
    arg_parser.add_argument("-e", "--erwyn", action="store_true", help="erwyn")
    arg_parser.add_argument("-s", "--sofia", action="store_true", help="sofia")
    arg_parser.add_argument("--debug", action="store_true", help="debug mode")
    arg_parser.add_argument("-d", "--dryrun", action="store_true", help="dry run mode")
    arg_parser.add_argument(
        "-m", "--max_count", type=int, help="maximum file count", default=None
    )
    arg_parser.add_argument(
        "-y", "--year_limit", type=int, help="year limit", default=2021
    )
    arg_parser.add_argument(
        "-msd",
        "--min_sync_date",
        type=str,
        help="minimum sync date",
        default="2021-10-01",
    )
    return arg_parser.parse_args()


args = get_args()
log_helper.setup_logger(args.debug, log_path="/tmp/fileorg", app_name="file_org")

log.info(f"dryrun: {args.dryrun}")
log.info(f"max_count: {args.max_count}")
log.info(f"debug: {args.debug}")
log.info(f"year limit: {args.year_limit}")

log.info(f"args:{args}")

yr_limit = str(args.year_limit)
organizer = Organizer(
    dryrun=args.dryrun, max_cnt=args.max_count, min_sync_date=args.min_sync_date
)

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
