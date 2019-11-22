# Uniwagon #

An assembly line generator for trains in the video game Factorio. The goal is to create an optimal train assembly line for producible item item in the game.  The rationale for doing this is 1: direct insertion is very UPS efficient and 2: it would be fun to see if you can make rockets without using a single belt in the factory. 

# Explenation #

General procedure:
1. Parse the *.ini supplied by user.
2. Parse the game data JSON files specified in the config.
3. Create a recipe tree of the item specified in the config.
4. Create a a wagon tree with 0 output. This wagon structure looks like a type lattice, with the front wagon at the top, and the base wagon at the bottom. The wagons are also linked linearly as a train.
5. Increment the output of the front wagon. This will cause a recursive increase of output downwards through the wagon lattice. The increased output of a provider wagon is also added to any wagons between it and the consumer. 
6. Repeat step 5 and confirm the reservations until the result of the recursive call is False. At least one of the wagons in the train has now reached its capacity limit, and the last increase should be unreserved. 
7. Print the resulting train assembly line. Verbosity of the print is specified in the config.

# State of the project #

Uniwagon is currently in a working and useful state. However, it has a long way to go before it can produce a full set of assembly lines that makes rockets. The biggest remaining challenge is chemical processing, which needs to be designed in-game first. 

# How to run #

Syntax:
~~~sh
[path to python] -m uniwagon [name of config file]
~~~

Example:
~~~sh
python -m uniwagon advanced_circuit.ini
~~~

Uniwagon can also be installed with pip.