from random import randint
from BaseAI import BaseAI
import time

# TODO: Tune weights for obtaining a better performance
# TODO: Try more heuristics
# TODO: Try an optimization scheme for weights
# TODO: Try other ordering schemes

# Time limit for moves
timeLimit = 0.1
allowance = 0.05
debug = {}

class State:
    def __init__(self, grid, move=None, depth=0):
        self.grid = grid
        self.move = move
        self.depth = depth

    def children(self, isMax=True):
        """
        Returns a list of the states, that are childs of the current state
        """
        children = []

        if isMax:
            moves = self.grid.getAvailableMoves()
            for move in moves:
                newGrid = self.grid.clone()
                newGrid.move(move)
                children.append(State(newGrid, move, self.depth + 1))
            children.sort(key=evalFun, reverse=True)
        else:
            availableCells = self.grid.getAvailableCells()
            if len(availableCells) > 0:
                for cell in self.grid.getAvailableCells():
                    newGrid = self.grid.clone()
                    newGrid.setCellValue(cell, 2)
                    children.append(State(newGrid, self.move, self.depth + 1))
                    newGrid = self.grid.clone()
                    newGrid.setCellValue(cell, 4)
                    children.append(State(newGrid, self.move, self.depth + 1))
                
            children.sort(key=evalFun)
        return children

    def __eq__(self, other):
        """
        """
        for row in xrange( self.grid.size ):
            if self.grid.map[row] != other.grid.map[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.grid.map))


def evalFun(state):
    """
    Use heuristics to give a value to the state. Returns that value
    """

    # TODO: Improve heuristic to pass grader tests
    maxTile = state.grid.getMaxTile()
    availableCells = len(state.grid.getAvailableCells())

    # Path Search Heuristic
    r = 0.5
    score1 = state.grid.map[3][0] + state.grid.map[3][1]*r
    score1 += state.grid.map[3][2]*r**2 + state.grid.map[3][3]*r**3
    score1 += state.grid.map[2][3]*r**4 + state.grid.map[2][2]*r**5 + state.grid.map[2][1]*r**6
    score1 += state.grid.map[2][0]*r**7 + state.grid.map[1][0]*r**8 + state.grid.map[1][1]*r**9
    score1 += state.grid.map[1][2]*r**10 + state.grid.map[1][3]*r**11 + state.grid.map[0][3]*r**12
    score1 += state.grid.map[0][2]*r**13 + state.grid.map[0][1]*r**14 + state.grid.map[0][0]*r**15
    
    score2 = state.grid.map[3][0] + state.grid.map[2][0]*r
    score2 += state.grid.map[1][0]*r**2 + state.grid.map[0][0]*r**3
    score2 += state.grid.map[0][1]*r**4 + state.grid.map[1][1]*r**5 + state.grid.map[2][1]*r**6
    score2 += state.grid.map[3][1]*r**7 + state.grid.map[3][2]*r**8 + state.grid.map[2][2]*r**9
    score2 += state.grid.map[1][2]*r**10 + state.grid.map[0][2]*r**11 + state.grid.map[0][3]*r**12
    score2 += state.grid.map[1][3]*r**13 + state.grid.map[2][3]*r**14 + state.grid.map[3][3]*r**15
    return maxTile + 10*max(score1, score2) + 3*availableCells

class InterruptExecution (Exception):
    """
    This is used to imprement IDS with time constraint, just for passing the grader.
    """

    pass

def minimize(state, alpha, beta, maxDepth):
    """
    Minimize function, using alpha beta prunning, implemented as lecture slides.
    Finds the child state with the lowest utility value
    """
    global start_time
    deltaT = time.clock() - start_time

    if deltaT >= timeLimit:
        raise (InterruptExecution('Stop the damn thing'))

    children = state.children(False)
    terminalTest = len(children) == 0
    if state.depth > maxDepth or deltaT > timeLimit + allowance or terminalTest:
        return (None, evalFun(state))

    (minChild, minUtility) = (None, float('Inf'))

    for child in children:
        (_, utility) = maximize(child, alpha, beta, maxDepth)
        
        if utility < minUtility:
            (minChild, minUtility) = (child, utility)

        if minUtility <= alpha:
            break
    
        if minUtility < beta:
            beta = minUtility

    return (minChild, minUtility)

def maximize(state, alpha, beta, maxDepth):
    """
    Maximize function, using alpha beta prunning, implemented as lecture slides.
    Finds the child state with the highest utility value
    """
    global start_time, deltaT
    deltaT = time.clock() - start_time

    if deltaT >= timeLimit:
        raise (InterruptExecution('Stop the damn thing'))

    children = state.children()
    terminalTest = len(children) == 0
    if state.depth > maxDepth or terminalTest:
        return (None, evalFun(state))

    (maxChild, maxUtility) = (None, float('-Inf'))
    
    for child in children:
        (_, utility) = minimize(child, alpha, beta, maxDepth)

        if utility > maxUtility:
            (maxChild, maxUtility) = (child, utility)

        if maxUtility >= beta:
            break

        if maxUtility > alpha:
            alpha = maxUtility

    return (maxChild, maxUtility)

def decision(state, maxDepth):
    """
    Finds and returns de state with the highest utility value
    """
    global start_time
      
    (child, _) = maximize(state, float('-Inf'), float('Inf'), maxDepth)

    return child



class PlayerAI(BaseAI):
    def getMove(self, grid):
        """
        Uses minimax with alpha-beta prunning, modified to IDS for time constraints.
        Returns the last deeper answer.
        """
        global start_time, deltaT
        start_time = time.clock()
        #moves = grid.getAvailableMoves()
        #return moves[randint(0, len(moves) - 1)] if moves else None

        depth = 1
        initial = State(grid)
        lastAnswer = decision(initial, depth)
        while True:
            depth += 1
            #initial = State(grid)
            try:
                child = decision(initial, depth)
            except InterruptExecution:
                break
            
            lastAnswer = child
            
            

        return lastAnswer.move

# Test client, for testing with different configurations of the grid
if __name__ == '__main__':
    from Grid import Grid
    grid = Grid()
    grid.map = [[4, 16, 8, 2], [8, 32, 512, 2], [256, 64, 32, 8], [2, 4, 16, 2]]

    playerAI = PlayerAI()
    print playerAI.getMove(grid)

    
