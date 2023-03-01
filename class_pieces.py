import pygame as py
from config import NB_CASE_LINE, IMAGE_HEIGHT, IMAGE_WIDTH
from functions import coordinates_to_indexes, remove_unvalide_coordinates, copy_case_chessboard, check_controlled_case


class Piece:
    def __init__(self, color, case, player):
        self.color = color

        self.app = py.image.load(
            "sprites/"+color.lower()+"-"+self.type+".png").convert_alpha()
        self.app = py.transform.scale(self.app, (IMAGE_WIDTH, IMAGE_HEIGHT))

        self.case = case
        self.player = player

        self.x = self.case.x
        self.y = self.case.y

        self.first_move = True
        self.movements = []

        self.is_on_board = True

    def set_new_case(self, new_case):
        self.case = new_case

        self.x = new_case.x
        self.y = new_case.y


class Pawn(Piece):
    def __init__(self, color, case, player, low):
        self.type = "pawn"
        self.low = low
        super().__init__(color, case, player)

    def copy(self):
        copy_pawn = Pawn(self.color, self.case, self.player, self.low)

        return (copy_pawn)

    def possible_movements(self, chessboard):
        i, j = coordinates_to_indexes(self.case.x, self.case.y)
        possible_moves = []

        if (self.low):
            if (chessboard[i-1][j].piece == None):
                possible_moves += [(i-1, j)]

            if (self.first_move and chessboard[i-1][j].piece == None and chessboard[i-2][j].piece == None):
                possible_moves += [(i-2, j)]

            if (j != 0 and chessboard[i-1][j-1].piece != None):
                possible_moves += [(i-1, j-1)]

            if (j != NB_CASE_LINE-1 and chessboard[i-1][j+1].piece != None):
                possible_moves += [(i-1, j+1)]

        else:
            if (chessboard[i+1][j].piece == None):
                possible_moves += [(i+1, j)]

            if (self.first_move and chessboard[i+1][j].piece == None and chessboard[i+2][j].piece == None):
                possible_moves += [(i+2, j)]

            if (j != 0 and chessboard[i+1][j-1].piece != None):
                possible_moves += [(i+1, j-1)]

            if (j != NB_CASE_LINE-1 and chessboard[i+1][j+1].piece != None):
                possible_moves += [(i+1, j+1)]

        possible_moves = remove_unvalide_coordinates(
            possible_moves, chessboard, self.color)

        return (possible_moves)


class Tower(Piece):
    def __init__(self, color, case, player):
        self.type = 'tower'
        super().__init__(color, case, player)

    def copy(self):
        copy_tower = Tower(self.color, self.case, self.player)

        return (copy_tower)

    def possible_movements(self, chessboard):
        i, j = coordinates_to_indexes(self.case.x, self.case.y)
        possible_moves = []

        for k in range(i-1, -1, -1):
            if (chessboard[k][j].piece != None):
                if (chessboard[k][j].piece.color != self.color):
                    possible_moves += [(k, j)]
                break

            possible_moves += [(k, j)]

        for k in range(i+1, NB_CASE_LINE):
            if (chessboard[k][j].piece != None):
                if (chessboard[k][j].piece.color != self.color):
                    possible_moves += [(k, j)]
                break

            possible_moves += [(k, j)]

        for l in range(j-1, -1, -1):
            if (chessboard[i][l].piece != None):
                if (chessboard[i][l].piece.color != self.color):
                    possible_moves += [(i, l)]
                break

            possible_moves += [(i, l)]

        for l in range(j+1, NB_CASE_LINE):
            if (chessboard[i][l].piece != None):
                if (chessboard[i][l].piece.color != self.color):
                    possible_moves += [(i, l)]
                break

            possible_moves += [(i, l)]

        return (possible_moves)


class Knight(Piece):
    def __init__(self, color, case, player):
        self.type = 'knight'
        super().__init__(color, case, player)

    def copy(self):
        copy_knight = Knight(self.color, self.case, self.player)

        return (copy_knight)

    def possible_movements(self, chessboard):
        i, j = coordinates_to_indexes(self.case.x, self.case.y)
        possible_moves = []

        possible_moves += [(i-2, j-1), (i-2, j+1), (i+2, j-1),
                           (i+2, j+1), (i+1, j-2), (i-1, j-2), (i-1, j+2), (i+1, j+2)]

        possible_moves = remove_unvalide_coordinates(
            possible_moves, chessboard, self.color)

        return (possible_moves)


