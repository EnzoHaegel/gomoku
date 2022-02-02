# This is a 'Board' Class in python for a gomoku game:
#
# The board is a board_size x board_size matrix, and each element can be 'X', 'O', or None.
# The board starts with all elements set to None.
from __future__ import annotations

import random


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
        if position == None or self._board[position[0]][position[1]] != None:
            return False
        self._board[position[0]][position[1]] = symbol
        if symbol == 'X':
            self._last_X_played = position
        else:
            self._last_O_played = position
        return True

    def set_symbol(self, row: int, col: int,
                   symbol: str | None) -> bool:  # set a specific position on the board to be 'X' or 'O' with row and col
        """
        :param row: position X of the board
        :param col: position Y of the board
        :param symbol: 'X' 'O' or None
        :return: True if the symbol have been set, otherwise False
        """
        if self.is_valid_move((row, col)):
            self._board[row][col] = symbol
            return True
        return False

    def is_valid_move(self, position: tuple(int, int)) -> bool:
        """
        :param position: position on the board (x, y)
        :return: True if the move is valid, False if not
        """
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
        for i in range(len(self._board) - 1, 3, -1):
            for j in range(len(self._board[i])):
                if self._board[i][j] == symbol and self._board[i - 1][j] == symbol and self._board[i - 2][j] == symbol \
                        and self._board[i - 3][j] == symbol and self._board[i - 4][j] == symbol:
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

    def random_play(self, symbol: str | None):  # fill the board with a random position
        """
        :param symbol: 'X' 'O' or None
        :return: None
        """
        row = random.randint(0, self._board_size - 1)
        col = random.randint(0, self._board_size - 1)
        while not self.is_valid_move((row, col)):
            row = random.randint(0, self._board_size - 1)
            col = random.randint(0, self._board_size - 1)
        if self._board[row][col] == None:
            self._board[row][col] = symbol

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
        new_board = Board(min(self._board_size, position[0] + 5) - max(0, position[0] - 5) + 1)

        for i in range(max(0, position[0] - 5), min(self._board_size, position[0] + 5)):
            for j in range(max(0, position[1] - 5), min(self._board_size, position[1] + 5)):
                new_board.update_board(self._board[i][j], (i - max(0, position[0] - 5), j - max(0, position[1] - 5)))
        return new_board
    
    def reset_board(self):
        """
        :return: reset the board to all None
        """
        self._board = [[None for _ in range(self._board_size)] for _ in range(self._board_size)]



# ------------------------------Unit Test---------------------------------- #

def test_class_Board():
    board = Board(7)
    assert board._board_size == 7
    assert board._board == [[None for _ in range(7)] for _ in range(7)]
    assert board._last_X_played == None
    assert board._last_O_played == None

    board.update_board('X', (0, 0))
    assert board.get_row_col(0, 0) == 'X'
    assert board._last_X_played == (0, 0)

    board.update_board('O', (1, 1))
    assert board.get_row_col(1, 1) == 'O'
    assert board._last_O_played == (1, 1)

    assert not board.is_valid_move((-1, -1))
    assert not board.is_valid_move((8, 8))

    print("Test of constructor class Board: OK")

def test_create_sub_board_Board():
    board = Board(7)
    board.update_board('X', (0, 0))
    board.update_board('X', (2, 2))
    board.update_board('O', (1, 1))
    sub_board = board.create_sub_board((0, 0))
    assert board._board == [['X', None, None, None, None, None, None], [None, 'O', None, None, None, None, None],
                                [None, None, 'X', None, None, None, None], [None, None, None, None, None ,None, None],
                                [None ,None ,None ,None ,None ,None, None], [None ,None ,None ,None ,None ,None, None],
                                [None ,None ,None ,None ,None ,None, None]]
    assert sub_board._board_size == 6
    assert sub_board._board == [['X', None, None, None, None, None], [None, 'O', None, None, None, None],
                                [None, None, 'X', None, None, None], [None, None, None, None, None ,None],
                                [None ,None ,None ,None ,None ,None], [None ,None ,None ,None ,None ,None]]
    sub_board2 = board.create_sub_board((3, 4))
    assert sub_board2._board_size == 6
    assert sub_board2._board == [['X', None, None, None, None, None], [None, 'O', None, None, None, None],
                                [None, None, 'X', None, None, None], [None, None, None, None, None ,None],
                                [None ,None ,None ,None ,None ,None], [None ,None ,None ,None ,None ,None]]

    print("Test of create sub board class Board: OK")

def test_is_position_in_range():
    board = Board(7)
    assert board.is_position_in_range((0, 0))
    assert not board.is_position_in_range((-1, -1))
    assert not board.is_position_in_range((8, 8))

    print("Test of is position in range class Board: OK")

def test_get_empty_positions():
    board = Board(7)
    assert len(board.get_empty_positions()) == 49

    board.update_board('X', (0, 0))
    assert len(board.get_empty_positions()) == 48

    print("Test of get empty positions class Board: OK")

def test_update_board():
    board = Board(7)
    assert board.update_board('X', (0, 0))
    assert not board.update_board('X', (0, 0))

    print("Test of update board class Board: OK")

def test_check_winner():
    board = Board(7)
    assert not board.check_winner('X')

    # set 5 'X' and check winner
    for i in range(4):
        board.update_board('X', (i, 0))
        board.update_board('X', (i, 0))
        board.update_board('X', (i, 0))
        board.update_board('X', (i, 0))
    assert not board.check_winner('X')

    # set the last 'X' and check winner
    board.update_board('X', (4, 0))
    assert board.check_winner('X')