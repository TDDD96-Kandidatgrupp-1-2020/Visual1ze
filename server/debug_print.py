import sys
"""
                                                                     _____
                                                                    /     |
                                                                   /  /|  |
___         ___  ____    _______    __    __       _____      ___  \_/ |  |    ______    ______
\  \       /  /  |  |   /  _____|  |  |  |  |     /     \     |  |     |  |   |____  |  |  ____|
 \  \     /  /   |  |  |  (_____   |  |  |  |    /  /_\  \    |  |     |  |      /  /   |  |___
  \  \   /  /    |  |   \____   \  |  |  |  |   /  _____  \   |  |     |  |     /  /    |   ___|
   \  \_/  /     |  |    ____)   | |  |__|  |  /  /     \  \  |  |___  |  |    /  /__   |  |___
    \_____/      |__|   |_______/   \______/  /__/       \ _\ |______| |  |   /______|  |______|
                                                                     __|  |___
                                                                    |_________|
File to print colors to the console to make debugging easier.
"""

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"


def print_rblue(st):
    sys.stdout.write(REVERSE + BLUE)
    print(st)
    sys.stdout.write(RESET)


def print_rcyan(st):
    sys.stdout.write(REVERSE + CYAN)
    print(st)
    sys.stdout.write(RESET)


def print_rred(st):
    sys.stdout.write(REVERSE + RED)
    print(st)
    sys.stdout.write(RESET)


def print_green(st):
    sys.stdout.write(GREEN)
    print(st)
    sys.stdout.write(RESET)


def print_red(st):
    sys.stdout.write(RED)
    print(st)
    sys.stdout.write(RESET)


def print_blue(st):
    sys.stdout.write(BLUE)
    print(st)
    sys.stdout.write(RESET)


def print_cyan(st):
    sys.stdout.write(CYAN)
    print(st)
    sys.stdout.write(RESET)


def test_printer():
    """ test function to see all prints"""
    st = "testing"
    print_green(st)
    print_blue(st)
    print_rblue(st)
    print_cyan(st)
    print_rcyan(st)
    print_red(st)
    print_rred(st)


if __name__=='__main__':
    test_printer()


def tester():
    print_cyan("it_works")