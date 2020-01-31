# Some utilities

def draw_board(board):


    board.prepare_symbol_list()
    string = "    a   b   c   d   e   f   g   h"
    line = ""
    for i, s in enumerate(board.symbols):
        if i % 8 == 0:
            string = f"\n  ---------------------------------\n" + line + string
            line = f"{int(i / 8 + 1)} |"
        if s:
            line = line + f" {s} |"
            continue
        line = line + "   |"
    string = "\n  ---------------------------------\n" + line + string
    print(string)
