import sys
import json

with open("data/wiki-recipes-0.17.52.json", "r") as recipe_file:
    recipes = json.load(recipe_file)

def print_recipe(item_name):
    print("Looking for: ", item_name)
    for _recipe_name in recipes:
        if _recipe_name == item_name:
            _recipe = recipes[_recipe_name]
            print("Found recipe: %s" % _recipe_name)
            for _ingredient in _recipe["recipe"]:
                print("Ingredient: %s" % _ingredient[0])
                print("Amount: %s" % _ingredient[1])
                print("----------")


def main(as_module=False):
    if len(sys.argv) > 1:
        print_recipe(str(sys.argv[1]))
    else:
        print("Error: No recipe name provided")

if __name__ == "__main__":
    main(as_module=True)