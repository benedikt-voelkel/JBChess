from jbchess.chessboard.board import BoardBase, BoardCollection


def play():
    """Steering a game

    This is the steering function to be called when a new game should be played
    """
    print("Play JBChess")

    board = BoardBase(1, symbol="o")

    board2 = BoardBase(2, symbol="H")
    board3 = BoardBase(4, symbol="O")

    print(board)

    print(board2)
    print(board3)

    board_coll = BoardCollection(board, board2, board3)

    print(board_coll)
