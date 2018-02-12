# !/usr/bin/env python2.7

import logging
import argparse
from utils.helpers import results_logs
from utils.helpers import generate_final_results
from utils.helpers import yaml2dict
from importlib import import_module


log = logging.getLogger("bender")


def _get_cases(case_info_name):
    cases_info_module = import_module(
        "cases.cases_info." + case_info_name, __package__)
    cases_map = getattr(cases_info_module, 'cases', None)  # {$polarion_id: $checkpoint}
    each_cfg = getattr(cases_info_module, 'config', None)
    return cases_map, each_cfg


def _get_check(case_info_name):
    check_file_name = "test_" + case_info_name
    check_module = import_module('cases.checks.' + check_file_name, __package__)
    chk_cls_name = ''
    for attr in dir(check_module):
        if attr.startswith('Test'):
            chk_cls_name = attr
            break
    chk_cls = getattr(check_module, chk_cls_name, None)
    return chk_cls


def run(tier):
    """"""
    config_dict = yaml2dict('./config.yml')
    host_string = config_dict['host_string']
    host_user = config_dict['host_user']
    host_pass = config_dict['host_pass']
    browser = config_dict['browser']
    test_build = config_dict['test_build']
    results_logs.test_build = test_build
    expect_cases = {}
    test_scens = yaml2dict('./scen.yml')

    try:
        case_infos = test_scens[tier]['cases']
        for case_info_name in case_infos:
            results_logs.logger_name = 'checkpoints.log'
            results_logs.get_actual_logger(case_info_name)

            # Get cases map and configurations
            cases_map, each_cfg = _get_cases(case_info_name)
            expect_cases.update(cases_map)

            # Get checkpoint class
            chk_cls = _get_check(case_info_name)

            # Make the instance of checkpoint class
            check = chk_cls()
            check.host_string = host_string
            check.host_user = host_user
            check.host_pass = host_pass
            check.browser = browser
            check.build = test_build
            check.cases = cases_map
            check.config = each_cfg

            # Go check
            log.info(check.go_check())
    except Exception as e:
        log.exception(e)

    generate_final_results(expect_cases, results_logs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--test_tier",
        type=str,
        choices=[
            "debug_tier", "all_tier", "virt_tier", 
            "he_tier", "common_tier", "rhel_tier"
        ],
        help="select desired test tier")

    args = parser.parse_args()
    if args.test_tier is None:
        parser.print_help()
    else:
        run(args.test_tier)


if __name__ == '__main__':
    main()
