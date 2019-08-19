from pathlib import Path

from configparser import ConfigParser


class TrainConfig:
    def __init__(self):
        self.config = ConfigParser(allow_no_value=True)
        self.configs_path = Path().cwd() / "trainconfigs"
        self.gamedata_path = Path().cwd() / "gamedata"
        self.items_path = ""
        self.recipes_path = ""
        self.output_name = None
        self.base_products = {}


    def create(self, config_name):
        _path = self.configs_path / config_name
        if len(self.config.read(_path)) == 0:
            print("Config Error: No trainconfig at \"{}\"".format(_path.name))
            return False

        _items_file = self.get_value("items file", "Game Data")
        if _items_file is None:
            return False
        self.items_path = self.gamedata_path / _items_file
        
        _recipes_file = self.get_value("recipes file", "Game Data")
        if _recipes_file is None:
            return False
        self.recipes_path = self.gamedata_path / _recipes_file

        _output_name = self.get_value("output", "Train Configuration")
        if _output_name is None:
            return False
        self.output_name = _output_name.capitalize()

        _base_products = self.get_keys("Base Products")
        if _base_products is None:
            return False
        self.base_products = [i.capitalize() for i in _base_products]
        return True


    def get_value(self, key, section_name):
        if not self.config.has_section(section_name):
            print("TrainConfig Error: Section \"{}\" not found".format(section_name))
            return None
        _section = self.config[section_name]

        _value = _section.get(key, None)
        if _value is None:
            print("TrainConfig Error: Key \"{}}\" not found in section [{}}]]".format(key, section_name))
            return False
        return _value


    def get_keys(self, section_name):
        if not self.config.has_section(section_name):
            print("TrainConfig Error: Section \"{}\" not found".format(section_name))
            return None
        _section = self.config[section_name]
        return [i for i in _section]
