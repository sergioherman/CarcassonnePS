from dominio.peca import Peça
from dominio.posicao import Posicao
from dominio.segmento import Segmento
from dominio.territorio import Campo, Cidade, Estrada, Monasterio

N, L, S, O = Posicao.NORTE, Posicao.LESTE, Posicao.SUL, Posicao.OESTE

TIPO_INICIAL = "D"

DEFINICOES = {
    "A": (2, [(Monasterio, []), (Estrada, [S]), (Campo, [N, L, O])]),
    "B": (4, [(Monasterio, []), (Campo, [N, L, S, O])]),
    "C": (1, [(Cidade, [N, L, S, O], 1)]),
    "D": (4, [(Cidade, [N]), (Estrada, [L, O]), (Campo, [S])]),
    "E": (5, [(Cidade, [N]), (Campo, [L, S, O])]),
    "F": (2, [(Cidade, [L, O], 1), (Campo, [N]), (Campo, [S])]),
    "G": (1, [(Cidade, [L, O]), (Campo, [N]), (Campo, [S])]),
    "H": (3, [(Cidade, [L]), (Cidade, [O]), (Campo, [N, S])]),
    "I": (2, [(Cidade, [N]), (Cidade, [O]), (Campo, [L, S])]),
    "J": (3, [(Cidade, [N]), (Estrada, [L, S]), (Campo, [O])]),
    "K": (3, [(Cidade, [N]), (Estrada, [S, O]), (Campo, [L])]),
    "L": (3, [(Cidade, [N]), (Estrada, [L]), (Estrada, [S]), (Estrada, [O])]),
    "M": (2, [(Cidade, [N, O], 1), (Campo, [L, S])]),
    "N": (3, [(Cidade, [N, O]), (Campo, [L, S])]),
    "O": (2, [(Cidade, [N, O], 1), (Estrada, [L, S])]),
    "P": (3, [(Cidade, [N, O]), (Estrada, [L, S])]),
    "Q": (1, [(Cidade, [N, L, O], 1), (Campo, [S])]),
    "R": (3, [(Cidade, [N, L, O]), (Campo, [S])]),
    "S": (2, [(Cidade, [N, L, O], 1), (Estrada, [S])]),
    "T": (1, [(Cidade, [N, L, O]), (Estrada, [S])]),
    "U": (8, [(Estrada, [N, S]), (Campo, [L]), (Campo, [O])]),
    "V": (9, [(Estrada, [S, O]), (Campo, [N, L])]),
    "W": (4, [(Estrada, [L]), (Estrada, [S]), (Estrada, [O]), (Campo, [N])]),
    "X": (1, [(Estrada, [N]), (Estrada, [L]), (Estrada, [S]), (Estrada, [O])]),
}


def criarPeca(tipo):
    _, partes = DEFINICOES[tipo]
    segmentos = [Segmento(lados, classe(*extras)) for classe, lados, *extras in partes]
    return Peça(segmentos, tipo)


def criarPecaInicial():
    return criarPeca(TIPO_INICIAL)


def criarPecasDoMonte():
    pecas = []
    for tipo, (quantidade, _) in DEFINICOES.items():
        copias = quantidade - 1 if tipo == TIPO_INICIAL else quantidade
        pecas.extend(criarPeca(tipo) for _ in range(copias))
    return pecas
