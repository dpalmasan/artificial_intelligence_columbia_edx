import sys
import time
from utils import *

class State:
    """
    Should be an abstract class valid for a given problem. For simplicity, now 
    only works with the 8-puzzle problem
    """
    def __init__(self, board, zero, cost):
        self.board = [list(b) for b in board]
        self.cost = cost
        self.zero = zero
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
                successors.append((State(board, (i-1, j), self.cost + 1), action))
            elif action == 'Down':
                board[i][j] = self.board[i+1][j]
                board[i+1][j] = 0
                successors.append((State(board, (i+1, j), self.cost + 1), action))
            elif action == 'Left':
                board[i][j] = self.board[i][j - 1]
                board[i][j - 1] = 0
                successors.append((State(board, (i, j-1), self.cost + 1), action))
            elif action == 'Right':
                board[i][j] = self.board[i][j + 1]
                board[i][j+1] = 0
                successors.append((State(board, (i, j+1), self.cost + 1), action))
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
        self.path = 0
        self.cost_of_path = 0
        self.nodes_expanded = 0
        self.fringe_size = 0
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
        closed = set()
        fringe = Queue()
        paths = Queue()
        
        initial = self.start_state
        fringe.enqueue(initial)
        paths.enqueue([])
        while True:
            if fringe.isEmpty():
                self.path = []
                return
           
            # We add every node we want to expand, to the closed list 
            node = fringe.dequeue()
            closed.add(node)
            path = paths.dequeue()
            if node.isGoal():
                self.cost_of_path = len(path)
                self.fringe_size = len(fringe)
                self.path = path
                self.search_depth = self.cost_of_path
                self.running_time = time.time() - start_time
                return
            
            self.nodes_expanded += 1
            for child_node in node.expand():
                if child_node[0] not in closed:
                    tmp = list(path)
                    fringe.enqueue(child_node[0])
                    tmp.append(child_node[1])
                    paths.enqueue(tmp)
                    if len(fringe) > self.max_fringe_size:
                        self.max_fringe_size = len(fringe)
                    if child_node[0].cost > self.max_search_depth:
                        self.max_search_depth = child_node[0].cost

             
    def depthFirstSearch(self):
        """
        Implements Depth First Search Strategy
        """
        start_time = time.time()
        closed = set()
        fringe = Stack()
        paths = Stack()

        initial = self.start_state
        fringe.push(initial)
        paths.push([])
       
        while True:
            if fringe.isEmpty():
                self.path = []
                return

            # We add every node we want to expand, to the closed list 
            node = fringe.pop()
            closed.add(node)
            path = paths.pop()
            if node.isGoal():
                self.cost_of_path = len(path)
                self.fringe_size = len(fringe)
                self.path = path
                self.search_depth = self.cost_of_path
                self.running_time = time.time() - start_time
                return

            self.nodes_expanded += 1
            successors = node.expand()
            successors.reverse()
            for child_node in successors:
                if child_node[0] not in closed and child_node[0] not in fringe.stack:
                    tmp = list(path)
                    fringe.push(child_node[0])
                    tmp.append(child_node[1])
                    paths.push(tmp)
                    if len(fringe) > self.max_fringe_size:
                        self.max_fringe_size = len(fringe)
                    if child_node[0].cost > self.max_search_depth:
                        self.max_search_depth = child_node[0].cost

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
    print "path_to_goal:", 
    print solver.path
    print "cost_of_path:", 
    print solver.cost_of_path
    print "nodes_expanded:",
    print solver.nodes_expanded
    print "fringe_size:",
    print solver.fringe_size
    print "max_fringe_size:",
    print solver.max_fringe_size
    print "search_depth:",
    print solver.search_depth
    print "max_search_depth:",
    print solver.max_search_depth
    print "running_time:",
    print ("%.8f") % solver.running_time
