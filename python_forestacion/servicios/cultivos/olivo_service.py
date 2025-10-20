# Standard library
from typing import TYPE_CHECKING

# Local application
from python_forestacion.servicios.cultivos.arbol_service import ArbolService
from python_forestacion.constantes import CRECIMIENTO_OLIVO
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.olivo import Olivo


class OlivoService(ArbolService):
    """Servicio específico para la gestión de Olivos."""

    def __init__(self, estrategia_absorcion: AbsorcionAguaStrategy):
        """Inicializa el servicio de Olivo.

        Args:
            estrategia_absorcion (AbsorcionAguaStrategy): La estrategia a usar para
                el cálculo de absorción de agua.
        """
        super().__init__(estrategia_absorcion)

    def absorber_agua(self, cultivo: 'Olivo') -> int:
        """Aplica la lógica de absorción de agua y crecimiento para un Olivo.

        Args:
            cultivo (Olivo): El olivo que absorberá agua.

        Returns:
            int: La cantidad de agua absorbida.
        """
        agua_absorbida = super().absorber_agua(cultivo)
        cultivo.set_altura(cultivo.get_altura() + CRECIMIENTO_OLIVO)
        return agua_absorbida

    def mostrar_datos(self, cultivo: 'Olivo') -> None:
        """Muestra los datos específicos de un Olivo.

        Args:
            cultivo (Olivo): El olivo del que se mostrarán los datos.
        """
        super().mostrar_datos(cultivo)
        print(f"Tipo de aceituna: {cultivo.get_tipo_aceituna().value}")
