from configparser import ConfigParser

config = ConfigParser()
config.optionxform = lambda option: option
config['init'] = {
    'initState':'',
    'nGen':50
}
config['variation'] = {
    'bbAngle':True,
    'fragReplacement':True,
    'fragLength':9
}
config['improvement'] = {
    'representation':'centroid',
    'scoreFxn':'score3',
    'relaxType':'fast'
}

with open('cfg.ini', 'w') as filename:
    config.write(filename)
