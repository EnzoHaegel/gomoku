#!/usr/bin/env python3
from sys import argv
import sys
from input_parser import InputParser


def usage(reason, exit_code):
    print(f'\033[91m\033[1m' + reason + '\033[0m')
    print("USAGE")
    print("")
    print("DESCRIPTION")
    sys.exit(exit_code)


def gomoku(args) -> int:
    if not InputParser().are_io_open():
        return 84
    playing = True

    while playing:
        playing = InputParser().read_input()
    return 0


def main(args):
    try:
        if "-h" in args:
            usage("Help:", 0)
        if len(args) != 0:
            usage("Bad number of arguments", 84)
        gomoku(args)
    except ValueError:
        usage("Value Error", 84)
    except RecursionError:
        usage("Recursion Error", 84)
    except Exception:
        usage("Error", 84)


if __name__ == "__main__":
    try:
        main(argv[1:])
    except KeyboardInterrupt:
        print("Exited")
        sys.exit(84)
