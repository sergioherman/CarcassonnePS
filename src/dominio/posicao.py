from enum import Enum


class Posicao(Enum):
    NORTE = 0
    LESTE = 1
    SUL = 2
    OESTE = 3

    def girar(self, quartosDeVolta):
        return Posicao((self.value + quartosDeVolta) % 4)

    def oposta(self):
        return self.girar(2)

    def deslocamento(self):
        return _DESLOCAMENTOS[self]


_DESLOCAMENTOS = {
    Posicao.NORTE: (0, -1),
    Posicao.LESTE: (1, 0),
    Posicao.SUL: (0, 1),
    Posicao.OESTE: (-1, 0),
}
