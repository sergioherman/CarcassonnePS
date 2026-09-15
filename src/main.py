import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from game import Game

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()