class Bishop(Piece):
    def __init__(self, color, case, player):
        self.type = "bishop"
        super().__init__(color, case, player)

    def copy(self):
        copy_bishop = Bishop(self.color, self.case, self.player)

        return (copy_bishop)

    def possible_movements(self, chessboard):
        i, j = coordinates_to_indexes(self.case.x, self.case.y)
        possible_moves = []

        for k in range(1, min(i, j)+1):
            if (chessboard[i-k][j-k].piece != None):
                if (chessboard[i-k][j-k].piece.color != self.color):
                    possible_moves += [(i-k, j-k)]
                break

            possible_moves += [(i-k, j-k)]

        for k in range(1, min(NB_CASE_LINE-j, NB_CASE_LINE-i)):
            if (chessboard[i+k][j+k].piece != None):
                if (chessboard[i+k][j+k].piece.color != self.color):
                    possible_moves += [(i+k, j+k)]
                break

            possible_moves += [(i+k, j+k)]

        for k in range(1, min(NB_CASE_LINE-i, j+1)):
            if (chessboard[i+k][j-k].piece != None):
                if (chessboard[i+k][j-k].piece.color != self.color):
                    possible_moves += [(i+k, j-k)]
                break

            possible_moves += [(i+k, j-k)]

        for k in range(1, min(i+1, NB_CASE_LINE-j)):
            if (chessboard[i-k][j+k].piece != None):
                if (chessboard[i-k][j+k].piece.color != self.color):
                    possible_moves += [(i-k, j+k)]
                break

            possible_moves += [(i-k, j+k)]

        return (possible_moves)


class Queen(Piece):
    def __init__(self, color, case, player):
        self.type = "queen"
        super().__init__(color, case, player)

    def copy(self):
        copy_queen = Queen(self.color, self.case, self.player)

        return (copy_queen)

    def possible_movements(self, chessboard):
        possible_moves = []

        possible_moves = Tower(self.color, self.case, self.player).possible_movements(chessboard
                                                                                      )+Bishop(self.color, self.case, self.player).possible_movements(chessboard)

        return (possible_moves)


class King(Piece):
    def __init__(self, color, case, player):
        self.type = "king"
        super().__init__(color, case, player)

    def copy(self):
        copy_king = King(self.color, self.case, self.player)

        return (copy_king)

    def check_chess(self, chessboard):
        i, j = coordinates_to_indexes(self.x, self.y)

        return ((chessboard[i][j].controlled != []) and not (self.color in chessboard[i][j].controlled))

    def possible_movements(self, chessboard):
        i, j = coordinates_to_indexes(self.case.x, self.case.y)
        possible_moves = []

        possible_moves += [(i-1, j), (i-1, j+1), (i, j+1),
                           (i+1, j+1), (i+1, j), (i+1, j-1), (i, j-1), (i-1, j-1)]

        if (self.first_move):
            possible_moves += self.roque_possible(
                chessboard, i, j)

        possible_moves = remove_unvalide_coordinates(
            possible_moves, chessboard, self.color)

        return (possible_moves)

    def roque_possible(self, chessboard, row, column):
        possible_moves = []

        for j in range(column-1, -1, -1):
            if (j == 0):
                if (chessboard[row][j].piece != None and chessboard[row][j].piece.first_move):
                    possible_moves += [(row, column-2)]
                    self.roque = True

            else:
                if (j != column and (chessboard[row][j].piece != None or ((chessboard[row][j].controlled != []) and not (self.color in chessboard[row][j].controlled)))):
                    break

        for j in range(column+1, NB_CASE_LINE):
            if (j == NB_CASE_LINE-1):
                if (chessboard[row][j].piece != None and chessboard[row][j].piece.first_move):
                    possible_moves += [(row, column+2)]
                    self.roque = True

            else:
                if (j != column and (chessboard[row][j].piece != None or ((chessboard[row][j].controlled != []) and not (self.color in chessboard[row][j].controlled)))):
                    break

        return (possible_moves)
