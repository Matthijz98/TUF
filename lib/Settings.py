import configparser

config = configparser.ConfigParser()


def makeDefaultConfig():
    config['SQLite'] = {'fileName': 'database.db',
                        'filePatch': ''}
    saveConfig()


def getSettings():
    settings = dict(config.items())
    return settings


def saveConfig():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def setSetting(section, key, value):
    newConfig = config
    newConfig[section][key] = value
    saveConfig()

