import math
import random
import time
import copy
from threading import Thread, Event

import pygame.display

DIM = 9
FRAME_TIME = 0.02


class Grid:
    def __init__(self, grid):
        self.OriginalGrid = grid
        self.CopyGrid = copy.deepcopy(self.OriginalGrid)  # KEEP COPY IN CASE, WE NEED TO REST.

    def displayGrid(self, screen, evt):
        while True:    # KEEP DISPLAYING GRID VALUES
            if evt.isSet():
                return ()
            for i in range(DIM):
                for j in range(DIM):
                    self.CopyGrid[i][j].show(screen)

            pygame.display.update()

    def solve(self, screen):

        e = Event()
        display_thread = Thread(target=self.displayGrid, args=[screen, e]) # TO AVOID GUI GOING UNRESPONSIVE
        display_thread.start() # WE SET THE GUI UPDATE TO A SEPARATE THREAD FROM THE MAIN SOLVE LOOP

        while self.notSolved():
            success = self.waveFunction_collapse()
            if success:
                time.sleep(FRAME_TIME)
            else:
                print("Solving failed. Resetting")
                self.reset()

        e.set()
        display_thread.join() # ONCE SOLVED, WE RELEASE THE THREAD AND RETURN
        return True

    def notSolved(self):

        for i in range(DIM):
            for j in range(DIM):
                if self.CopyGrid[i][j].collapsed is False: # CHECK IF EVERY CELL WAS COLLAPSED
                    return True

        return False

    def waveFunction_collapse(self):
        min_options = math.inf  # FIND THE MINIMUM OPTIONS NUMBER
        for i in range(DIM):
            for j in range(DIM):
                if not self.CopyGrid[i][j].collapsed:  # ONLY CONSIDER CELLS NOT COLLAPSED
                    min_options = min(min_options, len(self.CopyGrid[i][j].options))

        least_entropy_cells = []  # FIND ALL THE CELLS HAVING LEAST OPTIONS AVAILABLE -> HAVING MINIMUM ENTROPY
        for i in range(DIM):
            for j in range(DIM):
                if not self.CopyGrid[i][j].collapsed:  # ONLY CONSIDER CELLS NOT COLLAPSED
                    if len(self.CopyGrid[i][j].options) == min_options:
                        self.CopyGrid[i][j].highlight = True
                        least_entropy_cells.append(self.CopyGrid[i][j])

        if len(least_entropy_cells) > 0:
            random_cell = random.choice(least_entropy_cells)  # PICK ONE RANDOMLY FROM THOSE MIN-ENTROPY CELLS

            if len(random_cell.options) == 0:
                # IN THE CASE WHERE WE HAVE RUN OUT OF OPTIONS FOR A CELL,
                # IMPLIES THAT THE RANDOM CHOICES BEING TAKEN SINCE NOW LED TO A SCENARIO,
                # WHERE GRID HAS BECOME UNSOLVABLE.
                # WE RETURN AND RESET THE GRID, AND TRY AGAIN FOR BETTER RANDOM CHOICES :)
                return False

            random_cell.collapse()  # COLLAPSE THE CELL TO A RANDOM VALUE FROM ITS AVAILABLE OPTIONS -> VALUE GETS FIXED

            self.reduce_entropy(random_cell)  # REDUCE ENTROPY OF THE CORRESPONDING ROW, COLUMN AND BLOCK
            # CELLS IN THOSE ROW/COLUMN/BLOCK NOW HAVE LESS OPTIONS TO CHOOSE FROM
            return True

    def reduce_entropy(self, cell):
        row = cell.row
        column = cell.column
        block = cell.block
        pick = cell.options[0]

        for i in range(DIM):
            for j in range(DIM):
                # CONSIDER OTHER CELLS EXCLUDING ITSELF
                if self.CopyGrid[i][j] != cell and self.CopyGrid[i][j].collapsed is False:

                    if self.CopyGrid[i][j].row == row:
                        if pick in self.CopyGrid[i][j].options:
                            # REMOVE THE OPTION SINCE WE CAN'T HAVE DUPLICATES IN A ROW
                            self.CopyGrid[i][j].options.remove(pick)

                    if self.CopyGrid[i][j].column == column:
                        if pick in self.CopyGrid[i][j].options:
                            # REMOVE THE OPTION SINCE WE CAN'T HAVE DUPLICATES IN A COLUMN
                            self.CopyGrid[i][j].options.remove(pick)

                    if self.CopyGrid[i][j].block == block:
                        if pick in self.CopyGrid[i][j].options:
                            # REMOVE THE OPTION SINCE WE CAN'T HAVE DUPLICATES IN A BLOCK
                            self.CopyGrid[i][j].options.remove(pick)

    def setEntropy(self):
        input_cells = []

        for i in range(DIM):
            for j in range(DIM):
                if self.CopyGrid[i][j].value != 0:  # FIND USER-FILLED CELLS
                    input_cells.append(self.CopyGrid[i][j])

        if len(input_cells) > 0:
            for cell in input_cells:
                value = cell.value
                cell.collapse(value)  # PERFORM COLLAPSE TO THE VALUE WHICH WAS FILLED BY USER
                self.reduce_entropy(cell)  # REDUCE ENTROPY OF CORRESPONDING ROW/COLUMN/BLOCK

    def reset(self):
        self.CopyGrid = copy.deepcopy(self.OriginalGrid)  # RESET GRID
        self.setEntropy()  # RESET INITIAL ENTROPY


def isValidGrid(grid):
    input_cells = []

    for i in range(DIM):
        for j in range(DIM):
            if grid[i][j].value != 0:  # FIND CELLS THAT HAVE BEEN PRE-FILLED BY USER
                input_cells.append(grid[i][j])

    for cell in input_cells:
        if check_RowsColsBlocks(cell, grid) is False:  # CHECKS FOR DUPLICATES IN ROW/COLUMN/BLOCK FOR THE
            # USER-FILLED GRID
            return False

    return True


def check_RowsColsBlocks(cell, grid):
    row = cell.row
    column = cell.column
    block = cell.block
    value = cell.value

    for i in range(DIM):
        for j in range(DIM):
            if grid[i][j] != cell:
                if grid[i][j].row == row or grid[i][j].column == column or grid[i][j] == block:
                    if grid[i][j].value == value:  # DUPLICATES FOUND ALONG ROW/COLUMN/BLOCK MAKES THE USER-grid INVALID
                        return False
    return True
