# LEGENDA: 
#   0 = campo
#   1 = cidade
#   2 = estrada
#   3 = rio

from models.tile import Tile

class TileFactory:
    @staticmethod
    def create_all():
        layouts = {
            1: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [None, 1, 1, 1, None],
            ],
            2: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [None, 0, 2, 0, None],
            ],
            3: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [None, 0, 2, 0, None],
            ],
            4: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [None, 0, 0, 0, None],
            ],
            5: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [None, 0, 0, 0, None],
            ],
            6: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 0],
                [1, None, None, None, 2],
                [1, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            7: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 0],
                [1, None, None, None, 2],
                [1, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            8: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 0],
                [1, None, None, None, 0],
                [1, None, None, None, 0],
                [None, 0, 0, 0, None],
            ],
            9: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 0],
                [1, None, None, None, 0],
                [1, None, None, None, 0],
                [None, 0, 0, 0, None],
            ],
            10: [
                [None, 0, 0, 0, None],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [None, 0, 0, 0, None],
            ],
            11: [
                [None, 0, 0, 0, None],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [None, 0, 0, 0, None],
            ],
            12: [
                [None, 0, 0, 0, None],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [1, None, None, None, 1],
                [None, 0, 0, 0, None],
            ],
            13: [
                [None, 1, 1, 1, None],
                [0, None, None, None, 0],
                [2, None, None, None, 2],
                [0, None, None, None, 0],
                [None, 0, 0, 0, None],
            ],
            14: [
                [None, 1, 1, 1, None],
                [0, None, None, None, 0],
                [0, None, None, None, 2],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            15: [
                [None, 1, 1, 1, None],
                [1, None, None, None, 0],
                [1, None, None, None, 0],
                [1, None, None, None, 0],
                [None, 0, 0, 0, None],
            ],
            16: [
                [None, 1, 1, 1, None],
                [0, None, None, None, 0],
                [2, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            17: [
                [None, 1, 1, 1, None],
                [0, None, None, None, 0],
                [2, None, None, None, 2],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            18: [
                [None, 1, 1, 1, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 0, 0, None],
            ],
            19: [
                [None, 0, 0, 0, None],
                [0, None, None, None, 0],
                [2, None, None, None, 2],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            20: [
                [None, 0, 2, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            21: [
                [None, 0, 2, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            22: [
                [None, 0, 0, 0, None],
                [0, None, None, None, 0],
                [2, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            23: [
                [None, 0, 2, 0, None],
                [0, None, None, None, 0],
                [2, None, None, None, 2],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            24: [
                [None, 0, 0, 0, None],
                [0, None, None, None, 0],
                [2, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            25: [
                [None, 0, 0, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            26: [
                [None, 0, 0, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 0, 0, None],
            ],
            27: [
                [None, 0, 0, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 3, 0, None],
            ],
            28: [
                [None, 0, 0, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 3],
                [0, None, None, None, 0],
                [None, 0, 3, 0, None],
            ],
            29: [
                [None, 0, 0, 0, None],
                [0, None, None, None, 0],
                [3, None, None, None, 3],
                [0, None, None, None, 0],
                [None, 0, 2, 0, None],
            ],
            30: [
                [None, 0, 2, 0, None],
                [0, None, None, None, 0],
                [3, None, None, None, 2],
                [0, None, None, None, 0],
                [None, 0, 3, 0, None],
            ],
            31: [
                [None, 0, 3, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 3, 0, None],
            ],
            32: [
                [None, 0, 3, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 0, 0, None],
            ],
            33: [
                [None, 0, 3, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [0, None, None, None, 0],
                [None, 0, 3, 0, None],
            ],
            34: [
                [None, 0, 3, 0, None],
                [0, None, None, None, 1],
                [2, None, None, None, 1],
                [0, None, None, None, 1],
                [None, 0, 3, 0, None],
            ],
            35: [
                [None, 0, 3, 0, None],
                [0, None, None, None, 0],
                [0, None, None, None, 3],
                [0, None, None, None, 0],
                [None, 0, 0, 0, None],
            ],
            36: [
                [None, 1, 1, 1, None],
                [0, None, None, None, 0],
                [3, None, None, None, 3],
                [0, None, None, None, 0],
                [None, 1, 1, 1, None],
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