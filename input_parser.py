import re
import sys
from Singleton import Singleton
from AI import Ai
from Board import Board


class InputParser(metaclass=Singleton):
    def __init__(self):
        self.timeout_turn = 5000
        self.timeout_match = 0
        self.max_memory = 70000000
        self.time_left = 2147483647
        self.game_type = 1
        self.rule = 0
        self.evaluate = (0, 0)
        self.folder = "./"
        self.game_board: Board = None
        self.ai: Ai = None

    def are_io_open(self) -> bool:
        try:
            sys.stdin.fileno()
            sys.stdout.fileno()
            sys.stderr.fileno()
            return True
        except ValueError:
            return False

    def start(self, size: str = "15") -> bool:
        supported_sizes = [i for i in range(25)]
        if int(size) in supported_sizes:
            try:
                self.game_board = Board(int(size))
                self.ai = Ai(int(size), 'X')
            except TypeError:
                return False
            print("OK")
        else:
            print("ERROR unsupported size")
        return True

    def turn(self, x: str = "0", y: str = "0") -> bool:
        try:
            x = int(x)
            y = int(y)
        except TypeError:
            return False
        self.game_board.update_board(self.ai.get_opponent_symbol(), (x, y))
        x, y = self.ai.play_best_move(self.game_board)
        print(x, y, sep=',')
        return True

    def begin(self) -> bool:
        if self.ai == None:
            return False
        x, y = self.ai.play_best_move(self.game_board)
        print(x, y, sep=',')
        return True

    def board(self) -> bool:
        pos = input()
        while pos != "DONE":
            try:
                x, y, player = list(map(int ,pos.split(",")))
            except Exception:
                pass
            if player == 1:
                self.game_board.update_board(self.ai.get_symbol(), (x, y))
            if player == 2:
                self.game_board.update_board(self.ai.get_opponent_symbol(), (x, y))
            pos = input()
        x, y = self.ai.play_best_move(self.game_board)
        print(x, y, sep=',')
        return True

    def info(self, key: str = "folder", value: str = "./") -> bool:
        if key not in self.__dict__:
            return True
        self.__dict__[key] = value
        return True

    def end(self) -> bool:
        return False

    def about(self) -> bool:
        print('name="gomoku-ai", version="1.0", author="Paul-Tanguy & EnzoHaegel", country="France"')
        return True

    def read_input(self) -> bool:
        if not self.are_io_open():
            return False
        func, *arguments = re.split('[\\s,]', input())
        func = func.lower()

        if func not in [method for method in dir(InputParser) if not method.startswith('__')]:
            return False
        return getattr(self, func)(*arguments)
