# cockpit-auto

This project uses selenium and avocado to automate tests for:

    cockpit-ovirt-dashboard
    cockpit-machines
    cockpit-machines-ovirt

## Usage

1. Clone the repo
2. Enter the project directory, install the dependency packages and enter to the virtualenv
```sh
$ pipenv install
$ pipenv shell
```

3. Configure config.yml with correct parameters.
4. Run tests
```sh
$ python run.py $tags -m $mode -b $browser
```

**$tags** is the avocado tests filter, for example:

>`python run.py ovirt_dashboard|ovirt_hostedengine` is to run the tests tagged with ovirt_dashboard, and the tests tagged with ovirt_hostedengine.
>
>`python run.py ovirt_hostedengine,tier1` is to run the tests tagged with both ovirt_hostedengine and tier1.

**$mode** defines how to setup browser. It has four values, **local**, **grid**, **standalone** and **manual**. If this parameter is omitted, **local** is used.

**local** means to use local webdriver. You need to download chromedriver, geckodriver and put them under /usr/local/bin. Only chrome and firefox are supported.
  
**grid** is to create grid automatically by docker-compose on local machine. You have to install docker-compose beforehand. Only chrome and firefox are supported.

**standalone** is to create a standalone selenium server by docker command line on local machine. Only chrome and firefox are supported.

**manual** is to use a grid created manually in advance. Here list the steps to configure a grid supporting Internet Explorer:
  
* Download Selenium Standalone Server and the Internet Explorer Driver Server [here](https://www.seleniumhq.org/download/).
* Configure Internet Explorer. For Internet Explorer tests you should make some additional configuration on the browser. See [IE Required Configuration](https://github.com/SeleniumHQ/selenium/wiki/InternetExplorerDriver#required-configuration)
* Start selenium hub: 
```sh
java -jar path-to-selenium-standalone-server -role hub
```

* Start selenium node:
```sh
java -Dwebdriver.ie.driver=path-to-ie-driver -jar path-to-selenium-standalone-server -role webdriver -hub http://hubip:4444/grid/register
```

**$browser** defines browser type, includes chrome, firefox, ie. If this option is omitted, chrome is used.
