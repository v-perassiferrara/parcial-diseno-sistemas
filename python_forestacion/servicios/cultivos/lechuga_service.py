# Standard library
from typing import TYPE_CHECKING

# Local application
from python_forestacion.servicios.cultivos.cultivo_service import CultivoService
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.lechuga import Lechuga


class LechugaService(CultivoService):
    """Servicio específico para la gestión de Lechugas."""

    def __init__(self, estrategia_absorcion: AbsorcionAguaStrategy):
        """Inicializa el servicio de Lechuga.

        Args:
            estrategia_absorcion (AbsorcionAguaStrategy): La estrategia a usar para
                el cálculo de absorción de agua.
        """
        super().__init__(estrategia_absorcion)

    def mostrar_datos(self, cultivo: 'Lechuga') -> None:
        """Muestra los datos específicos de una Lechuga.

        Args:
            cultivo (Lechuga): La lechuga de la que se mostrarán los datos.
        """
        super().mostrar_datos(cultivo)
        print(f"Variedad: {cultivo.get_variedad()}")
        print(f"Invernadero: {cultivo.is_invernadero()}")
