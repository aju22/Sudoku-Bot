import pygame
import random

WHITE = (255, 255, 255, 255)
ALPHA = 100

BLOCK_COLORS = {
    0: (240, 128, 128, ALPHA),  # RED
    1: (152, 251, 152, ALPHA),  # GREEN
    2: (135, 206, 235, ALPHA),  # BLUE
    3: (127, 255, 212, ALPHA),  # CYAN
    4: (147, 112, 219, ALPHA),  # MAGENTA
    5: (250, 250, 210, ALPHA),  # YELLOW
    6: (244, 164, 96, ALPHA),  # ORANGE
    7: (255, 182, 193, ALPHA),  # PINK
    8: (119, 136, 153, ALPHA)  # GRAY
}

CELL_W = 50
CELL_H = 50
X_OFFSET = 30
Y_OFFSET = 100

pygame.font.init()
my_font = pygame.font.SysFont('Century Schoolbook', 30)


class Cell:
    def __init__(self, x, y, value=0):
        self.row = x
        self.column = y
        self.value = value
        self.block = y // 3 + (x // 3) * 3

        self.collapsed = False
        self.options = [i + 1 for i in range(9)]

    def show(self, screen):
        rec = pygame.Rect((X_OFFSET + self.column * CELL_W, Y_OFFSET + self.row * CELL_H, CELL_W, CELL_H))
        screen.fill(pygame.Color("black"),
                         (X_OFFSET + self.column * CELL_W, Y_OFFSET + self.row * CELL_H, CELL_W, CELL_H))

        surf = pygame.Surface((CELL_W - 20, CELL_H - 20), flags=pygame.SRCALPHA)
        surf.fill(BLOCK_COLORS[self.block])
        screen.blit(surf, (X_OFFSET + self.column * CELL_W + 10, Y_OFFSET + self.row * CELL_H + 10))

        pygame.draw.rect(screen, WHITE, rec, width=1)
        value_text = my_font.render(str(self.value), False, WHITE)

        if self.value:
            screen.blit(value_text, (X_OFFSET + self.column * CELL_W + 15, Y_OFFSET + self.row * CELL_H + 5))

    def update_value(self):
        self.value = (self.value + 1) % 10

    def collapse(self, value=None):
        self.collapsed = True
        choice = None

        if value is None:  # IF VALUE NOT SPECIFIED COLLAPSE TO A RANDOM AVAILABLE OPTION
            choice = random.choice(self.options)
        else:
            choice = value  # IF VALUE PRE-FILLED BY USER, COLLAPSE TO THAT CHOICE

        self.value = choice
        self.options = [choice]

    def getInfo(self):  # FOR DEBUGGING PURPOSES
        print(
            f"\nRow : {self.row}\nColumn : {self.column}\nBlock : {self.block}\nValue: {self.value}"
        )
