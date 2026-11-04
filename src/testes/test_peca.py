import unittest

from dominio.posicao import Posicao
from dominio.territorio import Cidade
from testes.pecas import N, L, S, O, cidadeNorte, criarPeca, Campo


class TestPosicao(unittest.TestCase):
    def test_oposta(self):
        self.assertIs(N.oposta(), S)
        self.assertIs(L.oposta(), O)

    def test_unico_enum_tem_quatro_lados(self):
        self.assertEqual(len(list(Posicao)), 4)


class TestPeca(unittest.TestCase):
    def test_rn03_rotacao_em_incrementos_de_90(self):
        peca = cidadeNorte()
        rotacoes = []
        for _ in range(4):
            peca.rotacionar()
            rotacoes.append(peca.rotacao)
        self.assertEqual(rotacoes, [90, 180, 270, 0])

    def test_rn03_segmento_no_lado_considera_rotacao(self):
        peca = criarPeca((Cidade(), [O]), (Campo(), [N, L, S]))
        cidade = peca.segmentos[0]
        peca.rotacionar()
        self.assertIs(peca.segmentoNoLado(N), cidade)
        self.assertTrue(cidade.ocupaLado(N))
        self.assertFalse(cidade.ocupaLado(O))

    def test_todo_segmento_nasce_com_territorio(self):
        peca = cidadeNorte()
        for segmento in peca.segmentos:
            self.assertIn(segmento, segmento.territorio.segmentos)

    def test_compativel_por_tipo_de_territorio(self):
        a, b = cidadeNorte(), cidadeNorte()
        self.assertTrue(a.segmentoNoLado(N).compativel(b.segmentoNoLado(N)))
        self.assertFalse(a.segmentoNoLado(N).compativel(b.segmentoNoLado(S)))


if __name__ == "__main__":
    unittest.main()
