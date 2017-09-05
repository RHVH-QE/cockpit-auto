# !/usr/bin/env python2.7

import os, sys, time, json, re, shutil, logging
from collections import OrderedDict
from utils.reports import ResultSummary
from cases import CONF
from utils.helpers import results_logs


log = logging.getLogger("sherry")


def generate_final_results(results_logs):
    try:
        log_path = results_logs.current_log_path
        test_build = results_logs.test_build
        if test_build not in log_path:
            return
        final_path = os.path.join(
            log_path.split(test_build)[0], test_build)
        report = ResultSummary(final_path, test_build)
        report.run()
    except Exception as e:
        log.error(e)


def main():
    if sys.argv[1] == 'h':
        str = """Main function entry.
    Usage:
        python run.py [argv]

    Options:
        h,help                                          Menu
        v41_debug_tier                                     Test v41_debug_tier
        v41_rhvh_tier1                                     Test v41_rhvh_tier1
        v41_rhvh_tier2                                     Test v41_rhvh_tier2
        v41_rhvh_dashboard_uefi                            Test v41_rhvh_dashboard_uefi
        v41_rhvh_dashboard_fc                              Test v41_rhvh_dashboard_fc
        v41_rhvh_he_install_bond                           Test v41_rhvh_he_install_bond
        v41_rhvh_he_install_bv                             Test v41_rhvh_he_install_bv
        v41_rhvh_he_install_vlan                           Test v41_rhvh_he_install_vlan
        v41_rhvh_he_install_non_default_port               Test v41_rhvh_he_install_non_default_port
        v41_rhvh_he_install_redeploy                       Test v41_rhvh_he_install_redeploy
        v41_rhvh_he_info_add_host                          Test v41_rhvh_he_info_add_host
        v41_rhel_tier1v41_rhvh_he_install_redeploy         Test v41_rhel_tier1v41_rhvh_he_install_redeploy
        v41_rhel_tier2                                     Test v41_rhel_tier2
        v41_centos_tier1                                   Test v41_centos_tier1
        v41_centos_tier2                                   Test v41_centos_tier2
        v41_fedora_tier1                                   Test v41_fedora_tier1
        v41_fedora_tier2                                   Test v41_fedora_tier2

    Example:
        python run.py v41_debug_tier
    """
        print str
    else:
        tier = sys.argv[1]
        
        version = tier.split('_')[0]
        if version.startswith('v41'):
            import cases.v41 as ver_cases
        else:
            raise Exception("Not support such scenario")

        results_logs.test_build = CONF.get('common').get('test_build')

        from cases import scen
        cases_file = [c for c in getattr(scen, sys.argv[1])["CASES"]]
        for cf in cases_file:
            case = cf.split('/')[2].split('.')[0]
            results_logs.logger_name = 'check.log'
            results_logs.get_actual_logger(case)
            try:
                getattr(ver_cases, case).runtest()
            except NameError as e:
                log.error(e)

        generate_final_results(results_logs)


if __name__ == '__main__':
    main()
