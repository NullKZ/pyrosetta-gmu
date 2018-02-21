from configparser import ConfigParser

def config(eaObj, path):
    eaObj.cfg = ConfigParser()
    eaObj.cfg.optionxform = lambda option: option
    eaObj.cfg.read(path)
