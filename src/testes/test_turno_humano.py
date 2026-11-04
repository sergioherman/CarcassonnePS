import random
import unittest

from dominio.jogada import Jogada
from dominio.jogador import JogadorHumano
from dominio.jogo import Jogo
from testes.pecas import N, S, SemEmbaralhar, campo, cidadeCanto, cidadeNorte, cidadeSul


def jogoHumano(inicial, pecas):
    jogo = Jogo([None, None], SemEmbaralhar(), inicial, pecas)
    jogo.iniciar()
    return jogo


class TestTurnoHumano(unittest.TestCase):
    def test_rf01_estrategia_ausente_cria_jogador_humano(self):
        jogo = jogoHumano(campo(), [campo()])
        self.assertTrue(all(isinstance(j, JogadorHumano) for j in jogo.jogadores))
        self.assertTrue(jogo.jogadorAtual.ehHumano())

    def test_rf06_rf07_comprar_expoe_peca_da_vez_e_jogadas_legais(self):
        peca = cidadeSul()
        jogo = jogoHumano(cidadeNorte(), [peca])
        self.assertIs(jogo.comprarPeca(), peca)
        self.assertIs(jogo.pecaDaVez, peca)
        self.assertIn(Jogada(0, -1, 0), jogo.legais)

    def test_rf11_rf14_turno_em_passos_coloca_meeple_e_pontua(self):
        jogo = jogoHumano(cidadeNorte(), [cidadeSul(), campo()])
        jogador = jogo.jogadorAtual
        peca = jogo.comprarPeca()
        jogo.jogar(Jogada(0, -1, 0))
        self.assertIn(peca.segmentoNoLado(S), jogo.segmentosParaMeeple())
        jogo.colocarMeeple(peca.segmentoNoLado(S))
        self.assertEqual(jogador.pontos, 4)
        self.assertEqual(jogador.meeplesDisponiveis(), 7)
        self.assertIsNone(jogo.pecaDaVez)
        self.assertIsNot(jogo.jogadorAtual, jogador)

    def test_rf11_meeple_e_opcional(self):
        jogo = jogoHumano(cidadeNorte(), [cidadeSul(), campo()])
        jogador = jogo.jogadorAtual
        jogo.comprarPeca()
        jogo.jogar(Jogada(0, -1, 0))
        jogo.colocarMeeple(None)
        self.assertEqual(jogador.pontos, 0)
        self.assertEqual(jogador.meeplesDisponiveis(), 7)

    def test_passos_fora_de_ordem_sao_recusados(self):
        jogo = jogoHumano(cidadeNorte(), [cidadeSul(), campo()])
        with self.assertRaises(ValueError):
            jogo.jogar(Jogada(0, -1, 0))
        with self.assertRaises(ValueError):
            jogo.colocarMeeple(None)
        jogo.comprarPeca()
        with self.assertRaises(ValueError):
            jogo.comprarPeca()
        with self.assertRaises(ValueError):
            jogo.colocarMeeple(None)
        jogo.jogar(Jogada(0, -1, 0))
        with self.assertRaises(ValueError):
            jogo.jogar(Jogada(0, 1, 0))

    def test_rf09_humano_nao_joga_fora_das_legais(self):
        jogo = jogoHumano(cidadeNorte(), [cidadeSul()])
        jogo.comprarPeca()
        with self.assertRaisesRegex(ValueError, "RF-09"):
            jogo.jogar(Jogada(0, 1, 180))

    def test_rn05_segmentos_para_meeple_excluem_campo(self):
        jogo = jogoHumano(campo(), [cidadeNorte()])
        peca = jogo.comprarPeca()
        jogo.jogar(jogo.legais[0])
        cidade = peca.segmentos[0]
        self.assertEqual(jogo.segmentosParaMeeple(), [cidade])

    def test_rf20_nao_termina_com_peca_da_vez_pendente(self):
        jogo = jogoHumano(campo(), [campo()])
        jogo.comprarPeca()
        self.assertTrue(jogo.monte.vazio())
        self.assertFalse(jogo.terminou())
        jogo.jogar(jogo.legais[0])
        jogo.colocarMeeple(None)
        self.assertTrue(jogo.terminou())

    def test_executar_turno_e_exclusivo_da_ia(self):
        jogo = jogoHumano(campo(), [campo()])
        with self.assertRaises(ValueError):
            jogo.executarTurno()

    def test_rf01_partida_criada_pelo_nome_da_estrategia(self):
        jogo = Jogo.comEstrategias([None, "Gulosa"])
        jogo.iniciar()
        humano, ia = jogo.jogadores
        self.assertTrue(humano.ehHumano())
        self.assertFalse(ia.ehHumano())
        self.assertEqual(Jogo.nomesDeEstrategias(), ["Gulosa", "Aleatória"])
        self.assertEqual(len(jogo.mapa.matriz), 1)
        self.assertEqual(jogo.monte.pecasRestantes(), 71)

    def test_rn03_lados_ocupados_consideram_rotacao(self):
        peca = cidadeNorte()
        peca.rotacionar()
        self.assertEqual([lado.name for lado in peca.segmentos[0].ladosOcupados()], ["LESTE"])

    def test_rn05_campo_nao_aceita_meeple(self):
        peca = cidadeNorte()
        self.assertTrue(peca.segmentos[0].territorio.aceitaMeeple())
        self.assertFalse(peca.segmentos[1].territorio.aceitaMeeple())
        self.assertEqual(peca.segmentosLivres(), [peca.segmentos[0]])

    def test_rf05_quem_comeca_e_sorteado(self):
        primeiros = set()
        for semente in range(20):
            jogo = Jogo([None, None], random.Random(semente), campo(), [campo()])
            jogo.iniciar()
            primeiros.add(jogo.jogadorAtual.cor)
        self.assertEqual(primeiros, {"vermelho", "azul"})

    def test_rf12_meeple_recusado_em_territorio_com_meeple_do_adversario(self):
        jogo = jogoHumano(cidadeNorte(), [cidadeCanto([N, S]), cidadeCanto([N, S]), campo()])
        primeiro = jogo.comprarPeca()
        jogo.jogar(Jogada(0, -1, 0))
        jogo.colocarMeeple(primeiro.segmentos[0])
        segunda = jogo.comprarPeca()
        jogo.jogar(Jogada(0, -2, 0))
        self.assertEqual(jogo.segmentosParaMeeple(), [])
        with self.assertRaisesRegex(ValueError, "RN-06"):
            jogo.colocarMeeple(segunda.segmentos[0])

    def test_partida_deve_ter_dois_jogadores(self):
        with self.assertRaises(ValueError):
            Jogo([None])


if __name__ == "__main__":
    unittest.main()
