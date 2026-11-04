import unittest

from dominio.jogada import Jogada
from dominio.mapa import Mapa
from dominio.territorio import Cidade, Monasterio
from testes.pecas import (
    N, L, S, O, Campo, campo, cidadeCanto, cidadeInteira, cidadeNorte, cidadeSul, criarPeca,
    estradaReta, estradaTerminaEm, monasterio,
)


class TestMapa(unittest.TestCase):
    def test_rn01_jogadas_so_em_casas_ortogonais_adjacentes(self):
        mapa = Mapa(campo())
        casas = {(j.posicaoX, j.posicaoY) for j in mapa.jogadasLegais(campo())}
        self.assertEqual(casas, {(0, -1), (1, 0), (0, 1), (-1, 0)})

    def test_rn02_lados_encostados_devem_ser_do_mesmo_tipo(self):
        mapa = Mapa(cidadeNorte())
        legais = mapa.jogadasLegais(cidadeSul())
        self.assertIn(Jogada(0, -1, 0), legais)
        self.assertNotIn(Jogada(0, -1, 180), legais)

    def test_rn03_rotacao_torna_jogada_legal(self):
        mapa = Mapa(cidadeNorte())
        peca = criarPeca((Cidade(), [L]), (Campo(), [N, S, O]))
        legais = mapa.jogadasLegais(peca)
        self.assertIn(Jogada(0, -1, 90), legais)
        self.assertNotIn(Jogada(0, -1, 0), legais)
        self.assertEqual(peca.rotacao, 0)

    def test_rf10_peca_sem_jogada_legal(self):
        mapa = Mapa(cidadeInteira())
        self.assertEqual(mapa.jogadasLegais(campo()), [])

    def test_rn09_cidade_completa_ao_fechar(self):
        inicial = cidadeNorte()
        mapa = Mapa(inicial)
        nova = cidadeSul()
        mapa.colocarPeca(nova, Jogada(0, -1, 0))
        territorio = inicial.segmentoNoLado(N).territorio
        self.assertIs(nova.segmentoNoLado(S).territorio, territorio)
        self.assertTrue(territorio.estaCompleta())
        self.assertEqual(territorio.qtdPecas, 2)

    def test_rn09_cidade_em_anel_encosta_duas_vezes_no_mesmo_territorio(self):
        inicial = cidadeCanto([N, L])
        mapa = Mapa(inicial)
        mapa.colocarPeca(cidadeCanto([S, L]), Jogada(0, -1, 0))
        mapa.colocarPeca(cidadeCanto([S, O]), Jogada(1, -1, 0))
        ultima = cidadeCanto([N, O])
        mapa.colocarPeca(ultima, Jogada(1, 0, 0))
        territorio = ultima.segmentoNoLado(N).territorio
        self.assertIs(inicial.segmentoNoLado(N).territorio, territorio)
        self.assertEqual(territorio.bordasAbertas, 0)
        self.assertTrue(territorio.estaCompleta())
        self.assertEqual(territorio.qtdPecas, 4)

    def test_rn10_estrada_completa_com_duas_pontas_fechadas(self):
        inicial = estradaTerminaEm(S)
        mapa = Mapa(inicial)
        mapa.colocarPeca(estradaReta(), Jogada(0, 1, 0))
        self.assertFalse(inicial.segmentoNoLado(S).territorio.estaCompleta())
        mapa.colocarPeca(estradaTerminaEm(N), Jogada(0, 2, 0))
        estrada = inicial.segmentoNoLado(S).territorio
        self.assertTrue(estrada.estaCompleta())
        self.assertEqual(estrada.pontosPorPeca(), 3)

    def test_rn11_monasterio_conta_vizinhas_anteriores_e_posteriores(self):
        inicial = campo()
        mapa = Mapa(inicial)
        mapa.colocarPeca(campo(), Jogada(1, 0, 0))
        peca = monasterio()
        mapa.colocarPeca(peca, Jogada(1, 1, 0))
        territorio = peca.segmentos[0].territorio
        self.assertIsInstance(territorio, Monasterio)
        self.assertEqual(territorio.vizinhosPresentes, 2)
        for x, y in [(2, 1), (2, 0), (0, 1), (0, 2), (1, 2)]:
            mapa.colocarPeca(campo(), Jogada(x, y, 0))
        self.assertFalse(territorio.estaCompleta())
        ultima = campo()
        mapa.colocarPeca(ultima, Jogada(2, 2, 0))
        self.assertTrue(territorio.estaCompleta())
        self.assertIn(territorio, mapa.territoriosAfetados(ultima))

    def test_vizinhos_ortogonais(self):
        mapa = Mapa(campo())
        mapa.colocarPeca(campo(), Jogada(1, 0, 0))
        mapa.colocarPeca(campo(), Jogada(1, 1, 0))
        self.assertEqual(len(mapa.vizinhos(0, 1)), 2)
        self.assertEqual(len(mapa.vizinhos(0, 0)), 1)

    def test_segmento_pertence_a_um_unico_territorio_apos_unir(self):
        inicial = cidadeNorte()
        mapa = Mapa(inicial)
        mapa.colocarPeca(cidadeSul(), Jogada(0, -1, 0))
        for territorio in mapa.territorios():
            for segmento in territorio.segmentos:
                self.assertIs(segmento.territorio, territorio)


if __name__ == "__main__":
    unittest.main()
