import random
import unittest

from dominio.estrategia import EstrategiaAleatoria, EstrategiaIA
from dominio.jogada import Jogada
from dominio.jogo import Jogo
from dominio.monte import Monte
from testes.pecas import (
    N, S, SemEmbaralhar, campo, cidadeCanto, cidadeInteira, cidadeNorte, cidadeSul, misturaDePecas,
)


class EstrategiaRoteirizada(EstrategiaIA):
    def __init__(self, jogadas=(), meeples=()):
        self.jogadas = list(jogadas)
        self.meeples = list(meeples)

    def escolherJogada(self, peca, legais, mapa):
        return self.jogadas.pop(0) if self.jogadas else legais[0]

    def escolherSegmentoMeeple(self, peca, jogador):
        escolha = self.meeples.pop(0) if self.meeples else None
        return escolha(peca) if escolha else None


def jogoRoteirizado(inicial, pecas, primeira, segunda=None):
    jogo = Jogo([primeira, segunda or EstrategiaRoteirizada()], SemEmbaralhar(), inicial, pecas)
    jogo.iniciar()
    return jogo


class TestJogo(unittest.TestCase):
    def test_rf04_sete_meeples_por_jogador(self):
        jogo = jogoRoteirizado(campo(), [campo()], EstrategiaRoteirizada())
        for jogador in jogo.jogadores:
            self.assertEqual(jogador.meeplesDisponiveis(), 7)

    def test_rf14_rf15_meeple_colocado_pontuado_e_devolvido_no_mesmo_turno(self):
        estrategia = EstrategiaRoteirizada(
            jogadas=[Jogada(0, -1, 0)],
            meeples=[lambda peca: peca.segmentoNoLado(S)],
        )
        jogo = jogoRoteirizado(cidadeNorte(), [cidadeSul()], estrategia)
        jogador = jogo.jogadorAtual
        jogo.executarTurno()
        self.assertEqual(jogador.pontos, 4)
        self.assertEqual(jogador.meeplesDisponiveis(), 7)

    def test_rn06_meeple_em_territorio_ocupado(self):
        estrategia = EstrategiaRoteirizada(
            jogadas=[Jogada(0, -1, 0), Jogada(0, -2, 0)],
            meeples=[lambda peca: peca.segmentoNoLado(N)],
        )
        segunda = EstrategiaRoteirizada(meeples=[lambda peca: peca.segmentoNoLado(S)])
        meio = cidadeCanto([N, S])
        jogo = jogoRoteirizado(cidadeNorte(), [meio, cidadeNorte()], estrategia, segunda)
        jogo.executarTurno()
        jogo.jogadorAtual.estrategia = EstrategiaRoteirizada(
            jogadas=[Jogada(0, -2, 180)],
            meeples=[lambda peca: peca.segmentoNoLado(S)],
        )
        with self.assertRaisesRegex(ValueError, "RN-06"):
            jogo.executarTurno()

    def test_rn05_meeple_em_campo_e_recusado(self):
        estrategia = EstrategiaRoteirizada(meeples=[lambda peca: peca.segmentos[0]])
        jogo = jogoRoteirizado(campo(), [campo()], estrategia)
        with self.assertRaisesRegex(ValueError, "RN-05"):
            jogo.executarTurno()

    def test_rn04_meeple_fora_da_peca_recem_colocada(self):
        inicial = cidadeNorte()
        estrategia = EstrategiaRoteirizada(meeples=[lambda peca: inicial.segmentos[0]])
        jogo = jogoRoteirizado(inicial, [campo()], estrategia)
        with self.assertRaisesRegex(ValueError, "RN-04"):
            jogo.executarTurno()

    def test_rf13_sem_meeples_na_reserva(self):
        estrategia = EstrategiaRoteirizada(meeples=[lambda peca: peca.segmentoNoLado(N)])
        jogo = jogoRoteirizado(campo(), [cidadeNorte()], estrategia)
        for meeple in jogo.jogadorAtual.meeples:
            meeple.segmento = cidadeNorte().segmentos[0]
        with self.assertRaisesRegex(ValueError, "RF-13"):
            jogo.executarTurno()

    def test_rf09_jogada_fora_das_legais_e_recusada(self):
        estrategia = EstrategiaRoteirizada(jogadas=[Jogada(5, 5, 0)])
        jogo = jogoRoteirizado(campo(), [campo()], estrategia)
        with self.assertRaisesRegex(ValueError, "RF-09"):
            jogo.executarTurno()

    def test_rf10_descarta_peca_sem_posicao_legal(self):
        pecaJogavel = cidadeInteira()
        jogo = jogoRoteirizado(cidadeInteira(), [campo(), pecaJogavel], EstrategiaRoteirizada())
        jogo.executarTurno()
        self.assertIn(pecaJogavel, jogo.mapa.matriz.values())
        self.assertEqual(len(jogo.mapa.matriz), 2)

    def test_rf16_alterna_jogador(self):
        jogo = jogoRoteirizado(campo(), [campo(), campo()], EstrategiaRoteirizada())
        primeiro = jogo.jogadorAtual
        jogo.executarTurno()
        self.assertIsNot(jogo.jogadorAtual, primeiro)

    def test_rf20_termina_apos_ultima_peca(self):
        jogo = jogoRoteirizado(campo(), [campo(), campo()], EstrategiaRoteirizada())
        jogo.executarTurno()
        self.assertFalse(jogo.terminou())
        jogo.executarTurno()
        self.assertTrue(jogo.terminou())

    def test_rf21_pontuacao_final_de_territorio_incompleto(self):
        estrategia = EstrategiaRoteirizada(meeples=[lambda peca: peca.segmentoNoLado(N)])
        jogo = jogoRoteirizado(campo(), [cidadeNorte(escudos=1)], estrategia)
        jogador = jogo.jogadorAtual
        jogo.executarTurno()
        jogo.pontuarFinal()
        self.assertEqual(jogador.pontos, 2)

    def test_rf22_rf23_vencedor_e_empate(self):
        jogo = jogoRoteirizado(campo(), [campo()], EstrategiaRoteirizada())
        vermelho, azul = jogo.jogadores
        self.assertIsNone(jogo.vencedor())
        vermelho.addPontos(3)
        self.assertIs(jogo.vencedor(), vermelho)

    def test_partida_ia_contra_ia_mantem_invariantes(self):
        for semente in range(20):
            rng = random.Random(semente)
            jogo = Jogo(
                [EstrategiaAleatoria(random.Random(semente)), EstrategiaAleatoria(random.Random(-semente))],
                rng,
                cidadeNorte(),
                misturaDePecas(71, semente),
            )
            jogo.iniciar()
            while not jogo.terminou():
                jogo.executarTurno()
                for jogador in jogo.jogadores:
                    noTabuleiro = sum(1 for m in jogador.meeples if m.segmento is not None)
                    self.assertEqual(jogador.meeplesDisponiveis() + noTabuleiro, 7)
            jogo.pontuarFinal()
            for territorio in jogo.mapa.territorios():
                for segmento in territorio.segmentos:
                    self.assertIs(segmento.territorio, territorio)


class TestMonte(unittest.TestCase):
    def test_rf03_monte_compra_ate_esvaziar(self):
        monte = Monte([campo(), campo()], random.Random(0))
        self.assertEqual(monte.pecasRestantes(), 2)
        monte.comprar()
        monte.comprar()
        self.assertTrue(monte.vazio())


class TestEstrategiaAleatoria(unittest.TestCase):
    def test_rf17_escolhe_dentre_as_legais(self):
        legais = [Jogada(0, 1, 0), Jogada(1, 0, 90)]
        estrategia = EstrategiaAleatoria(random.Random(1))
        self.assertIn(estrategia.escolherJogada(None, legais, None), legais)

    def test_rn05_rn06_meeple_so_em_segmento_valido(self):
        from dominio.jogador import JogadorIA
        estrategia = EstrategiaAleatoria(random.Random(3))
        jogador = JogadorIA("vermelho", estrategia, None)
        for _ in range(30):
            peca = cidadeNorte()
            escolha = estrategia.escolherSegmentoMeeple(peca, jogador)
            self.assertIn(escolha, [peca.segmentoNoLado(N), None])


if __name__ == "__main__":
    unittest.main()
