from .functions import coordinates_to_indexes, remove_chess_moves, second_element
import random as rd


class Player():
    def __init__(self, color, ia):
        self.color = color

        self.pieces = {"pawn": [], "tower": [],
                       "knight": [], "bishop": [], "queen": [], "king": []}

        self.chess = False
        self.ia = ia

    def check_chess_mate(self, chessboard, adverse_player, possible_moves):
        king_i, king_j = coordinates_to_indexes(
            self.pieces["king"][0].x, self.pieces["king"][0].y)

        return (self.chess and remove_chess_moves(possible_moves, chessboard, king_i, king_j, adverse_player) == [])

    def get_possible_movements(self, chessboard, copy_piece=None):
        move_list = []

        if (copy_piece != None):

            for piece in copy_piece:
                if (piece.color == self.color and piece.is_on_board):
                    piece.movements = []

                    i, j = coordinates_to_indexes(piece.x, piece.y)
                    for (k, l) in piece.possible_movements(chessboard):
                        piece.movements.append((k, l, i, j))
                        move_list.append((k, l, i, j))

        else:
            for list_piece in self.pieces.values():
                for piece in list_piece:
                    piece.movements = []

                    if (piece.is_on_board):
                        i, j = coordinates_to_indexes(piece.x, piece.y)

                        for (k, l) in piece.possible_movements(chessboard):
                            piece.movements.append((k, l, i, j))
                            move_list.append((k, l, i, j))

        return (move_list)

    def get_valide_moves(self, chessboard, adverse_player, copy_piece=None, evaluate=False):
        king_i, king_j = coordinates_to_indexes(
            self.pieces["king"][0].x, self.pieces["king"][0].y)

        real_possible_moves = remove_chess_moves(
            self.get_possible_movements(chessboard, copy_piece=copy_piece), chessboard, king_i, king_j, adverse_player, evaluate=evaluate)

        return (real_possible_moves)

    def choose_move(self, chessboard, adverse_player):
        real_possible_moves = self.get_valide_moves(
            chessboard, adverse_player, copy_piece=None, evaluate=True)

        if (self.color == "white"):
            real_possible_moves.sort(key=second_element)
        else:
            real_possible_moves.sort(key=second_element, reverse=True)

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
