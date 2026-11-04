import unittest
from collections import Counter

from dominio.catalogo import DEFINICOES, TIPO_INICIAL, criarPeca, criarPecaInicial, criarPecasDoMonte
from dominio.posicao import Posicao
from dominio.territorio import Cidade, Monasterio


class TestCatalogo(unittest.TestCase):
    def test_rf02_rf03_72_pecas_sendo_1_inicial_e_71_no_monte(self):
        self.assertEqual(len(criarPecasDoMonte()), 71)
        self.assertEqual(criarPecaInicial().tipo, TIPO_INICIAL)
        self.assertEqual(sum(quantidade for quantidade, _ in DEFINICOES.values()), 72)

    def test_24_tipos_do_jogo_base(self):
        self.assertEqual(len(DEFINICOES), 24)

    def test_quantidade_de_cada_tipo_no_monte(self):
        contagem = Counter(peca.tipo for peca in criarPecasDoMonte())
        for tipo, (quantidade, _) in DEFINICOES.items():
            esperado = quantidade - 1 if tipo == TIPO_INICIAL else quantidade
            self.assertEqual(contagem[tipo], esperado, tipo)

    def test_rn02_todo_lado_tem_exatamente_um_segmento(self):
        for tipo in DEFINICOES:
            peca = criarPeca(tipo)
            for lado in Posicao:
                ocupantes = [s for s in peca.segmentos if s.ocupaLado(lado)]
                self.assertEqual(len(ocupantes), 1, f"{tipo} {lado}")

    def test_escudos_e_monasterios_do_jogo_base(self):
        pecas = criarPecasDoMonte() + [criarPecaInicial()]
        territorios = [s.territorio for peca in pecas for s in peca.segmentos]
        escudos = sum(t.escudos for t in territorios if isinstance(t, Cidade))
        monasterios = sum(1 for t in territorios if isinstance(t, Monasterio))
        self.assertEqual(escudos, 10)
        self.assertEqual(monasterios, 6)

    def test_pecas_criadas_nao_compartilham_territorios(self):
        a, b = criarPeca("E"), criarPeca("E")
        self.assertIsNot(a.segmentos[0].territorio, b.segmentos[0].territorio)


if __name__ == "__main__":
    unittest.main()
