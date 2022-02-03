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
        if board.update_board(self._symbol, board.block_threat_of_three(board.get_opponent_symbol())):
            return board
        board.random_play(self._symbol)
        return board
