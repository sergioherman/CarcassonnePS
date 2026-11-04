import pygame

ORDEM_LADOS = ("NORTE", "LESTE", "SUL", "OESTE")
MEIO_DO_LADO = {"NORTE": (0.5, 0.0), "LESTE": (1.0, 0.5), "SUL": (0.5, 1.0), "OESTE": (0.0, 0.5)}
PONTO_DO_MEEPLE_NO_LADO = {"NORTE": (0.5, 0.2), "LESTE": (0.8, 0.5), "SUL": (0.5, 0.8), "OESTE": (0.2, 0.5)}
CENTRO = (0.5, 0.5)
GRAUS_POR_QUARTO = 90
SUPERAMOSTRAGEM = 2
PASSOS_CURVA = 28

CAMPO = (108, 168, 80)
GRAMA = (72, 128, 56)
CIDADE = (201, 126, 78)
MURALHA = (138, 76, 44)
CASA = (238, 198, 156)
TELHADO = (166, 62, 46)
CONTORNO_CASA = (112, 58, 34)
ESTRADA = (234, 223, 198)
BORDA_ESTRADA = (188, 168, 132)
MONASTERIO = (246, 232, 204)
TELHADO_MONASTERIO = (162, 52, 40)
PORTA = (108, 60, 38)
ESCUDO = (46, 88, 164)
ESCUDO_FAIXA = (240, 236, 226)
BORDA_PECA = (66, 44, 26)
CONTORNO_MEEPLE = (36, 24, 16)

TUFOS_DE_GRAMA = ((0.18, 0.72), (0.46, 0.86), (0.78, 0.76), (0.3, 0.46), (0.8, 0.38), (0.14, 0.24), (0.62, 0.2))
LINHAS_DE_CASAS = ((0.1, (0.18, 0.5, 0.82)), (0.34, (0.3, 0.7)), (0.56, (0.18, 0.5, 0.82)), (0.8, (0.32, 0.68)))
CASAS_POR_CIDADE = 5
SILHUETA_MEEPLE = (
    (0.5, 0.3), (0.7, 0.36), (0.96, 0.5), (0.92, 0.62), (0.68, 0.57), (0.8, 1.0), (0.57, 1.0),
    (0.5, 0.8), (0.43, 1.0), (0.2, 1.0), (0.32, 0.57), (0.08, 0.62), (0.04, 0.5), (0.3, 0.36),
)

_cachePecas = {}
_cacheMeeples = {}


def _bezier(inicio, controle, fim):
    pontos = []
    for i in range(PASSOS_CURVA + 1):
        t = i / PASSOS_CURVA
        a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
        pontos.append((
            a * inicio[0] + b * controle[0] + c * fim[0],
            a * inicio[1] + b * controle[1] + c * fim[1],
        ))
    return pontos


def _cidadeUmLado():
    curva = _bezier((1, 0.2), (0.5, 0.46), (0, 0.2))
    return [(0, 0), (1, 0)] + curva, [curva]


def _cidadeCanto():
    curva = _bezier((1, 0), (0.58, 0.58), (0, 1))
    return [(0, 0)] + curva, [curva]


def _cidadeFaixa():
    cima = _bezier((0, 0), (0.5, 0.5), (1, 0))
    baixo = _bezier((1, 1), (0.5, 0.5), (0, 1))
    return cima + baixo, [cima, baixo]


def _cidadeTresLados():
    curva = _bezier((1, 1), (0.5, 0.42), (0, 1))
    return [(0, 0), (1, 0)] + curva, [curva]


def _cidadeInteira():
    return [(0, 0), (1, 0), (1, 1), (0, 1)], []


FORMAS_CANONICAS = (
    (("NORTE",), _cidadeUmLado),
    (("NORTE", "OESTE"), _cidadeCanto),
    (("LESTE", "OESTE"), _cidadeFaixa),
    (("NORTE", "LESTE", "OESTE"), _cidadeTresLados),
    (ORDEM_LADOS, _cidadeInteira),
)


def _girarLado(nome, quartos):
    return ORDEM_LADOS[(ORDEM_LADOS.index(nome) + quartos) % len(ORDEM_LADOS)]


def _girarPonto(ponto, quartos):
    u, v = ponto
    for _ in range(quartos % 4):
        u, v = 1 - v, u
    return u, v


