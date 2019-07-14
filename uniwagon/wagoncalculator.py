import sys
import json

with open("data/wiki-recipes-0.17.52.json", "r") as recipe_file:
    recipes = json.load(recipe_file)


def print_recipe(item_name):
    _recipe = recipes.get(item_name)
    if not _recipe:
        print("Found no recipe for: ", item_name)
        return

    _ingredients = _recipe.get("recipe")
    if not _ingredients:
        print("No \"recipe\" key found for: ", item_name)
        return

    print("Found recipe for: %s" % item_name)
    for _ingredient in _ingredients:
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