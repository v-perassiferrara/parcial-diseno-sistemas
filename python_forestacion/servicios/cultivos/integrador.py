"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 8
"""

# ================================================================================
# ARCHIVO 1/8: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/8: arbol_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\arbol_service.py
# ================================================================================

from typing import TYPE_CHECKING
from python_forestacion.servicios.cultivos.cultivo_service import CultivoService

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.arbol import Arbol

class ArbolService(CultivoService):
    """Servicio base para la gestion de arboles."""

    def mostrar_datos(self, cultivo: 'Arbol') -> None:
        super().mostrar_datos(cultivo)
        print(f"Altura: {cultivo.get_altura()} m")


# ================================================================================
# ARCHIVO 3/8: cultivo_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\cultivo_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/8: cultivo_service_registry.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\cultivo_service_registry.py
# ================================================================================

# Standard library
from threading import Lock
from typing import Dict, Type, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    # Local application
    from python_forestacion.entidades.cultivos.cultivo import Cultivo
    from python_forestacion.entidades.cultivos.pino import Pino
    from python_forestacion.entidades.cultivos.olivo import Olivo
    from python_forestacion.entidades.cultivos.lechuga import Lechuga
    from python_forestacion.entidades.cultivos.zanahoria import Zanahoria
    from python_forestacion.servicios.cultivos.pino_service import PinoService
    from python_forestacion.servicios.cultivos.olivo_service import OlivoService
    from python_forestacion.servicios.cultivos.lechuga_service import LechugaService
    from python_forestacion.servicios.cultivos.zanahoria_service import ZanahoriaService


class CultivoServiceRegistry:
    """Registro de servicios de cultivo (Singleton y Registry).

    Esta clase sigue el patrón Singleton para garantizar una única instancia
    y el patrón Registry para mapear tipos de cultivo a sus servicios
    correspondientes, desacoplando la lógica de invocación.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._inicializar_servicios()
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Obtiene la instancia única del registro.

        Returns:
            CultivoServiceRegistry: La instancia única de la clase.
        """
        if cls._instance is None:
            cls()
        return cls._instance

    def _inicializar_servicios(self):
        from python_forestacion.entidades.cultivos.pino import Pino
        from python_forestacion.entidades.cultivos.olivo import Olivo
        from python_forestacion.entidades.cultivos.lechuga import Lechuga
        from python_forestacion.entidades.cultivos.zanahoria import Zanahoria
        from python_forestacion.servicios.cultivos.pino_service import PinoService
        from python_forestacion.servicios.cultivos.olivo_service import OlivoService
        from python_forestacion.servicios.cultivos.lechuga_service import LechugaService
        from python_forestacion.servicios.cultivos.zanahoria_service import ZanahoriaService
        from python_forestacion.patrones.strategy.impl.absorcion_seasonal_strategy import AbsorcionSeasonalStrategy
        from python_forestacion.patrones.strategy.impl.absorcion_constante_strategy import AbsorcionConstanteStrategy
        from python_forestacion.constantes import ABSORCION_CONSTANTE_LECHUGA, ABSORCION_CONSTANTE_ZANAHORIA

        # Instanciar estrategias
        estrategia_arbol = AbsorcionSeasonalStrategy()
        estrategia_lechuga = AbsorcionConstanteStrategy(ABSORCION_CONSTANTE_LECHUGA)
        estrategia_zanahoria = AbsorcionConstanteStrategy(ABSORCION_CONSTANTE_ZANAHORIA)

        # Inyectar estrategias en servicios
        self._pino_service: 'PinoService' = PinoService(estrategia_arbol)
        self._olivo_service: 'OlivoService' = OlivoService(estrategia_arbol)
        self._lechuga_service: 'LechugaService' = LechugaService(estrategia_lechuga)
        self._zanahoria_service: 'ZanahoriaService' = ZanahoriaService(estrategia_zanahoria)

        self._absorber_agua_handlers: Dict[Type['Cultivo'], Callable[['Cultivo'], int]] = {
            Pino: self._absorber_agua_pino,
            Olivo: self._absorber_agua_olivo,
            Lechuga: self._absorber_agua_lechuga,
            Zanahoria: self._absorber_agua_zanahoria
        }

        self._mostrar_datos_handlers: Dict[Type['Cultivo'], Callable[['Cultivo'], None]] = {
            Pino: self._mostrar_datos_pino,
            Olivo: self._mostrar_datos_olivo,
            Lechuga: self._mostrar_datos_lechuga,
            Zanahoria: self._mostrar_datos_zanahoria
        }

    def absorber_agua(self, cultivo: 'Cultivo') -> int:
        handler = self._absorber_agua_handlers.get(type(cultivo))
        if not handler:
            raise ValueError(f"No hay handler de absorcion para {type(cultivo).__name__}")
        return handler(cultivo)

    def mostrar_datos(self, cultivo: 'Cultivo') -> None:
        handler = self._mostrar_datos_handlers.get(type(cultivo))
        if not handler:
            raise ValueError(f"No hay handler de mostrar_datos para {type(cultivo).__name__}")
        handler(cultivo)

    # Handlers para absorber agua
    def _absorber_agua_pino(self, cultivo: 'Pino') -> int:
        return self._pino_service.absorber_agua(cultivo)

    def _absorber_agua_olivo(self, cultivo: 'Olivo') -> int:
        return self._olivo_service.absorber_agua(cultivo)

    def _absorber_agua_lechuga(self, cultivo: 'Lechuga') -> int:
        return self._lechuga_service.absorber_agua(cultivo)

    def _absorber_agua_zanahoria(self, cultivo: 'Zanahoria') -> int:
        return self._zanahoria_service.absorber_agua(cultivo)

    # Handlers para mostrar datos
    def _mostrar_datos_pino(self, cultivo: 'Pino') -> None:
        self._pino_service.mostrar_datos(cultivo)

    def _mostrar_datos_olivo(self, cultivo: 'Olivo') -> None:
        self._olivo_service.mostrar_datos(cultivo)

    def _mostrar_datos_lechuga(self, cultivo: 'Lechuga') -> None:
        self._lechuga_service.mostrar_datos(cultivo)

    def _mostrar_datos_zanahoria(self, cultivo: 'Zanahoria') -> None:
        self._zanahoria_service.mostrar_datos(cultivo)


# ================================================================================
# ARCHIVO 5/8: lechuga_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\lechuga_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 6/8: olivo_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\olivo_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 7/8: pino_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\pino_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 8/8: zanahoria_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\zanahoria_service.py
# ================================================================================

# Standard library
from typing import TYPE_CHECKING

# Local application
from python_forestacion.servicios.cultivos.cultivo_service import CultivoService
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.zanahoria import Zanahoria


class ZanahoriaService(CultivoService):
    """Servicio específico para la gestión de Zanahorias."""

    def __init__(self, estrategia_absorcion: AbsorcionAguaStrategy):
        """Inicializa el servicio de Zanahoria.

        Args:
            estrategia_absorcion (AbsorcionAguaStrategy): La estrategia a usar para
                el cálculo de absorción de agua.
        """
        super().__init__(estrategia_absorcion)

    def mostrar_datos(self, cultivo: 'Zanahoria') -> None:
        """Muestra los datos específicos de una Zanahoria.

        Args:
            cultivo (Zanahoria): La zanahoria de la que se mostrarán los datos.
        """
        super().mostrar_datos(cultivo)
        print(f"Es baby carrot: {cultivo.is_baby_carrot()}")


