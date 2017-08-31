import os

# Project root dir
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

# Log root dir
LOG_PATH = os.path.join(PROJECT_ROOT, 'report', 'log')

# Img path
IMG_PATH = os.path.join(PROJECT_ROOT, 'report', 'image')

TEST_BUILD = "rhvh-4.1-0.20170817.0"

"""
class Conf(object):

    def __init__(self):
        self.conf_file = os.path.join(PROJECT_ROOT, 'config.yml')
        self.conf_dict = self.conf_to_dict()

    def conf_to_dict(self):
        return yaml.load(open(self.conf_file))
    
    # Common in conf
    @property
    def common(self):
        return self.conf_dict['common']

    # Subscription in conf
    @property
    def subscription(self):
        return self.conf_dict['subscription']

    # hosted-engine in conf
    @property
    def he(self):
        return self.conf_dict['hosted_engine']

CONF = Conf()
"""
