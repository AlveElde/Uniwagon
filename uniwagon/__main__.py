import sys

from .trainconfig import TrainConfig
from .gamedata import GameData
from .recipe import Recipe
from .train import Train

def main():
    if len(sys.argv) <= 1:
        print("Error: No trainconfig provided")
        return
    
    # Parse command line arguments.
    _separator = " "
    _config_name = _separator.join(sys.argv[1:])
    
    # Parse production line config file.
    _config = TrainConfig()
    if not _config.create(_config_name):
        return
    
    # Parse game data files at path specified by config.
    _data = GameData()
    if not _data.create(_config):
        return
    
    # Create the Recipe specified by config.
    _recipe = Recipe()
    if not _recipe.create(_config, _data):
        return

    # Create the Train specified by config.
    _train = Train()
    if not _train.create(_config, _recipe):
        return

    _train.find_max_output()
    _train.print()

if __name__ == "__main__":
    main()

