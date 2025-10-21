"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: absorcion_agua_strategy.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\absorcion_agua_strategy.py
# ================================================================================

from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo

class AbsorcionAguaStrategy(ABC):
    """Interfaz para las estrategias de absorcion de agua."""

    @abstractmethod
    def calcular_absorcion(
        self,
        fecha: date,
        temperatura: float,
        humedad: float,
        cultivo: 'Cultivo'
    ) -> int:
        pass


