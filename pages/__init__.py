import yaml

__all__ = ['CONF']

CONF = list(yaml.load_all(open("./config.yml")))[0]
