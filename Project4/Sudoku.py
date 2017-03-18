from CSP import *

# TODO: Just for fun, implement methods for a pc version of sudoku
class Sudoku:
    """
    This class represents a sudoku board.    
    """

    def __init__(self, board):
        """
        Board state is passed as a string of numbers which represents the sudoku from 
        top-left to bottom-right
        """
        self.unassigned = []
        self.board = {}
        k = 0
        for row in "ABCDEFGHI":
            for col in "123456789":
                self.board[row + col] = int(board[k])
                if self.board[row + col] == 0:
                    self.unassigned.append(row + col)
                k += 1

    def getFreeCells(self):
        return list(self.unassigned)

    def getCell(self, var):
        return self.board[var]

    def setCell(self, var, val):
        self.board[var] = val

    def keys(self):
        return self.board.keys()
            
    def __str__(self):
        """
        For debugging purposes, prints the sudoku as a grid of numbers
        """
        s = ""
        line = "-------------------------------------\n"
        s += line
        for row in "ABCDEFGHI":
            s += "|"
            for col in "123456789":
                if self.board[row + col] != 0:
                    s += ("%3d" % self.board[row + col]) + "|"
                else:
                    s += ("%3c" % ' ') + "|"
            s += "\n" + line

        return s

# TODO: This should inherit properties from an abstract class, in order for the algorithms to work with any csp
class SudokuCSP(CSP):
    """
    Class representing the sudoku CSP:
    - Variables: Rows are named from A-I, columns are named from 1-9 and variable names from A1, to I9
    - Domain: Each variable can take values from 1-9
    - Constraints: Sudoku's constraints 
    """

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.variables = sudoku.keys()
        self.unassigned_vars = sudoku.getFreeCells()
        self.domain = {var: [self.sudoku.getCell(var)] if self.sudoku.getCell(var) != 0 else [1, 2, 3, 4, 5, 6, 7, 8, 9] for var in self.variables}
        self.constraints = []
        self.empty = 0

        # Row Constraints (9 in total)
        self.constraints.append(["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"])
        self.constraints.append(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"])
        self.constraints.append(["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"])
        self.constraints.append(["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"])
        self.constraints.append(["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"])
        self.constraints.append(["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"])
        self.constraints.append(["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"])
        self.constraints.append(["H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9"])
        self.constraints.append(["I1", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9"])

        # Col Constraints (9 in total)
        self.constraints.append(["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", "I1"])
        self.constraints.append(["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2"])
        self.constraints.append(["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3", "I3"]) 
        self.constraints.append(["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4", "I4"])
        self.constraints.append(["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5", "I5"]) 
        self.constraints.append(["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6", "I6"])
        self.constraints.append(["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7", "I7"])
        self.constraints.append(["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8", "I8"])
        self.constraints.append(["A9", "B9", "C9", "D9", "E9", "F9", "G9", "H9", "I9"])

        # Squares constraints (9 in total)
        self.constraints.append(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"])
        self.constraints.append(["D1", "D2", "D3", "E1", "E2", "E3", "F1", "F2", "F3"])
        self.constraints.append(["G1", "G2", "G3", "H1", "H2", "H3", "I1", "I2", "I3"])
        self.constraints.append(["A4", "A5", "A6", "B4", "B5", "B6", "C4", "C5", "C6"])
        self.constraints.append(["D4", "D5", "D6", "E4", "E5", "E6", "F4", "F5", "F6"])
        self.constraints.append(["G4", "G5", "G6", "H4", "H5", "H6", "I4", "I5", "I6"])
        self.constraints.append(["A7", "A8", "A9", "B7", "B8", "B9", "C7", "C8", "C9"])
        self.constraints.append(["D7", "D8", "D9", "E7", "E8", "E9", "F7", "F8", "F9"])
        self.constraints.append(["G7", "G8", "G9", "H7", "H8", "H9", "I7", "I8", "I9"])

        self.binary_constraints = []
        for cell in self.variables:
            for constraint in self.constraints:
                if cell in constraint:
                    for otherCell in constraint:
                        if otherCell != cell:
                            self.binary_constraints.append((cell, otherCell))

    def getNeighbors(self, X, restriction=None):
        neighbors = []
        for arc in self.binary_constraints:
            if X == arc[0]:
                if not restriction is None:
                    if restriction != arc[1]:
                        neighbors.append(arc[1])
                else:
                    neighbors.append(arc[1])
        return neighbors
                
    def getUnassignedVariables(self):
        return self.unassigned_vars

    def assignVariable(self, variable, value):
        self.sudoku.setCell(variable, value)

    def checkConsistency(self):
        """
        Returns True if all the constraints are satisfied, false otherwise
        """

        satisfy = True
        for constraint in self.constraints:
            satisfy = satisfy and self.allDiff(constraint)
        return satisfy

    def allDiff(self, variables):
        """
        Check if given variables have all different values (helper method)
        """
        n = len(variables)
        for i in xrange(n - 1):
            if self.sudoku.getCell(variables[i]) != 0:
                for j in xrange(i + 1, n):
                    if self.sudoku.getCell(variables[j]) != 0:
                        if self.sudoku.getCell(variables[i]) == self.sudoku.getCell(variables[j]):
                            return False
        return True

        
# Test client
# TODO: Fix maximum recursion, because the backtraacking search is not properly implemented, does not work on puzzle 4
if __name__ == "__main__":
    s = "000100702030950000001002003590000301020000070703000098800200100000085060605009000"    
    sudoku = Sudoku(s)

    print "Sudoku Inicial:"
    print sudoku
    csp = SudokuCSP(sudoku)
    AC3(csp)
    x = BacktrackingSearch(csp)
    #print x
    for var in x:
        csp.domain[var] = [x[var]]
    sol = ""
    for row in "ABCDEFGHI":
        for col in "123456789":
            sol += str(csp.domain[row + col][0])

    print "Sudoku Final:"
    print Sudoku(sol)
    
