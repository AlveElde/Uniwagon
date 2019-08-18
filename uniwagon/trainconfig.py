from pathlib import Path

from configparser import ConfigParser


class TrainConfig:
    def __init__(self):
        self.config = ConfigParser(allow_no_value=True)
        self.configs_path = Path().cwd() / "trainconfigs"
        self.gamedata_path = Path().cwd() / "gamedata"
        self.output_name = None
        self.base_products = {}
        self.recipes_path = ""
        self.items_path = ""


    def load(self, config_name):
        _path = self.configs_path / config_name
        if len(self.config.read(_path)) == 0:
            print("Config Error: No trainconfig at \"{}\"".format(_path.name))
            return False
        
        if not self.config.has_section("Game Data"):
            print("TrainConfig Error: Section \"Game Data\" not found")
            return False
        _game_data = self.config["Game Data"]

        _items_file = _game_data.get("items file", None)
        if _items_file is None:
            print("TrainConfig Error: Key \"recipes file\" not found in section [Game Data]")
            return False
        self.items_path = self.gamedata_path / _items_file

        _recipes_file = _game_data.get("recipes file", None)
        if _recipes_file is None:
            print("TrainConfig Error: Key \"recipes file\" not found in section [Game Data]")
            return False
        self.recipes_path = self.gamedata_path / _recipes_file
        
        if not self.config.has_section("Train Config"):
            print("TrainConfig Error: Section \"Train Config\" not found")
            return False
        _train_config = self.config["Train Config"]

        _output_name = _train_config.get("output", None)
        if _recipes_file is None:
            print("TrainConfig Error: Key \"output\" not found in section [Train Config]")
            return False
        self.output_name = _output_name.capitalize()

        if self.config.has_section("Base Products"):
            _base_products = self.config["Base Products"]
            self.base_products = [i.capitalize() for i in _base_products]
        
        #TODO: Read output
        #TODO: Read base products
        #TODO: Make first letter upper case
        return True
