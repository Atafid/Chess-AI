import pygame as py
from class_case import *
from class_pieces import *
from class_player import *
from config import *
from functions import *

py.init()

screen = py.display.set_mode((512, 512))
py.display.set_caption("test")

pawn = py.image.load("sprites/white-pawn.png").convert_alpha()

tower = py.image.load("sprites/white-tower.png").convert_alpha()
knight = py.image.load("sprites/white-knight.png").convert_alpha()
bishop = py.image.load("sprites/white-bishop.png").convert_alpha()
queen = py.image.load("sprites/white-queen.png").convert_alpha()

pieces = [tower, knight, bishop, queen]

circle = py.Rect((0, 0), (50, 50))

case = []

for i in range(4):
    case.append(py.Rect((60*i, 50), (60, 60)))

pawn_width = pawn.get_width()
pawn_height = pawn.get_height()

pawn_x = 256-pawn_width/2
pawn_y = 256-pawn_height/2

quit = False

i = 3

if (1 == 1):
    if (i == 3):
        print("ok")

    if (2 == 2):
        print("test")


def construct_chessboard():
    colors = [WHITE, BLACK]
    chessboard = []

    for i in range(8):
        row = []

        for j in range(8):
            new_case = Case(j*CASE_WIDTH, i*CASE_HEIGHT, colors[(i+j) % 2])
            row.append(new_case)

        chessboard.append(row)

    return (chessboard)


chessboard = construct_chessboard()
player = Player("white", False)

chessboard[0][5].piece = Knight("white", chessboard[0][5], player)


def animation(piece, new_case):
    i, j = coordinates_to_indexes(piece.x, piece.y)
    i_case, j_case = coordinates_to_indexes(new_case.x, new_case.y)
    
    


while (not (quit)):
    screen.fill((0, 0, 0))

    for e in py.event.get():
        if (e.type == py.QUIT):
            quit = True

    for row in chessboard:
        for case in row:
            piece = case.display(screen)

            if (piece != None):
                screen.blit(piece.app, (piece.x, piece.y))

    py.display.update()
