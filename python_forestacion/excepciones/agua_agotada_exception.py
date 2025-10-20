from python_forestacion.excepciones.forestacion_exception import ForestacionException
from python_forestacion.excepciones.mensajes_exception import MensajesException

class AguaAgotadaException(ForestacionException):
    """Excepcion lanzada cuando no hay suficiente agua."""

    def __init__(self, agua_requerida: int, agua_disponible: int):
        user_message = MensajesException.AGUA_AGOTADA_USER
        technical_message = MensajesException.AGUA_AGOTADA_TECH.format(
            requerida=agua_requerida,
            disponible=agua_disponible
        )
        super().__init__(user_message, technical_message)
        self._agua_requerida = agua_requerida
        self._agua_disponible = agua_disponible

    def get_agua_requerida(self) -> int:
        return self._agua_requerida

    def get_agua_disponible(self) -> int:
        return self._agua_disponible
