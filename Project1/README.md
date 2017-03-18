# Project 1

These are my solutions for the project 1. The project consisted on implementing a solver of 8-puzzle instances (actually N-puzzle). It contains 3 source codes:

* driver.py: The main file of this project. It receives 2 arguments, the search strategy and the puzzle as a comma separated string.

* utils.py: Contain implementation of basic data structure for implementing the search strategies.

* search.py: It is sort of a framework, in which given a problem (defined as a class), can apply search strategies to that problem for finding a solution.

* visualizer.py: Solves a random instance of 8-puzzle given a strategy, and then, shows in a GUI the path to the solution (It uses Tkinter).

## Test Case no. 1


`python driver.py bfs 3,1,2,0,4,5,6,7,8`

`python driver.py dfs 3,1,2,0,4,5,6,7,8`

`python driver.py ast 3,1,2,0,4,5,6,7,8`

`python driver.py ida 3,1,2,0,4,5,6,7,8`


## Test Case no. 2

`python driver.py bfs 1,2,5,3,4,0,6,7,8`

`python driver.py dfs 1,2,5,3,4,0,6,7,8`

`python driver.py ast 1,2,5,3,4,0,6,7,8`

`python driver.py ida 1,2,5,3,4,0,6,7,8`

