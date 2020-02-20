from jbchess.chessboard.board import BoardBase, BoardCollection
from jbchess.chessboard.utils import draw_board


def play():
    """Steering a game

    This is the steering function to be called when a new game should be played
    """
    print("Play JBChess")

    # Tell the user how to use place pieces on the board
    print("\nThe Position prompt requires a 2**n value.")
    print("For 'Piece' enter one of the following symbols: K,Q,R,N,B,P,k,q,r,n,b,p.")

    # Initialise an empty board
    board_prev = BoardBase()

    # Variable to terminate the game if true
    mate = None

    # Loop over input/drawing procedure
    while not mate:

        # Ask user for position and piece-type
        pos = int(input("Position: "))
        piece = input("Piece: ")

        # Store input in a BoardBase object
        board_in = BoardBase(pos, symbol=piece)

        # Make a collection of previous board and input
        board_prev = BoardCollection(board_prev, board_in)

        # Check for mate
        # mate_checking_function(board_prev) returns mate is true

        # Draw board
        draw_board(board_prev)
