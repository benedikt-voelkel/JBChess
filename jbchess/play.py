from jbchess.chessboard.board import Board, Team
from jbchess.chessboard.pieces import King
from jbchess.chessboard.utils import make_chess_board, place
from jbchess.game.game import Game, Frontend


def play():
    """Steering a game

    This is the steering function to be called when a new game should be played
    """
    print("Play JBChess")

    frontend = Frontend()
    frontend.world = make_chess_board()
    game = Game(frontend, None)


    game.start()
