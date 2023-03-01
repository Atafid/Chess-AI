import pygame as py
import numpy as np
from config import WINDOW_HEIGHT, WINDOW_WIDTH, BACKGROUND_COLOR
from class_game import Game

py.init()

screen = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
py.display.set_caption("Chess AI")

quit = False

game = Game(screen)


while (not (quit)):

    screen.fill(BACKGROUND_COLOR)

    keys = py.key.get_pressed()

    quit = game.update(keys)

    py.display.update()

    for e in py.event.get():
        if (e.type == py.QUIT):
            quit = True
