# Project 4

These are my solutions for the project 4. The project consisted on implementing a sudoku's solver, seeing the problem as a constraint satisfaction problem (CSP):

* CSP.py: Implements the algorithms for solving CSPs (AC-3, Backtracking Search w/ forward checking). It also contains an abstract class, to extend the functionality for your own CSP.
* Sudoku.py: It contains a CSP definition for the sudoku problem.
* test.py: Test the solver on 400 different sudokus. It may take a while to run.
* driver.py: The main file for the project. It receives a sudoku as a string from command line and solves it.

## To execute the codes:

`python test.py`

`python driver.py <input_string>`



