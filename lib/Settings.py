class Settings:

    import configparser

    config = configparser.ConfigParser()

    def make_default_config(self):
        self.config['SQLite'] = {'fileName': 'database.db', 'filePatch': ''}
        self.saveConfig()

    def get_settings(self):
        self.settings = dict(config.items())
        return self.settings

    def save_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def set_setting(self, section, key, value):
        self.config[section][key] = value
        self.saveConfig()

