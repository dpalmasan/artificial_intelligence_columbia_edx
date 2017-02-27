from Grid       import Grid
from ComputerAI import ComputerAI
from PlayerAI   import PlayerAI
from random     import randint
import time

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.1
allowance = 0.05

class Experiments:
    def __init__(self, size = 4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        self.computerAI = None
        self.playerAI   = None
        self.over       = False

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI


    def updateAlarm(self, currTime):
        if currTime - self.prevTime > timeLimit + allowance:
            self.over = True
        else:
            while time.clock() - self.prevTime < timeLimit + allowance:
                pass

            self.prevTime = time.clock()

    def start(self):
        for i in xrange(self.initTiles):
            self.insertRandonTile()


        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0

        self.prevTime = time.clock()

        while not self.isGameOver() and not self.over:
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()

            move = None

            if turn == PLAYER_TURN:
                move = self.playerAI.getMove(gridCopy)

                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canMove([move]):
                        self.grid.move(move)

                        # Update maxTile
                        maxTile = self.grid.getMaxTile()
                    else:
                        self.over = True
                else:
                    self.over = True
            else:
                move = self.computerAI.getMove(gridCopy)

                # Validate Move
                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    self.over = True


            # Exceeding the Time Allotted for Any Turn Terminates the Game
            self.updateAlarm(time.clock())

            turn = 1 - turn
        return maxTile

    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];

    def insertRandonTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

def main():

    results = {}
    runs = 25
    average = 0.0

    for run in xrange(runs):
        experiments = Experiments()
        playerAI  	= PlayerAI()
        computerAI  = ComputerAI()

        experiments.setPlayerAI(playerAI)
        experiments.setComputerAI(computerAI)

        result = experiments.start()
        average += result
        if result not in results:
            results[result] = 1.0
        else:
            results[result] += 1.0

    for key in results.keys():
        results[key] /= runs * 100.0

    print "Average: %1.3f" % average
    print results

if __name__ == '__main__':
    main()
