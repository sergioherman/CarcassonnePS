class Meeple:
    def __init__(self, dono):
        self.dono = dono
        self._segmento = None

    @property
    def segmento(self):
        return self._segmento

    @segmento.setter
    def segmento(self, novo):
        if self._segmento is not None:
            self._segmento.meeple = None
        self._segmento = novo
        if novo is not None:
            novo.meeple = self
