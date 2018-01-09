# !/usr/bin/env python2.7

import logging
import argparse
from utils.helpers import results_logs
from utils.helpers import generate_final_results
from utils.helpers import yaml2dict
from importlib import import_module

log = logging.getLogger("bender")


def run(tier):
    """"""
    config_dict = yaml2dict('./config.yml')
    host_string = config_dict['host_string']
    host_user = config_dict['host_user']
    host_pass = config_dict['host_pass']
    browser = config_dict['browser']
    test_build = config_dict['test_build']
    results_logs.test_build = test_build

    test_scens = yaml2dict('./scen.yml')
    try:
        case_files = test_scens[tier]['cases']
        for cf in case_files:
            # Get file name from scenario file
            cf_name = cf.split('.')[0]
            results_logs.logger_name = 'checkpoints.log'
            results_logs.get_actual_logger(cf_name)

            # Import module by case file name
            case_module = import_module('cases.checks.' + cf_name, __package__)
            testclss_name = ''
            for attr in dir(case_module):
                if attr.startswith('Test'):
                    testclss_name = attr
                    break
            testclss = getattr(case_module, testclss_name, None)

            # Make the instance of test class
            test = testclss()
            test.host_string = host_string
            test.host_user = host_user
            test.host_pass = host_pass
            test.browser = browser
            test.build = test_build

            # Go check
            log.info(test.go_check(cf_name))
    except Exception as e:
        log.exception(e)

    generate_final_results(results_logs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--test_tier",
        type=str,
        choices=[
            "debug_tier", "he_tier", "virt_tier", "common_tier", "all_tier"
        ],
        help="select desired test tier")

    args = parser.parse_args()
    if args.test_tier is None:
        parser.print_help()
    else:
        run(args.test_tier)


if __name__ == '__main__':
    main()
