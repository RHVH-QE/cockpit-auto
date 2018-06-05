#!/usr/bin/env python2.7

import os
import yaml
import argparse
import simplejson
import subprocess
from collections import OrderedDict


def gen_polarion_results(avocado_results_dir):
    avocado_json_results = simplejson.load(
        open(os.path.join(avocado_results_dir, 'latest', 'results.json')))
    polarion_test_map = yaml.load(open('./polarion_test_map.yml'))

    polarion_results = OrderedDict()
    vers = avocado_results_dir.split('/')
    polarion_results['title'] = 'Auto_Test_' + vers[-2] + '_' + vers[-1]
    polarion_results['results'] = OrderedDict()
    for test in avocado_json_results['tests']:
        if test['status'] == 'PASS':
            test_status = 'passed'
        else:
            test_status = 'failed'

        test_name = test['id'].split('/')[-1]
        for key, value in polarion_test_map.items():
            if value == test_name:
                polarion_results['results'][key] = test_status

    polarion_results_file = os.path.join(
        avocado_results_dir, 'latest', 'polarion_results.json')

    with open(polarion_results_file, 'w') as json_file:
        json_file.write(
            simplejson.dumps(
                polarion_results, indent=4))


def create_selenium_grid_by_docker():
    subprocess.check_call(["docker-compose", "up", "-d"])


def del_selenium_grid_by_docker():
    subprocess.check_call(["docker-compose", "down"])


def run_tests(tags, browser, grid):
    config_dict = yaml.load(open('./config.yml'))

    os.environ['HOST_STRING'] = config_dict['host_string']
    os.environ['USERNAME'] = config_dict['host_user']
    os.environ['PASSWD'] = config_dict['host_pass']
    os.environ['BROWSER'] = browser
    if grid == 'auto':
        create_selenium_grid_by_docker()
        os.environ['HUB'] = 'localhost'
    elif grid == 'manual':
        os.environ['HUB'] = config_dict['selenium_hub']

    avocado_root_dir = config_dict['avocado_results_dir']
    test_pkg_ver = config_dict['test_pkg_ver']
    test_sys_ver = config_dict['test_sys_ver']
    avocado_results_dir = avocado_root_dir + \
        test_pkg_ver + "_" + test_sys_ver + "/" + browser

    tag_filter_list = ["--filter-by-tags=%s" %
                       x.replace(' ', '') for x in tags.split('|')]
    avocado_run_cmd = ["avocado", "run", "./",
                       "--job-results-dir", avocado_results_dir]
    avocado_run_cmd.extend(tag_filter_list)

    subprocess.call(avocado_run_cmd)
    if grid == 'auto':
        del_selenium_grid_by_docker()
    gen_polarion_results(avocado_results_dir)


def main():
    parser = argparse.ArgumentParser(description='Run Cockpit Avocado test(s)')
    parser.add_argument(
        "tags", nargs='?',
        help=("Avocado tags filter specifying which tests need to be run. "
              "For example, if you want to run the tests with both tag A and tag B, "
              "the tests with tag C, "
              "and the tests with tag D, "
              "then you should define the filter as 'A,B|C|D'. "
              "Refer to each test to see the actual avocado tags."))
    parser.add_argument("-b", "--browser", choices=['firefox', 'chrome', 'ie'],
                        default='chrome',
                        help="selenium browser choice")
    parser.add_argument('-g', '--grid', choices=['none', 'auto', 'manual'],
                        default='none',
                        help=('selenium grid choice. none means not to use grid, '
                              'auto is to create grid automatically by docker-compose on the local machine, '
                              'manual is to use a grid created manually in advance.'))

    args = parser.parse_args()
    run_tests(args.tags, args.browser, args.grid)


if __name__ == '__main__':
    main()
