# This is a 'Board' Class in python for a gomoku game:
#
# The board is a board_size x board_size matrix, and each element can be 'X', 'O', or None.
# The board starts with all elements set to None.
from __future__ import annotations

from Board import Board


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

def test_is_full_Board():
    board = Board(5)
    assert board.is_full() == False
    for i in range(5):
        for j in range(5):
            board.update_board('X', (i, j))
    assert board.is_full() == True


def test_get_empty_positions():
    board = Board(5)
    assert len(board.get_empty_positions()) == 25

    for i in range(5):
        for j in range(5):
            board.update_board('X', (i, j))

    assert len(board.get_empty_positions()) == 0

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
    assert sub_board2._board_size == 7
    assert sub_board2._board == [['X', None, None, None, None, None, None], [None, 'O', None, None, None, None, None],
                                [None, None, 'X', None, None, None, None], [None, None, None, None, None ,None, None],
                                [None ,None ,None ,None ,None ,None, None], [None ,None ,None ,None ,None ,None, None],
                                [None ,None ,None ,None ,None ,None, None]]

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
    # board2 = Board(7)
    board_long = Board(100)
    assert not board.check_winner('X')
    assert not board_long.check_winner('X')

    # set 5 'X' and check winner
    for i in range(4):
        board.update_board('X', (i, 0))
    assert not board.check_winner('X')

    # set the last 'X' and check winner
    board.update_board('X', (4, 0))
    assert board.check_winner('X')

def test_block_threat_of_three():
    board = Board(7)
    assert board.block_threat_of_three('X') == (None, [])
    for i in range (3):
        board.update_board('X', (i + 1, 0))
    assert board.block_threat_of_three('X') == ((4, 0), [(4, 0)])
    
    board.reset_board()
    assert board.block_threat_of_three('X') == (None, [])
    for i in range (3):
        board.update_board('X', (i + 1, i + 1))
    assert board.block_threat_of_three('X') == ((4, 4), [(4, 4)])
    
    board.reset_board()
    assert board.block_threat_of_three('X') == (None, [])
    for i in range (3):
        board.update_board('X', (i + 2, i + 2))
    assert board.block_threat_of_three('X') == ((1, 1), [(1, 1), (5, 5)])

    board.reset_board()
    assert board.block_threat_of_three('X') == (None, [])
    board.update_board('X', (2, 0))
    board.update_board('X', (3, 0))
    board.update_board('X', (5, 0))
    assert board.block_threat_of_three('X') == ((4, 0), [(4, 0)])
