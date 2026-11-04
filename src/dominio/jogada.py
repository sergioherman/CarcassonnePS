from dataclasses import dataclass


@dataclass(frozen=True)
class Jogada:
    posicaoX: int
    posicaoY: int
    rotacao: int
