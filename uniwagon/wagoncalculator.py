import sys
import json

with open("data/wiki-recipes-0.17.52.json", "r") as recipe_file:
    recipes = json.load(recipe_file)

class Item:
    name = ""
    time = 0
    stack = 0
    materials = {}

    def __init__(self, name):
        self.name = name

    def print_materials(self):
        print("Recipe for: %s" % self.name)
        for _material in self.materials:
            print("Material: %s" % _material[0])
            print("Amount:   %s" % _material[1])
            

def create_item(item_name, item_dict):
    # Check if the item has already been created.
    if item_dict.get(item_name) is not None:
        return True

     # Get the item recipe.
    _recipe = recipes.get(item_name)
    if _recipe is None:
        return True

    # Get the materials required for the normal recipe.
    _materials = _recipe.get("recipe")
    if _materials is None:
        print("File format error: No \"recipe\" key found for: ", item_name)
        return False
    
    # Create new item and insert in the dict.
    _item = Item(item_name)
    _item.time = _materials[0]
    item_dict[item_name] = _item

    # Create items for each material.
    for _material in _materials[1:]:
        if not create_item(_material[0], item_dict):
            return False
    return True
    

def main(as_module=False):
    if len(sys.argv) <= 1:
        print("Error: No recipe name provided")
        return

    # Create item structure from name argument.
    _item_name = str(sys.argv[1])
    _item_dict = {}
    if not create_item(_item_name, _item_dict):
        return

    # Get the requested item.
    _item = _item_dict.get(_item_name)
    if _item is None:
        print("Argument error: No recipe entry found for: ", _item_name)
        return
    
    print("Recipe created for: ", _item.name)

if __name__ == "__main__":
    main(as_module=True)