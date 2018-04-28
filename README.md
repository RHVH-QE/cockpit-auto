# cockpit-auto

This project is for cockpit automation, uses selenium and avocado.

## Usage

1. Clone the repo to a machine with firefox, chrome drivers
2. Enter the project directory, install the dependency packages and enter to the virtualenv
```
$ pipenv install
$ pipenv shell
```
3. Configure config.yml with correct parameters.
4. Run tests
```
$ python run.py $tags
```
$tags is the avocado tests filter, for example:

`python run.py ovirt_dashboard|ovirt_hostedengine` is to run the tests tagged with ovirt_dashboard, and the tests tagged with ovirt_hostedengine.

`python run.py ovirt_hostedengine,tier1` is to run the tests tagged with both ovirt_hostedengine and tier1.
