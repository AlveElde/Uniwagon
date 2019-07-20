import sys
import json
import copy

with open("data/wiki-recipes-0.17.52.json", "r") as recipe_file:
    recipes = json.load(recipe_file)

with open("data/wiki-items-0.17.52.json", "r") as item_file:
    items = json.load(item_file)

# Wagon constants.
STACK_CAPACITY = 40

# Station constants.
MOD_PER_ASM = 4
MOD_PER_BCN = 2
PRD_MOD_PRD = 0.10
PRD_MOD_SPD = -0.15
SPD_MOD_SPD = 0.50
BCN_EFF     = 0.50
ASM_SPD     = 1.25
ASM_PRD     = 1
BCN_SPD     = MOD_PER_BCN * SPD_MOD_SPD * BCN_EFF

class Train:
    def __init__(self):
        pass



class Wagon:
    def __init__(self, product, station):
        self.name = product.name
        self.product = product
        self.station = station
        self.output_stacks = []
        self.prev = Wagon()
        self.next = Wagon()
        self.suppliers = {}
       

    def unreserve_all(self):
        for _stack in self.output_stacks:
                _stack.unreserve()


    def increase_all(self):
        for _stack in self.output_stacks:
                _stack.increase()
        
        
    def increase_output(self, amount):
        # Find smallest amount of production cycles that will produce at least amount
        _production_cycles = amount
        while (_production_cycles-1) * self.station.productivity >= amount:
            _production_cycles -= 1
        _output_left = _production_cycles * self.station.productivity

        # Reserve any non-empty stack of the same item
        for _stack in self.output_stacks:
            if _stack.empty:
                continue
            _reserved = _stack.reserve(self.product, _output_left)
            if _reserved > 0:
                _output_left -= _reserved
                break

        # Reserve empty stack(s) for the remaining amount
        for _stack in self.output_stacks:
            if not _stack.empty:
                continue
            _output_left -= _stack.reserve(self.product, _output_left)

        # Not enough room in the wagon.
        if _output_left > 0:
            print("Not enough room")#TODO: Provide better feedback
            self.unreserve_all()
            return False

        # Recursively check if supplier wagons can increase output.
        for _component in self.product.components:
            _supplier = suppliers.get(_component.name)
            if _supplier == None:
                print("Error: Wagon supplier not found")
                self.unreserve_all()
                return False
            
            _output_increase = _component.amount * _production_cycles
            if not _supplier.increase_output(_output_increase):
                self.unreserve_all()
                return False
            
        #Increase output
        self.increase_all()
        return True

        

class Station:
    def __init__(self, asm = 2, bcn_per_asm = 8):
        self.asm = asm
        self.bcn_per_asm = bcn_per_asm
        self.crafting_speed = asm * (ASM_SPD * (1 + (BCN_SPD * bcn_per_asm) + (PRD_MOD_SPD * MOD_PER_ASM)))
        self.productivity = ASM_PRD * (1 + (PRD_MOD_PRD * MOD_PER_ASM))
        #TODO: Calculate efficiency


    def print(self):
        print("---------------------------")
        print("Station crafting speed:", self.crafting_speed)
        print("Station productivity:", self.productivity)
        print("---------------------------")


class Stack:
    def __init__(self):
        self.name = "Empty"
        self.product = None
        self.count = 0
        self.count_reserved = 0
        self.empty = True


    def reserve(self, product, amount):
        if not self.empty:
            if self.count == self.product.stack_size:
                return 0
            if product.name != self.name:
                return 0

        if self.empty:
            self.name = product.name
            self.product = product
            self.empty = False
        
        # The stack can fit the entire amount.
        if self.count + amount < product.stack_size:
            self.count += amount
            self.count_reserved += amount
            return amount
        
        # The stack can fit the some of the amount.
        _reserved = self.product.stack_size - self.count
        self.count = self.product.stack_size
        self.count_reserved = self.product.stack_size
        return _reserved


    def unreserve(self):
        self.count -= self.count_reserved
        self.count_reserved = 0
        if self.count == 0:
            self.name = "Empty"
            self.product = None
            self.empty = True
            
    
    def increase(self):
        self.count_reserved = 0



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
        


class Product:
    def __init__(self, name):
        self.name = name
        self.time = 0
        self.stack_size = 0
        self.components = []

    def print(self):
        print("---------------------------")
        print("Product:", self.name)
        print("Stack size:", self.stack_size)
        print("Components:")
        for _component in self.components:
            _component.print()
        print("---------------------------")


def create_miniimal_train():
    pass


def print_recipe_breakdown(product):
    if product is None:
        return

    for _component in product.components:
        pass


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
    _stack_size = _item.get("stack-size")
    if _stack_size is None:
        print("File format error: No \"stack-size\" key found for: ", product_name)
        return None

    # Create and initialize new product.
    _product.time = _components[0][1]
    _product.stack_size = _stack_size
    product_dict[product_name] = _product

    # Create Products for each component.
    for _component in _components[1:]:
        _new_product = create_product(_component[0], product_dict)
        if _new_product is not None:
            _new_component = Component(_new_product, _component[1])
            _product.components.append(_new_component)

    return _product
    

def main(as_module=False):
    if len(sys.argv) <= 1:
        print("Error: No recipe name provided")
        return

    # Create rooted product graph
    _product_name = str(sys.argv[1]) #TODO: Concatenate 1 - n args
    _product_dict = {}
    _product = create_product(_product_name, _product_dict)
    if _product is None :
        print("Argument error: No recipe entry found for: ", _product_name)
        return

    print("Recipe created for: ", _product.name)
    _product.print()
    _station = Station()
    _station.print()


if __name__ == "__main__":
    main(as_module=True)