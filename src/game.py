# cria os 71 tiles → embaralha → compra um com draw_next_tile() → guarda-o em _current_tile → desenha-o

from factories.tile_factory import TileFactory
from views.game_view import GameView
import random


class Game:
    def __init__(self):
        self._view = GameView()
        self._tiles = TileFactory.create_all()

        random.shuffle(self._tiles)
        self._current_tile = None
        self.draw_next_tile()

    def draw_next_tile(self):
        if not self._tiles:
            return None

        self._current_tile = self._tiles.pop()
        return self._current_tile

    
    def run(self):
        while True:
            self._view.draw_tile(self._current_tile, 0, 0)
            self._view.update()