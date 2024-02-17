from . import *
from .builtins import str as s

def _main():
    this = "this:that" | s.swapcase
    print(this)


if __name__ == "__main__":
    _main()
