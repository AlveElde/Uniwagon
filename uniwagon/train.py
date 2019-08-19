from .recipe import Product, Recipe
from .station import Station

# Train contants.
INITAL_OUTPUT = 1

# Wagon constants.
STACK_CAPACITY = 40

# Printout constants.
LINE_LEN = 41

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


    def print(self):
        print(" - {0:<25} : {1:>10.2f}".format(self.name, self.count))



class Wagon:
    def __init__(self):
        self.name = ""
        self.output = None
        self.station = None
        self.stacks = []
        self.suppliers = {}
        self.next_wagon = None
        self.prev_wagon = None


    def create(self, output, station):
        self.name = output.name
        self.output = output
        self.station = station
        self.stacks = [Stack() for i in range(STACK_CAPACITY)]
        return True


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
        if not self.reserve_space(self.output, _product_increase):
            return False

        for _component in self.output.components:
            _component_increase = _production_cycles * _component.amount
            _supplier = self.suppliers.get(_component.name)
            _wagon_iter = self.prev_wagon

            # Reserve space until the supplier or the base wagon is reached.
            while _wagon_iter is not _supplier:
                if not _wagon_iter.reserve_space(_component.product, amount):
                    return False
                _wagon_iter = _wagon_iter.prev_wagon

            # Reserve space in the base wagon.
            if _component.product.is_base:
                if not _wagon_iter.reserve_space(_component.product, amount):
                    return False
                continue

            # Recursively reserve output of supplier.
            if not _supplier.reserve_output(_component_increase):
                return False
        return True


    def unreserve_all(self):
        for _stack in self.stacks:
                _stack.unreserve()


    def confirm_all(self):
        for _stack in self.stacks:
                _stack.confirm()


    def print(self, verbosity):
        _empty_stacks = 0
        for _stack in self.stacks:
            if _stack.empty:
                _empty_stacks += 1
                continue
            if verbosity == "High":
                _stack.print()

        print(" - {0:<25} : {1:>10.2f}\n".format("Empty stacks", _empty_stacks))



class Train:
    def __init__(self):
        self.name = ""
        self.output = None
        self.config = None
        self.wagons = []
        self.wagon_tree = None
        self.base_wagon = None


    def create(self, config, recipe):
        self.name = recipe.root.name
        self.output = recipe.root
        self.config = config

        self.base_wagon = Wagon()
        if not self.base_wagon.create(Product("Base"), Station()):
            print("Train erro: Failed to create base wagon")
            return False

        self.wagon_tree = self.create_tree(recipe.root)
        if self.wagon_tree is self.base_wagon:
            print("Train error: Failed to create train")
            return False

        # Place the base wagon at the end of the train.
        self.wagons[-1].prev_wagon = self.base_wagon
        self.wagons.append(self.base_wagon)
        return True
   

    def create_tree(self, product):
        # Base products are supplied by the base wagon.
        if product.is_base:
            return self.base_wagon

        _wagon = Wagon()
        if not _wagon.create(product, Station()):
            print("Train warning: Failed to create wagon for:", product.name)
            return self.base_wagon

        # Link previous wagon wagon to this wagon. 
        if len(self.wagons) > 0:
            self.wagons[-1].prev_wagon = _wagon
    
        self.wagons.append(_wagon)

        # Create supplier wagon(s) for each component.
        for _component in product.components:
            _wagon.suppliers[_component.name] = self.create_tree(_component.product)
        return _wagon


    def find_max_output(self):
        # Find the max output with this train configuration.
        _i = 0
        while True:
            if not self.wagon_tree.reserve_output(_i):
                self.unreserve_all()
                break
            self.confirm_all()
            _i += 1
        return True


    def unreserve_all(self):
        for _wagon in self.wagons:
            _wagon.unreserve_all()


    def confirm_all(self):
        for _wagon in self.wagons:
            _wagon.confirm_all()


    def print(self):
        if len(self.wagons) == 0:
            print("Train is empty")
            return

        print("\n{0:-^{line_len}s}\n".format(self.name + " train", line_len=LINE_LEN))
        _output = 0
        for _stack in self.wagons[0].stacks:
            _output += _stack.count
        print("Output: {} {}\n".format(_output, self.name))

        _wagon_num = 1
        for _wagon in self.wagons:
            print("Wagon {} --> {}".format(_wagon_num, _wagon.name))
            _wagon.print(self.config.verbosity)
            _wagon_num += 1
        print("\n{0:-^{line_len}s}\n".format("", line_len=LINE_LEN))