"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 6
"""

# ================================================================================
# ARCHIVO 1/6: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/6: agua_agotada_exception.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\agua_agotada_exception.py
# ================================================================================

from python_forestacion.excepciones.forestacion_exception import ForestacionException
from python_forestacion.excepciones.mensajes_exception import MensajesException

class AguaAgotadaException(ForestacionException):
    """Excepcion lanzada cuando no hay suficiente agua."""

    def __init__(self, agua_requerida: int, agua_disponible: int):
        user_message = MensajesException.AGUA_AGOTADA_USER
        technical_message = MensajesException.AGUA_AGOTADA_TECH.format(
            requerida=agua_requerida,
            disponible=agua_disponible
        )
        super().__init__(user_message, technical_message)
        self._agua_requerida = agua_requerida
        self._agua_disponible = agua_disponible

    def get_agua_requerida(self) -> int:
        return self._agua_requerida

    def get_agua_disponible(self) -> int:
        return self._agua_disponible


# ================================================================================
# ARCHIVO 3/6: forestacion_exception.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\forestacion_exception.py
# ================================================================================

class ForestacionException(Exception):
    """Clase base para excepciones del sistema de forestacion."""

    def __init__(self, user_message: str, technical_message: str):
        super().__init__(f"{user_message} ({technical_message})")
        self._user_message = user_message
        self._technical_message = technical_message

    def get_user_message(self) -> str:
        return self._user_message

    def get_technical_message(self) -> str:
        return self._technical_message

    def get_full_message(self) -> str:
        return f"Error: {self._user_message}\nDetalles: {self._technical_message}"


# ================================================================================
# ARCHIVO 4/6: mensajes_exception.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\mensajes_exception.py
# ================================================================================

class MensajesException:
    """Clase que centraliza los mensajes de error del sistema."""

    # Superficie
    SUPERFICIE_INSUFICIENTE_USER = "No hay suficiente superficie disponible en la plantacion."
    SUPERFICIE_INSUFICIENTE_TECH = "La superficie requerida ({requerida} m²) es mayor que la disponible ({disponible} m²)."

    # Agua
    AGUA_AGOTADA_USER = "No hay suficiente agua en la plantacion para regar."
    AGUA_AGOTADA_TECH = "Se requieren {requerida} L de agua, pero solo hay {disponible} L disponibles."

    # Persistencia
    PERSISTENCIA_ESCRITURA_USER = "Ocurrio un error al intentar guardar el registro."
    PERSISTENCIA_ESCRITURA_TECH = "Error de I/O al escribir en el archivo: {archivo}."
    PERSISTENCIA_LECTURA_USER = "Ocurrio un error al intentar leer el registro."
    PERSISTENCIA_LECTURA_TECH = "Error de I/O al leer el archivo: {archivo}."
    PERSISTENCIA_NOT_FOUND_USER = "No se encontro el registro solicitado."
    PERSISTENCIA_NOT_FOUND_TECH = "El archivo de datos no existe: {archivo}."
    PERSISTENCIA_CORRUPTO_USER = "El archivo de registro parece estar corrupto."
    PERSISTENCIA_CORRUPTO_TECH = "Error de deserializacion (pickle) en el archivo: {archivo}."


# ================================================================================
# ARCHIVO 5/6: persistencia_exception.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\persistencia_exception.py
# ================================================================================

from enum import Enum
from python_forestacion.excepciones.forestacion_exception import ForestacionException

class TipoOperacion(Enum):
    LECTURA = "lectura"
    ESCRITURA = "escritura"

class PersistenciaException(ForestacionException):
    """Excepcion lanzada por errores de persistencia."""

    def __init__(self, user_message: str, technical_message: str, nombre_archivo: str, tipo_operacion: TipoOperacion):
        super().__init__(user_message, technical_message)
        self._nombre_archivo = nombre_archivo
        self._tipo_operacion = tipo_operacion

    def get_nombre_archivo(self) -> str:
        return self._nombre_archivo

    def get_tipo_operacion(self) -> TipoOperacion:
        return self._tipo_operacion


# ================================================================================
# ARCHIVO 6/6: superficie_insuficiente_exception.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\superficie_insuficiente_exception.py
# ================================================================================

from python_forestacion.excepciones.forestacion_exception import ForestacionException
from python_forestacion.excepciones.mensajes_exception import MensajesException

class SuperficieInsuficienteException(ForestacionException):
    """Excepcion lanzada cuando no hay suficiente superficie."""

    def __init__(self, superficie_requerida: float, superficie_disponible: float):
        user_message = MensajesException.SUPERFICIE_INSUFICIENTE_USER
        technical_message = MensajesException.SUPERFICIE_INSUFICIENTE_TECH.format(
            requerida=superficie_requerida,
            disponible=superficie_disponible
        )
        super().__init__(user_message, technical_message)
        self._superficie_requerida = superficie_requerida
        self._superficie_disponible = superficie_disponible

    def get_superficie_requerida(self) -> float:
        return self._superficie_requerida

    def get_superficie_disponible(self) -> float:
        return self._superficie_disponible


