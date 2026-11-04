import random
import time
import unittest

from dominio.estrategia import EstrategiaAleatoria, EstrategiaGulosa
from dominio.jogada import Jogada
from dominio.jogador import JogadorIA
from dominio.jogo import Jogo
from dominio.mapa import Mapa
from testes.pecas import N, S, campo, cidadeNorte, cidadeSul

LIMITE_RNF01_SEGUNDOS = 1.0


class EstrategiaCronometrada(EstrategiaGulosa):
    def __init__(self, rng):
        super().__init__(rng)
        self.maiorTempo = 0.0

    def escolherJogada(self, peca, legais, mapa):
        inicio = time.perf_counter()
        jogada = super().escolherJogada(peca, legais, mapa)
        self.maiorTempo = max(self.maiorTempo, time.perf_counter() - inicio)
        return jogada


class TestEstrategiaGulosa(unittest.TestCase):
    def test_rf17_gulosa_prefere_jogada_que_completa_cidade(self):
        mapa = Mapa(cidadeNorte())
        peca = cidadeSul()
        legais = mapa.jogadasLegais(peca)
        escolha = EstrategiaGulosa(random.Random(0)).escolherJogada(peca, legais, mapa)
        self.assertEqual(escolha, Jogada(0, -1, 0))

    def test_gulosa_nao_altera_o_mapa_real(self):
        inicial = cidadeNorte()
        mapa = Mapa(inicial)
        peca = cidadeSul()
        EstrategiaGulosa(random.Random(0)).escolherJogada(peca, mapa.jogadasLegais(peca), mapa)
        self.assertEqual(len(mapa.matriz), 1)
        self.assertFalse(inicial.segmentoNoLado(N).territorio.estaCompleta())
        self.assertIsNone(peca.segmentoNoLado(S).territorio.meeples() or None)

    def test_rn06_gulosa_coloca_meeple_em_territorio_completo(self):
        mapa = Mapa(cidadeNorte())
        peca = cidadeSul()
        mapa.colocarPeca(peca, Jogada(0, -1, 0))
        jogador = JogadorIA("vermelho", EstrategiaGulosa(), mapa)
        self.assertIs(jogador.escolherSegmentoMeeple(peca), peca.segmentoNoLado(S))

    def test_rn05_gulosa_nao_coloca_meeple_em_campo(self):
        jogador = JogadorIA("vermelho", EstrategiaGulosa(), None)
        self.assertIsNone(jogador.escolherSegmentoMeeple(campo()))

    def test_rnf01_partida_completa_com_catalogo_em_menos_de_1s_por_jogada(self):
        gulosa = EstrategiaCronometrada(random.Random(7))
        jogo = Jogo([gulosa, EstrategiaAleatoria(random.Random(8))], random.Random(9))
        jogo.iniciar()
        while not jogo.terminou():
            jogo.executarTurno()
        jogo.pontuarFinal()
        self.assertEqual(jogo.monte.pecasRestantes(), 0)
        self.assertLess(gulosa.maiorTempo, LIMITE_RNF01_SEGUNDOS)


if __name__ == "__main__":
    unittest.main()
