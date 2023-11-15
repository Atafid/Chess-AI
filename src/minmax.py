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
        best_node = self.root.alpha_beta(-inf, inf)

        return (best_node.move)


class minMaxNode():
    def __init__(self, parent, chessboard, depth, actual_player, move, pieces, max):
        self.parent = parent
        self.child = []

        self.move = move

        self.chessboard = chessboard
        self.player = actual_player
        self.pieces = pieces

        self.depth = depth
        self.max = max

    def construct_child(self, against_player=None):
        if (against_player == None):
            against_player = self.parent.player

        moves = self.player.get_valide_moves(
            self.chessboard, against_player, copy_piece=self.pieces)

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
                    self, copy_chessboard, (k, l, i, j), copy_pieces, against_player, not (self.max)))

            else:
                self.child.append(minMaxNode(self, copy_chessboard,
                                             self.depth+1, against_player, (k, l, i, j), copy_pieces, not (self.max)))

    def get_eval(self):

        if (self.child == []):
            self.construct_child()

        if (self.max):
            val = -inf

            for node in self.child:
                node_eval = node.get_eval()
                if (val < node_eval):
                    val = node_eval

        else:
            val = inf

            for node in self.child:
                node_eval = node.get_eval()
                if (val > node_eval):
                    val = node_eval

        return (val)

    def alpha_beta(self, alpha, beta):
        if (self.child == []):
            self.construct_child()

        if (self.max):
            v = -inf
            for node in self.child:
                v = max(v, node.alpha_beta(alpha, beta))

                if (v >= beta):
                    return (v)

                alpha = max(alpha, v)

        else:
            v = inf
            for node in self.child:
                v = min(v, node.alpha_beta(alpha, beta))

                if (alpha >= v):
                    return (v)

                beta = min(beta, v)

        return (v)


class minMaxRoot(minMaxNode):
    def __init__(self, chessboard, actual_player, against_player):
        self.against_player = against_player
        super().__init__(None, chessboard, 0, actual_player,
                         None, flat_list_of_list(actual_player.pieces.values()), False)

    def construct_child(self):
        super().construct_child(self.against_player)

    def get_eval(self):
        if (self.child == []):
            self.construct_child()

        best_node = None

        if (self.max):
            val = -inf

            for node in self.child:
                node_eval = node.get_eval()
                if (val < node_eval):
                    val = node_eval
                    best_node = node

        else:
            val = inf

            for node in self.child:
                node_eval = node.get_eval()
                if (val > node_eval):
                    val = node_eval
                    best_node = node

        return (best_node)

    def alpha_beta(self, alpha, beta):
        if (self.child == []):
            self.construct_child()

        best_node = None

        if (self.max):
            v = -inf
            for node in self.child:
                eval = node.alpha_beta(alpha, beta)

                if (v <= eval):
                    v = eval
                    best_node = node

                if (v >= beta):
                    return (best_node)

                alpha = max(alpha, v)

        else:
            v = inf
            for node in self.child:
                eval = node.alpha_beta(alpha, beta)

                if (v >= eval):
                    v = eval
                    best_node = node

                if (alpha >= v):
                    return (best_node)

                beta = min(beta, v)

        return (best_node)


class minMaxLeaf(minMaxNode):
    def __init__(self, parent, chessboard, move, pieces, actual_player, max):
        self.parent = parent
        self.chessboard = chessboard
        self.move = move

        self.pieces = pieces
        self.player = actual_player
        self.max = max

        if (self.max):
            self.eval = evaluation(self.pieces, self.player.color)
        else:
            self.eval = evaluation(self.pieces, self.parent.player.color)

    def get_eval(self):
        return (self.eval)

    def alpha_beta(self, alpha, beta):
        return (self.eval)
