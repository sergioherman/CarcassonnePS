import pygame

from interface.estilo import ALTURA_BASE, LARGURA_BASE

OCUPACAO_MAXIMA_LARGURA = 0.92
OCUPACAO_MAXIMA_ALTURA = 0.86


class Escala:
    fator = 1.0
    deslocamento = (0, 0)

    @classmethod
    def tamanhoInicialDaJanela(cls):
        larguraTela, alturaTela = pygame.display.get_desktop_sizes()[0]
        fator = min(
            1.0,
            OCUPACAO_MAXIMA_LARGURA * larguraTela / LARGURA_BASE,
            OCUPACAO_MAXIMA_ALTURA * alturaTela / ALTURA_BASE,
        )
        return int(LARGURA_BASE * fator), int(ALTURA_BASE * fator)

    @classmethod
    def ajustar(cls, largura, altura):
        cls.fator = min(largura / LARGURA_BASE, altura / ALTURA_BASE)
        cls.deslocamento = (
            int((largura - LARGURA_BASE * cls.fator) / 2),
            int((altura - ALTURA_BASE * cls.fator) / 2),
        )

    @classmethod
    def tamanhoEscalado(cls):
        return int(LARGURA_BASE * cls.fator), int(ALTURA_BASE * cls.fator)

    @classmethod
    def paraLogico(cls, posicao):
        return (
            int((posicao[0] - cls.deslocamento[0]) / cls.fator),
            int((posicao[1] - cls.deslocamento[1]) / cls.fator),
        )

    @classmethod
    def mouse(cls):
        return cls.paraLogico(pygame.mouse.get_pos())
