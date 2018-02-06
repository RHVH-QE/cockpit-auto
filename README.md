# cockpit-auto

This project is for cockpit automation, which using selenium to locate web elements and operate as a test user.

## Bound Mac, IP, Hostname For Hosted-Engine Testing

http://red.ht/2Dq5dcO

## Test machines used
http://red.ht/2Dq5dcO


## How To Run

1. Clone source codes to local directory on above "TEST RUN" machine
```bash
git clone https://github.com/RHVH-QE/cockpit-auto.git
```
2. Install the dependency packages
```bash
pipenv install --dev
```
3. All the test scenarios are defined in the scen.yml

4. Run the executable file run.py and append the $test_scen defined in scen.yml
```bash
python run.py -t $test_tier
```

## Branches
master
> Auto testing for ovirt 4.2 cockpit, where files and test cases were refatored

v41
> Auto testing for ovirt 4.1 cockpit

## Cases development
Under cases file, there are 3 sections.

- cases_info
> which represent the {$polarion_id: $checkpoint_name} and configuration be used in each check file.
- checks
> Detail check file which defined a class inherit from CheckBase defined under helpers. In this class, should define all the checkpoint function list under cases_info
- helpers
> Some helper library used by the checkpoints

**Name rules should be followed**
1. All the checks file should be started with "test_" under checks directory
2. The class defined in the checks file, should start with "Test", Such as "TestDashboardUi", "TestSubscription", besides, define just one Test.* class in one check file
3. Strip the "test_" from checks file name, this is cases info file. Such as "dashboard_ui.py","tools_subscription.py"

After all, Don't forget to append the cases_info file name into scen.yml under PROJECT_ROOT directory
