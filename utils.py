import os
import pygame

pygame.init()
pygame.font.init()


WIN_SIZE = (800, 600)
WIN_WIDTH = WIN_SIZE[0]
WIN_HEIGHT = WIN_SIZE[1]

COLORS = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "CYAN": (0, 255, 255),
    "MAGENTA": (255, 0, 255),
    "PURPLE": (128, 0, 128),
    "SALMON": (250, 128, 114),
    "GOLD": (218, 165, 32),
    "SLATE_GRAY": (112, 128, 144)
}

BUTTON_FONT = pygame.font.SysFont("comicsans", 40)
MAIN_TEXT_FONT = pygame.font.SysFont("arial", 30)
TEXT_FONT = pygame.font.SysFont("comicsans", 25)
NOTIFICATIONS_FONT = pygame.font.SysFont("arial", 20)


class Button():
    def __init__(self, color, x, y, width, height, text="", text_size=10):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size


    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            text = BUTTON_FONT.render(self.text, 1, COLORS["BLACK"])
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


class Box:
    DEFAULT_BOX_IMG = pygame.transform.scale(pygame.image.load(os.path.join("src", "box.png")), (120, 120))
    X_IMG = pygame.transform.scale(pygame.image.load(os.path.join("src", "x.png")), (120, 120))
    O_IMG = pygame.transform.scale(pygame.image.load(os.path.join("src", "o.png")), (120, 120))

    WIDTH = DEFAULT_BOX_IMG.get_width()
    HEIGHT = DEFAULT_BOX_IMG.get_height()


    def __init__(self, x, y, width=10, height=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = Box.DEFAULT_BOX_IMG

    
    def draw(self, win: pygame.Surface):
        win.blit(self.img, (self.x, self.y))


    def set(self, symbole: str):
        if symbole.upper() == "X":
            self.img = Box.X_IMG
        elif symbole.upper() == "O":
            self.img = Box.O_IMG
