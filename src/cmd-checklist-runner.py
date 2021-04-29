#!/usr/bin/env python3

# (C) 2021 by Arturo Borrero Gonzalez <arturo@debian.org>

#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#

# checklist.yaml file format:
#  - name: "this is a test that does something"
#    tests:
#      - cmd: cmd1
#        retcode: 0
#        stdout: "expected stdout from cmd1"
#        stderr: "expected stderr from cmd1"
#      - cmd: cmd2
#        retcode: 0
#        stdout: "expected stdout from cmd2"
#        stderr: "expected stderr from cmd2"
#

import os
import sys
import argparse
import subprocess
import yaml
import logging


def read_yaml_file(file):
    try:
        with open(file, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as e:
                logging.error(e)
                exit(2)
    except FileNotFoundError as e:
        logging.error(e)
        exit(2)


def validate_dictionary(dictionary, keys):
    if not isinstance(dictionary, dict):
        logging.error(f"not a dictionary:\n{dictionary}")
        return False
    for key in keys:
        if dictionary.get(key) is None:
            logging.error(f"missing key '{key}' in dictionary:\n{dictionary}")
            return False
    return True


def stage_validate_config(args):
    checklist_dict = read_yaml_file(args.checklist_file)
    for definition in checklist_dict:
        if not validate_dictionary(definition, ["name", "tests"]):
            logging.error(f"couldn't validate file '{args.checklist_file}'")
            return False
        for test in definition["tests"]:
            if not validate_dictionary(test, ["cmd", "retcode", "stdout", "stderr"]):
                logging.error(f"couldn't validate file '{args.checklist_file}'")
                return False

    logging.debug(f"'{args.checklist_file}' seems valid")
    ctx.checklist_dict = checklist_dict
    return True


def cmd_run(cmd, expected_retcode, expected_stdout, expected_stderr):
    success = True
    logging.debug(f"running command: {cmd}")
    r = subprocess.run(cmd, capture_output=True, shell=True)

    if r.returncode != expected_retcode:
        logging.warning(
            f"Expected return code '{expected_retcode}', but got '{r.returncode}'"
        )
        success = False

    stdout = r.stdout.decode("utf-8").strip()
    if stdout != expected_stdout:
        logging.warning(f"Expected stdout '{expected_stdout}', but got '{stdout}'")
        success = False

    stderr = r.stderr.decode("utf-8").strip()
    if stderr != expected_stderr:
        logging.warning(f"Expected stderr '{expected_stderr}', but got '{stderr}'")
        success = False

    return success


def test_run(test_definition):
    logging.info("--- running test: {}".format(test_definition["name"]))

    for test in test_definition["tests"]:
        if cmd_run(test["cmd"], test["retcode"], test["stdout"], test["stderr"]):
            continue

        logging.warning("--- failed test: {}".format(test_definition["name"]))
        ctx.counter_test_failed += 1
        return

    logging.info("--- passed test: {}".format(test_definition["name"]))
    ctx.counter_test_ok += 1


def stage_run_tests(args):
    for test_definition in ctx.checklist_dict:
        test_run(test_definition)


def stage_report():
    logging.info("---")
    logging.info("--- finished")
    total = ctx.counter_test_ok + ctx.counter_test_failed
    logging.info("--- passed tests: {}".format(ctx.counter_test_ok))
    logging.info("--- failed tests: {}".format(ctx.counter_test_failed))
    logging.info("--- total tests: {}".format(total))


def parse_args():
    description = "Utility to run arbitrary command tests"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--checklist-file",
        default="cmd-checklist.yaml",
        help="File with testcase definitions. Defaults to '%(default)s'",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="debug mode",
    )

    return parser.parse_args()


class Context:
    def __init__(self):
        self.checklist_dict = None
        self.counter_test_failed = 0
        self.counter_test_ok = 0


# global data
ctx = Context()


def main():
    args = parse_args()

    logging_format = "[%(filename)s] %(levelname)s: %(message)s"
    if args.debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging.basicConfig(format=logging_format, level=logging_level, stream=sys.stdout)

    if not stage_validate_config(args):
        sys.exit(1)
    stage_run_tests(args)
    stage_report()


if __name__ == "__main__":
    main()
