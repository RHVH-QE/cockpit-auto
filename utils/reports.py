import os
import time
import re
import json
from constants import LOG_URL
from collections import OrderedDict


class ResultSummary(object):
    """
    /home/dracher/Zoidberg/logs/2017-03-08/redhat-virtualization-host-4.1-20170208.0
    """

    def __init__(self, path, test_build=None):
        self.path = path.rstrip('/')
        self.test_build = test_build
        self.jfilename = "final_results.json"

    @staticmethod
    def get_current_date():
        return time.strftime("%m%d%H%M", time.localtime())

    def _parse_checkpoints(self, res):
        p1 = re.compile(r'{"RHEVM-\d')
        rets = {}
        if os.path.exists(res):
            for line in open(res):
                if p1.search(line):
                    rets.update(eval(line.split("||")[-1]))

        return rets

    def _gen_title(self):
        src_ver = self.test_build.split('-')[-2].replace('.', '_')

        title = src_ver + "_Node_Cockpit_AutoTest_" + self.test_build
        return title

    def _gen_log_url(self):
        log_url = LOG_URL + self.path.split('logs')[-1]
        return log_url

    def _gen_results_jfile(self):
        root_path = self.path

        final_results = OrderedDict()
        final_results[self.test_build] = OrderedDict()
        actual_run_cases = []
        pass_cases_results = []
        failed_cases_results = []
        pass_num = 0
        failed_num = 0
        for a, b, c in os.walk(root_path):
            for case in sorted(b):
                ret = self._parse_checkpoints(os.path.join(a, case, 'check.log'))
                final_results[self.test_build][case] = ret
                for k, v in ret.items():
                    if v == "passed":
                        pass_cases_results.append(k)
                    if v == "failed":
                        failed_cases_results.append(k)

                actual_run_cases.extend(list(ret.keys()))
                values = list(ret.values())
                pass_num = pass_num + values.count('passed')
                failed_num = failed_num + values.count('failed')
            break
        total_num = pass_num + failed_num
        final_results['sum'] = OrderedDict()
        final_results['sum']['title'] = self._gen_title()
        final_results['sum']['log_url'] = self._gen_log_url()
        final_results['sum']['total'] = total_num
        final_results['sum']['passed'] = pass_num
        final_results['sum']['failed'] = failed_num
        final_results['sum']['error'] = 0
        final_results['sum']['errorlist']=failed_cases_results
        final_results_jfile = os.path.join(root_path,
                                           self.jfilename)
        try:
            with open(final_results_jfile, 'w') as json_file:
                json_file.write(
                    json.dumps(
                        final_results, indent=4))

            return final_results_jfile
        except Exception as e:
            print e
            return None

    def run(self):
        final_results_jfile = self._gen_results_jfile()
        if not final_results_jfile:
            print "Generate final results json file failed."
            return
        else:
            print "Generated {}".format(final_results_jfile)
