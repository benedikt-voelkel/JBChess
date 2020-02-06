from jbchess.chessboard.board import BoardBase, BoardCollection
from jbchess.chessboard.utils import draw_board


def play():
    """Steering a game

    This is the steering function to be called when a new game should be played
    """
    print("Play JBChess")

    # Make 4 boards with pieces at different positions. Each board represents pieces of one type
    # at their current position
    board1 = BoardBase(1, symbol="o")
    board2 = BoardBase(2, symbol="H")
    board3 = BoardBase(4, symbol="O")
    board4 = BoardBase(512 + 2048, symbol="X")

    # Draw the first board
    draw_board(board1)

    # Make a collection of boards
    board_coll = BoardCollection(board1, board2, board3, board4)

    board5 = BoardBase(4096, symbol="Y")

    board_coll1 = BoardCollection(board1, board2, board3, board4)

    board_coll2 = BoardCollection(board_coll1, board5)

    # Draw the collection
    draw_board(board_coll1)

    # Draw collection of collection
    draw_board(board_coll2)

    # This is a test
