import configparser

CONFIG_FILE = 'configuration.ini'


def read():
    try:
        configuration = {}
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        for section in config.sections():
            options = config.options(section)
            for option in options:
                configuration[option] = config.get(section, option)
        return configuration
    except:
        return None
