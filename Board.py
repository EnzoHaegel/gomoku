# This is a 'Board' Class in python for a gomoku game:
#
# The board is a board_size x board_size matrix, and each element can be 'X', 'O', or None.
# The board starts with all elements set to None.
from __future__ import annotations

import random
import AI


class Board:
    def __init__(self, board_size):
        self._board_size = board_size
        self._board = [[None for _ in range(self._board_size)] for _ in range(self._board_size)]
        self._last_X_played: tuple(int, int) | None = None
        self._last_O_played: tuple(int, int) | None = None

    def get_board(self) -> list[list[str | None]]:
        """
        :return: return the current state of the board
        """
        return self._board

    def get_row_col(self, row: int, col: int) -> str | None:
        """
        :param row: position X of the board
        :param col: position Y of the board
        :return: return the symbol at a specific position on the board
        """
        return self._board[row][col]

    def print_board(self):
        print("\n")
        for i in range(len(self._board)):
            temp = []
            for j in range(len(self._board[i])):
                if self._board[i][j] == None:
                    temp.append(".")
                else:
                    temp.append(self._board[i][j])
            print(" ".join(temp))

    def update_board(self, symbol: str | None,
                     position: tuple(int, int)):  # set a specific position on the board to be 'X' or 'O' with tuple
        """
        :param symbol: 'X' 'O' or None
        :param position: position on the board (x, y)
        :return: None
        """
        if not self.is_valid_move(position):
            return False
        if position == None or self._board[position[0]][position[1]] != None:
            return False
        self._board[position[0]][position[1]] = symbol
        if symbol == 'X' and position != None:
            self._last_X_played = position
        elif symbol == 'O' and position != None:
            self._last_O_played = position
        return True

    def is_valid_move(self, position: tuple(int, int)) -> bool:
        """
        :param position: position on the board (x, y)
        :return: True if the move is valid, False if not
        """
        if position == None or position[0] == None or position[1] == None:
            return False
        if not self.is_position_in_range(position):
            return False
        if self._board[position[0]][position[1]] == None:
            return True
        return False

    def is_full(self) -> bool:
        """
        :return: True if the board is full, else false
        """
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] == None:
                    return False
        return True

    def check_winner(self, symbol: str | None) -> bool:
        """
        :param symbol: 'X' 'O' or None
        :return: True if the player that played the symbol have won, else False
        """
        # Check horizontal wins
        for i in range(len(self._board) - 4):
            for j in range(len(self._board[i])):
                if self._board[i][j] == symbol and self._board[i + 1][j] == symbol and self._board[i + 2][j] == symbol \
                        and self._board[i + 3][j] == symbol and self._board[i + 4][j] == symbol:
                    return True

        # Check vertical wins
        for i in range(len(self._board)):
            for j in range(len(self._board[i]) - 4):
                if self._board[i][j] == symbol and self._board[i][j + 1] == symbol and self._board[i][j + 2] == symbol \
                        and self._board[i][j + 3] == symbol and self._board[i][j + 4] == symbol:
                    return True

        # Check positive slope diagonal
        for i in range(len(self._board) - 4):
            for j in range(len(self._board[i]) - 4):
                if self._board[i][j] == symbol and self._board[i + 1][j + 1] == symbol and self._board[i + 2][j + 2] ==\
                        symbol and self._board[i + 3][j + 3] == symbol and self._board[i + 4][j + 4] == symbol:
                    return True

        # Check negative slope diagonal
        for i in range(4, len(self._board)):
            for j in range(len(self._board[i]) - 4):
                if self._board[i][j] == symbol and self._board[i - 1][j + 1] == symbol and self._board[i - 2][j + 2] ==\
                        symbol and self._board[i - 3][j + 3] == symbol and self._board[i - 4][j + 4] == symbol:
                    return True
        return False

    def random_play(self, symbol: str | None) -> tuple(int, int) | None:  # fill the board with a random position
        """
        :param symbol: 'X' 'O' or None
        :return: None
        """
        if self.is_valid_move((self._board_size//2, self._board_size//2)):
            self.update_board(symbol, (self._board_size//2, self._board_size//2))
            return (self._board_size//2, self._board_size//2)
        if len(self.get_empty_positions()) == 0:
            return None
        row = random.randint(0, self._board_size - 1)
        col = random.randint(0, self._board_size - 1)
        while not self.is_valid_move((row, col)):
            row = random.randint(0, self._board_size - 1)
            col = random.randint(0, self._board_size - 1)
        self.update_board(symbol, (row, col))
        return (row, col)

    def get_empty_positions(self) -> list[(int, int)]:
        """
        :return: return a list of tuples with all the empty positions on the board
        """
        empty_positions = []

        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                if self._board[i][j] == None:
                    empty_positions.append((i, j))
        return empty_positions

    def copy_board(self) -> Board:
        """
        :return: return a copy of the current board
        """
        new_board = Board(self._board_size)

        for i in range(self._board_size):
            for j in range(self._board_size):
                new_board.update_board(self._board[i][j], (i, j))
        return new_board

    #check if position is in range of the board
    def is_position_in_range(self, position: tuple(int, int)) -> bool:
        """
        :param position: position on the board (x, y)
        :return: return True if the position is in range of the board, else False
        """
        int(position[0]) + int(position[1])
        if position[0] < 0 or position[0] > self._board_size - 1:
            return False
        if position[1] < 0 or position[1] > self._board_size - 1:
            return False
        return True

    # Create a Sub board of this board with size position -5 to position +5 but that don't exced size of actual board and check if position is in range
    def create_sub_board(self, position: tuple(int, int)) -> Board:
        """
        :param position: position on the board (x, y)
        :return: return a copy of the current board
        """
        new_board = Board(min(min(self._board_size, position[0] + 5) - max(0, position[0] - 5) + 1, self._board_size))

        for i in range(max(0, position[0] - 5), min(self._board_size, position[0] + 5)):
            for j in range(max(0, position[1] - 5), min(self._board_size, position[1] + 5)):
                new_board.update_board(self._board[i][j], (i - max(0, position[0] - 5), j - max(0, position[1] - 5)))
        return new_board
    
    def reset_board(self):
        """
        :return: reset the board to all None
        """
        self._board = [[None for _ in range(self._board_size)] for _ in range(self._board_size)]

    def block_threat_of_three(self, symbol: str | None) -> tuple(int, int) | None:
        """
        :param symbol: 'X' 'O' or None
        :return: True if the player that played the symbol have won, else False
        """
        # Check horizontal threat
        res: list[tuple(int, int)] = []
        for i in range(len(self._board) - 4):
            for j in range(len(self._board[i])):
                if self.is_valid_move((i, j)) and self.is_valid_move((i + 5, j)):
                    empty: list[tuple(int, int)] = []
                    for k in range(1, 5):
                        if self._board[i + k][j] != symbol and self._board[i + k][j] != None:
                            empty = []
                            break
                        if self.is_valid_move((i + k, j)):
                            empty.append((i + k, j))
                    if len(empty) == 1:
                        res.append(empty[0])

        # Check vertical threat
        for i in range(len(self._board)):
            for j in range(len(self._board[i]) - 4):
                if self.is_valid_move((i, j)) and self.is_valid_move((i, j + 5)):
                    empty: list[tuple(int, int)] = []
                    for k in range(1, 5):
                        if self._board[i][j + k] != symbol and self._board[i][j + k] != None:
                            empty = []
                            break
                        if self.is_valid_move((i, j + k)):
                            empty.append((i, j + k))
                    if len(empty) == 1:
                        res.append(empty[0])

        # Check positive slope diagonal threat
        for i in range(len(self._board) - 4):
            for j in range(len(self._board[i]) - 4):
                if self.is_valid_move((i, j)) and self.is_valid_move((i + 5, j + 5)):
                    empty: list[tuple(int, int)] = []
                    for k in range(1, 5):
                        if self._board[i + k][j + k] != symbol and self._board[i + k][j + k] != None:
                            empty = []
                            break
                        if self.is_valid_move((i + k, j + k)):
                            empty.append((i + k, j + k))
                    if len(empty) == 1:
                        res.append(empty[0])

        # Check negative slope diagonal threat
        for i in range(4, len(self._board)):
            for j in range(len(self._board[i]) - 4):
                if self.is_valid_move((i, j)) and self.is_valid_move((i - 5, j + 5)):
                    empty: list[tuple(int, int)] = []
                    for k in range(1, 5):
                        if self._board[i - k][j + k] != symbol and self._board[i - k][j + k] != None:
                            empty = []
                            break
                        if self.is_valid_move((i - k, j + k)):
                            empty.append((i - k, j + k))
                    if len(empty) == 1:
                        res.append(empty[0])
        if len(res) > 0:
            return res[0], res
        return None, []

    def is_one_side_tile_empty(self, position: tuple(int, int)) -> tuple(int, int) | None:
        """
        :param position: position on the board (x, y)
        :return: True if a side tile of position is empty, else False
        """
        res: list[tuple(int, int)] = []
        if position == None:
            return None
        for i in range(3):
            for j in range(3):
                if self.is_valid_move((position[0] + i - 1, position[1] + j - 1)):
                    res.append((position[0] + i - 1, position[1] + j - 1))
        if len(res) == 0:
            return None
        return res[random.randint(0, len(res) - 1)]

    def check_if_there_is_symbol_next(self, position: tuple(int, int)) -> bool:
        """
        :param position: position on the board (x, y)
        :return: True if there is a symbol 'O' or 'X' on the 3x3 square, else False
        """
        if position == None:
            return False
        for i in range(3):
            for j in range(3):
                if position[0] == i and position[1] == j:
                    continue
                try:
                    if self._board[position[0] + i - 1][position[1] + j - 1] != None:
                        return True
                except IndexError:
                    continue
        return False
    
    def check_if_there_is_symbol_next_two(self, position: tuple(int, int)) -> bool:
        """
        :param position: position on the board (x, y)
        :return: True if there is a symbol 'O' or 'X' on the 3x3 square, else False
        """
        if position == None:
            return False
        for i in range(5):
            for j in range(5):
                if position[0] == i and position[1] == j:
                    continue
                try:
                    if self._board[position[0] + i - 2][position[1] + j - 2] != None:
                        return True
                except IndexError:
                    continue
        return False
