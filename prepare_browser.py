import subprocess
import os
import yaml
import time

STANDALONE_CONTAINER_NAME = "standalone-browser"


def create_selenium_grid_by_docker_compose():
    subprocess.check_call(["docker-compose", "up", "-d"])
    # wait for nodes to connect to hub
    time.sleep(3)


def del_selenium_grid_by_docker_compose():
    subprocess.check_call(["docker-compose", "down"])


def create_selenium_standalone(browser):
    if browser not in ['chrome', 'firefox']:
        raise ValueError(
            "Do not support to create standalone server for {}".format(browser))
    cmd = "docker run -d -p 4444:4444 -p 5900:5900 -v /dev/shm:/dev/shm " \
        "--name {} selenium/standalone-{}-debug".format(
            STANDALONE_CONTAINER_NAME, browser)
    subprocess.check_call(cmd, shell=True)
    for count in range(0, 10):
        cmd = "curl http://localhost:4444/grid/console > /dev/null 2>&1"
        try:
            subprocess.check_call(cmd, shell=True)
            break
        except Exception:
            time.sleep(2)
    else:
        del_selenium_standalone()
        raise RuntimeError("The selenium standalone server is not ready!")


def del_selenium_standalone():
    subprocess.check_call(
        ["docker", "stop", "{}".format(STANDALONE_CONTAINER_NAME)])
    subprocess.check_call(
        ["docker", "rm", "{}".format(STANDALONE_CONTAINER_NAME)])


def setup_browser(mode, browser):
    if mode != 'manual' and browser in ['ie', 'edge']:
        raise ValueError(
            "{} mode doesn't support Windows browser".format(mode))

    os.environ['BROWSER'] = browser
    if mode == 'grid':
        create_selenium_grid_by_docker_compose()
        os.environ['HUB'] = 'localhost'
    elif mode == 'standalone':
        create_selenium_standalone(browser)
        os.environ['HUB'] = 'localhost'
    elif mode == 'manual':
        os.environ['HUB'] = yaml.load(open('./config.yml'))['selenium_hub']


def destroy_browser(mode):
    if mode == 'grid':
        del_selenium_grid_by_docker_compose()
    elif mode == 'standalone':
        del_selenium_standalone()
