import sys
import time
from resource import getrusage, RUSAGE_SELF
from utils import *

class State:
    """
    Should be an abstract class valid for a given problem. For simplicity, now 
    only works with the 8-puzzle problem
    """
    def __init__(self, board, zero, cost, prev = None, action = None):
        self.board = [list(b) for b in board]
        self.cost = cost
        self.zero = zero
        self.prev = prev
        self.action = action
    def isGoal(self):
        for i in range(3):
            for j in range(3):
                if (3*i + j) != self.board[i][j]:
                    return False
        return True
    def getActions(self):
        """
        Returns a list of available actions from the current state.
        """
        actions = []
        i = self.zero[0]
        j = self.zero[1]
        if i > 0:
            actions.append('Up')
        if i < 2:
            actions.append('Down')
        if j > 0:
            actions.append('Left')
        if j < 2:
            actions.append('Right')
        return actions

    def expand(self):
        """
        Returns a list of states, that are the result of applying
        a list of actions to a current state (successor states)
        """
        actions = self.getActions()
        successors = []
        i, j = self.zero
        for action in actions:
            board = [list(b) for b in self.board]
            if action == 'Up':
                board[i][j] = self.board[i-1][j]
                board[i-1][j] = 0
                successors.append(State(board, (i-1, j), self.cost + 1, self, action))
            elif action == 'Down':
                board[i][j] = self.board[i+1][j]
                board[i+1][j] = 0
                successors.append(State(board, (i+1, j), self.cost + 1, self, action))
            elif action == 'Left':
                board[i][j] = self.board[i][j - 1]
                board[i][j - 1] = 0
                successors.append(State(board, (i, j-1), self.cost + 1, self, action))
            elif action == 'Right':
                board[i][j] = self.board[i][j + 1]
                board[i][j+1] = 0
                successors.append(State(board, (i, j+1), self.cost + 1, self, action))
        return successors


    def __eq__(self, other):
        """
        """
        for row in range( 3 ):
            if self.board[row] != other.board[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        s = "Current moves: " + str(self.cost) + "\n"
        s += "Zero Position: " + str(self.zero) + "\n"
        s += "Board:\n"
        s += '\n'.join([' '.join(str(y) for y in w) for w in self.board ])
        return s           

class Solver:
    def __init__(self, start_state):
        self.path = []
        self.cost_of_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 1
        self.max_fringe_size = 1
        self.search_depth = 0
        self.max_search_depth = 0
        self.running_time = 0
        self.max_ram_usage = 0
        self.start_state = start_state

    def breadthFirstSearch(self):
        """
        Implements Breadth First Search Strategy
        """
        start_time = time.time()
        frontier = Queue()
        frontier.enqueue(self.start_state)
        explored = set()
        while not frontier.isEmpty():
            state = frontier.dequeue()
            self.fringe_size -= 1
            explored.add(state)
            if state.isGoal():
                curr = state
                path = []
                while curr.prev != None:
                    path.insert(0, curr.action)
                    curr = curr.prev
                self.cost_of_path = state.cost
                self.path = path
                self.search_depth = self.cost_of_path
                self.running_time = time.time() - start_time
                return True
            
            neighbors = state.expand()
            self.nodes_expanded += 1
            for neighbor in neighbors:
                if neighbor not in explored:
                    frontier.enqueue(neighbor)
                    explored.add(neighbor)
                    self.fringe_size += 1
                    if self.fringe_size > self.max_fringe_size:
                        self.max_fringe_size = self.fringe_size
                    if neighbor.cost > self.max_search_depth:
                        self.max_search_depth = neighbor.cost
            ram = getrusage(RUSAGE_SELF).ru_maxrss / 1e6
            if ram > self.max_ram_usage:
                self.max_ram_usage = ram
        return False

             
    def depthFirstSearch(self):
        """
        Implements Depth First Search Strategy
        """
        start_time = time.time()
        frontier = Stack()
        frontier.push(self.start_state)
        explored = set()
        while not frontier.isEmpty():
            state = frontier.pop()
            self.fringe_size -= 1
            explored.add(state)
            if state.isGoal():
                curr = state
                path = []
                while curr.prev != None:
                    path.insert(0, curr.action)
                    curr = curr.prev
                self.cost_of_path = state.cost
                self.path = path
                self.search_depth = self.cost_of_path
                self.running_time = time.time() - start_time
                return True
            
            neighbors = state.expand()
            self.nodes_expanded += 1
            neighbors.reverse()
            for neighbor in neighbors:
                if neighbor not in explored:
                    frontier.push(neighbor)
                    explored.add(neighbor)
                    self.fringe_size += 1
                    if self.fringe_size > self.max_fringe_size:
                        self.max_fringe_size = self.fringe_size
                    if neighbor.cost > self.max_search_depth:
                        self.max_search_depth = neighbor.cost
            ram = getrusage(RUSAGE_SELF).ru_maxrss / 1e6
            if ram > self.max_ram_usage:
                self.max_ram_usage = ram
        return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python driver.py <method> <board>'
        sys.exit(0)

    method = sys.argv[1]
    board = [int(i) for i in sys.argv[2].split(",")]
    board = [board[i:i+3] for i in range(0, len(board), 3)]
    zero = next(((i, array.index(0))
        for i, array in enumerate(board)
        if 0 in array),
        None)
    
    state = State(board, zero, 0)
    
    
    solver = Solver(state)
    if method == 'bfs':
        solver.breadthFirstSearch()
    else:
        solver.depthFirstSearch()

    with open("output.txt", "w") as text_file:
        text_file.write("path_to_goal: ") 
        text_file.write(str(solver.path) + "\n")
        text_file.write("cost_of_path: ") 
        text_file.write(str(solver.cost_of_path) + "\n")
        text_file.write("nodes_expanded: ")
        text_file.write(str(solver.nodes_expanded) + "\n")
        text_file.write("fringe_size: ")
        text_file.write(str(solver.fringe_size) + "\n")
        text_file.write("max_fringe_size: ")
        text_file.write(str(solver.max_fringe_size) + "\n")
        text_file.write("search_depth: ")
        text_file.write(str(solver.search_depth) + "\n")
        text_file.write("max_search_depth: ")
        text_file.write(str(solver.max_search_depth) + "\n")
        text_file.write("running_time: ")
        text_file.write(("%.8f") % solver.running_time + "\n")
        text_file.write("max_ram_usage: ")
        text_file.write(("%.8f") % solver.max_ram_usage + "\n")
