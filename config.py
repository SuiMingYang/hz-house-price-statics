import configparser

def getConf():
    config_url="config.conf"
    conf = configparser.ConfigParser()
    conf.read(config_url)
    return conf

conf = getConf()