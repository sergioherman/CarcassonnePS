import pygame

from dominio.jogo import Jogo
from interface.escala import Escala
from interface.estilo import ALTURA_BASE, LARGURA_BASE
from interface.tela_menu import TelaMenu
from interface.tela_partida import TelaPartida

FPS = 30
EVENTOS_DE_MOUSE = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION)


class Aplicacao:
    def __init__(self):
        pygame.init()
        largura, altura = Escala.tamanhoInicialDaJanela()
        self.janela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
        Escala.ajustar(largura, altura)
        pygame.display.set_caption("Carcassonne")
        self.quadro = pygame.Surface((LARGURA_BASE, ALTURA_BASE))
        self._relogio = pygame.time.Clock()
        self.telaAtual = TelaMenu()

    def executar(self):
        while self.processarQuadro():
            pass
        pygame.quit()

    def processarQuadro(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.VIDEORESIZE:
                Escala.ajustar(evento.w, evento.h)
                continue
            self.telaAtual.tratarEvento(self._paraLogico(evento))
        self.telaAtual.atualizar(pygame.time.get_ticks())
        self._trocarDeTela()
        self.telaAtual.desenhar(self.quadro)
        self._apresentar()
        self._relogio.tick(FPS)
        return True

    def _apresentar(self):
        janela = pygame.display.get_surface()
        if Escala.fator == 1.0:
            janela.blit(self.quadro, (0, 0))
        else:
            janela.fill((0, 0, 0))
            janela.blit(pygame.transform.smoothscale(self.quadro, Escala.tamanhoEscalado()), Escala.deslocamento)
        pygame.display.flip()

    @staticmethod
    def _paraLogico(evento):
        if evento.type not in EVENTOS_DE_MOUSE:
            return evento
        dados = dict(evento.dict)
        dados["pos"] = Escala.paraLogico(evento.pos)
        if "rel" in dados:
            dados["rel"] = (evento.rel[0] / Escala.fator, evento.rel[1] / Escala.fator)
        return pygame.event.Event(evento.type, dados)

    def _trocarDeTela(self):
        if isinstance(self.telaAtual, TelaMenu) and self.telaAtual.escolha is not None:
            escolha = self.telaAtual.escolha
            jogo = Jogo.comEstrategias(escolha.nomesDeEstrategias())
            jogo.iniciar()
            self.telaAtual = TelaPartida(jogo, escolha.descricoes(), escolha.iaContraIa())
        elif isinstance(self.telaAtual, TelaPartida) and self.telaAtual.voltarAoMenu:
            self.telaAtual = TelaMenu()
