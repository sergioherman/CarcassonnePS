GRAUS_POR_QUARTO = 90


class Segmento:
    def __init__(self, posicoes, territorio):
        self.posicoes = list(posicoes)
        self.territorio = territorio
        self.peca = None
        self.meeple = None
        territorio.adicionar(self)

    def ocupaLado(self, lado):
        return lado in self.ladosOcupados()

    def ladosOcupados(self):
        rotacao = self.peca.rotacao if self.peca is not None else 0
        return [lado.girar(rotacao // GRAUS_POR_QUARTO) for lado in self.posicoes]

    def compativel(self, outro):
        return type(self.territorio) is type(outro.territorio)
