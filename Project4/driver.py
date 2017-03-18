#########################################################
# Author: Diego Palma S.
#
# Solves a sudoku passed as a string from comand line
# This is the main file for project 3 in the course
# Artificial Intelligence offered by Columbia University
# through edX
#########################################################

from Sudoku import *
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python driver.py <input_string>'
        sys.exit(0)

    sudoku = Sudoku(sys.argv[1])
    csp = SudokuCSP(sudoku)
    AC3(csp)

    # Gets assignment from remaining cells
    x = BacktrackingSearch(csp)

    for var in x:
        csp.domain[var] = [x[var]]

    sol = ""
    for row in "ABCDEFGHI":
        for col in "123456789":
            sol += str(csp.domain[row + col][0])

    with open("output.txt", "w") as output:
        output.write(sol)

