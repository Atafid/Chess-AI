import pygame as py
from src.class_case import *
from src.class_pieces import *
from src.class_player import *
from src.config import *
from src.functions import *
from src.minmax import *
from random import randint

py.init()

screen = py.display.set_mode((512, 512))
py.display.set_caption("test")

pawn = py.image.load("ressources/sprites/white-pawn.png").convert_alpha()

tower = py.image.load("ressources/sprites/white-tower.png").convert_alpha()
knight = py.image.load("ressources/sprites/white-knight.png").convert_alpha()
bishop = py.image.load("ressources/sprites/white-bishop.png").convert_alpha()
queen = py.image.load("ressources/sprites/white-queen.png").convert_alpha()

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

anim_piece = False
anim_compt = 0

points = []
y_points = []

pressed = False


def construct_chessboard(players):
    colors = [WHITE, BLACK]
    chessboard = []

    low_player = randint(0, 1)
    players[1-low_player].ia = False

    for i in range(NB_CASE_LINE):
        line = []

        for j in range(NB_CASE_LINE):
            new_case = Case(j*CASE_WIDTH, i*CASE_HEIGHT, colors[(i+j) % 2])

            if (i == 0):
                if (j == 0 or j == NB_CASE_LINE-1):
                    new_case.piece = Tower(
                        players[1-low_player].color, new_case, players[1-low_player])
                    players[1 -
                            low_player].pieces["tower"] += [new_case.piece]

                if (j == 1 or j == NB_CASE_LINE-2):
                    new_case.piece = Knight(
                        players[1-low_player].color, new_case, players[1-low_player])
                    players[1 -
                            low_player].pieces["knight"] += [new_case.piece]

                if (j == 2 or j == NB_CASE_LINE-3):
                    new_case.piece = Bishop(
                        players[1-low_player].color, new_case, players[1-low_player])
                    players[1 -
                            low_player].pieces["bishop"] += [new_case.piece]

                if (j == 3):
                    new_case.piece = Queen(
                        players[1-low_player].color, new_case, players[1-low_player])
                    players[1 -
                            low_player].pieces["queen"] += [new_case.piece]

                if (j == NB_CASE_LINE-4):
                    new_case.piece = King(
                        players[1-low_player].color, new_case, players[1-low_player])
                    players[1 -
                            low_player].pieces["king"] += [new_case.piece]

            if (i == NB_CASE_LINE-1):
                if (j == 0 or j == NB_CASE_LINE-1):
                    new_case.piece = Tower(
                        players[low_player].color, new_case, players[low_player])
                    players[low_player].pieces["tower"] += [new_case.piece]

                if (j == 1 or j == NB_CASE_LINE-2):
                    new_case.piece = Knight(
                        players[low_player].color, new_case, players[low_player])
                    players[low_player].pieces["knight"] += [new_case.piece]

                if (j == 2 or j == NB_CASE_LINE-3):
                    new_case.piece = Bishop(
                        players[low_player].color, new_case, players[low_player])
                    players[low_player].pieces["bishop"] += [new_case.piece]

                if (j == 3):
                    new_case.piece = Queen(
                        players[low_player].color, new_case, players[low_player])
                    players[low_player].pieces["queen"] += [new_case.piece]

                if (j == NB_CASE_LINE-4):
                    new_case.piece = King(
                        players[low_player].color, new_case, players[low_player])
                    players[low_player].pieces["king"] += [new_case.piece]

            if (i == 1):
                new_case.piece = Pawn(
                    players[1-low_player].color, new_case, players[1-low_player], False)
                players[1 -
                        low_player].pieces["pawn"] += [new_case.piece]

            if (i == NB_CASE_LINE-2):
                new_case.piece = Pawn(
                    players[low_player].color, new_case, players[low_player], True)
                players[low_player].pieces["pawn"] += [new_case.piece]

            line.append(new_case)

        chessboard.append(line)

    return (chessboard)


player = Player("white", False)
playerTwo = Player("black", False)

players = [player, playerTwo]

chessboard = construct_chessboard(players)

check_controlled_case(chessboard, players[0].get_possible_movements(chessboard), players[0].color,
                      players[1].get_possible_movements(chessboard), players[1].color)
test = minMaxTree([player, playerTwo], 0, chessboard)

k, l, i, j = test.get_best_move()
chessboard[k][l].piece = chessboard[i][j].piece
chessboard[i][j].piece = None

chessboard[k][l].piece.set_new_case(chessboard[k][l])


def animation(piece, new_case):
    i, j = coordinates_to_indexes(piece.x, piece.y)
    i_case, j_case = coordinates_to_indexes(new_case.x, new_case.y)

    alpha = (new_case.y - piece.y)/(new_case.x - piece.x)
    beta = piece.y-alpha*piece.x

    nb_points = 1000
    interv = abs(piece.x-new_case.x)

    begin_point = min(piece.x, new_case.x)
    h = interv/nb_points

    x_points = [piece.x+((-1)**(piece.x-new_case.x > 0))
                * h*i for i in range(nb_points+1)]
    y_points = [alpha*x+beta for x in x_points]

    return ((x_points, y_points))


while (not (quit)):
    screen.fill((0, 0, 0))

    for e in py.event.get():
        if (e.type == py.QUIT):
            quit = True

    if (py.key.get_pressed()[py.K_SPACE] and not (pressed)):
        anim_piece = True

        points, y_points = animation(chessboard[0][5].piece, chessboard[2][4])
        pressed = True

    if (anim_piece):
        chessboard[0][5].piece.x = points[anim_compt]
        chessboard[0][5].piece.y = y_points[anim_compt]

        anim_compt += 1

        if (anim_compt > 1000):
            anim_piece = False
            anim_compt = 0

            chessboard[0][5].piece.case = chessboard[2][4]
            chessboard[2][4].piece = chessboard[0][5].piece

            chessboard[0][5].piece = None

    piece_to_disp = []

    for row in chessboard:
        for case in row:
            piece = case.display(screen)

            if (piece != None):
                piece_to_disp.append(piece)

    for piece in piece_to_disp:
        screen.blit(piece.app, (piece.x, piece.y))

    py.display.update()
