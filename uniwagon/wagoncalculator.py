import sys
import json

with open("data/wiki-recipes-0.17.52.json", "r") as recipe_file:
    recipes = json.load(recipe_file)

with open("data/wiki-items-0.17.52.json", "r") as item_file:
    items = json.load(item_file)

class Product:
    def __init__(self, name):
        self.name = name
        self.time = 0
        self.stack = 0
        self.components = []

    def print_components(self):
        print("Recipe for: %s" % self.name)
        print("Stack size: %s" % self.stack)
        for _component in self.components:
            print("Material:   %s" % _component[0].name)
            print("Amount:     %s" % _component[1])
            print("Stack size: %s" % _component[0].stack)


def create_product(product_name, product_dict):
    # Check if the product has already been created.
    _product = product_dict.get(product_name)
    if _product is not None:
        return _product
    _product = Product(product_name)

    # Get the product recipe.
    _recipe = recipes.get(product_name)
    if _recipe is None:
        return None

    # Get the components required for the normal recipe.
    _components = _recipe.get("recipe")
    if _components is None:
        print("File format error: No \"recipe\" key found for: ", product_name)
        return None

    # Get the product item information.
    _item = items.get(product_name)
    if _item is None:
        return None

    # Get the stack size of the product.
    _stack = _item.get("stack-size")
    if _stack is None:
        print("File format error: No \"stack-size\" key found for: ", product_name)
        return None

    # Create and initialize new product.
    _product.time = _components[0][1]
    _product.stack = _stack
    product_dict[product_name] = _product

    # Create products for each component.
    for _component in _components[1:]:
        _name = _component[0]
        _amount = _component[1]
        _new_product = create_product(_name, product_dict)
        if _new_product is not None:
            _product.components.append([_new_product, _amount])

    return _product
    

def main(as_module=False):
    if len(sys.argv) <= 1:
        print("Error: No recipe name provided")
        return

    # Create product recipe structure from name argument.
    _product_name = str(sys.argv[1])
    _product_dict = {}
    _product = create_product(_product_name, _product_dict)
    if _product is None :
        print("Argument error: No recipe entry found for: ", _product_name)
        return

    print("Recipe created for: ", _product.name)
    _product.print_components()

if __name__ == "__main__":
    main(as_module=True)