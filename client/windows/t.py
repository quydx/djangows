import os
import sys
import argparse
# import getpass
from crontab import CronTab
import logging
import utils


def main():
    utils.setup_logging()
    logger = logging.getLogger(__name__)

    print(logger)

    parser = argparse.ArgumentParser(description="Schedule for backup, using crontab")
    subparsers = parser.add_subparsers(help='sub-command help')

    # subcommand : add
    parser_add = subparsers.add_parser('add', help='addition a job to crontab')
    parser_add.add_argument('path', help='target to backup')
    parser_add.add_argument('-t', '--time', dest='time', required=True, help='time to backup')
    parser_add.add_argument('-c', '--comment', dest='comment', help='comment of job')

    # subcommand : list
    parser_list = subparsers.add_parser('list', help='list jobs in crontab')

    # subcommand : edit
    parser_edit = subparsers.add_parser('edit', help='edit a job in crontab')
    parser_edit.add_argument('path', help='target to backup')
    parser_edit.add_argument('-t', '--time', dest='time', help='time to backup')
    parser_edit.add_argument('-c', '--comment', dest='comment', help='comment of job')

    # subcommand : del
    parser_del = subparsers.add_parser('del', help='delete a job in crontab')
    parser_del.add_argument('path', help='target to backup')
    parser_del.add_argument('-c', '--comment', dest='comment', help='comment of job')


    args = parser.parse_args()

    PWD = os.path.dirname(os.path.realpath(__file__))
    print(os.path.realpath(__file__))
    print(PWD)
    