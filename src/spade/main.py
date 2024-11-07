import os

from src.spade.spade import Spade


def main():
    spade = Spade()
    spade.start()


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../"))
    main()
