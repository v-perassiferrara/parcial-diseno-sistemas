from python_forestacion.excepciones.forestacion_exception import ForestacionException
from python_forestacion.excepciones.mensajes_exception import MensajesException

class SuperficieInsuficienteException(ForestacionException):
    """Excepcion lanzada cuando no hay suficiente superficie."""

    def __init__(self, superficie_requerida: float, superficie_disponible: float):
        user_message = MensajesException.SUPERFICIE_INSUFICIENTE_USER
        technical_message = MensajesException.SUPERFICIE_INSUFICIENTE_TECH.format(
            requerida=superficie_requerida,
            disponible=superficie_disponible
        )
        super().__init__(user_message, technical_message)
        self._superficie_requerida = superficie_requerida
        self._superficie_disponible = superficie_disponible

    def get_superficie_requerida(self) -> float:
        return self._superficie_requerida

    def get_superficie_disponible(self) -> float:
        return self._superficie_disponible