def _formaDaCidade(lados):
    for canonicos, criarForma in FORMAS_CANONICAS:
        for quartos in range(4):
            if {_girarLado(lado, quartos) for lado in canonicos} == set(lados):
                poligono, muralhas = criarForma()
                girar = lambda pontos: [_girarPonto(p, quartos) for p in pontos]
                return girar(poligono), [girar(muralha) for muralha in muralhas]
    raise ValueError(f"Forma de cidade desconhecida: {lados}")


def _dentro(ponto, poligono):
    x, y = ponto
    dentro = False
    j = len(poligono) - 1
    for i, (xi, yi) in enumerate(poligono):
        xj, yj = poligono[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            dentro = not dentro
        j = i
    return dentro


def _partesDaPeca(peca, rotacao):
    quartos = rotacao // GRAUS_POR_QUARTO
    return [
        (
            type(segmento.territorio).__name__,
            [_girarLado(posicao.name, quartos) for posicao in segmento.posicoes],
            getattr(segmento.territorio, "escudos", 0),
        )
        for segmento in peca.segmentos
    ]


def desenharPeca(peca, rotacao, tamanho):
    chave = (peca.tipo, rotacao, tamanho)
    if chave not in _cachePecas:
        _cachePecas[chave] = _renderizarPeca(_partesDaPeca(peca, rotacao), tamanho)
    return _cachePecas[chave]


def _renderizarPeca(partes, tamanho):
    lado = tamanho * SUPERAMOSTRAGEM
    superficie = pygame.Surface((lado, lado))
    superficie.fill(CAMPO)
    escala = lambda ponto: (ponto[0] * lado, ponto[1] * lado)
    for ponto in TUFOS_DE_GRAMA:
        _desenharTufo(superficie, escala(ponto), lado)
    estradas = [lados for nome, lados, _ in partes if nome == "Estrada"]
    for lados in estradas:
        _desenharEstrada(superficie, [escala(p) for p in _caminhoDaEstrada(lados)], lado)
    if len(estradas) >= 3:
        _desenharCasa(superficie, escala(CENTRO), lado * 0.13)
    for nome, lados, escudos in partes:
        if nome == "Cidade":
            _desenharCidade(superficie, lados, escudos, lado, escala)
    if any(nome == "Monasterio" for nome, _, _ in partes):
        _desenharMonasterio(superficie, lado, escala)
    pygame.draw.rect(superficie, BORDA_PECA, (0, 0, lado, lado), max(2, int(lado * 0.014)))
    return pygame.transform.smoothscale(superficie, (tamanho, tamanho))


def _desenharTufo(superficie, centro, lado):
    largura = lado * 0.07
    caixa = pygame.Rect(0, 0, largura, largura * 0.6)
    caixa.center = centro
    pygame.draw.arc(superficie, GRAMA, caixa, 0.5, 2.64, max(2, int(lado * 0.008)))


def _caminhoDaEstrada(lados):
    if len(lados) == 1:
        return [MEIO_DO_LADO[lados[0]], CENTRO]
    inicio, fim = MEIO_DO_LADO[lados[0]], MEIO_DO_LADO[lados[1]]
    opostos = _girarLado(lados[0], 2) == lados[1]
    return [inicio, fim] if opostos else _bezier(inicio, CENTRO, fim)


def _desenharEstrada(superficie, pontos, lado):
    for cor, largura in ((BORDA_ESTRADA, lado * 0.12), (ESTRADA, lado * 0.085)):
        pygame.draw.lines(superficie, cor, False, pontos, int(largura))
        for ponto in pontos:
            pygame.draw.circle(superficie, cor, ponto, largura / 2)


def _desenharCidade(superficie, lados, escudos, lado, escala):
    poligono, muralhas = _formaDaCidade(lados)
    pygame.draw.polygon(superficie, CIDADE, [escala(p) for p in poligono])
    for muralha in muralhas:
        pygame.draw.lines(superficie, MURALHA, False, [escala(p) for p in muralha], max(3, int(lado * 0.03)))
    candidatos = [
        (x, y) for y, xs in LINHAS_DE_CASAS for x in xs
        if all(_dentro((x + dx, y + dy), poligono) for dx, dy in ((-0.07, -0.07), (0.07, -0.07), (-0.07, 0.07), (0.07, 0.07)))
    ]
    casas = candidatos[:CASAS_POR_CIDADE]
    for ponto in casas:
        _desenharCasa(superficie, escala(ponto), lado * 0.11)
    if escudos:
        sobra = candidatos[CASAS_POR_CIDADE:] or candidatos[-1:] or [poligono[0]]
        _desenharEscudo(superficie, escala(sobra[0]), lado * 0.1)


def _desenharCasa(superficie, centro, largura):
    cx, cy = centro
    corpo = pygame.Rect(0, 0, largura, largura * 0.8)
    corpo.midtop = (cx, cy - largura * 0.15)
    telhado = [(corpo.left - largura * 0.08, corpo.top), (cx, corpo.top - largura * 0.5), (corpo.right + largura * 0.08, corpo.top)]
    contorno = max(2, int(largura * 0.08))
    pygame.draw.rect(superficie, CASA, corpo)
    pygame.draw.rect(superficie, CONTORNO_CASA, corpo, contorno)
    pygame.draw.polygon(superficie, TELHADO, telhado)
    pygame.draw.polygon(superficie, CONTORNO_CASA, telhado, contorno)


def _desenharEscudo(superficie, centro, largura):
    cx, cy = centro
    pontos = [
        (cx - largura / 2, cy - largura / 2), (cx + largura / 2, cy - largura / 2),
        (cx + largura / 2, cy + largura * 0.1), (cx, cy + largura * 0.6), (cx - largura / 2, cy + largura * 0.1),
    ]
    pygame.draw.polygon(superficie, ESCUDO, pontos)
    pygame.draw.line(superficie, ESCUDO_FAIXA, (cx, cy - largura / 2), (cx, cy + largura * 0.55), max(2, int(largura * 0.14)))
    pygame.draw.polygon(superficie, CONTORNO_CASA, pontos, max(2, int(largura * 0.08)))


def _desenharMonasterio(superficie, lado, escala):
    corpo = pygame.Rect(escala((0.32, 0.44)), (lado * 0.36, lado * 0.28))
    telhado = [escala((0.27, 0.45)), escala((0.5, 0.28)), escala((0.73, 0.45))]
    contorno = max(2, int(lado * 0.012))
    pygame.draw.rect(superficie, MONASTERIO, corpo)
    pygame.draw.rect(superficie, CONTORNO_CASA, corpo, contorno)
    pygame.draw.polygon(superficie, TELHADO_MONASTERIO, telhado)
    pygame.draw.polygon(superficie, CONTORNO_CASA, telhado, contorno)
    porta = pygame.Rect(0, 0, lado * 0.07, lado * 0.12)
    porta.midbottom = corpo.midbottom
    pygame.draw.rect(superficie, PORTA, porta)
    topo = escala((0.5, 0.28))
    pygame.draw.line(superficie, CONTORNO_CASA, topo, (topo[0], topo[1] - lado * 0.08), contorno + 1)
    pygame.draw.line(superficie, CONTORNO_CASA, (topo[0] - lado * 0.025, topo[1] - lado * 0.055),
                     (topo[0] + lado * 0.025, topo[1] - lado * 0.055), contorno + 1)


def pontoDoSegmento(segmento):
    lados = [lado.name for lado in segmento.ladosOcupados()]
    if not lados or len(lados) == len(ORDEM_LADOS):
        return CENTRO
    u = sum(PONTO_DO_MEEPLE_NO_LADO[lado][0] for lado in lados) / len(lados)
    v = sum(PONTO_DO_MEEPLE_NO_LADO[lado][1] for lado in lados) / len(lados)
    return u, v


def desenharMeeple(cor, tamanho):
    chave = (cor, tamanho)
    if chave not in _cacheMeeples:
        _cacheMeeples[chave] = _renderizarMeeple(cor, tamanho)
    return _cacheMeeples[chave]


def _renderizarMeeple(cor, tamanho):
    lado = tamanho * 4
    superficie = pygame.Surface((lado, lado), pygame.SRCALPHA)
    corpo = [(x * lado * 0.9 + lado * 0.05, y * lado * 0.88 + lado * 0.08) for x, y in SILHUETA_MEEPLE]
    cabeca = (lado * 0.5, lado * 0.2)
    raio = lado * 0.14
    borda = lado * 0.05
    pygame.draw.polygon(superficie, CONTORNO_MEEPLE, corpo, int(borda * 2))
    pygame.draw.circle(superficie, CONTORNO_MEEPLE, cabeca, raio + borda)
    pygame.draw.polygon(superficie, cor, corpo)
    pygame.draw.circle(superficie, cor, cabeca, raio)
    return pygame.transform.smoothscale(superficie, (tamanho, tamanho))
