#########################################################
# Author: Diego Palma S.
#
# Apply implemented algorithm for all test cases in .txt
# files, and checks whether it solves the sudokus properly
# This is an auxiliary file for project 3 in the course
# Artificial Intelligence offered by Columbia University
# through edX
#########################################################

from Sudoku import *
import time

with open('sudokus_start.txt') as temp_file:
    sudokus_start = [line.rstrip('\r\n') for line in temp_file]

with open('sudokus_finish.txt') as temp_file:
    sudokus_finish = [line.rstrip('\r\n') for line in temp_file]

N = len(sudokus_start)
for k in xrange(N):
    sudoku = Sudoku(sudokus_start[k])
    csp = SudokuCSP(sudoku)
    AC3(csp)
    x = BacktrackingSearch(csp)
    for var in x:
        csp.domain[var] = [x[var]]
    sol = ""
    for row in "ABCDEFGHI":
        for col in "123456789":
            sol += str(csp.domain[row + col][0])

    print (k + 1, sol == sudokus_finish[k])
    
    time.sleep(0.001)
    
