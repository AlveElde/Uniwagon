import sys
import json

with open("data/wiki-recipes-0.17.52.json", "r") as recipe_file:
    recipes = json.load(recipe_file)

class Item:
    name = ""
    time = 0
    stack = 0
    materials = []

    def __init__(self, name):
        self.name = name

    def print_materials(self):
        print("Recipe for: %s" % self.name)
        for _material in self.materials:
            print("Material: %s" % _material[0])
            print("Amount:   %s" % _material[1])
            

def create_item_recipe(item_name):
    _recipe = recipes.get(item_name)
    if _recipe is None:
        print("Found no recipe for: ", item_name)
        return None

    _materials = _recipe.get("recipe")
    if _materials is None:
        print("No \"recipe\" key found for: ", item_name)
        return None
    
    _item = Item(item_name)
    _item.time = _materials[0]
    for _material in _materials[1:]:
        _item.materials.append(_material)
    
    return _item
    

def main(as_module=False):
    if len(sys.argv) <= 1:
        print("Error: No recipe name provided")
        return

    _item_name = str(sys.argv[1])
    _item = create_item_recipe(_item_name)
    _item.print_materials()

if __name__ == "__main__":
    main(as_module=True)