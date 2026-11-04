import pygame

LARGURA_BASE = 1920
ALTURA_BASE = 1200

MADEIRA = (86, 60, 37)
MADEIRA_BORDA = (60, 40, 24)
TABULEIRO = (139, 107, 72)
GRADE = (127, 97, 64)
CREME = (244, 236, 218)
CREME_SOBRE = (250, 245, 233)
CREME_BORDA = (226, 213, 188)
SOMBRA = (52, 34, 20)
SOMBRA_BOTAO = (124, 100, 74)
TEXTO = (58, 40, 26)
TEXTO_SUAVE = (112, 92, 72)
TEXTO_INATIVO = (172, 158, 140)
TITULO = (104, 88, 74)
BOTAO_ESCURO = (74, 46, 26)
BOTAO_ESCURO_SOBRE = (98, 63, 36)
BARRA_FUNDO = (217, 207, 188)
CASA_LEGAL = (250, 238, 214, 48)
CASA_LEGAL_SOBRE = (250, 238, 214, 96)
TRACEJADO = (244, 236, 220)
DESTAQUE = (242, 196, 84)
VEU = (30, 20, 12, 150)

CORES_JOGADOR = {"vermelho": (184, 50, 40), "azul": (44, 92, 158)}
NOMES_JOGADOR = {"vermelho": "Vermelho", "azul": "Azul"}

FONTES_SERIFADAS = "timesnewroman,times,liberationserif,dejavuserif,cambria,georgia"


class Fontes:
    _cache = {}

    @classmethod
    def obter(cls, tamanho, negrito=False):
        chave = (tamanho, negrito)
        if chave not in cls._cache:
            cls._cache[chave] = pygame.font.SysFont(FONTES_SERIFADAS, tamanho, bold=negrito)
        return cls._cache[chave]
