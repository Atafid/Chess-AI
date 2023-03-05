from .functions import coordinates_to_indexes, remove_chess_moves, second_element
import random as rd


class Player():
    def __init__(self, color, ia):
        self.color = color

        self.pieces = {"pawn": [], "tower": [],
                       "knight": [], "bishop": [], "queen": [], "king": []}

        self.chess = False

        self.move_list = []
        self.ia = ia

    def get_possible_movements(self, chessboard, copy_piece=None):
        if (copy_piece != None):
            self.move_list = []

            for piece in copy_piece:
                if (piece.color == self.color and piece.is_on_board):
                    piece.movements = []

                    i, j = coordinates_to_indexes(piece.x, piece.y)
                    for (k, l) in piece.possible_movements(chessboard):
                        piece.movements.append((k, l, i, j))
                        self.move_list.append((k, l, i, j))

        else:
            self.move_list = []

            for list_piece in self.pieces.values():
                for piece in list_piece:
                    piece.movements = []

                    if (piece.is_on_board):
                        i, j = coordinates_to_indexes(piece.x, piece.y)

                        for (k, l) in piece.possible_movements(chessboard):
                            piece.movements.append((k, l, i, j))
                            self.move_list.append((k, l, i, j))

    def check_chess_mate(self, chessboard, players):
        king_i, king_j = coordinates_to_indexes(
            self.pieces["king"][0].x, self.pieces["king"][0].y)

        return (self.chess and remove_chess_moves(self.move_list, chessboard, king_i, king_j, players) == [])

    def choose_move(self, chessboard, players):
        king_i, king_j = coordinates_to_indexes(
            self.pieces["king"][0].x, self.pieces["king"][0].y)

        real_possible_moves = remove_chess_moves(
            self.move_list, chessboard, king_i, king_j, players, evaluate=True)

        real_possible_moves.sort(key=second_element)

        if (len(real_possible_moves) >= 2 and real_possible_moves[-1][1] == real_possible_moves[-2][1]):
            first_index_max_value = 0

            for m, e in real_possible_moves:
                if (e == real_possible_moves[-1][1]):
                    break

                else:
                    first_index_max_value += 1

            move = rd.randint(first_index_max_value,
                              len(real_possible_moves)-1)

        else:
            move = -1

        return (real_possible_moves[move][0])
