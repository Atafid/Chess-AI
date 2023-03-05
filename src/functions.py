from .config import CASE_HEIGHT, CASE_WIDTH, NB_CASE_LINE, NB_POINTS_ANIMATION


def coordinates_to_indexes(x, y):
    return (int(y/CASE_HEIGHT), int(x/CASE_WIDTH))


def indexes_to_coordinates(i, j):
    return (j*CASE_WIDTH, i*CASE_HEIGHT)


def remove_unvalide_coordinates(l, chessboard, color):
    l_copy = l

    for k in range(len(l_copy)-1, -1, -1):
        i, j, = l_copy[k]

        if (i < 0 or j < 0 or i > NB_CASE_LINE-1 or j > NB_CASE_LINE-1 or (chessboard[i][j].piece != None and chessboard[i][j].piece.color == color)):
            l_copy.pop(k)

    return (l_copy)


def copy_case_chessboard(l):
    result = []
    copy_pieces = []

    for row in l:
        new_row = []

        for case in row:
            new_case = case.copy()

            new_row.append(new_case)
            if (new_case.piece != None):
                copy_pieces.append(new_case.piece)

        result.append(new_row)

    return (result, copy_pieces)


def case_in_possible_moves_list(i, j, list):
    for a, b, c, d in list:
        if (a == i and b == j):
            return (True)

    return (False)


def check_controlled_case(chessboard, players):
    for i in range(NB_CASE_LINE):
        for j in range(NB_CASE_LINE):
            chessboard[i][j].controlled = []

            if (case_in_possible_moves_list(i, j, players[0].move_list)):
                chessboard[i][j].controlled.append(players[0].color)

            elif (case_in_possible_moves_list(i, j, players[1].move_list)):
                chessboard[i][j].controlled.append(players[1].color)


def remove_chess_moves(moves, chessboard, king_i, king_j, players, evaluate=False):
    real_possible_moves = []

    # k, l are the coordinates of the case to move on and i, j the coordinates of the case where the piece comes from
    for k, l, i, j in moves:

        copy_chessboard, copy_pieces = copy_case_chessboard(chessboard)

        if (copy_chessboard[k][l].piece != None):
            copy_chessboard[k][l].piece.is_on_board = False
        copy_chessboard[k][l].piece = copy_chessboard[i][j].piece

        copy_chessboard[k][l].piece.set_new_case(copy_chessboard[k][l])

        copy_chessboard[i][j].piece = None

        for player in players:
            player.get_possible_movements(copy_chessboard, copy_pieces)
        check_controlled_case(copy_chessboard, players)

        if ((king_i, king_j) == (i, j)):
            if (not (copy_chessboard[k][l].piece.check_chess(copy_chessboard))):
                if (evaluate):
                    real_possible_moves.append(((k, l, i, j), evaluation(
                        copy_chessboard, copy_chessboard[k][l].color)))
                else:
                    real_possible_moves.append((k, l, i, j))

        else:
            if (not (chessboard[king_i][king_j].piece.check_chess(copy_chessboard))):
                if (evaluate):
                    real_possible_moves.append(((k, l, i, j), evaluation(
                        copy_chessboard, copy_chessboard[k][l].color)))
                else:
                    real_possible_moves.append((k, l, i, j))

    # to reinitialize their movements after we change it in the following for loop
    for player in players:
        player.get_possible_movements(chessboard)

    return (real_possible_moves)


def minmax(depth):
    pass


def animation(piece, new_case):
    if (new_case.x - piece.x != 0):
        alpha = (new_case.y - piece.y)/(new_case.x - piece.x)
        beta = piece.y-alpha*piece.x

        h = abs(piece.x-new_case.x)/NB_POINTS_ANIMATION

        x_points = [piece.x+((-1)**(piece.x-new_case.x > 0))
                    * h*i for i in range(NB_POINTS_ANIMATION+1)]
        y_points = [alpha*x+beta for x in x_points]

    else:
        h = abs(piece.y-new_case.y)/NB_POINTS_ANIMATION

        x_points = [piece.x for i in range(NB_POINTS_ANIMATION+1)]
        y_points = [piece.y+((-1)**(piece.y-new_case.y > 0))
                    * h*i for i in range(NB_POINTS_ANIMATION+1)]

    return ((x_points, y_points))


def evaluation(chessboard, color):
    eva = 0

    for line in chessboard:
        for case in line:
            if (case.piece != None):
                eva += case.piece.value * \
                    ((-1)**(int(case.piece.color != color)))

    return (eva)


def second_element(couple):
    return (couple[1])
