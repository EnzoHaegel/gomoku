from __future__ import annotations
from AI import Ai
from Board import Board


def test_get_symbol():
    ai = Ai(3, 'X')
    assert ai.get_symbol() == 'X'


def test_get_opponent_symbol():
    ai = Ai(3, 'X')
    assert ai.get_opponent_symbol() == 'O'


def test_get_winning_move():
    board = Board(6)
    ai = Ai(board._board_size, 'X')

    assert ai.get_winning_move(board, ai._symbol) == None
    assert ai.get_opponent_winning_move(board) == None
    for i in range(4):
        board.update_board('X', (i, i))
        board.update_board('O', (i + 1, 0))
    assert ai.get_winning_move(board, ai._symbol) == (4, 4)
    assert ai.get_opponent_winning_move(board) == (5, 0)

def test_can_do_a_double_threat():
    board = Board(7)
    ai = Ai(board._board_size, 'O')
    assert ai.can_do_a_double_threat(board, 'X') == None
    board.update_board('X', (3, 2))
    board.update_board('X', (2, 3))
    board.update_board('X', (2, 4))
    board.update_board('X', (3, 4))

    assert ai.can_do_a_double_threat(board, 'X') == (1, 4)
    board.reset_board()
    for i in range(3):
        board.update_board('X', (i + 1, 3))
    assert ai.can_do_a_double_threat(board, 'X') == None
