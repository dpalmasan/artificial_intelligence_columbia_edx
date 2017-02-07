# File visualizer.py
# This file is used just for visualizing the solutions found by 
# a given search strategy for the 8-puzzle problem
#
# Author: Diego Palma S. (UdeC)

import Tkinter as tk
import sys
import time
from driver import *
import tkMessageBox

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        self.fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Solve Puzzle",underline=0, menu=self.fileMenu)

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        global puzzle
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=600, height=600, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        
        # delay in seconds, used for animation purposes.
        delay = 1

        # Menu
        menubar = MenuBar(self)
        menubar.fileMenu.add_command(label="Breadth First Search", underline=1, command=lambda: self.solve("bfs", delay))
        menubar.fileMenu.add_command(label="Depth First Search", underline=1, command=lambda: self.solve("dfs", delay))
        menubar.fileMenu.add_command(label="Iterative Deepening", underline=1, command=lambda: self.solve("ids", delay))
        menubar.fileMenu.add_command(label="Uniform Cost Search", underline=1, command=lambda: self.solve("ucs", delay))
        menubar.fileMenu.add_command(label="A*", underline=1, command=lambda: self.solve("ast", delay))
        menubar.fileMenu.add_command(label="Iterative Deepening A*", underline=1, command=lambda: self.solve("ida", delay))
        menubar.fileMenu.add_separator()
        menubar.fileMenu.add_command(label="Exit", underline=1, command=self.exit)
        self.config(menu=menubar)

        # Dimensions of GUI, should be edited in future releases
        self.rows = 3
        self.columns = 3
        self.cellwidth = 200
        self.cellheight = 200

        self.rect = {}
        self.puzzle = puzzle
        for column in range(3):
            for row in range(3):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if self.puzzle[row][column] != 0:
                    self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
                    canvas_id = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, font=("Helvetica", 40))
                    self.canvas.itemconfig(canvas_id, text=str(self.puzzle[row][column]))
                else:
                    self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="black", tags="rect")


    def solve(self, method, delay):
        """
        Solves the puzzle using a search strategy (method) and the
        animation has a delay given by delay
        """
        global solver
        global problem
        global state

        print "Searching for a solution using " + method + " strategy"        
        if method == 'bfs':
            solver.breadthFirstSearch(problem)
        elif method == 'dfs':
            solver.depthFirstSearch(problem)
        elif method == 'ucs':
            solver.uniformCostSearch(problem)
        elif method == 'ast':
            solver.aStarSearch(problem, manhattanDistance)
        elif method == 'ida':
            solver.iterativeDeepeningAstar(problem, manhattanDistance)
        else:
            solver.iterativeDeepening(problem)

        print "Solution found!"

        time.sleep(delay)
        for action in solver.path:
            state.move(action)
            for column in range(3):
                for row in range(3):
                    x1 = column*self.cellwidth
                    y1 = row * self.cellheight
                    x2 = x1 + self.cellwidth
                    y2 = y1 + self.cellheight
                    if state.board[row][column] != 0:
                        self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
                        canvas_id = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, font=("Helvetica", 40))
                        self.canvas.itemconfig(canvas_id, text=str(state.board[row][column]))
                    else:
                        self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="black", tags="rect")
            
            # Forcing to refresh after mainloop
            self.update_idletasks()
            time.sleep(delay)

        output = "# of moves: " + str(solver.cost_of_path) + "\n"
        output += "Nodes Expanded: " + str(solver.nodes_expanded) + "\n"
        output += "Fringe Size: " + str(solver.fringe_size) + "\n"
        output += "Max Fringe Size: " + str(solver.max_fringe_size) + "\n"
        output += "Search Depth: " + str(solver.search_depth) + "\n"
        output += "Max Search Depth: " + str(solver.max_search_depth) + "\n"
        output += "Running Time: %.8f\n" % solver.running_time
        output += "Max RAM usage: %.8f\n" % solver.max_ram_usage
        tkMessageBox.showinfo("Statistics", output)

    def exit(self):
        sys.exit(0)

if __name__ == "__main__":
    # We are testing with the "worst case" puzzle
    # TODO: Add command line arguments to test any puzzle
    n = 3
    board = [8, 7, 6, 5, 4, 3, 2, 1, 0]
    board = [board[i:i+n] for i in range(0, len(board), n)]
    zero = next(((i, array.index(0))
        for i, array in enumerate(board)
        if 0 in array),
        None)
    
    state = State(board, zero, 0)
    problem = Npuzzle(state)
    solver = Solver()
    puzzle = state.board
    app = App()
    app.mainloop()
