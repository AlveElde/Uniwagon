import copy
import json
import sys

with open("data/wiki-recipes-0.17.52.json", "r") as recipe_file:
    recipes = json.load(recipe_file)

with open("data/wiki-items-0.17.52.json", "r") as item_file:
    items = json.load(item_file)

# Train contants.
INITAL_OUTPUT = 1

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
        if self.count + amount <= product.stack_size:
            self.count += amount
            self.count_reserved += amount
            return amount
        
        # The stack can fit the some of the amount.
        _reserved = self.product.stack_size - self.count
        self.count += _reserved
        self.count_reserved += _reserved
        return _reserved


    def unreserve(self):
        self.count -= self.count_reserved
        self.count_reserved = 0
        if self.count == 0:
            self.name = "Empty"
            self.product = None
            self.empty = True
            
    
    def confirm(self):
        self.count_reserved = 0



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
        print("Station productivity  :", self.productivity)
        print("---------------------------")



class Wagon:
    def __init__(self, output, station):
        self.name = output.name
        self.output = output
        self.station = station
        self.stacks = [Stack() for i in range(STACK_CAPACITY)]
        self.suppliers = {}
        self.next_wagon = None
        self.prev_wagon = None


    def unreserve_all(self):
        for _stack in self.stacks:
                _stack.unreserve()


    def confirm_all(self):
        for _stack in self.stacks:
                _stack.confirm()
    

    def reserve_space(self, product, amount):
        # Reserve any non-empty stack of the same item.
        for _stack in self.stacks:
            if _stack.empty:
                continue
            amount -= _stack.reserve(product, amount)
            if amount == 0:
                return True

        # Reserve empty stack(s) for the remaining amount.
        for _stack in self.stacks:
            if not _stack.empty:
                continue
            amount -= _stack.reserve(product, amount)
            if amount == 0:
                return True
            
        # Not enough room in the wagon.
        print("Warning: Not enough room: ", product.name)#TODO: Provide better feedback
        return False

    
    def reserve_output(self, amount):
        # Find smallest amount of production cycles that will produce at least amount.
        _production_cycles = amount
        while (_production_cycles-1) * self.station.productivity >= amount:
            _production_cycles -= 1
        _product_increase = _production_cycles * self.station.productivity

        # Reserve space for this wagons output.
        self.reserve_space(self.output, _product_increase)

        for _component in self.output.components:
            _component_increase = _production_cycles * _component.amount
            _supplier = self.suppliers.get(_component.name)
            _wagon_iter = self.prev_wagon

            if _supplier is None:
                print("Error:", self.name, "can not find supplier for", _component.name)
                return False

            # Reserve space for the component in the wagons between this and the supplier.
            while _wagon_iter is not _supplier:
                if _wagon_iter is None:
                    print("Error: Wagon iterator is None")
                    return False

                if not _wagon_iter.reserve_space(_component.product, _component_increase):
                    return False
                _wagon_iter = _wagon_iter.prev_wagon

            # Recursively reserve output of supplier.
            if not _wagon_iter.reserve_output(_component_increase):
               return False
        return True


    def print(self):
        print("Wagon output:", self.name)
        print("Stacks:")
        _empty_stacks = 0
        for _stack in self.stacks:
            if _stack.empty:
                _empty_stacks += 1
            else:
                print(" - ",_stack.name, ":", _stack.count)
        print(" -  Empty stacks :", _empty_stacks)       



class Train:
    def __init__(self, output):
        self.name = output.name
        self.output = output
        self.wagons = []
        

    def unreserve_all(self):
        for _wagon in self.wagons:
                _wagon.unreserve_all()


    def increase_all(self):
        for _wagon in self.wagons:
                _wagon.confirm_all()


    def create_wagon_tree(self, product):
        _wagon = Wagon(product, Station())

        # Link previous wagon wagon to this wagon
        if len(self.wagons) > 0:
            self.wagons[-1].prev_wagon = _wagon
    
        self.wagons.append(_wagon)

        # Create supplier wagon(s) for each component.
        for _component in product.components:
            _wagon.suppliers[_component.name] = self.create_wagon_tree(_component.product)
        return _wagon


    def create_minimal_train(self):
        print("Creating minimal train...")
        self.wagon_tree = self.create_wagon_tree(self.output)
        if self.wagon_tree is None:
            print("Error: Failed to create wagon tree")
            return False
        if not self.wagon_tree.reserve_output(INITAL_OUTPUT):
            print("Error: Minimal train resvation failed")
            return False
        print("Minimal train created!")
        return True
        

    def print(self):
        print("---------------------------")
        print("Train producing:", self.name)
        if len(self.wagons) == 0:
            print("Train is empty")
            return

        print("Wagons:\n") #TODO: Move to Wagon print method
        for _wagon in self.wagons:
            _wagon.print()

        _initial_wagon = self.wagons[-1]
        print("\nInitial wagon: ", _initial_wagon.name)
        print("---------------------------")



def print_recipe_breakdown(product):
    if product is None:
        return

    for _component in product.components:
        pass


def create_product_graph(product_name, product_dict):
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
        _new_product = create_product_graph(_component[0], product_dict)
        if _new_product is not None:
            _new_component = Component(_new_product, _component[1])
            _product.components.append(_new_component)
    return _product


    
    

def main(as_module=False):
    if len(sys.argv) <= 1:
        print("Error: No recipe name provided")
        return

    # Create rooted product graph
    _separator = " "
    _product_name = _separator.join(sys.argv[1:])
    _product_dict = {}
    _product = create_product_graph(_product_name, _product_dict)
    if _product is None :
        print("Argument error: No recipe entry found for: ", _product_name)
        return

    print("Recipe created for: ", _product.name)
    _product.print()
    _station = Station()
    _station.print()

    _test_train = Train(_product)
    _test_train.create_minimal_train()
    _test_train.print()
if __name__ == "__main__":
    main(as_module=True)
