import random

from dominio.catalogo import criarPecasDoMonte


class Monte:
    def __init__(self, pecas=None, rng=None):
        self._pecas = list(pecas) if pecas is not None else criarPecasDoMonte()
        (rng or random.Random()).shuffle(self._pecas)

    def comprar(self):
        return self._pecas.pop(0)

    def vazio(self):
        return not self._pecas

    def pecasRestantes(self):
        return len(self._pecas)
