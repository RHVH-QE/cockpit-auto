import yaml

__all__ = ['CONF']

CONF = list(yaml.load_all(open("/home/ramakasturinarra/automation/cockpit-auto/config.yml")))[0]
