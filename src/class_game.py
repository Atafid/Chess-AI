import pygame as py
from .config import WINDOW_WIDTH, KEYBOARD_CONTROLL, WHITE, BLACK, NB_CASE_LINE, CASE_HEIGHT, CASE_WIDTH, POINT_MOVE_HEIGHT, POINT_MOVE_WIDTH, POSSIBLE_MOVE_COLOR, PROMOTE_CASE_HEIGHT, PROMOTE_CASE_WIDTH, NB_POINTS_ANIMATION
from .functions import indexes_to_coordinates, coordinates_to_indexes, check_controlled_case, remove_chess_moves, animation
from .class_player import Player
from .class_case import Case
from .class_pieces import Pawn, Tower, Knight, Bishop, Queen, King
from random import randint


class Game:
    def __init__(self, window):

        self.players = [Player("white", False), Player("black", False)]
        self.turn = 0
        self.actual_player = self.players[0]

        self.chessboard = self.init_chessboard()
        self.update_moves()

        self.window = window

        self.piece_floating = False

        if (KEYBOARD_CONTROLL):
            self.selected_case = self.chessboard[0][0]
            self.selected_case_coordinates = (0, 0)
            self.selected_case.selected = True

        self.selected_piece = None
        self.selected_piece_coordinates = (0, 0)

        self.key_pressed = False

        self.movements = []

        self.end = False

        self.promoting = False

        self.animation = False
        self.animation_count = 0
        self.animated_piece = None
        self.animation_points = []

    def init_chessboard(self):
        colors = [WHITE, BLACK]
        chessboard = []

        low_player = randint(0, 1)
        self.players[1-low_player].ia = False

        for i in range(NB_CASE_LINE):
            line = []

            for j in range(NB_CASE_LINE):
                new_case = Case(j*CASE_WIDTH, i*CASE_HEIGHT, colors[(i+j) % 2])

                if (i == 0):
                    if (j == 0 or j == NB_CASE_LINE-1):
                        new_case.piece = Tower(
                            self.players[1-low_player].color, new_case, self.players[1-low_player])
                        self.players[1 -
                                     low_player].pieces["tower"] += [new_case.piece]

                    if (j == 1 or j == NB_CASE_LINE-2):
                        new_case.piece = Knight(
                            self.players[1-low_player].color, new_case, self.players[1-low_player])
                        self.players[1 -
                                     low_player].pieces["knight"] += [new_case.piece]

                    if (j == 2 or j == NB_CASE_LINE-3):
                        new_case.piece = Bishop(
                            self.players[1-low_player].color, new_case, self.players[1-low_player])
                        self.players[1 -
                                     low_player].pieces["bishop"] += [new_case.piece]

                    if (j == 3):
                        new_case.piece = Queen(
                            self.players[1-low_player].color, new_case, self.players[1-low_player])
                        self.players[1 -
                                     low_player].pieces["queen"] += [new_case.piece]

                    if (j == NB_CASE_LINE-4):
                        new_case.piece = King(
                            self.players[1-low_player].color, new_case, self.players[1-low_player])
                        self.players[1 -
                                     low_player].pieces["king"] += [new_case.piece]

                if (i == NB_CASE_LINE-1):
                    if (j == 0 or j == NB_CASE_LINE-1):
                        new_case.piece = Tower(
                            self.players[low_player].color, new_case, self.players[low_player])
                        self.players[low_player].pieces["tower"] += [new_case.piece]

                    if (j == 1 or j == NB_CASE_LINE-2):
                        new_case.piece = Knight(
                            self.players[low_player].color, new_case, self.players[low_player])
                        self.players[low_player].pieces["knight"] += [new_case.piece]

                    if (j == 2 or j == NB_CASE_LINE-3):
                        new_case.piece = Bishop(
                            self.players[low_player].color, new_case, self.players[low_player])
                        self.players[low_player].pieces["bishop"] += [new_case.piece]

                    if (j == 3):
                        new_case.piece = Queen(
                            self.players[low_player].color, new_case, self.players[low_player])
                        self.players[low_player].pieces["queen"] += [new_case.piece]

                    if (j == NB_CASE_LINE-4):
                        new_case.piece = King(
                            self.players[low_player].color, new_case, self.players[low_player])
                        self.players[low_player].pieces["king"] += [new_case.piece]

                if (i == 1):
                    new_case.piece = Pawn(
                        self.players[1-low_player].color, new_case, self.players[1-low_player], False)
                    self.players[1 -
                                 low_player].pieces["pawn"] += [new_case.piece]

                if (i == NB_CASE_LINE-2):
                    new_case.piece = Pawn(
                        self.players[low_player].color, new_case, self.players[low_player], True)
                    self.players[low_player].pieces["pawn"] += [new_case.piece]

                line.append(new_case)

            chessboard.append(line)

        return (chessboard)

    def update_moves(self):
        for player in self.players:
            player.get_possible_movements(self.chessboard)
        check_controlled_case(self.chessboard, self.players)

    def set_selected_case(self, i, j):
        self.selected_case.selected = False

        self.selected_case = self.chessboard[i][j]
        self.selected_case_coordinates = (i, j)
        self.selected_case.selected = True

    def handle_keyboard(self, keys):
        if (True in keys):
            if (not (self.key_pressed)):
                if (keys[py.K_RIGHT]):
                    i, j = self.selected_case_coordinates

                    if (j < NB_CASE_LINE-1):
                        self.set_selected_case(i, j+1)

                if (keys[py.K_LEFT]):
                    i, j = self.selected_case_coordinates

                    if (j > 0):
                        self.set_selected_case(i, j-1)

                if (keys[py.K_UP]):
                    i, j = self.selected_case_coordinates

                    if (i > 0):
                        self.set_selected_case(i-1, j)

                if (keys[py.K_DOWN]):
                    i, j = self.selected_case_coordinates

                    if (i < NB_CASE_LINE-1):
                        self.set_selected_case(i+1, j)

                if (keys[py.K_SPACE]):
                    if (self.selected_case.piece != None and self.selected_case.piece.color == self.actual_player.color):
                        self.selected_piece = self.selected_case.piece
                        self.selected_piece_coordinates = self.selected_case_coordinates

                        self.movements = remove_chess_moves(self.selected_case.piece.movements, self.chessboard, coordinates_to_indexes(self.actual_player.pieces["king"][0].x, self.actual_player.pieces["king"][0].y)[0],
                                                            coordinates_to_indexes(
                            self.actual_player.pieces["king"][0].x, self.actual_player.pieces["king"][0].y)[1], self.players)

                    if (self.selected_case.possible_move_to):
                        self.move_piece(self.selected_piece,
                                        self.selected_case)

                self.key_pressed = True

        else:
            self.key_pressed = False

    def move_piece(self, selected_piece, case_to_move):
        i_piece, j_piece = coordinates_to_indexes(
            selected_piece.x, selected_piece.y)
        i_case, j_case = coordinates_to_indexes(case_to_move.x, case_to_move.y)

        selected_piece.case.piece = None

        if (case_to_move.piece != None):
            case_to_move.piece.is_on_board = False
        case_to_move.piece = selected_piece

        selected_piece.set_new_case(case_to_move)
        selected_piece.first_move = False

        if (selected_piece.type == "pawn"):
            if ((case_to_move.y == 0 or case_to_move.y == (NB_CASE_LINE-1)*CASE_HEIGHT)):
                self.promote_pawn(selected_piece)

            if (abs(i_case-i_piece) == 2):
                if (j_case != 0 and self.chessboard[i_case][j_case-1].piece != None and self.chessboard[i_case][j_case-1].piece.type == 'pawn' and self.chessboard[i_case][j_case-1].piece.color != selected_piece.color):
                    self.chessboard[i_case][j_case -
                                            1].piece.en_passant = selected_piece

                if (j_case != NB_CASE_LINE-1 and self.chessboard[i_case][j_case+1].piece != None and self.chessboard[i_case][j_case+1].piece.type == 'pawn' and self.chessboard[i_case][j_case+1].piece.color != selected_piece.color):
                    self.chessboard[i_case][j_case +
                                            1].piece.en_passant = selected_piece

            if (selected_piece.en_passant != None and j_case == coordinates_to_indexes(selected_piece.en_passant.x, selected_piece.en_passant.y)[1]):
                selected_piece.en_passant.is_on_board = False
                selected_piece.en_passant = None

        if (selected_piece.type == "king"):
            if (j_case == j_piece-2):
                self.move_piece(
                    self.chessboard[i_piece][0].piece, self.chessboard[i_piece][3])

                # to undo the self.turn += 1 at the end of move_piece()
                self.turn -= 1

            if (j_case == j_piece+2):
                self.move_piece(
                    self.chessboard[i_piece][NB_CASE_LINE-1].piece, self.chessboard[i_piece][NB_CASE_LINE-3])

                # to undo the self.turn += 1 at the end of move_piece()
                self.turn -= 1

        self.selected_piece = None
        self.movements = []

        self.turn += 1

        self.update_moves()
        self.players[self.turn % 2].chess = self.players[self.turn % 2].pieces["king"][0].check_chess(
            self.chessboard)
        self.end = self.players[self.turn % 2].check_chess_mate(
            self.chessboard, self.players)

    def promote_pawn(self, pawn):
        self.promote_case = []
        self.promote_pieces = [py.image.load("sprites/"+pawn.color+"-tower.png").convert_alpha(),
                               py.image.load("sprites/"+pawn.color +
                                             "-knight.png").convert_alpha(),
                               py.image.load("sprites/"+pawn.color +
                                             "-bishop.png").convert_alpha(),
                               py.image.load("sprites/"+pawn.color+"-queen.png").convert_alpha()]
        self.promoted_pawn = pawn

        for i in range(4):
            self.promote_case.append(
                py.Rect((pawn.x+((-1)**(int(pawn.x >= WINDOW_WIDTH/2)))*i*PROMOTE_CASE_WIDTH, pawn.y+PROMOTE_CASE_HEIGHT), (PROMOTE_CASE_WIDTH, PROMOTE_CASE_HEIGHT)))

        self.promoting = True

    def handle_mouse(self):
        if (py.mouse.get_pressed()[0]):
            mouse_x, mouse_y = py.mouse.get_pos()
            if (self.promoting):
                for i in range(4):
                    if (mouse_y >= self.promote_case[i].y and mouse_y <= self.promote_case[i].y+PROMOTE_CASE_HEIGHT and
                       mouse_x >= self.promote_case[i].x and mouse_x <= self.promote_case[i].x+PROMOTE_CASE_WIDTH):
                        match(i):
                            case 0:
                                self.promoted_pawn.is_on_board = False

                                new_tower = Tower(
                                    self.promoted_pawn.color, self.promoted_pawn.case, self.promoted_pawn.player)

                                self.promoted_pawn.case.piece = new_tower
                                self.promoted_pawn.player.pieces["tower"].append(
                                    new_tower)

                            case 1:
                                self.promoted_pawn.is_on_board = False

                                new_knight = Knight(
                                    self.promoted_pawn.color, self.promoted_pawn.case, self.promoted_pawn.player)

                                self.promoted_pawn.case.piece = new_knight
                                self.promoted_pawn.player.pieces["knight"].append(
                                    new_knight)

                            case 2:
                                self.promoted_pawn.is_on_board = False

                                new_bishop = Bishop(
                                    self.promoted_pawn.color, self.promoted_pawn.case, self.promoted_pawn.player)

                                self.promoted_pawn.case.piece = new_bishop
                                self.promoted_pawn.player.pieces["bishop"].append(
                                    new_bishop)

                            case 3:
                                self.promoted_pawn.is_on_board = False

                                new_queen = Queen(
                                    self.promoted_pawn.color, self.promoted_pawn.case, self.promoted_pawn.player)

                                self.promoted_pawn.case.piece = new_queen
                                self.promoted_pawn.player.pieces["queen"].append(
                                    new_queen)

                        self.promoting = False

            else:

                i, j = coordinates_to_indexes(mouse_x, mouse_y)

                case_clicked = self.chessboard[i][j]

                if (self.piece_floating):
                    self.selected_piece.x = mouse_x-CASE_WIDTH/2
                    self.selected_piece.y = mouse_y-CASE_HEIGHT/2

                else:
                    if (case_clicked.piece != None and case_clicked.piece.color == self.actual_player.color):
                        self.selected_piece = case_clicked.piece
                        self.selected_piece_coordinates = (i, j)

                        self.movements = remove_chess_moves(self.selected_piece.movements, self.chessboard, coordinates_to_indexes(self.actual_player.pieces["king"][0].x, self.actual_player.pieces["king"][0].y)[0],
                                                            coordinates_to_indexes(
                            self.actual_player.pieces["king"][0].x, self.actual_player.pieces["king"][0].y)[1], self.players)

                        self.piece_floating = True

                    elif (case_clicked.possible_move_to):
                        self.move_piece(self.selected_piece, case_clicked)

                    else:
                        self.movements = []

        else:
            self.piece_floating = False

            if (self.selected_piece != None):
                k, l = coordinates_to_indexes(
                    self.selected_piece.x+self.selected_piece.app.get_width()/2, self.selected_piece.y+self.selected_piece.app.get_height()/2)
                above_case = self.chessboard[k][l]

                if (above_case.possible_move_to):
                    self.move_piece(self.selected_piece, above_case)
                else:
                    self.selected_piece.x = self.selected_piece.case.x
                    self.selected_piece.y = self.selected_piece.case.y

    def handle_ia(self):
        i, j, k, l = self.actual_player.choose_move(
            self.chessboard, self.players)

        self.animation = True
        self.animated_piece = self.chessboard[k][l].piece

        self.animation_points = animation(
            self.chessboard[k][l].piece, self.chessboard[i][j])

    def update(self, keys):
        self.display()

        self.actual_player = self.players[self.turn % 2]

        if (not (self.actual_player.ia)):
            if (KEYBOARD_CONTROLL):
                self.handle_keyboard(keys)
            self.handle_mouse()

        else:
            if (self.animation):
                self.animated_piece.x = self.animation_points[0][self.animation_count]
                self.animated_piece.y = self.animation_points[1][self.animation_count]

                self.animation_count += 1

                if (self.animation_count > NB_POINTS_ANIMATION):
                    self.animation = False
                    self.animation_count = 0

                    i, j = coordinates_to_indexes(
                        self.animation_points[0][NB_POINTS_ANIMATION], self.animation_points[1][NB_POINTS_ANIMATION])

                    self.move_piece(
                        self.animated_piece, self.chessboard[i][j])

            else:
                self.handle_ia()

        return (self.end)

    def display(self):
        pieces_to_disp = []

        for line in self.chessboard:
            for case in line:
                piece = case.display(self.window)
                case.possible_move_to = False

                if (piece != None):
                    pieces_to_disp.append(piece)

        for piece in pieces_to_disp:
            self.window.blit(piece.app,
                             (piece.x+CASE_WIDTH/2-piece.app.get_width()/2, piece.y+CASE_HEIGHT/2-piece.app.get_height()/2))

        self.display_possible_moves()

        if (self.promoting):
            for i in range(4):
                py.draw.rect(self.window, (255, 255, 255),
                             self.promote_case[i])
                self.window.blit(self.promote_pieces[i], (self.promote_case[i].x-self.promote_pieces[i].get_width() /
                                                          2+PROMOTE_CASE_WIDTH/2, self.promote_case[i].y-self.promote_pieces[i].get_height()/2+PROMOTE_CASE_HEIGHT/2))

    def display_possible_moves(self):
        for i, j, k, l in self.movements:
            self.chessboard[i][j].possible_move_to = True

            x, y = indexes_to_coordinates(i, j)

            point = py.Rect((x+CASE_WIDTH/2-POINT_MOVE_WIDTH/2, y+CASE_HEIGHT /
                             2-POINT_MOVE_HEIGHT/2), (POINT_MOVE_WIDTH, POINT_MOVE_HEIGHT))
            py.draw.rect(self.window, POSSIBLE_MOVE_COLOR,
                         point, border_radius=50)
