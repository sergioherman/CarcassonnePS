from PPlay.window import Window
from PPlay.gameimage import GameImage


class GameView:
    def __init__(self):
        self._window = Window(1200, 600)
        self._window.set_title("Carcassonne")
        self._images = {}

    def draw_tile(self, tile, x, y):
        if tile.tile_id not in self._images:
            self._images[tile.tile_id] = GameImage(tile.image_path)

        image = self._images[tile.tile_id]
        image.set_position(x, y)
        image.draw()

    def update(self):
        self._window.update()