# Standard library
from typing import TYPE_CHECKING

# Local application
from python_forestacion.servicios.cultivos.arbol_service import ArbolService
from python_forestacion.constantes import CRECIMIENTO_PINO
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.pino import Pino


class PinoService(ArbolService):
    """Servicio específico para la gestión de Pinos."""

    def __init__(self, estrategia_absorcion: AbsorcionAguaStrategy):
        """Inicializa el servicio de Pino.

        Args:
            estrategia_absorcion (AbsorcionAguaStrategy): La estrategia a usar para
                el cálculo de absorción de agua.
        """
        super().__init__(estrategia_absorcion)

    def absorber_agua(self, cultivo: 'Pino') -> int:
        """Aplica la lógica de absorción de agua y crecimiento para un Pino.

        Args:
            cultivo (Pino): El pino que absorberá agua.

        Returns:
            int: La cantidad de agua absorbida.
        """
        agua_absorbida = super().absorber_agua(cultivo)
        cultivo.set_altura(cultivo.get_altura() + CRECIMIENTO_PINO)
        return agua_absorbida

    def mostrar_datos(self, cultivo: 'Pino') -> None:
        """Muestra los datos específicos de un Pino.

        Args:
            cultivo (Pino): El pino del que se mostrarán los datos.
        """
        super().mostrar_datos(cultivo)
        print(f"Variedad: {cultivo.get_variedad()}")
