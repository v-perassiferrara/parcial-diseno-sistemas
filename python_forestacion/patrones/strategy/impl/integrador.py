"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\impl
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\impl\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: absorcion_constante_strategy.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\impl\absorcion_constante_strategy.py
# ================================================================================

from datetime import date
from typing import TYPE_CHECKING
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo

class AbsorcionConstanteStrategy(AbsorcionAguaStrategy):
    """Estrategia de absorcion de agua constante."""

    def __init__(self, cantidad_constante: int):
        self._cantidad = cantidad_constante

    def calcular_absorcion(self, fecha: date, temperatura: float, humedad: float, cultivo: 'Cultivo') -> int:
        return self._cantidad


# ================================================================================
# ARCHIVO 3/3: absorcion_seasonal_strategy.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\impl\absorcion_seasonal_strategy.py
# ================================================================================

from datetime import date
from typing import TYPE_CHECKING
from python_forestacion.patrones.strategy.absorcion_agua_strategy import AbsorcionAguaStrategy
from python_forestacion.constantes import MES_INICIO_VERANO, MES_FIN_VERANO, ABSORCION_SEASONAL_VERANO, ABSORCION_SEASONAL_INVIERNO

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo

class AbsorcionSeasonalStrategy(AbsorcionAguaStrategy):
    """Estrategia de absorcion de agua estacional."""

    def calcular_absorcion(self, fecha: date, temperatura: float, humedad: float, cultivo: 'Cultivo') -> int:
        mes = fecha.month
        if MES_INICIO_VERANO <= mes <= MES_FIN_VERANO:
            return ABSORCION_SEASONAL_VERANO
        else:
            return ABSORCION_SEASONAL_INVIERNO


