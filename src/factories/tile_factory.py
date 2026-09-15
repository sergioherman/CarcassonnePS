# LEGENDA: o = campo, x = cidade, : = estrada, m = monastério, ~ = rio

from models.tile import Tile

class TileFactory:
    @staticmethod
    def create_all():
        layouts = {
            1: [
                [None, "x", "x", "x", None],
                ["x", None, None, None, "x"],
                ["x", None, None, None, "x"],
                ["x", None, None, None, "x"],
                [None, "x", "x", "x", None],
            ],
            2: [
                [None, "x", "x", "x", None],
                ["x", None, None, None, "x"],
                ["x", None, None, None, "x"],
                ["x", None, None, None, "x"],
                [None, "o", ":", "o", None],
            ],
            # TODO: Adicione os layouts restantes dos tiles aqui, seguindo o mesmo padrão.
            # Ver imagens no assets e a legenda acima para entender como sao as matrizes.

            # ...
            # 71: [...],
        }

        tiles = []

        for tile_id, layout in layouts.items():
            tile = Tile(
                tile_id=tile_id,
                image_path=f"assets/tiles/tile{tile_id:02}.png",
                layout=layout,
            )
            tiles.append(tile)

        return tiles