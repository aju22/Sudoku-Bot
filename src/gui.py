import pygame
from cell import Cell

WIDTH, HEIGHT = 510, 700
DIM = 9
CELL_W = 50
CELL_H = 50
X_OFFSET = 30
Y_OFFSET = 100


class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # INITIALISE SCREEN
        pygame.display.set_caption("Sudoku")

        pygame.font.init()  # INITIALISE FONT
        self.my_font = pygame.font.SysFont('Century Schoolbook', 40)

        self.grid_cells = []  # INITIALISE GRID
        for i in range(DIM):
            self.grid_cells.append([Cell(i, j) for j in range(DIM)])

        self.showTitle()
        self.button_rec = pygame.Rect((180, 600), (150, 50))
        self.showButton()

    def clearSpace(self):
        self.screen.fill(pygame.Color("black"), (0, Y_OFFSET + DIM * CELL_H, WIDTH, HEIGHT - (Y_OFFSET + DIM * CELL_H)))

    def showTitle(self):
        title_text = self.my_font.render('Sudoku Solver', False, (255, 255, 255))
        self.screen.blit(title_text, (130, 20))

    def showButton(self):
        self.clearSpace()
        button_text = self.my_font.render('Solve', False, (255, 255, 255))
        pygame.draw.rect(self.screen, (0, 100, 100, 100), self.button_rec, border_radius=10)
        self.screen.blit(button_text, (205, 600))

    def showSolved(self):
        self.clearSpace()
        solved_text = self.my_font.render('Solved !', False, (255, 255, 255))
        self.screen.blit(solved_text, (190, 600))

    def showError(self):
        self.clearSpace()
        invalid_text = self.my_font.render('Configuration Invalid.', False, (255, 255, 255))
        self.screen.blit(invalid_text, (50, 600))

