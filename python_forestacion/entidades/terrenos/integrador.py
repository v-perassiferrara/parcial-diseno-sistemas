"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: plantacion.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos\plantacion.py
# ================================================================================

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo
    from python_forestacion.entidades.personal.trabajador import Trabajador

class Plantacion:
    """Entidad Plantacion - representa una finca agricola."""

    def __init__(self, nombre: str, superficie: float, agua: int):
        self._nombre = nombre
        self._superficie = superficie
        self._agua_disponible = agua
        self._cultivos: List['Cultivo'] = []
        self._trabajadores: List['Trabajador'] = []

    def get_nombre(self) -> str:
        return self._nombre

    def set_nombre(self, nombre: str) -> None:
        self._nombre = nombre

    def get_superficie(self) -> float:
        return self._superficie

    def set_superficie(self, superficie: float) -> None:
        self._superficie = superficie

    def get_agua_disponible(self) -> int:
        return self._agua_disponible

    def set_agua_disponible(self, agua: int) -> None:
        if agua < 0:
            raise ValueError("El agua no puede ser negativa")
        self._agua_disponible = agua

    def get_cultivos(self) -> List['Cultivo']:
        return self._cultivos.copy()  # Defensive copy

    def get_cultivos_interno(self) -> List['Cultivo']:
        return self._cultivos # Internal use only

    def set_cultivos(self, cultivos: List['Cultivo']) -> None:
        self._cultivos = cultivos

    def get_trabajadores(self) -> List['Trabajador']:
        return self._trabajadores.copy()  # Defensive copy

    def set_trabajadores(self, trabajadores: List['Trabajador']) -> None:
        self._trabajadores = trabajadores


# ================================================================================
# ARCHIVO 3/4: registro_forestal.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos\registro_forestal.py
# ================================================================================

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.tierra import Tierra
    from python_forestacion.entidades.terrenos.plantacion import Plantacion

class RegistroForestal:
    """Entidad que agrupa toda la informacion de una finca."""

    def __init__(self, id_padron: int, tierra: 'Tierra', plantacion: 'Plantacion', propietario: str, avaluo: float):
        self._id_padron = id_padron
        self._tierra = tierra
        self._plantacion = plantacion
        self._propietario = propietario
        self._avaluo = avaluo

    def get_id_padron(self) -> int:
        return self._id_padron

    def get_tierra(self) -> 'Tierra':
        return self._tierra

    def get_plantacion(self) -> 'Plantacion':
        return self._plantacion

    def get_propietario(self) -> str:
        return self._propietario

    def get_avaluo(self) -> float:
        return self._avaluo


# ================================================================================
# ARCHIVO 4/4: tierra.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos\tierra.py
# ================================================================================

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.plantacion import Plantacion

class Tierra:
    """Entidad Tierra - representa un terreno catastral."""

    def __init__(self, id_padron_catastral: int, superficie: float, domicilio: str):
        self._id_padron_catastral = id_padron_catastral
        self._superficie = superficie
        self._domicilio = domicilio
        self._finca: 'Plantacion' = None  # Forward reference

    def get_id_padron_catastral(self) -> int:
        return self._id_padron_catastral

    def set_id_padron_catastral(self, id_padron_catastral: int) -> None:
        self._id_padron_catastral = id_padron_catastral

    def get_superficie(self) -> float:
        return self._superficie

    def set_superficie(self, superficie: float) -> None:
        if superficie < 0:
            raise ValueError("La superficie debe ser mayor a cero")
        self._superficie = superficie

    def get_domicilio(self) -> str:
        return self._domicilio

    def set_domicilio(self, domicilio: str) -> None:
        self._domicilio = domicilio

    def get_finca(self) -> 'Plantacion':
        return self._finca

    def set_finca(self, finca: 'Plantacion') -> None:
        self._finca = finca


