import pygame as py
from config import CASE_HEIGHT, CASE_WIDTH, SELECTION_COLOR


class Case:
    def __init__(self, x, y, color, piece=None):
        self.app = py.Rect((x, y), (CASE_WIDTH, CASE_HEIGHT))
        self.x = x
        self.y = y

        self.color = color
        self.piece = piece

        self.selected = False
        self.possible_move_to = False

        self.controlled = []

    def copy(self):

        if (self.piece != None):
            copy_piece = self.piece.copy()

        else:
            copy_piece = None

        copy_case = Case(self.x, self.y, self.color, copy_piece)

        if (copy_piece != None):
            copy_piece.set_new_case(copy_case)

        return (copy_case)

    def display(self, window):
        if (not (self.selected)):
            py.draw.rect(window, self.color, self.app)

        else:
            py.draw.rect(window, SELECTION_COLOR, self.app)

        if (self.piece != None):
            return (self.piece)
