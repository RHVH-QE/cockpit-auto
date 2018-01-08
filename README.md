# cockpit-auto

[![build status](http://github.com/RHVH-QE/cockpit-auto/badges/master/build.svg)](https://github.com/RHVH-QE/cockpit-auto.git/commits/master)

This project is for cockpit automation, which using selenium to locate web elements and to operate as a test user.

## Binded Mac, IP, Hostname For HE Automation

| Hostname | Mac Addr | IP Addr | valid? |
| -------- | -------- | ------- | ------ |
| rhevh-hostedengine-vm-01.qe.lab.eng.nay.redhat.com | 52:54:00:05:61:f2  | 10.66.148.102 | *YES* |
| rhevh-hostedengine-vm-02.qe.lab.eng.nay.redhat.com | 52:54:00:71:d5:ff  | 10.66.148.103 | *YES* |
| rhevh-hostedengine-vm-03.qe.lab.eng.nay.redhat.com | 52:54:00:57:ef:59  | 10.66.148.104 | *YES* |
| rhevh-hostedengine-vm-04.lab.eng.pek2.redhat.com | 52:54:00:5e:8e:c7  | 10.73.73.100 | *YES* |
| rhevh-hostedengine-vm-05.lab.eng.pek2.redhat.com | 52:54:00:5d:21:64  | 10.73.73.101 | *YES* |
| rhevh-hostedengine-vm-06.lab.eng.pek2.redhat.com | 52:54:00:34:04:b0  | 10.73.73.102 | *YES* |

## Test machines used
| Hostname | Mac Addr | IP Addr | NIC | PURPOSE | valid?|
| -------- | -------- | ------- | ------ | ------ | ------ |
| dell-op790-01.qe.lab.eng.nay.redhat.com | `d4:be:d9:95:61:ca`  | 10.66.148.7 | em1 | Virt | *YES* |
| hp-z620-05.qe.lab.eng.nay.redhat.com | `2c:44:fd:3a:d7:d7`  | 10.66.150.175 | eno1 | HE | *YES* |
| hp-z620-04.qe.lab.eng.nay.redhat.com | `2c:44:fd:3a:d7:b6`  | 10.66.148.24 | enp1s0 | HE | *YES* |
| dell-pet105-02.qe.lab.eng.nay.redhat.com | `00:22:19:2d:4b:a3`  | 10.66.148.10 | enp2s0 | TEST RUN | *YES* |


## How To Run

1. Clone source codes to local directory on above "TEST RUN" machine
```bash
git clone https://github.com/RHVH-QE/cockpit-auto.git
```
2. Install the dependency packages
```bash
pip install -r requirements
```
3. All the test scenarios are defined in the scen.yml

4. Run the executable file run.py and append the $test_scen defined in scen.yml
```bash
python run.py $test_tier
```

## Branches
master
> Auto testing for rhv4.2 cockpit, where files and test cases were refatored

v41
> Auto testing for rhv4.1 cockpit

## Cases development
Under cases file, there are 3 section.

- cases_info
> which represent the {$polarion_id: $checkpoint_name} and configuration be used in each check file.
- checks
> Detail check file which defined a class inherit from CheckBase defined under helpers. In this class, should define all the checkpoint function list under cases_info
- helpers
> Some helper library used by the checkpoints

**Name rules should be followed**
1. All the checks file should be start with "test_" under checks directory
2. The class defined in the checks file, should start with "Test", Such as "TestDashboardUi", "TestSubscription"
3. Strip the "test_" from checks file name, this is cases info file. Such as "dashboard_ui.py","tools_subscription.py"

After all, Don't forget to append the check file name into scen.yml under PROJECT_ROOT directory
