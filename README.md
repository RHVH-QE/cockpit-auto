# cockpit-auto

This project is for cockpit automation, which using selenium to locate web elements， avocado testing framework and operate as a test user.

## Test machines, Bound Mac, IP, Hostname For Hosted-Engine Testing

[VMs of binding MAC, IP and hostname in lab for RHEV-H](http://red.ht/2Dq5dcO)


## How To Run

1. Clone source codes to local directory on above "TEST RUN" machine
```bash
git clone https://github.com/RHVH-QE/cockpit-auto.git
```
2. Install the dependency packages and enter to the virtualenv
```bash
pipenv install
pipenv shell
```
3. All the test scenarios or cases are related to the polarion in `polarion_test_map.yml`

4. Run the executable file run.py and append the $test_scen defined in scen.yml
```bash
python run.py $tags
```

## Branches
master
> Auto testing for ovirt 4.2 cockpit, where files and test cases were refatored

v41
> Auto testing for ovirt 4.1 cockpit

vm
> Auto testing for cockpit-VMs since 4.2.2 phase, it is the latest version

## Cases development
Under test_suites directory, there are two sections.

- test_case.py
> This file is used to write the test cases which defined in polarion
- test_case.py.data
> This directory is related to the test_case.py, it is the configuration or other files about the test cases used.


**Name rules should be followed**
1. All the test case file should be started with "test_" under test_suites directory
2. The class defined in the test_case.py file, should start with "Test", Such as "TestOvirtDashboard", "TestOvirtHostedEngine", besides, define just one Test.* class in one test_case.py file
3. All the pages in page_objects directory, and should be started with "page_" under page_objects" directory, such as "page_ovirt_dashboard"
