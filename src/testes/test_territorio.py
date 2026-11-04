import unittest

from dominio.jogador import JogadorIA
from dominio.territorio import Cidade, Estrada, Monasterio
from testes.pecas import N, S, L, O, Campo, criarPeca


def jogador(cor="vermelho"):
    return JogadorIA(cor, None, None)


def cidadeCom(*partes):
    peca = criarPeca(*partes)
    return peca.segmentos[0]


class TestTerritorio(unittest.TestCase):
    def test_rn12_cidade_completa_2_por_peca_e_2_por_escudo(self):
        a = cidadeCom((Cidade(escudos=1), [S]), (Campo(), [N, L, O]))
        b = cidadeCom((Cidade(), [N]), (Campo(), [S, L, O]))
        a.territorio.unir(b.territorio)
        self.assertTrue(a.territorio.estaCompleta())
        self.assertEqual(a.territorio.pontosPorPeca(), 6)

    def test_rn18_cidade_incompleta_1_por_peca_e_1_por_escudo(self):
        a = cidadeCom((Cidade(escudos=1), [S, N]), (Campo(), [L, O]))
        b = cidadeCom((Cidade(), [N]), (Campo(), [S, L, O]))
        a.territorio.unir(b.territorio)
        self.assertFalse(a.territorio.estaCompleta())
        self.assertEqual(a.territorio.pontosPorPecaFinal(), 3)

    def test_rn13_rn19_estrada_1_por_peca(self):
        a = cidadeCom((Estrada(), [S]), (Campo(), [N, L, O]))
        b = cidadeCom((Estrada(), [N]), (Campo(), [S, L, O]))
        a.territorio.unir(b.territorio)
        self.assertEqual(a.territorio.pontosPorPeca(), 2)
        self.assertEqual(a.territorio.pontosPorPecaFinal(), 2)

    def test_rn11_rn14_rn20_monasterio(self):
        monasterio = Monasterio()
        criarPeca((monasterio, []), (Campo(), [N, L, S, O]))
        for _ in range(3):
            monasterio.registrarVizinho()
        self.assertFalse(monasterio.estaCompleta())
        self.assertEqual(monasterio.pontosPorPecaFinal(), 4)
        for _ in range(5):
            monasterio.registrarVizinho()
        self.assertTrue(monasterio.estaCompleta())
        self.assertEqual(monasterio.pontosPorPeca(), 9)

    def test_rn15_maioria_pontua_minoria_nao(self):
        vermelho, azul = jogador("vermelho"), jogador("azul")
        segmentos = [cidadeCom((Cidade(), [N]), (Campo(), [L, S, O])) for _ in range(3)]
        vermelho.meeples[0].segmento = segmentos[0]
        vermelho.meeples[1].segmento = segmentos[1]
        azul.meeples[0].segmento = segmentos[2]
        territorio = segmentos[0].territorio
        territorio.unir(segmentos[1].territorio)
        territorio.unir(segmentos[2].territorio)
        self.assertEqual(territorio.vencedores(), [vermelho])

    def test_rn15_empate_todos_recebem_integral(self):
        vermelho, azul = jogador("vermelho"), jogador("azul")
        a = cidadeCom((Cidade(), [S]), (Campo(), [N, L, O]))
        b = cidadeCom((Cidade(), [N]), (Campo(), [S, L, O]))
        vermelho.meeples[0].segmento = a
        azul.meeples[0].segmento = b
        a.territorio.unir(b.territorio)
        a.territorio.calcularPontuacao()
        self.assertEqual((vermelho.pontos, azul.pontos), (4, 4))

    def test_rn16_meeples_voltam_inclusive_de_quem_nao_pontuou(self):
        vermelho, azul = jogador("vermelho"), jogador("azul")
        segmentos = [cidadeCom((Cidade(), [N]), (Campo(), [L, S, O])) for _ in range(3)]
        vermelho.meeples[0].segmento = segmentos[0]
        vermelho.meeples[1].segmento = segmentos[1]
        azul.meeples[0].segmento = segmentos[2]
        territorio = segmentos[0].territorio
        territorio.unir(segmentos[1].territorio)
        territorio.unir(segmentos[2].territorio)
        territorio.calcularPontuacao()
        self.assertEqual(azul.pontos, 0)
        self.assertEqual(vermelho.meeplesDisponiveis(), 7)
        self.assertEqual(azul.meeplesDisponiveis(), 7)
        self.assertEqual(territorio.meeples(), [])

    def test_rn21_pontuacao_final_mantem_meeples_e_maioria(self):
        vermelho, azul = jogador("vermelho"), jogador("azul")
        a = cidadeCom((Cidade(), [S, N]), (Campo(), [L, O]))
        vermelho.meeples[0].segmento = a
        a.territorio.calcularPontuacaoFinal()
        self.assertEqual((vermelho.pontos, azul.pontos), (1, 0))
        self.assertEqual(vermelho.meeplesDisponiveis(), 6)

    def test_rn07_unir_territorios_com_meeples_mantem_todos(self):
        vermelho, azul = jogador("vermelho"), jogador("azul")
        a = cidadeCom((Cidade(), [S]), (Campo(), [N, L, O]))
        b = cidadeCom((Cidade(), [N]), (Campo(), [S, L, O]))
        vermelho.meeples[0].segmento = a
        azul.meeples[0].segmento = b
        absorvido = b.territorio
        a.territorio.unir(absorvido)
        self.assertEqual(len(a.territorio.meeples()), 2)
        self.assertIs(b.territorio, a.territorio)
        self.assertEqual(absorvido.segmentos, [])

    def test_rn17_peca_conta_uma_vez_no_territorio(self):
        primeira, segunda = Cidade(), Cidade()
        criarPeca((primeira, [N]), (segunda, [S]), (Campo(), [L, O]))
        primeira.unir(segunda)
        self.assertEqual(primeira.qtdPecas, 1)

    def test_unir_consigo_mesmo_so_fecha_bordas(self):
        cidade = Cidade()
        criarPeca((cidade, [N, S]), (Campo(), [L, O]))
        cidade.unir(cidade)
        self.assertEqual(cidade.bordasAbertas, 0)
        self.assertEqual(len(cidade.segmentos), 1)

    def test_rn05_campo_nunca_completa_nem_pontua(self):
        campo = Campo()
        criarPeca((campo, [N, L, S, O]))
        self.assertFalse(campo.estaCompleta())
        self.assertEqual(campo.pontosPorPeca(), 0)
        self.assertEqual(campo.pontosPorPecaFinal(), 0)


if __name__ == "__main__":
    unittest.main()
