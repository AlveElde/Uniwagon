#import sys
#import json
#from .const import Constants as const
# with open("data/wiki-recipes-0.17.52.json", "r") as recipe_file:
#     recipes = json.load(recipe_file)
# with open("data/wiki-items-0.17.52.json", "r") as item_file:
#     items = json.load(item_file)

class Product:
    def __init__(self, name):
        self.name = name
        self.time = 0
        self.stack_size = 0
        self.components = []
        self.is_base = False

    def print(self):
        print("\n{0:-^{line_len}s}\n".format(self.name, line_len=const.LINE_LEN))
        print("Stack size:", self.stack_size)
        print("Components:")
        for _component in self.components:
            _component.print()
        print("\n{0:-^{line_len}s}\n".format("", line_len=const.LINE_LEN))



class Component:
    def __init__(self, product, amount):
        self.name = product.name
        self.product = product
        self.amount = amount
        
    def print(self):
        print()
        print(" - ", self.name)
        print("    Amount:", self.amount)
        print("    Stack size:", self.product.stack_size)


        
class Recipe:
    def __init__(self):
        self.root = None

    def create(self, config, data):
        _created_products = {}
        self.root = self.create_tree(config.output_name, _created_products, data.recipes, data.items)
        if self.root is None:
            return False
        return True

    def create_tree(self, product_name, created_products, recipes, items):
        # Check if the product has already been created.
        _product = created_products.get(product_name)
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
            print("Recipe error: \"recipe\" attribute not found for:", product_name)
            return None

        # Get the product item information.
        _item = items.get(product_name)
        if _item is None:
            print("Recipe error: \"{}\" not found in items".format(product_name))
            return None

        # Get the stack size of the product.
        _stack_size = _item.get("stack-size")
        if _stack_size is None:
            print("Recipe error: No \"stack-size\" found for:", product_name)
            return None

        # Create and initialize new product.
        _product.time = _components[0][1]
        _product.stack_size = _stack_size
        created_products[product_name] = _product

        # Create Products for each component.
        for _component in _components[1:]:
            _new_product = self.create_tree(_component[0], created_products, recipes, items)
            if _new_product is not None:
                _new_component = Component(_new_product, _component[1])
                _product.components.append(_new_component)

        # Products with no components are base.
        if len(_product.components) == 0:
            _product.is_base = True
        return _product

    def print(self):
        pass