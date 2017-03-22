# Project 2

These are my solutions for the project 2. The project consisted on implementing an AI for 2048-game, it uses minimax with alpha-beta pruning for getting the moves:

* PlayerAI.py: Is the class that contains the logic behind player moves. As it was said, it uses minimax search with alpha-beta pruning for getting the moves.

* GameManager.py. This is the driver program that loads your Computer AI and Player AI, and begins a game where they compete with each other.

* Grid.py. This module defines the Grid object, along with some useful operations: move(), getAvailableCells(), insertTile(), and clone(), which you may use in your code. These are available to get you started, but they are by no means the most efficient methods available. If you wish to strive for better performance, feel free to ignore these and write your own helper methods in a separate file.

* BaseAI.py. This is the base class for any AI component. All AIs inherit from this module, and implement the getMove() function, which takes a Grid object as parameter and returns a move (there are different "moves" for different AIs).

* ComputerAI.py. This inherits from BaseAI. The getMove() function returns a computer action that is a tuple (x, y) indicating the place you want to place a tile.

* BaseDisplayer.py and Displayer.py. These print the grid.

## To execute the code:

`python GameManager.py`



