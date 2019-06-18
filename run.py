#!/usr/bin/env python2.7

import os
import yaml
import argparse
import simplejson
import subprocess
from collections import OrderedDict
from prepare_browser import setup_browser, destroy_browser


def post_deal_with_polarion_results(file_path):
    tag_and_br = os.path.basename(file_path).rstrip('.json')
    test_ver = os.path.basename(os.path.dirname(os.path.dirname(file_path)))

    polarion_results = OrderedDict()
    polarion_results['title'] = test_ver + '_' + tag_and_br
    polarion_results['results'] = OrderedDict()
    for line in open(file_path).readlines():
        split_line = line.split(':')
        case_id = split_line[0].strip()
        case_state = split_line[1].strip()
        pre_state = polarion_results['results'].get(case_id)
        if pre_state == case_state or pre_state == 'failed':
            continue
        polarion_results['results'][case_id] = case_state
    with open(file_path, 'w') as json_file:
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
    os.environ['HOST_PORT'] = config_dict['host_port']
    os.environ['USERNAME'] = config_dict['host_user']
    os.environ['PASSWD'] = config_dict['host_pass']

    # compose avocado job results dir
    log_root_dir = config_dict['avocado_results_dir']
    test_ver = config_dict['test_pkg_ver'] + "_" + config_dict['test_sys_ver']
    log_ver_dir = os.path.join(log_root_dir, test_ver)
    browser = os.environ['BROWSER']
    tag_and_br = tags.replace(',', '_')
    if browser != 'none':
        tag_and_br = tag_and_br + "_" + browser
    log_dir = os.path.join(log_ver_dir, tag_and_br)

    # create polarion result file
    polarion_dir = os.path.join(log_ver_dir, "polarion")
    if not os.path.exists(polarion_dir):
        os.makedirs(polarion_dir)
    polarion_file = os.path.join(polarion_dir, tag_and_br + '.json')
    f = open(polarion_file, 'w')
    f.close()
    os.environ['POLARION_RESULT_FILE'] = polarion_file

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
    post_deal_with_polarion_results(polarion_file)


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
    parser.add_argument("-b", "--browser", choices=['firefox', 'chrome', 'edge', 'ie', 'none'],
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
