# Standard library
from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING

# Local application
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo


class CultivoService(ABC):
    """Servicio base abstracto para la gestión de cultivos.

    Esta clase utiliza el patrón Strategy para delegar el algoritmo
    de absorción de agua.
    """

    def __init__(self, estrategia_absorcion: AbsorcionAguaStrategy):
        """Inicializa el servicio de cultivo.

        Args:
            estrategia_absorcion (AbsorcionAguaStrategy): La estrategia a usar para
                el cálculo de absorción de agua. Así, la clase CultivoService es la que hace de "contexto" en el patrón
        """
        self._estrategia_absorcion = estrategia_absorcion

    def absorber_agua(self, cultivo: 'Cultivo') -> int:
        """Delega el cálculo de absorción de agua a la estrategia y actualiza el cultivo.

        Args:
            cultivo (Cultivo): El cultivo que absorberá agua.

        Returns:
            int: La cantidad de agua absorbida.
        """
        # Logica de absorcion delegada a la estrategia
        agua_absorbida = self._estrategia_absorcion.calcular_absorcion(
            fecha=date.today(),
            temperatura=0,  # Estos valores podrian venir de sensores
            humedad=0,
            cultivo=cultivo
        )
        cultivo.set_agua(cultivo.get_agua() + agua_absorbida)
        return agua_absorbida

    def mostrar_datos(self, cultivo: 'Cultivo') -> None:
        """Muestra los datos básicos y comunes de cualquier cultivo.

        Args:
            cultivo (Cultivo): El cultivo del que se mostrarán los datos.
        """
        print(f"Cultivo: {type(cultivo).__name__}")
        print(f"Superficie: {cultivo.get_superficie()} m²")
        print(f"Agua almacenada: {cultivo.get_agua()} L")
