from .functions import evaluation, copy_case_chessboard, flat_list_of_list
from .config import DEPTH_SEARCH
from math import inf


class minMaxTree():
    def __init__(self, players, turn, chessboard):
        self.root = minMaxRoot(
            chessboard, players[turn % 2], players[(turn+1) % 2])

        self.floors = []

        self.root.construct_child()
        self.floors += self.root.child

        # actual_floor = [self.root]
        # next_floor = []

        # for i in range(DEPTH_SEARCH):

        #     self.floors.append(actual_floor)

        #     for node in actual_floor:

        #         node.construct_child()
        #         next_floor += node.child

        #     actual_floor = next_floor
        #     next_floor = []

        # self.floors.append(actual_floor)

    def get_best_move(self):
        if (self.root.player.color == "white"):
            first_floor = self.root.child

            max_eval = -inf
            best_node = first_floor[0]

            for node in first_floor:
                actual_eval = node.get_eval()
                if (actual_eval > max_eval):
                    max_eval = actual_eval
                    best_node = node

        else:
            first_floor = self.root.child

            min_eval = inf
            best_node = first_floor[0]

            for node in first_floor:
                actual_eval = node.get_eval()
                if (actual_eval < min_eval):
                    min_eval = actual_eval
                    best_node = node

        return (best_node.move)


class minMaxNode():
    def __init__(self, parent, chessboard, depth, actual_player, move, pieces):
        self.parent = parent
        self.child = []

        self.move = move

        self.chessboard = chessboard
        self.player = actual_player
        self.pieces = pieces

        self.depth = depth

    def construct_child(self, against_player=None):
        if (against_player == None):
            against_player = self.parent.player

        moves = self.player.get_valide_moves(
            self.chessboard, [self.player, against_player], copy_piece=self.pieces)

        for m in moves:
            k, l, i, j = m

            copy_chessboard, copy_pieces = copy_case_chessboard(
                self.chessboard)

            if (copy_chessboard[k][l].piece != None):
                copy_chessboard[k][l].piece.is_on_board = False
            copy_chessboard[k][l].piece = copy_chessboard[i][j].piece

            copy_chessboard[k][l].piece.set_new_case(copy_chessboard[k][l])

            copy_chessboard[i][j].piece = None

            if (self.depth+1 == DEPTH_SEARCH):
                self.child.append(minMaxLeaf(
                    self, copy_chessboard, (k, l, i, j)))

            else:
                self.child.append(minMaxNode(self, copy_chessboard,
                                             self.depth+1, against_player, (k, l, i, j), copy_pieces))

    def get_eval(self):
        r = 0

        if (self.child == []):
            self.construct_child()

        for node in self.child:
            r += node.get_eval()

        return (r/len(self.child))


class minMaxRoot(minMaxNode):
    def __init__(self, chessboard, actual_player, against_player):
        self.against_player = against_player
        super().__init__(None, chessboard, 0, actual_player,
                         None, flat_list_of_list(actual_player.pieces.values()))

    def construct_child(self):
        super().construct_child(self.against_player)


class minMaxLeaf(minMaxNode):
    def __init__(self, parent, chessboard, move):
        self.parent = parent
        self.chessboard = chessboard
        self.move = move

        self.eval = evaluation(chessboard)

    def get_eval(self):
        return (self.eval)
