import pygame
import math
from grid import Grid, isValidGrid
from gui import GUI
import time

DIM = 9
CELL_W = 50
CELL_H = 50
X_OFFSET = 30
Y_OFFSET = 100

gui = GUI()

if __name__ == '__main__':

    SOLVING = False
    SOLVED = False
    GRID = None

    while True:

        if not SOLVING:

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:  # CHECKING IF MOUSE IS CLICKED
                    mouse_x, mouse_y = event.pos

                    # CALCULATING CELL ROW AND CELL COLUMN BASED ON MOUSE CLICK
                    cell_row = math.floor((mouse_y - Y_OFFSET) / CELL_H)
                    cell_column = math.floor((mouse_x - X_OFFSET) / CELL_W)

                    if 0 <= cell_row < DIM and 0 <= cell_column < DIM:
                        # IF VALID ROWS AND COLUMNS -> UPDATE VALUE PER CLICK
                        gui.grid_cells[cell_row][cell_column].update_value()

                    elif gui.button_rec.collidepoint(event.pos):
                        # IF SOLVE BUTTON PRESSED -> FIX VALUES AND START SOLVING
                        SOLVING = True

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        if SOLVING:

            gui.clearSpace() # CLEARS THE SOLVE BUTTON

            if not isValidGrid(gui.grid_cells):  # CHECK IF PRE-FILLED GRID IS VALID
                gui.showError()  # IF NOT THEN, SHOW ERROR FOR SOME TIME
                pygame.display.update()
                time.sleep(3)

                gui.showButton()  # BRING BACK SOLVE BUTTON AND LET USER RETRY
                SOLVING = False
                pygame.display.update()

            else:

                GRID = Grid(gui.grid_cells)  # ONCE GRID IS VERIFIED TO BE CORRECT, INITIALISE GRID OBJECT
                GRID.setEntropy()  # SET INITIAL ENTROPY FROM THE USER-INITIALISED CELLS

            if GRID:
                SOLVED = GRID.solve(gui.screen)  # COLLAPSE THE GRID CELL BY CELL, AND WAIT TILL IT SOLVES
                SOLVING = False

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        if SOLVED:
            gui.showSolved()  # IF SOLVED -> SHOW SOLVED !

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        if GRID is None:
            for i in range(DIM):
                for j in range(DIM):  # KEEP UPDATING AND DISPLAYING GRID VALUES UNTIL USER CLICK SOLVE
                    gui.grid_cells[i][j].show(gui.screen)

        pygame.display.update()
