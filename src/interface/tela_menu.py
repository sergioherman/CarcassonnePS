import pygame

from dominio.jogo import Jogo
from interface.componentes import Botao, cartao, texto, textoEspacado
from interface.desenho_peca import desenharMeeple
from interface.escala import Escala
from interface.estilo import CORES_JOGADOR, LARGURA_BASE, MADEIRA, MADEIRA_BORDA, TEXTO, TEXTO_SUAVE

RET_CARTAO = pygame.Rect(0, 0, 680, 720)
RET_CARTAO.center = (LARGURA_BASE // 2, 600)
MODOS = (
    ("Humano × Humano", (False, False)),
    ("Humano × IA", (False, True)),
    ("IA × IA", (True, True)),
)


class EscolhaDePartida:
    def __init__(self, ehIa, nomeEstrategia):
        self.ehIa = ehIa
        self.nomeEstrategia = nomeEstrategia

    def nomesDeEstrategias(self):
        return [self.nomeEstrategia if ia else None for ia in self.ehIa]

    def descricoes(self):
        return ["IA " + self.nomeEstrategia.lower() if ia else "Humano" for ia in self.ehIa]

    def iaContraIa(self):
        return all(self.ehIa)


class TelaMenu:
    def __init__(self):
        self._estrategias = Jogo.nomesDeEstrategias()
        self._indiceEstrategia = 0
        x = RET_CARTAO.left + 70
        largura = RET_CARTAO.width - 140
        self._botoesModo = [
            (Botao((x, RET_CARTAO.top + 250 + i * 100, largura, 76), nome, escuro=True, tamanhoFonte=30), ehIa)
            for i, (nome, ehIa) in enumerate(MODOS)
        ]
        self._botaoEstrategia = Botao((x, RET_CARTAO.top + 580, largura, 66), "", tamanhoFonte=26)
        self.escolha = None

    def tratarEvento(self, evento):
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return
        if self._botaoEstrategia.contem(evento.pos):
            self._indiceEstrategia = (self._indiceEstrategia + 1) % len(self._estrategias)
            return
        for botao, ehIa in self._botoesModo:
            if botao.contem(evento.pos):
                self.escolha = EscolhaDePartida(ehIa, self._estrategias[self._indiceEstrategia])

    def atualizar(self, agora):
        pass

    def desenhar(self, superficie):
        mouse = Escala.mouse()
        superficie.fill(MADEIRA)
        pygame.draw.rect(superficie, MADEIRA_BORDA, superficie.get_rect(), 8)
        cartao(superficie, RET_CARTAO)
        centroX = RET_CARTAO.centerx
        superficie.blit(desenharMeeple(CORES_JOGADOR["azul"], 64), (RET_CARTAO.left + 46, RET_CARTAO.top + 60))
        superficie.blit(desenharMeeple(CORES_JOGADOR["vermelho"], 64), (RET_CARTAO.right - 110, RET_CARTAO.top + 60))
        texto(superficie, "Carcassonne", (centroX, RET_CARTAO.top + 92), 72, TEXTO, True, "center")
        texto(superficie, "Escolha o modo de jogo", (centroX, RET_CARTAO.top + 180), 28, TEXTO_SUAVE, ancora="center")
        for botao, _ in self._botoesModo:
            botao.desenhar(superficie, mouse)
        textoEspacado(superficie, "Inteligência artificial", (RET_CARTAO.left + 70, RET_CARTAO.top + 540), 22)
        self._botaoEstrategia.rotulo = f"Estratégia: {self._estrategias[self._indiceEstrategia]}  (clique para trocar)"
        self._botaoEstrategia.desenhar(superficie, mouse)
