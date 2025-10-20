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
