import math

import pygame

from interface.estilo import (
    BOTAO_ESCURO, BOTAO_ESCURO_SOBRE, CREME, CREME_BORDA, CREME_SOBRE, Fontes, MADEIRA_BORDA, SOMBRA,
    SOMBRA_BOTAO, TEXTO, TEXTO_INATIVO, TITULO,
)

ESPACO_TITULO = 3
ALTURA_SOMBRA = 5


def texto(superficie, conteudo, posicao, tamanho, cor=TEXTO, negrito=False, ancora="topleft"):
    imagem = Fontes.obter(tamanho, negrito).render(conteudo, True, cor)
    retangulo = imagem.get_rect(**{ancora: posicao})
    superficie.blit(imagem, retangulo)
    return retangulo


def textoEspacado(superficie, conteudo, posicao, tamanho, cor=TITULO):
    x, y = posicao
    fonte = Fontes.obter(tamanho)
    for caractere in conteudo:
        imagem = fonte.render(caractere, True, cor)
        superficie.blit(imagem, (x, y))
        x += imagem.get_width() + ESPACO_TITULO


def textoEmPartes(superficie, partes, posicao, tamanho):
    x, y = posicao
    for conteudo, cor, negrito in partes:
        retangulo = texto(superficie, conteudo, (x, y), tamanho, cor, negrito, ancora="midleft")
        x = retangulo.right


def cartao(superficie, retangulo):
    retangulo = pygame.Rect(retangulo)
    pygame.draw.rect(superficie, SOMBRA, retangulo.move(0, 6))
    pygame.draw.rect(superficie, MADEIRA_BORDA, retangulo)
    pygame.draw.rect(superficie, CREME_BORDA, retangulo.inflate(-6, -6))
    pygame.draw.rect(superficie, CREME, retangulo.inflate(-22, -22))


def iconeGirar(superficie, centro, raio, cor):
    caixa = pygame.Rect(0, 0, raio * 2, raio * 2)
    caixa.center = centro
    pygame.draw.arc(superficie, cor, caixa, math.radians(-40), math.radians(250), 3)
    angulo = math.radians(-40)
    ponta = (centro[0] + raio * math.cos(angulo), centro[1] - raio * math.sin(angulo))
    pygame.draw.polygon(superficie, cor, [
        (ponta[0] - 7, ponta[1] - 7), (ponta[0] + 7, ponta[1] - 5), (ponta[0] + 1, ponta[1] + 6),
    ])


def iconeTocar(superficie, retangulo, cor):
    cx, cy = retangulo.center
    pygame.draw.polygon(superficie, cor, [(cx - 8, cy - 11), (cx - 8, cy + 11), (cx + 11, cy)])


def iconePausar(superficie, retangulo, cor):
    cx, cy = retangulo.center
    pygame.draw.rect(superficie, cor, (cx - 6, cy - 6, 4, 12))
    pygame.draw.rect(superficie, cor, (cx + 2, cy - 6, 4, 12))


def iconeAvancar(superficie, retangulo, cor):
    cx, cy = retangulo.center
    pygame.draw.polygon(superficie, cor, [(cx - 12, cy - 6), (cx - 12, cy + 6), (cx - 4, cy)])
    pygame.draw.polygon(superficie, cor, [(cx - 4, cy - 6), (cx - 4, cy + 6), (cx + 4, cy)])
    pygame.draw.rect(superficie, cor, (cx + 5, cy - 6, 3, 12))


def iconeMenos(superficie, retangulo, cor):
    cx, cy = retangulo.center
    pygame.draw.rect(superficie, cor, (cx - 10, cy - 1, 20, 3))


def iconeMais(superficie, retangulo, cor):
    iconeMenos(superficie, retangulo, cor)
    cx, cy = retangulo.center
    pygame.draw.rect(superficie, cor, (cx - 1, cy - 10, 3, 20))


class Botao:
    def __init__(self, retangulo, rotulo="", escuro=False, icone=None, tamanhoFonte=28):
        self.retangulo = pygame.Rect(retangulo)
        self.rotulo = rotulo
        self.escuro = escuro
        self.icone = icone
        self.tamanhoFonte = tamanhoFonte
        self.ativo = True

    def contem(self, ponto):
        return self.ativo and self.retangulo.collidepoint(ponto)

    def desenhar(self, superficie, mouse):
        sobre = self.contem(mouse)
        if self.escuro:
            cor = BOTAO_ESCURO_SOBRE if sobre else BOTAO_ESCURO
            pygame.draw.rect(superficie, cor if self.ativo else CREME_BORDA, self.retangulo)
            corConteudo = CREME if self.ativo else TEXTO_INATIVO
        else:
            pygame.draw.rect(superficie, SOMBRA_BOTAO, self.retangulo.move(0, ALTURA_SOMBRA))
            pygame.draw.rect(superficie, CREME_SOBRE if sobre else CREME, self.retangulo)
            pygame.draw.rect(superficie, MADEIRA_BORDA if self.ativo else CREME_BORDA, self.retangulo, 3)
            corConteudo = TEXTO if self.ativo else TEXTO_INATIVO
        self._desenharConteudo(superficie, corConteudo)

    def _desenharConteudo(self, superficie, cor):
        if self.icone is None:
            texto(superficie, self.rotulo, self.retangulo.center, self.tamanhoFonte, cor, ancora="center")
            return
        if not self.rotulo:
            self.icone(superficie, self.retangulo, cor)
            return
        largura = Fontes.obter(self.tamanhoFonte).size(self.rotulo)[0]
        inicio = self.retangulo.centerx - (largura + 34) // 2
        self.icone(superficie, pygame.Rect(inicio, self.retangulo.top, 26, self.retangulo.height), cor)
        texto(superficie, self.rotulo, (inicio + 34, self.retangulo.centery), self.tamanhoFonte, cor, ancora="midleft")


class ControleDeslizante:
    def __init__(self, inicioX, fimX, y, valor):
        self.inicioX = inicioX
        self.fimX = fimX
        self.y = y
        self.valor = valor
        self.ativo = True
        self._arrastando = False

    def tratarEvento(self, evento):
        if not self.ativo:
            return
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self._tocado(evento.pos):
            self._arrastando = True
            self._mover(evento.pos[0])
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self._arrastando = False
        elif evento.type == pygame.MOUSEMOTION and self._arrastando:
            self._mover(evento.pos[0])

    def desenhar(self, superficie):
        cor = MADEIRA_BORDA if self.ativo else CREME_BORDA
        pygame.draw.line(superficie, cor, (self.inicioX, self.y), (self.fimX, self.y), 3)
        x = int(self.inicioX + self.valor * (self.fimX - self.inicioX))
        pygame.draw.circle(superficie, CREME, (x, self.y), 14)
        pygame.draw.circle(superficie, cor, (x, self.y), 14, 3)

    def _tocado(self, ponto):
        return self.inicioX - 16 <= ponto[0] <= self.fimX + 16 and abs(ponto[1] - self.y) <= 18

    def _mover(self, x):
        self.valor = max(0.0, min(1.0, (x - self.inicioX) / (self.fimX - self.inicioX)))
