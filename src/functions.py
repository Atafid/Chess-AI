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


def check_controlled_case(chessboard, playerOneMoves, playerOneColor, playerTwoMoves, playerTwoColor):
    for k, l, i, j in (playerOneMoves):
        chessboard[k][l].controlled = []

        if (not (playerOneColor in chessboard[k][l].controlled)):
            chessboard[k][l].controlled.append(playerOneColor)

    for k, l, i, j in (playerTwoMoves):
        if (not (playerTwoColor in chessboard[k][l].controlled)):
            chessboard[k][l].controlled.append(playerTwoColor)


def remove_chess_moves(moves, chessboard, king_i, king_j, adverse_player, evaluate=False):
    real_possible_moves = []

    # k, l are the coordinates of the case to move on and i, j the coordinates of the case where the piece comes from
    for k, l, i, j in moves:

        eaten_piece = chessboard[k][l].piece

        if (eaten_piece != None):
            eaten_piece.is_on_board = False

        chessboard[k][l].piece = chessboard[i][j].piece
        chessboard[k][l].piece.set_new_case(chessboard[k][l])

        chessboard[i][j].piece = None

        adverse_moves = adverse_player.get_possible_movements(chessboard)

        if ((king_i, king_j) == (i, j)):
            if (not (chessboard[k][l].piece.check_chess(adverse_moves))):
                if (evaluate):
                    real_possible_moves.append(((k, l, i, j), evaluation(
                        chessboard)))
                else:
                    real_possible_moves.append((k, l, i, j))

        else:
            if (not (chessboard[king_i][king_j].piece.check_chess(adverse_moves))):
                if (evaluate):
                    real_possible_moves.append(((k, l, i, j), evaluation(
                        chessboard)))
                else:
                    real_possible_moves.append((k, l, i, j))

        if (eaten_piece != None):
            eaten_piece.is_on_board = True

        chessboard[i][j].piece = chessboard[k][l].piece
        chessboard[i][j].piece.set_new_case(chessboard[i][j])

        chessboard[k][l].piece = eaten_piece

    adverse_player.get_possible_movements(chessboard)

    return (real_possible_moves)


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


def evaluation(pieces, low_color):
    eva = 0

    for piece in pieces:
        i, j = coordinates_to_indexes(piece.x, piece.y)

        if (piece.color == low_color):
            eva += piece.value[i][j]

        else:
            eva += (-1)*piece.value[NB_CASE_LINE-1-i][j]

    # for line in chessboard:
    #     for case in line:
    #         if (case.piece != None):
    #             eva += case.piece.value * \
    #                 ((-1)**(int(case.piece.color != "white")))

    return (eva)


def second_element(couple):
    return (couple[1])


def flat_list_of_list(l):
    r = []

    for list in l:
        for a in list:
            r.append(a)

    return (r)
