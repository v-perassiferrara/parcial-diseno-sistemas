# Standard library
from abc import ABC

# Local application
from python_forestacion.servicios.cultivos.cultivo_service import CultivoService


class HortalizaService(CultivoService, ABC):
    """Servicio base para la gestión de hortalizas."""
    pass
