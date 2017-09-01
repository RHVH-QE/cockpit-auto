import os

# Project root dir
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

LOG_URL = "http://10.66.148.10"


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
