import json

class GameData:
    def __init__(self):
        self.recipes = None
        self.items = None

    def create(self, config):
        try:
            _recipe_file = open(config.recipes_path, "r")
        except IOError:
            print("Gamedata Error:",config.recipes_path,": Recipe file not found")
            return False
        self.recipes = json.load(_recipe_file)

        try:
            _items_file = open(config.items_path, "r")
        except IOError:
            print("Gamedata Error:",config.items_path,": Items file not found")
            return False
        self.items = json.load(_items_file)
        return True