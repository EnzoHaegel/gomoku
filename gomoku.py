from AI import Ai
from Board import Board
import sys

def main():
    bsize = 15
    board = Board(bsize)
    board.print_board()
    iax = Ai(bsize, 'X')
    iao = Ai(bsize, 'O')
    sym_start = 'X'
    while not board.is_full():
        try:
            if board.check_winner('X'):
                print("X gagne")
                sys.exit(0)
            if board.check_winner('O'):
                print("O gagne")
                sys.exit(0)
            if not '-g' in sys.argv:
                iax.play_best_move(board)
                print("IA 'X' PLAYED")
                print(board._last_X_played)
                board.print_board()
            else:
                pos = input().split()
                if not board.update_board(sym_start, (int(pos[1]), int(pos[0]))):
                    print("Input invalide")
                    pass

            iao.play_best_move(board)
            print("IA 'O' PLAYED")
            print(board._last_O_played)
            board.print_board()
                # if sym_start == 'X':
                #     sym_start = 'O'
                # else:
                #     sym_start = 'X'
        except ValueError:
            print("Input invalide, ex: '0 0'")
            pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exited")
        sys.exit(1)