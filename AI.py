from __future__ import annotations
import random
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
            tmp.update_board(symbol, (position[0], position[1]))
            if tmp.check_winner(symbol):
                return position
        return None

    def get_opponent_winning_move(self, board: Board) -> tuple(int, int) | None:
        """
        :param board: current state of the board (Board Class)
        :return: return a tuple with the position of the winning move, otherwise None
        """
        return self.get_winning_move(board, self.get_opponent_symbol())
    
    def can_do_a_double_threat(self, board: Board, symbol: str | None) -> tuple(int, int) | None:
        """
        :param board: current state of the board (Board Class)
        :return: return a tuple with the position of the winning move, otherwise None
        """
        res = []
        for position in board.get_empty_positions():
            tmp = board.copy_board()

            _, res = tmp.block_threat_of_three(symbol)
            nb = len(res)
            tmp.update_board(symbol, (position[0], position[1]))
            _, res = tmp.block_threat_of_three(symbol)
            if len(res) - nb > 1:
                vec1 = (position[0]-res[0][0], position[1]-res[0][1])
                vec2 = (position[0]-res[1][0], position[1]-res[1][1])
                if vec1[0] * vec2[0] + vec1[1] * vec2[1] == 0:
                    return position
                vec1 = (abs(position[0]-res[0][0]), abs(position[1]-res[0][1]))
                vec2 = (abs(position[0]-res[1][0]), abs(position[1]-res[1][1]))
                if not 0 in vec1 and not 0 in vec2 and vec2[0]/vec1[0] == vec2[1]/vec1[1]:
                    continue
                return position
        return None
    
    def play_best_move(self, board: Board) -> Board:
        """
        :param board: current state of the board (Board Class)
        :return: return the board updated with the new play
        """
        a = self.get_winning_move(board, self._symbol)
        if board.update_board(self._symbol, a):
            return board, a
        b = self.get_opponent_winning_move(board)
        if board.update_board(self._symbol, b):
            return board, b
        c, _ = board.block_threat_of_three(self._symbol)
        if board.update_board(self._symbol, c):
            return board, c
        d, _ = board.block_threat_of_three(self.get_opponent_symbol())
        if board.update_board(self._symbol, d):
            return board, d

        if board._board_size <= 15:
            f = self.can_do_a_double_threat(board, self._symbol)
            if board.update_board(self._symbol, f):
                print("Double at pos ", f)
                return board, f
            g = self.can_do_a_double_threat(board, self.get_opponent_symbol())
            if board.update_board(self._symbol, g):
                print("Double at pos ", g)
                return board, g

        if self._symbol == 'X':
            e = board.is_one_side_tile_empty(board._last_X_played)
        else:
            e = board.is_one_side_tile_empty(board._last_O_played)
        if board.update_board(self._symbol, e):
            return board, e
        if self._symbol == 'X':
            e = board.is_one_side_tile_empty(board._last_O_played)
        else:
            e = board.is_one_side_tile_empty(board._last_X_played)
        if board.update_board(self._symbol, e):
            return board, e

        return board, board.random_play(self._symbol)
