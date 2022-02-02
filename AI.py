from __future__ import annotations
import Board

class Ai:
    def __init__(self, board_size: int, symbol: str | None):
        self._board_size = board_size
        self._symbol = symbol

    def get_symbol(self) -> str | None:
        """
        :return: return the symbol of the AI
        """
        return self._symbol

    def get_opponent_symbol(self) -> str | None:
        """
        :return: return the opponent symbol of the AI
        """
        return 'O' if self._symbol == 'X' else 'X'

    def get_winning_move(self, board: Board, symbol: str | None) -> tuple(int, int) | None:
        """
        :param board: current state of the board (Board Class)
        :return: return a tuple with the position of the winning move, otherwise None
        """
        for position in board.get_empty_positions():
            tmp = board.copy_board()
            tmp.set_symbol(position[0], position[1], symbol)
            if tmp.check_winner(symbol):
                return position
        return None

    def get_opponent_winning_move(self, board: Board) -> tuple(int, int) | None:
        """
        :param board: current state of the board (Board Class)
        :return: return a tuple with the position of the winning move, otherwise None
        """
        return self.get_winning_move(board, self.get_opponent_symbol())
    
    def play_best_move(self, board: Board) -> Board:
        if board.update_board(self._symbol, self.get_winning_move(board, self._symbol)):
            return board
        if board.update_board(self._symbol, self.get_opponent_winning_move(board)):
            return board



# ------------------------------Unit Test---------------------------------- #


def test_get_symbol():
    ai = Ai(3, 'X')
    assert ai.get_symbol() == 'X'


def test_get_opponent_symbol():
    ai = Ai(3, 'X')
    assert ai.get_opponent_symbol() == 'O'


def test_get_winning_move():
    board = Board.Board(6)
    ai = Ai(board._board_size, 'X')

    assert ai.get_winning_move(board, ai._symbol) == None
    assert ai.get_opponent_winning_move(board) == None
    for i in range(4):
        board.update_board('X', (i, i))
        board.update_board('O', (i + 1, 0))
    assert ai.get_winning_move(board, ai._symbol) == (4, 4)
    assert ai.get_opponent_winning_move(board) == (5, 0)