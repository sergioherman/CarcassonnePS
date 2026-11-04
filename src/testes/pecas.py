import random

from dominio.peca import Peça
from dominio.posicao import Posicao
from dominio.segmento import Segmento
from dominio.territorio import Campo, Cidade, Estrada, Monasterio

N, L, S, O = Posicao.NORTE, Posicao.LESTE, Posicao.SUL, Posicao.OESTE


def criarPeca(*partes):
    return Peça([Segmento(posicoes, territorio) for territorio, posicoes in partes])


def cidadeNorte(escudos=0):
    return criarPeca((Cidade(escudos), [N]), (Campo(), [L, S, O]))


def cidadeSul(escudos=0):
    return criarPeca((Cidade(escudos), [S]), (Campo(), [N, L, O]))


def cidadeCanto(lados):
    restantes = [lado for lado in Posicao if lado not in lados]
    return criarPeca((Cidade(), lados), (Campo(), restantes))


def cidadeInteira():
    return criarPeca((Cidade(), [N, L, S, O]))


def estradaReta():
    return criarPeca((Estrada(), [N, S]), (Campo(), [L]), (Campo(), [O]))


def estradaTerminaEm(lado):
    restantes = [outro for outro in Posicao if outro is not lado]
    return criarPeca((Estrada(), [lado]), (Campo(), restantes))


def monasterio():
    return criarPeca((Monasterio(), []), (Campo(), [N, L, S, O]))


def campo():
    return criarPeca((Campo(), [N, L, S, O]))


class SemEmbaralhar:
    def shuffle(self, lista):
        pass

    def choice(self, lista):
        return lista[0]


def misturaDePecas(quantidade, semente):
    rng = random.Random(semente)
    fabricas = [
        cidadeNorte,
        lambda: cidadeNorte(escudos=1),
        lambda: cidadeCanto([N, L]),
        estradaReta,
        lambda: estradaTerminaEm(N),
        monasterio,
        campo,
        lambda: criarPeca((Cidade(), [N]), (Estrada(), [L, O]), (Campo(), [S])),
    ]
    return [rng.choice(fabricas)() for _ in range(quantidade)]
