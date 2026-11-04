import unittest

from dominio.estrategia import EstrategiaIA
from dominio.jogada import Jogada
from dominio.jogador import JogadorIA
from dominio.jogo import Jogo
from dominio.mapa import Mapa
from dominio.posicao import Posicao
from dominio.territorio import Cidade, Estrada, Monasterio
from testes.pecas import (
    N, L, S, O, Campo, SemEmbaralhar, campo, cidadeCanto, cidadeInteira, cidadeNorte,
    criarPeca, estradaReta, monasterio,
)


class EstrategiaEspia(EstrategiaIA):
    def __init__(self):
        self.chamadas = []

    def escolherJogada(self, peca, legais, mapa):
        self.chamadas.append(("jogada", peca, legais, mapa))
        return legais[0]

    def escolherSegmentoMeeple(self, peca, jogador):
        self.chamadas.append(("meeple", peca, jogador))
        return None


class TestRegrasComplementares(unittest.TestCase):
    def test_rn07_mapa_une_territorios_com_meeples_de_jogadores_diferentes(self):
        vermelho = JogadorIA("vermelho", None, None)
        azul = JogadorIA("azul", None, None)
        esquerda = criarPeca((Cidade(), [L]), (Campo(), [N, S, O]))
        mapa = Mapa(esquerda)
        direita = criarPeca((Cidade(), [O]), (Campo(), [N, L, S]))
        mapa.colocarPeca(direita, Jogada(2, 0, 0))
        vermelho.meeples[0].segmento = esquerda.segmentoNoLado(L)
        azul.meeples[0].segmento = direita.segmentoNoLado(O)
        ponte = criarPeca((Cidade(), [L, O]), (Campo(), [N, S]))
        mapa.colocarPeca(ponte, Jogada(1, 0, 0))
        territorio = ponte.segmentoNoLado(L).territorio
        self.assertIs(esquerda.segmentoNoLado(L).territorio, territorio)
        self.assertIs(direita.segmentoNoLado(O).territorio, territorio)
        self.assertEqual({m.dono.cor for m in territorio.meeples()}, {"vermelho", "azul"})
        self.assertTrue(territorio.estaCompleta())
        territorio.calcularPontuacao()
        self.assertEqual((vermelho.pontos, azul.pontos), (6, 6))

    def test_rn08_papel_do_meeple_e_o_tipo_do_territorio(self):
        jogador = JogadorIA("vermelho", None, None)
        pecas = {
            Cidade: cidadeNorte().segmentoNoLado(N),
            Estrada: estradaReta().segmentoNoLado(N),
            Monasterio: monasterio().segmentos[0],
        }
        for tipo, segmento in pecas.items():
            meeple = jogador.meeples[0]
            meeple.segmento = segmento
            self.assertIsInstance(meeple.segmento.territorio, tipo)
            meeple.segmento = None

    def test_rn21_maioria_na_pontuacao_final(self):
        vermelho = JogadorIA("vermelho", None, None)
        azul = JogadorIA("azul", None, None)
        inicial = cidadeCanto([N, S])
        mapa = Mapa(inicial)
        meio = cidadeCanto([N, S])
        mapa.colocarPeca(meio, Jogada(0, -1, 0))
        topo = cidadeCanto([N, S])
        vermelho.meeples[0].segmento = inicial.segmentos[0]
        vermelho.meeples[1].segmento = topo.segmentos[0]
        mapa.colocarPeca(topo, Jogada(0, -2, 0))
        azul.meeples[0].segmento = meio.segmentos[0]
        territorio = inicial.segmentos[0].territorio
        self.assertFalse(territorio.estaCompleta())
        territorio.calcularPontuacaoFinal()
        self.assertEqual((vermelho.pontos, azul.pontos), (3, 0))
        self.assertEqual(vermelho.meeplesDisponiveis(), 5)

    def test_d13_meeple_mantem_segmento_sincronizado(self):
        jogador = JogadorIA("vermelho", None, None)
        primeiro = cidadeNorte().segmentos[0]
        segundo = cidadeNorte().segmentos[0]
        meeple = jogador.meeples[0]
        meeple.segmento = primeiro
        self.assertIs(primeiro.meeple, meeple)
        meeple.segmento = segundo
        self.assertIsNone(primeiro.meeple)
        self.assertIs(segundo.meeple, meeple)
        meeple.segmento = None
        self.assertIsNone(segundo.meeple)

    def test_rf17_jogador_ia_delega_para_estrategia(self):
        estrategia = EstrategiaEspia()
        mapa = Mapa(campo())
        jogador = JogadorIA("vermelho", estrategia, mapa)
        legais = [Jogada(0, 1, 0)]
        peca = campo()
        self.assertEqual(jogador.escolherJogada(peca, legais), legais[0])
        self.assertIsNone(jogador.escolherSegmentoMeeple(peca))
        self.assertEqual(estrategia.chamadas, [("jogada", peca, legais, mapa), ("meeple", peca, jogador)])

    def test_rf10_rf20_monte_esvazia_so_com_descartes(self):
        jogo = Jogo([EstrategiaEspia(), EstrategiaEspia()], SemEmbaralhar(), cidadeInteira(), [campo(), campo()])
        jogo.iniciar()
        primeiro = jogo.jogadorAtual
        jogo.executarTurno()
        self.assertTrue(jogo.terminou())
        self.assertEqual(len(jogo.mapa.matriz), 1)
        self.assertIs(jogo.jogadorAtual, primeiro)


class TestPosicaoEMapa(unittest.TestCase):
    def test_d14_girar_em_sentido_horario(self):
        self.assertIs(Posicao.NORTE.girar(1), Posicao.LESTE)
        self.assertIs(Posicao.NORTE.girar(-1), Posicao.OESTE)

    def test_d14_deslocamento_norte_diminui_y(self):
        self.assertEqual(Posicao.NORTE.deslocamento(), (0, -1))
        self.assertEqual(Posicao.LESTE.deslocamento(), (1, 0))

    def test_posicao_de_peca_so_no_mapa(self):
        mapa = Mapa(campo())
        peca = campo()
        mapa.colocarPeca(peca, Jogada(0, 1, 0))
        self.assertEqual(mapa.posicaoDe(peca), (0, 1))
        self.assertFalse(hasattr(peca, "x"))


if __name__ == "__main__":
    unittest.main()
