#!/usr/bin/env python2.7

import os
import yaml
import argparse
import simplejson
import subprocess
from collections import OrderedDict
from prepare_browser import setup_browser, destroy_browser


def gen_polarion_results(avocado_results_dir):
    avocado_json_results = simplejson.load(
        open(os.path.join(avocado_results_dir, 'latest', 'results.json')))
    polarion_test_map = yaml.load(open('./polarion_test_map.yml'))

    test_ver_dir = os.path.dirname(avocado_results_dir)
    polarion_dir = os.path.join(test_ver_dir, 'polarion')
    if not os.path.exists(polarion_dir):
        os.mkdir(polarion_dir)
    test_ver = os.path.basename(test_ver_dir)
    polarion_file_name = os.path.basename(avocado_results_dir) + ".json"

    polarion_results = OrderedDict()
    polarion_results['title'] = 'Auto_Test_' + \
        test_ver + '_' + polarion_file_name.rstrip('.json')
    polarion_results['results'] = OrderedDict()
    for test in avocado_json_results['tests']:
        if test['status'] == 'PASS':
            test_status = 'passed'
        else:
            test_status = 'failed'

        test_name = test['id'].split('/')[-1]
        for key, value in polarion_test_map.items():
            if value == test_name.split(';')[0]:
                polarion_results['results'][key] = test_status

    polarion_results_file = os.path.join(polarion_dir, polarion_file_name)

    with open(polarion_results_file, 'w') as json_file:
        json_file.write(
            simplejson.dumps(
                polarion_results, indent=4))


def run_tests(tags):
    cmd = "avocado list ./ -t {}|awk '{{print $2}}'|awk -F':' '{{print $1}}'|sed -n '1p'".format(
        tags)
    test_dir = subprocess.check_output(cmd, shell=True).strip()
    if not test_dir:
        raise RuntimeError("No tests tagged with {}".format(tags))

    config_dict = yaml.load(open('./config.yml'))

    os.environ['HOST_STRING'] = config_dict['host_string']
    os.environ['USERNAME'] = config_dict['host_user']
    os.environ['PASSWD'] = config_dict['host_pass']

    # compose job os.path.joinresults dir
    log_root_dir = config_dict['avocado_results_dir']
    test_ver = config_dict['test_pkg_ver'] + "_" + config_dict['test_sys_ver']
    log_ver_dir = os.path.join(log_root_dir, test_ver)
    browser = os.environ['BROWSER']
    tag_and_br = tags.replace(',', '_')
    if browser != 'none':
        tag_and_br = tag_and_br + "_" + browser
    log_dir = os.path.join(log_ver_dir, tag_and_br)

    # compose avocado run
    avocado_run_cmd = ["avocado", "run", "./",
                       "-t", tags, "--job-results-dir", log_dir]
    # check yaml-to-mux
    test_file_name = test_dir.split('/')[-1]
    params_yaml_file = test_dir + '.data/' + \
        test_file_name.rstrip('py') + 'yml'
    if os.path.exists(params_yaml_file):
        avocado_run_cmd.extend(["-m", params_yaml_file])
    # run
    subprocess.call(avocado_run_cmd)
    gen_polarion_results(log_dir)


def main():
    parser = argparse.ArgumentParser(description='Run Cockpit Avocado test(s)')
    parser.add_argument(
        "tags", nargs='?',
        help=("Limited Avocado tags specifying which tests to run. "
              "The limitations are: "
              "1) Each test_*.py must has one unique file level tag, zero or more subtags. "
              "2) tags can only contain one file level tag. "
              "3) tests in different test_*.py files can't be run together. "
              "Example: "
              "There is a test_a.py with file level tag 'TEST_A', and a subtag 'SUB1'. "
              "tags='TEST_A' means to run all tests in test_a.py, "
              "tags='TEST_A,SUB1' means to run tests tagged with 'SUB1' in test_a.py, "
              "tags='TEST_A,-SUB1' means to run tests not tagged with 'SUB1' in test_a.py"))
    parser.add_argument("-b", "--browser", choices=['firefox', 'chrome', 'ie', 'none'],
                        default='chrome',
                        help="selenium browser choice")
    parser.add_argument('-m', '--mode', choices=['local', 'grid', 'standalone', 'manual'],
                        default='local',
                        help=("browser setup mode. "
                              "local is to use local webdriver; "
                              "grid is to create grid automatically by docker-compose on local machine; "
                              "standalone is to create a standalone selenium server by docker command line on local machine; "
                              "manual is to use a grid or standalone server created manully."))

    args = parser.parse_args()
    mode = args.mode
    browser = args.browser

    setup_browser(mode, browser)
    run_tests(args.tags)
    destroy_browser(mode)


if __name__ == '__main__':
    main()
