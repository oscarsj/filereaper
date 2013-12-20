#!/usr/bin/env python

#
# MAIN ENTRY POINT FOR FILEREAPER
#

import argparse
import executor

frversion = '0.1'
progname = 'filereaper'
description = "filereaper removes files and directories based on flexible policies"
bool_choices = ['False', 'True', 'false', 'true']

parser = argparse.ArgumentParser(prog=progname,
                                 description=description)
parser.add_argument('path', type=str, help="path to apply the removal")
parser.add_argument('--version', action='version',
                    version='%s %s' % (progname, frversion))
parser.add_argument('--file_match', default='.*', type=str,
                    help='remove files that match this regexp (default: %(default)s)')
parser.add_argument('--run_with', default='root', type=str,
                    help='perform the removal with this user (default: %(default)s))')
parser.add_argument('--test_mode', default=True, nargs='?',
                    help='with the test_mode just logs what\'s to be removed, does not actually remove',
                    const=True, choices=bool_choices)
parser.add_argument('--groups_match', default=None, type=str)
parser.add_argument('--recurse', default=False, nargs='?',
                    const=True, choices=bool_choices)
parser.add_argument('--keepminimum', default=0, type=int)
parser.add_argument('--exclude_list', type=str)
parser.add_argument('--time_mode', default='atime', type=str)
parser.add_argument('--remove_links', default=False, nargs='?',
                    const=True, choices=bool_choices)
parser.add_argument('--keeplast', type=int)
parser.add_argument('--older_than_d', type=int)
parser.add_argument('--older_than_m', type=int)
parser.add_argument('--older_than_s', type=int)
parser.add_argument('--newer_than_d', type=int)
parser.add_argument('--newer_than_m', type=int)
parser.add_argument('--newer_than_s', type=int)
parser.add_argument('--dir_size_threshold', type=int)
parser.add_argument('--partition_size_threshold', type=int)
parser.add_argument('--file_owners', type=str)
parser.add_argument('--file_groups', type=str)

args = parser.parse_args()

executor = executor.Executor(vars(args))
executor.execute()
