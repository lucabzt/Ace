import os

rdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../")
os.chdir(rdir)
print("root:" + os.getcwd())

from src.spade.spade import Spade


def main():
    spade = Spade()
    spade.start()


if __name__ == "__main__":
    print("root:" + rdir)
    main()
