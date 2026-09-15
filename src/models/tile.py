class Tile:
    def __init__(self, tile_id, image_path, layout):
        self.tile_id = tile_id
        self.image_path = image_path
        self.layout = layout  # matriz 5x5
        self.rotation = 0

    def rotate_clockwise(self):
        self.layout = [list(row) for row in zip(*self.layout[::-1])]
        self.rotation = (self.rotation + 90) % 360

    def north_edge(self):
        return self.layout[0]

    def south_edge(self):
        return self.layout[-1]

    def west_edge(self):
        return [row[0] for row in self.layout]

    def east_edge(self):
        return [row[-1] for row in self.layout]