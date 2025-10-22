"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion
Fecha de generacion: 2025-10-21 19:58:16
Total de archivos integrados: 67
Total de directorios procesados: 22
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: ..
#   1. main.py
#
# DIRECTORIO: .
#   2. __init__.py
#   3. constantes.py
#
# DIRECTORIO: entidades
#   4. __init__.py
#
# DIRECTORIO: entidades\cultivos
#   5. __init__.py
#   6. arbol.py
#   7. cultivo.py
#   8. hortaliza.py
#   9. lechuga.py
#   10. olivo.py
#   11. pino.py
#   12. tipo_aceituna.py
#   13. zanahoria.py
#
# DIRECTORIO: entidades\personal
#   14. __init__.py
#   15. apto_medico.py
#   16. herramienta.py
#   17. tarea.py
#   18. trabajador.py
#
# DIRECTORIO: entidades\terrenos
#   19. __init__.py
#   20. plantacion.py
#   21. registro_forestal.py
#   22. tierra.py
#
# DIRECTORIO: excepciones
#   23. __init__.py
#   24. agua_agotada_exception.py
#   25. forestacion_exception.py
#   26. mensajes_exception.py
#   27. persistencia_exception.py
#   28. superficie_insuficiente_exception.py
#
# DIRECTORIO: patrones
#   29. __init__.py
#
# DIRECTORIO: patrones\factory
#   30. __init__.py
#   31. cultivo_factory.py
#
# DIRECTORIO: patrones\observer
#   32. __init__.py
#   33. observable.py
#   34. observer.py
#
# DIRECTORIO: patrones\observer\eventos
#   35. __init__.py
#   36. evento_plantacion.py
#   37. evento_sensor.py
#
# DIRECTORIO: patrones\singleton
#   38. __init__.py
#
# DIRECTORIO: patrones\strategy
#   39. __init__.py
#   40. absorcion_agua_strategy.py
#
# DIRECTORIO: patrones\strategy\impl
#   41. __init__.py
#   42. absorcion_constante_strategy.py
#   43. absorcion_seasonal_strategy.py
#
# DIRECTORIO: riego
#   44. __init__.py
#
# DIRECTORIO: riego\control
#   45. __init__.py
#   46. control_riego_task.py
#
# DIRECTORIO: riego\sensores
#   47. __init__.py
#   48. humedad_reader_task.py
#   49. temperatura_reader_task.py
#
# DIRECTORIO: servicios
#   50. __init__.py
#
# DIRECTORIO: servicios\cultivos
#   51. __init__.py
#   52. arbol_service.py
#   53. cultivo_service.py
#   54. cultivo_service_registry.py
#   55. lechuga_service.py
#   56. olivo_service.py
#   57. pino_service.py
#   58. zanahoria_service.py
#
# DIRECTORIO: servicios\negocio
#   59. __init__.py
#   60. fincas_service.py
#   61. paquete.py
#
# DIRECTORIO: servicios\personal
#   62. __init__.py
#   63. trabajador_service.py
#
# DIRECTORIO: servicios\terrenos
#   64. __init__.py
#   65. plantacion_service.py
#   66. registro_forestal_service.py
#   67. tierra_service.py
#



################################################################################
# DIRECTORIO: ..
################################################################################

# ==============================================================================
# ARCHIVO 1/67: main.py
# Directorio: .
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\main.py
# ==============================================================================


import time
from datetime import date

# Importaciones de entidades
from python_forestacion.entidades.personal.trabajador import Trabajador
from python_forestacion.entidades.personal.tarea import Tarea
from python_forestacion.entidades.personal.herramienta import Herramienta
from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal
from python_forestacion.entidades.cultivos.pino import Pino
from python_forestacion.entidades.cultivos.lechuga import Lechuga

# Importaciones de servicios
from python_forestacion.servicios.terrenos.tierra_service import TierraService
from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService
from python_forestacion.servicios.terrenos.registro_forestal_service import RegistroForestalService
from python_forestacion.servicios.personal.trabajador_service import TrabajadorService
from python_forestacion.servicios.negocio.fincas_service import FincasService
from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry

# Importaciones de riego
from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask
from python_forestacion.riego.control.control_riego_task import ControlRiegoTask

# Importaciones de excepciones
from python_forestacion.excepciones.superficie_insuficiente_exception import SuperficieInsuficienteException
from python_forestacion.excepciones.persistencia_exception import PersistenciaException

# Importaciones de constantes
from python_forestacion.constantes import THREAD_JOIN_TIMEOUT


def main():
    """Punto de entrada principal de la aplicacion."""
    print("=" * 70)
    print("         SISTEMA DE GESTION FORESTAL - PATRONES DE DISENO")
    print("=" * 70)

    # ----------------------------------------------------------------------
    # PATRON SINGLETON: Inicializando servicios
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  PATRON SINGLETON: Inicializando servicios")
    print("-" * 70)

    tierra_service = TierraService()
    plantacion_service = PlantacionService()
    trabajador_service = TrabajadorService()
    registro_service = RegistroForestalService()
    fincas_service = FincasService()

    # Validar que el Registry es un Singleton
    registry1 = CultivoServiceRegistry.get_instance()
    registry2 = CultivoServiceRegistry.get_instance()
    if registry1 is registry2:
        print("[OK] Todos los servicios comparten la misma instancia del Registry")
    else:
        print("[ERROR] Las instancias del Registry son diferentes")

    # ----------------------------------------------------------------------
    # 1. Creacion de Entidades
    # ----------------------------------------------------------------------
    print("\n1. Creando tierra con plantacion...")
    terreno = tierra_service.crear_tierra_con_plantacion(
        id_padron_catastral=1,
        superficie=100.0,  # Superficie pequeña para probar limites
        domicilio="Agrelo, Mendoza",
        nombre_plantacion="Finca del Madero"
    )
    plantacion = terreno.get_finca()
    print(f"[OK] Plantacion '{plantacion.get_nombre()}' creada en '{terreno.get_domicilio()}' con {plantacion.get_superficie()} m².")

    registro = RegistroForestal(
        id_padron=1,
        tierra=terreno,
        plantacion=plantacion,
        propietario="Juan Perez",
        avaluo=50309233.55
    )
    print(f"[OK] Registro Forestal para '{registro.get_propietario()}' creado.")

    # ----------------------------------------------------------------------
    # 2. PATRON FACTORY: Plantando cultivos
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  PATRON FACTORY: Plantando cultivos")
    print("-" * 70)

    try:
        print("Plantando 5 Pinos...")
        plantacion_service.plantar(plantacion, "Pino", 5)
        print("Plantando 5 Olivos...")
        plantacion_service.plantar(plantacion, "Olivo", 5)
        print("Plantando 5 Lechugas...")
        plantacion_service.plantar(plantacion, "Lechuga", 5)
        print("Plantando 5 Zanahorias...")
        plantacion_service.plantar(plantacion, "Zanahoria", 5)
        print("[OK] Cultivos plantados exitosamente.")
    except SuperficieInsuficienteException as e:
        print(f"[!] ADVERTENCIA: {e.get_user_message()}")

    # ----------------------------------------------------------------------
    # 3. PATRON OBSERVER: Sistema de Riego Automatizado (20 segundos)
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  PATRON OBSERVER: Sistema de Riego Automatizado (20 segundos)")
    print("-" * 70)

    tarea_temp = TemperaturaReaderTask()
    tarea_hum = HumedadReaderTask()
    tarea_control = ControlRiegoTask(tarea_temp, tarea_hum, plantacion, plantacion_service)

    print("Iniciando sensores y control de riego...")
    tarea_temp.start()
    tarea_hum.start()
    tarea_control.start()

    time.sleep(20)

    print("\nDeteniendo sistema de riego...")
    tarea_temp.detener()
    tarea_hum.detener()
    tarea_control.detener()
    tarea_temp.join(timeout=THREAD_JOIN_TIMEOUT)
    tarea_hum.join(timeout=THREAD_JOIN_TIMEOUT)
    tarea_control.join(timeout=THREAD_JOIN_TIMEOUT)
    print("[OK] Sistema de riego detenido de forma segura.")

    # ----------------------------------------------------------------------
    # 4. Gestion de Personal
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  Gestion de Personal")
    print("-" * 70)

    tareas = [
        Tarea(1, date.today(), "Desmalezar"),
        Tarea(2, date.today(), "Abonar"),
        Tarea(3, date.today(), "Marcar surcos")
    ]
    trabajador = Trabajador(dni=43888734, nombre="Juan Perez", tareas=tareas)
    plantacion.set_trabajadores([trabajador])
    print(f"[OK] Trabajador '{trabajador.get_nombre()}' asignado a la plantacion.")

    print("\nAsignando apto medico...")
    trabajador_service.asignar_apto_medico(
        trabajador=trabajador,
        apto=True,
        fecha_emision=date.today(),
        observaciones="Estado de salud: excelente"
    )
    print("[OK] Apto medico asignado.")

    herramienta = Herramienta(id_herramienta=1, nombre="Pala", certificado_hys=True)
    print("\nEjecutando tareas del trabajador...")
    trabajador_service.trabajar(trabajador, date.today(), herramienta)

    # ----------------------------------------------------------------------
    # 5. Operaciones de Negocio y Persistencia
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  Operaciones de Negocio y Persistencia")
    print("-" * 70)

    fincas_service.add_finca(registro)
    print("[OK] Finca agregada al servicio de gestion de fincas.")

    fincas_service.fumigar(id_padron=1, plaguicida="insecto organico")

    # Cosecha (usa Paquete generico)
    caja_lechugas = fincas_service.cosechar_yempaquetar(Lechuga)
    caja_lechugas.mostrar_contenido_caja()

    caja_pinos = fincas_service.cosechar_yempaquetar(Pino)
    caja_pinos.mostrar_contenido_caja()

    # Persistencia
    try:
        print("\nPersistiendo registro...")
        registro_service.persistir(registro)
    except PersistenciaException as e:
        print(f"[!] ERROR: {e.get_user_message()}")

    # Lectura
    try:
        print("\nLeyendo registro desde disco...")
        registro_leido = RegistroForestalService.leer_registro("Juan Perez")
        registro_service.mostrar_datos(registro_leido)
    except (PersistenciaException, ValueError) as e:
        print(f"[!] ERROR: {e}")

    # ----------------------------------------------------------------------
    # Finalizacion
    # ----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("              EJEMPLO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print("  [OK] SINGLETON   - CultivoServiceRegistry (instancia unica)")
    print("  [OK] FACTORY     - Creacion de cultivos")
    print("  [OK] OBSERVER    - Sistema de sensores y eventos")
    print("  [OK] STRATEGY    - Algoritmos de absorcion de agua")
    print("=" * 70)

if __name__ == "__main__":
    main()



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 2/67: __init__.py
# Directorio: .
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 3/67: constantes.py
# Directorio: .
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\constantes.py
# ==============================================================================

# Constantes del sistema de Gestion Forestal

# Agua
AGUA_MINIMA = 10
AGUA_INICIAL_PLANTACION = 500
AGUA_CONSUMIDA_RIEGO = 10

# Riego
TEMP_MIN_RIEGO = 8
TEMP_MAX_RIEGO = 15
HUMEDAD_MAX_RIEGO = 50
INTERVALO_CONTROL_RIEGO = 2.5  # segundos

# Sensores
INTERVALO_SENSOR_TEMPERATURA = 2.0  # segundos
SENSOR_TEMP_MIN = -25  # °C
SENSOR_TEMP_MAX = 50  # °C
INTERVALO_SENSOR_HUMEDAD = 3.0  # segundos
SENSOR_HUMEDAD_MIN = 0  # %
SENSOR_HUMEDAD_MAX = 100  # %

# Cultivos
# Pino
SUPERFICIE_PINO = 2.0
AGUA_INICIAL_PINO = 2
ALTURA_INICIAL_ARBOL = 1.0
CRECIMIENTO_PINO = 0.10

# Olivo
SUPERFICIE_OLIVO = 3.0
AGUA_INICIAL_OLIVO = 5
CRECIMIENTO_OLIVO = 0.01

# Lechuga
SUPERFICIE_LECHUGA = 0.10
AGUA_INICIAL_LECHUGA = 1

# Zanahoria
SUPERFICIE_ZANAHORIA = 0.15
AGUA_INICIAL_ZANAHORIA = 0

# Estrategia de absorcion
MES_INICIO_VERANO = 3  # Marzo
MES_FIN_VERANO = 8   # Agosto
ABSORCION_SEASONAL_VERANO = 5
ABSORCION_SEASONAL_INVIERNO = 2
ABSORCION_CONSTANTE_LECHUGA = 1
ABSORCION_CONSTANTE_ZANAHORIA = 2

# Persistencia
DIRECTORIO_DATA = "data"
EXTENSION_DATA = ".dat"

# Threading
THREAD_JOIN_TIMEOUT = 2.0  # segundos



################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 4/67: __init__.py
# Directorio: entidades
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: entidades\cultivos
################################################################################

# ==============================================================================
# ARCHIVO 5/67: __init__.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 6/67: arbol.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\arbol.py
# ==============================================================================

from abc import ABC
from python_forestacion.entidades.cultivos.cultivo import Cultivo

class Arbol(Cultivo, ABC):
    """Clase abstracta para cultivos de tipo arbol."""

    def __init__(self, agua: int, superficie: float, altura: float):
        super().__init__(agua, superficie)
        self._altura = altura

    def get_altura(self) -> float:
        return self._altura

    def set_altura(self, altura: float) -> None:
        if altura < 0:
            raise ValueError("La altura no puede ser negativa")
        self._altura = altura


# ==============================================================================
# ARCHIVO 7/67: cultivo.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\cultivo.py
# ==============================================================================

from abc import ABC, abstractmethod

class Cultivo(ABC):
    """Clase abstracta que representa un cultivo generico."""

    def __init__(self, agua: int, superficie: float):
        self._agua = agua
        self._superficie = superficie

    def get_agua(self) -> int:
        return self._agua

    def set_agua(self, agua: int) -> None:
        if agua < 0:
            raise ValueError("El agua no puede ser negativa")
        self._agua = agua

    def get_superficie(self) -> float:
        return self._superficie

    def set_superficie(self, superficie: float) -> None:
        if superficie < 0:
            raise ValueError("La superficie debe ser mayor a cero")
        self._superficie = superficie


# ==============================================================================
# ARCHIVO 8/67: hortaliza.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\hortaliza.py
# ==============================================================================

from abc import ABC
from python_forestacion.entidades.cultivos.cultivo import Cultivo

class Hortaliza(Cultivo, ABC):
    """Clase abstracta para cultivos de tipo hortaliza."""

    def __init__(self, agua: int, superficie: float, invernadero: bool):
        super().__init__(agua, superficie)
        self._invernadero = invernadero

    def is_invernadero(self) -> bool:
        return self._invernadero

    def set_invernadero(self, invernadero: bool) -> None:
        self._invernadero = invernadero


# ==============================================================================
# ARCHIVO 9/67: lechuga.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\lechuga.py
# ==============================================================================

from python_forestacion.entidades.cultivos.hortaliza import Hortaliza
from python_forestacion.constantes import AGUA_INICIAL_LECHUGA, SUPERFICIE_LECHUGA

class Lechuga(Hortaliza):
    """Entidad Lechuga - solo datos."""

    def __init__(self, variedad: str):
        super().__init__(
            agua=AGUA_INICIAL_LECHUGA,
            superficie=SUPERFICIE_LECHUGA,
            invernadero=True
        )
        self._variedad = variedad

    def get_variedad(self) -> str:
        return self._variedad

    def set_variedad(self, variedad: str) -> None:
        self._variedad = variedad


# ==============================================================================
# ARCHIVO 10/67: olivo.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\olivo.py
# ==============================================================================

from python_forestacion.entidades.cultivos.arbol import Arbol
from python_forestacion.entidades.cultivos.tipo_aceituna import TipoAceituna
from python_forestacion.constantes import AGUA_INICIAL_OLIVO, SUPERFICIE_OLIVO, ALTURA_INICIAL_ARBOL

class Olivo(Arbol):
    """Entidad Olivo - solo datos."""

    def __init__(self, tipo_aceituna: TipoAceituna):
        super().__init__(
            agua=AGUA_INICIAL_OLIVO,
            superficie=SUPERFICIE_OLIVO,
            altura=ALTURA_INICIAL_ARBOL
        )
        self._tipo_aceituna = tipo_aceituna

    def get_tipo_aceituna(self) -> TipoAceituna:
        return self._tipo_aceituna

    def set_tipo_aceituna(self, tipo_aceituna: TipoAceituna) -> None:
        self._tipo_aceituna = tipo_aceituna


# ==============================================================================
# ARCHIVO 11/67: pino.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\pino.py
# ==============================================================================

from python_forestacion.entidades.cultivos.arbol import Arbol
from python_forestacion.constantes import AGUA_INICIAL_PINO, SUPERFICIE_PINO, ALTURA_INICIAL_ARBOL

class Pino(Arbol):
    """Entidad Pino - solo datos."""

    def __init__(self, variedad: str):
        super().__init__(
            agua=AGUA_INICIAL_PINO,
            superficie=SUPERFICIE_PINO,
            altura=ALTURA_INICIAL_ARBOL
        )
        self._variedad = variedad

    def get_variedad(self) -> str:
        return self._variedad

    def set_variedad(self, variedad: str) -> None:
        self._variedad = variedad


# ==============================================================================
# ARCHIVO 12/67: tipo_aceituna.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\tipo_aceituna.py
# ==============================================================================

from enum import Enum

class TipoAceituna(Enum):
    """Enum para los tipos de aceituna."""
    ARBEQUINA = "Arbequina"
    PICUAL = "Picual"
    MANZANILLA = "Manzanilla"


# ==============================================================================
# ARCHIVO 13/67: zanahoria.py
# Directorio: entidades\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\cultivos\zanahoria.py
# ==============================================================================

from python_forestacion.entidades.cultivos.hortaliza import Hortaliza
from python_forestacion.constantes import AGUA_INICIAL_ZANAHORIA, SUPERFICIE_ZANAHORIA

class Zanahoria(Hortaliza):
    """Entidad Zanahoria - solo datos."""

    def __init__(self, is_baby: bool):
        super().__init__(
            agua=AGUA_INICIAL_ZANAHORIA,
            superficie=SUPERFICIE_ZANAHORIA,
            invernadero=False
        )
        self._is_baby = is_baby

    def is_baby_carrot(self) -> bool:
        return self._is_baby

    def set_is_baby(self, is_baby: bool) -> None:
        self._is_baby = is_baby



################################################################################
# DIRECTORIO: entidades\personal
################################################################################

# ==============================================================================
# ARCHIVO 14/67: __init__.py
# Directorio: entidades\personal
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\personal\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 15/67: apto_medico.py
# Directorio: entidades\personal
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\personal\apto_medico.py
# ==============================================================================

from datetime import date

class AptoMedico:
    """Entidad que representa la certificacion medica de un trabajador."""

    def __init__(self, apto: bool, fecha_emision: date, observaciones: str):
        self._apto = apto
        self._fecha_emision = fecha_emision
        self._observaciones = observaciones

    def esta_apto(self) -> bool:
        return self._apto

    def get_fecha_emision(self) -> date:
        return self._fecha_emision

    def get_observaciones(self) -> str:
        return self._observaciones


# ==============================================================================
# ARCHIVO 16/67: herramienta.py
# Directorio: entidades\personal
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\personal\herramienta.py
# ==============================================================================

class Herramienta:
    """Entidad que representa una herramienta de trabajo."""

    def __init__(self, id_herramienta: int, nombre: str, certificado_hys: bool):
        self._id_herramienta = id_herramienta
        self._nombre = nombre
        self._certificado_hys = certificado_hys

    def get_id_herramienta(self) -> int:
        return self._id_herramienta

    def get_nombre(self) -> str:
        return self._nombre

    def has_certificado_hys(self) -> bool:
        return self._certificado_hys


# ==============================================================================
# ARCHIVO 17/67: tarea.py
# Directorio: entidades\personal
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\personal\tarea.py
# ==============================================================================

from datetime import date

class Tarea:
    """Entidad que representa una tarea asignada a un trabajador."""

    def __init__(self, id_tarea: int, fecha_programada: date, descripcion: str):
        self._id_tarea = id_tarea
        self._fecha_programada = fecha_programada
        self._descripcion = descripcion
        self._completada = False

    def get_id_tarea(self) -> int:
        return self._id_tarea

    def get_fecha_programada(self) -> date:
        return self._fecha_programada

    def get_descripcion(self) -> str:
        return self._descripcion

    def is_completada(self) -> bool:
        return self._completada

    def set_completada(self, completada: bool) -> None:
        self._completada = completada


# ==============================================================================
# ARCHIVO 18/67: trabajador.py
# Directorio: entidades\personal
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\personal\trabajador.py
# ==============================================================================

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.personal.tarea import Tarea
    from python_forestacion.entidades.personal.apto_medico import AptoMedico

class Trabajador:
    """Entidad que representa a un trabajador agricola."""

    def __init__(self, dni: int, nombre: str, tareas: List['Tarea']):
        self._dni = dni
        self._nombre = nombre
        self._tareas = tareas
        self._apto_medico: 'AptoMedico' = None

    def get_dni(self) -> int:
        return self._dni

    def get_nombre(self) -> str:
        return self._nombre

    def get_tareas(self) -> List['Tarea']:
        return self._tareas.copy()  # Defensive copy

    def get_apto_medico(self) -> 'AptoMedico':
        return self._apto_medico

    def set_apto_medico(self, apto_medico: 'AptoMedico') -> None:
        self._apto_medico = apto_medico



################################################################################
# DIRECTORIO: entidades\terrenos
################################################################################

# ==============================================================================
# ARCHIVO 19/67: __init__.py
# Directorio: entidades\terrenos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 20/67: plantacion.py
# Directorio: entidades\terrenos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos\plantacion.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 21/67: registro_forestal.py
# Directorio: entidades\terrenos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos\registro_forestal.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 22/67: tierra.py
# Directorio: entidades\terrenos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\entidades\terrenos\tierra.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: excepciones
################################################################################

# ==============================================================================
# ARCHIVO 23/67: __init__.py
# Directorio: excepciones
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 24/67: agua_agotada_exception.py
# Directorio: excepciones
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\agua_agotada_exception.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 25/67: forestacion_exception.py
# Directorio: excepciones
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\forestacion_exception.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 26/67: mensajes_exception.py
# Directorio: excepciones
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\mensajes_exception.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 27/67: persistencia_exception.py
# Directorio: excepciones
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\persistencia_exception.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 28/67: superficie_insuficiente_exception.py
# Directorio: excepciones
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\excepciones\superficie_insuficiente_exception.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 29/67: __init__.py
# Directorio: patrones
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: patrones\factory
################################################################################

# ==============================================================================
# ARCHIVO 30/67: __init__.py
# Directorio: patrones\factory
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\factory\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 31/67: cultivo_factory.py
# Directorio: patrones\factory
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\factory\cultivo_factory.py
# ==============================================================================

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo
    from python_forestacion.entidades.cultivos.pino import Pino
    from python_forestacion.entidades.cultivos.olivo import Olivo
    from python_forestacion.entidades.cultivos.lechuga import Lechuga
    from python_forestacion.entidades.cultivos.zanahoria import Zanahoria

class CultivoFactory:
    """Factory para la creacion de cultivos."""

    @staticmethod
    def _crear_pino() -> 'Pino':
        from python_forestacion.entidades.cultivos.pino import Pino
        return Pino(variedad="Parana")

    @staticmethod
    def _crear_olivo() -> 'Olivo':
        from python_forestacion.entidades.cultivos.olivo import Olivo
        from python_forestacion.entidades.cultivos.tipo_aceituna import TipoAceituna
        return Olivo(tipo_aceituna=TipoAceituna.ARBEQUINA)

    @staticmethod
    def _crear_lechuga() -> 'Lechuga':
        from python_forestacion.entidades.cultivos.lechuga import Lechuga
        return Lechuga(variedad="Mantecosa")

    @staticmethod
    def _crear_zanahoria() -> 'Zanahoria':
        from python_forestacion.entidades.cultivos.zanahoria import Zanahoria
        return Zanahoria(is_baby=False)

    @staticmethod
    def crear_cultivo(especie: str) -> 'Cultivo':
        factories = {
            "Pino": CultivoFactory._crear_pino,
            "Olivo": CultivoFactory._crear_olivo,
            "Lechuga": CultivoFactory._crear_lechuga,
            "Zanahoria": CultivoFactory._crear_zanahoria
        }

        if especie not in factories:
            raise ValueError(f"Especie de cultivo desconocida: {especie}")

        return factories[especie]()



################################################################################
# DIRECTORIO: patrones\observer
################################################################################

# ==============================================================================
# ARCHIVO 32/67: __init__.py
# Directorio: patrones\observer
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 33/67: observable.py
# Directorio: patrones\observer
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\observable.py
# ==============================================================================

from abc import ABC
from typing import Generic, TypeVar, List
from python_forestacion.patrones.observer.observer import Observer

T = TypeVar('T')

class Observable(Generic[T], ABC):
    """Clase observable para el patron Observer."""

    def __init__(self):
        self._observadores: List[Observer[T]] = []

    def agregar_observador(self, observador: Observer[T]) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador: Observer[T]) -> None:
        self._observadores.remove(observador)

    def notificar_observadores(self, evento: T) -> None:
        for observador in self._observadores:
            observador.actualizar(evento)


# ==============================================================================
# ARCHIVO 34/67: observer.py
# Directorio: patrones\observer
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\observer.py
# ==============================================================================

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class Observer(Generic[T], ABC):
    """Interfaz para el patron Observer."""

    @abstractmethod
    def actualizar(self, evento: T) -> None:
        pass



################################################################################
# DIRECTORIO: patrones\observer\eventos
################################################################################

# ==============================================================================
# ARCHIVO 35/67: __init__.py
# Directorio: patrones\observer\eventos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\eventos\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 36/67: evento_plantacion.py
# Directorio: patrones\observer\eventos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\eventos\evento_plantacion.py
# ==============================================================================

from dataclasses import dataclass
from datetime import datetime

@dataclass
class EventoPlantacion:
    """
    Representa un evento que ocurre en una plantación.
    """
    mensaje: str
    timestamp: datetime


# ==============================================================================
# ARCHIVO 37/67: evento_sensor.py
# Directorio: patrones\observer\eventos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\eventos\evento_sensor.py
# ==============================================================================

from dataclasses import dataclass
from datetime import datetime

@dataclass
class EventoSensor:
    """
    Representa un evento de lectura de un sensor.
    """
    tipo_sensor: str
    valor: float
    timestamp: datetime



################################################################################
# DIRECTORIO: patrones\singleton
################################################################################

# ==============================================================================
# ARCHIVO 38/67: __init__.py
# Directorio: patrones\singleton
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\singleton\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: patrones\strategy
################################################################################

# ==============================================================================
# ARCHIVO 39/67: __init__.py
# Directorio: patrones\strategy
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 40/67: absorcion_agua_strategy.py
# Directorio: patrones\strategy
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\absorcion_agua_strategy.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: patrones\strategy\impl
################################################################################

# ==============================================================================
# ARCHIVO 41/67: __init__.py
# Directorio: patrones\strategy\impl
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\impl\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 42/67: absorcion_constante_strategy.py
# Directorio: patrones\strategy\impl
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\impl\absorcion_constante_strategy.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 43/67: absorcion_seasonal_strategy.py
# Directorio: patrones\strategy\impl
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\strategy\impl\absorcion_seasonal_strategy.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: riego
################################################################################

# ==============================================================================
# ARCHIVO 44/67: __init__.py
# Directorio: riego
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: riego\control
################################################################################

# ==============================================================================
# ARCHIVO 45/67: __init__.py
# Directorio: riego\control
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\control\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 46/67: control_riego_task.py
# Directorio: riego\control
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\control\control_riego_task.py
# ==============================================================================

import threading
import time
from typing import TYPE_CHECKING
from python_forestacion.patrones.observer.observer import Observer
from python_forestacion.patrones.observer.eventos.evento_sensor import EventoSensor
from python_forestacion.constantes import TEMP_MIN_RIEGO, TEMP_MAX_RIEGO, HUMEDAD_MAX_RIEGO, INTERVALO_CONTROL_RIEGO
from python_forestacion.excepciones.agua_agotada_exception import AguaAgotadaException

if TYPE_CHECKING:
    from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
    from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask
    from python_forestacion.entidades.terrenos.plantacion import Plantacion
    from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService

class ControlRiegoTask(threading.Thread, Observer[EventoSensor]):
    """Controlador de riego que observa los sensores y reacciona a eventos."""

    def __init__(
        self,
        sensor_temperatura: 'TemperaturaReaderTask',
        sensor_humedad: 'HumedadReaderTask',
        plantacion: 'Plantacion',
        plantacion_service: 'PlantacionService'
    ):
        threading.Thread.__init__(self, daemon=True)
        self._plantacion = plantacion
        self._plantacion_service = plantacion_service
        self._ultima_temperatura: float = 20.0  # Valor inicial seguro
        self._ultima_humedad: float = 60.0     # Valor inicial seguro
        self._detenido = threading.Event()

        # Suscribirse a los sensores
        sensor_temperatura.agregar_observador(self)
        sensor_humedad.agregar_observador(self)

    def actualizar(self, evento: EventoSensor) -> None:
        """Este metodo es llamado por los sensores (Observable) cuando hay un nuevo evento."""
        if evento.tipo_sensor == "temperatura":
            self._ultima_temperatura = evento.valor
        elif evento.tipo_sensor == "humedad":
            self._ultima_humedad = evento.valor

    def _evaluar_condiciones_y_regar(self) -> None:
        temp = self._ultima_temperatura
        hum = self._ultima_humedad

        print(f"[Control Riego] Evaluando: Temp={temp:.2f}°C, Hum={hum:.2f}%")

        if (TEMP_MIN_RIEGO <= temp <= TEMP_MAX_RIEGO) and (hum <= HUMEDAD_MAX_RIEGO):
            try:
                print(f"[Control Riego] *** CONDICIONES OPTIMAS - REGANDO ***")
                self._plantacion_service.regar(self._plantacion)
                print(f"[Control Riego] Riego finalizado. Agua restante: {self._plantacion.get_agua_disponible()} L")
            except AguaAgotadaException as e:
                print(f"[Control Riego] [!] ADVERTENCIA: {e.get_user_message()}")
        else:
            print("[Control Riego] Condiciones no optimas para riego.")

    def run(self) -> None:
        print("[INFO] Control de Riego iniciado. Esperando lecturas de sensores...")
        while not self._detenido.is_set():
            self._evaluar_condiciones_y_regar()
            # La evaluación ahora podría ser menos frecuente o incluso eliminarse si
            # la lógica de riego se moviera completamente dentro de 'actualizar'.
            # Por ahora, se mantiene para no alterar demasiado el flujo.
            time.sleep(INTERVALO_CONTROL_RIEGO)

    def detener(self) -> None:
        self._detenido.set()



################################################################################
# DIRECTORIO: riego\sensores
################################################################################

# ==============================================================================
# ARCHIVO 47/67: __init__.py
# Directorio: riego\sensores
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\sensores\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 48/67: humedad_reader_task.py
# Directorio: riego\sensores
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\sensores\humedad_reader_task.py
# ==============================================================================

import threading
import time
import random
from datetime import datetime
from python_forestacion.patrones.observer.observable import Observable
from python_forestacion.patrones.observer.eventos.evento_sensor import EventoSensor
from python_forestacion.constantes import INTERVALO_SENSOR_HUMEDAD, SENSOR_HUMEDAD_MIN, SENSOR_HUMEDAD_MAX

class HumedadReaderTask(threading.Thread, Observable[EventoSensor]):
    """Sensor de humedad que se ejecuta en un hilo separado y notifica eventos."""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._detenido = threading.Event()

    def _leer_humedad(self) -> float:
        return random.uniform(SENSOR_HUMEDAD_MIN, SENSOR_HUMEDAD_MAX)

    def run(self) -> None:
        while not self._detenido.is_set():
            humedad = self._leer_humedad()
            evento = EventoSensor(
                tipo_sensor="humedad",
                valor=humedad,
                timestamp=datetime.now()
            )
            self.notificar_observadores(evento)
            time.sleep(INTERVALO_SENSOR_HUMEDAD)

    def detener(self) -> None:
        self._detenido.set()


# ==============================================================================
# ARCHIVO 49/67: temperatura_reader_task.py
# Directorio: riego\sensores
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\sensores\temperatura_reader_task.py
# ==============================================================================

import threading
import time
import random
from datetime import datetime
from python_forestacion.patrones.observer.observable import Observable
from python_forestacion.patrones.observer.eventos.evento_sensor import EventoSensor
from python_forestacion.constantes import INTERVALO_SENSOR_TEMPERATURA, SENSOR_TEMP_MIN, SENSOR_TEMP_MAX

class TemperaturaReaderTask(threading.Thread, Observable[EventoSensor]):
    """Sensor de temperatura que se ejecuta en un hilo separado y notifica eventos."""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._detenido = threading.Event()

    def _leer_temperatura(self) -> float:
        return random.uniform(SENSOR_TEMP_MIN, SENSOR_TEMP_MAX)

    def run(self) -> None:
        while not self._detenido.is_set():
            temperatura = self._leer_temperatura()
            evento = EventoSensor(
                tipo_sensor="temperatura",
                valor=temperatura,
                timestamp=datetime.now()
            )
            self.notificar_observadores(evento)
            time.sleep(INTERVALO_SENSOR_TEMPERATURA)

    def detener(self) -> None:
        self._detenido.set()



################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 50/67: __init__.py
# Directorio: servicios
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: servicios\cultivos
################################################################################

# ==============================================================================
# ARCHIVO 51/67: __init__.py
# Directorio: servicios\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 52/67: arbol_service.py
# Directorio: servicios\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\arbol_service.py
# ==============================================================================

from typing import TYPE_CHECKING
from python_forestacion.servicios.cultivos.cultivo_service import CultivoService

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.arbol import Arbol

class ArbolService(CultivoService):
    """Servicio base para la gestion de arboles."""

    def mostrar_datos(self, cultivo: 'Arbol') -> None:
        super().mostrar_datos(cultivo)
        print(f"Altura: {cultivo.get_altura()} m")


# ==============================================================================
# ARCHIVO 53/67: cultivo_service.py
# Directorio: servicios\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\cultivo_service.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 54/67: cultivo_service_registry.py
# Directorio: servicios\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\cultivo_service_registry.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 55/67: lechuga_service.py
# Directorio: servicios\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\lechuga_service.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 56/67: olivo_service.py
# Directorio: servicios\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\olivo_service.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 57/67: pino_service.py
# Directorio: servicios\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\pino_service.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 58/67: zanahoria_service.py
# Directorio: servicios\cultivos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\cultivos\zanahoria_service.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: servicios\negocio
################################################################################

# ==============================================================================
# ARCHIVO 59/67: __init__.py
# Directorio: servicios\negocio
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\negocio\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 60/67: fincas_service.py
# Directorio: servicios\negocio
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\negocio\fincas_service.py
# ==============================================================================

from typing import Dict, Type, TypeVar, TYPE_CHECKING
from python_forestacion.servicios.negocio.paquete import Paquete

if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal
    from python_forestacion.entidades.cultivos.cultivo import Cultivo

T = TypeVar('T', bound='Cultivo')

class FincasService:
    """Servicio de alto nivel para gestionar multiples fincas."""

    def __init__(self):
        self._fincas: Dict[int, 'RegistroForestal'] = {}

    def add_finca(self, registro: 'RegistroForestal') -> None:
        self._fincas[registro.get_id_padron()] = registro

    def buscar_finca(self, id_padron: int) -> 'RegistroForestal':
        return self._fincas.get(id_padron)

    def fumigar(self, id_padron: int, plaguicida: str) -> None:
        registro = self.buscar_finca(id_padron)
        if registro:
            print(f"Fumigando plantacion de {registro.get_plantacion().get_nombre()} con: {plaguicida}")
        else:
            print(f"No se encontro la finca con padron {id_padron}")

    def cosechar_yempaquetar(self, tipo_cultivo: Type[T]) -> Paquete[T]:
        print(f"\nCOSECHANDO {tipo_cultivo.__name__} de todas las fincas...")
        caja = Paquete(tipo_cultivo)
        
        for registro in self._fincas.values():
            plantacion = registro.get_plantacion()
            cultivos_a_cosechar = [c for c in plantacion.get_cultivos_interno() if isinstance(c, tipo_cultivo)]
            
            for cultivo in cultivos_a_cosechar:
                caja.agregar_item(cultivo)
                plantacion.get_cultivos_interno().remove(cultivo)

        print(f"Se cosecharon {len(caja.get_contenido())} unidades de {tipo_cultivo.__name__}")
        return caja


# ==============================================================================
# ARCHIVO 61/67: paquete.py
# Directorio: servicios\negocio
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\negocio\paquete.py
# ==============================================================================

from typing import Generic, TypeVar, List, Type

T = TypeVar('T')
_id_counter = 0

def _generar_id():
    global _id_counter
    _id_counter += 1
    return _id_counter

class Paquete(Generic[T]):
    """Clase generica para empaquetar cultivos."""

    def __init__(self, tipo_contenido: Type[T]):
        self._id_paquete = _generar_id()
        self._tipo_contenido = tipo_contenido
        self._contenido: List[T] = []

    def agregar_item(self, item: T) -> None:
        if not isinstance(item, self._tipo_contenido):
            raise TypeError(f"Este paquete solo acepta {self._tipo_contenido.__name__}")
        self._contenido.append(item)

    def get_contenido(self) -> List[T]:
        return self._contenido

    def get_tipo_contenido(self) -> Type[T]:
        return self._tipo_contenido

    def mostrar_contenido_caja(self) -> None:
        print("\nContenido de la caja:")
        print(f"  Tipo: {self._tipo_contenido.__name__}")
        print(f"  Cantidad: {len(self._contenido)}")
        print(f"  ID Paquete: {self._id_paquete}")



################################################################################
# DIRECTORIO: servicios\personal
################################################################################

# ==============================================================================
# ARCHIVO 62/67: __init__.py
# Directorio: servicios\personal
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\personal\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 63/67: trabajador_service.py
# Directorio: servicios\personal
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\personal\trabajador_service.py
# ==============================================================================

from datetime import date
from typing import TYPE_CHECKING
from python_forestacion.entidades.personal.apto_medico import AptoMedico

if TYPE_CHECKING:
    from python_forestacion.entidades.personal.trabajador import Trabajador
    from python_forestacion.entidades.personal.herramienta import Herramienta
    from python_forestacion.entidades.personal.tarea import Tarea

class TrabajadorService:
    """Servicio para la gestion de Trabajador."""

    def asignar_apto_medico(self, trabajador: 'Trabajador', apto: bool, fecha_emision: date, observaciones: str) -> None:
        """Asigna un certificado de apto médico a un trabajador.

        Args:
            trabajador (Trabajador): El trabajador al que se le asigna el apto.
            apto (bool): True si el trabajador está apto, False en caso contrario.
            fecha_emision (date): La fecha de emisión del certificado.
            observaciones (str): Observaciones adicionales del médico.
        """
        apto_medico = AptoMedico(apto, fecha_emision, observaciones)
        trabajador.set_apto_medico(apto_medico)

    def trabajar(self, trabajador: 'Trabajador', fecha: date, util: 'Herramienta') -> bool:
        """Simula a un trabajador realizando todas sus tareas para una fecha.

        Args:
            trabajador (Trabajador): El trabajador que realizará las tareas.
            fecha (date): La fecha para la cual se buscan las tareas.
            util (Herramienta): La herramienta que usará para las tareas.

        Returns:
            bool: True si el trabajador pudo realizar tareas, False si no tenía
                apto médico.
        """
        apto_medico = trabajador.get_apto_medico()
        if not apto_medico or not apto_medico.esta_apto():
            print(f"El trabajador {trabajador.get_nombre()} no tiene apto medico vigente.")
            return False

        tareas_del_dia = [t for t in trabajador.get_tareas() if t.get_fecha_programada() == fecha and not t.is_completada()]
        
        # Ordenar por ID descendente sin lambda
        tareas_del_dia.sort(key=self._obtener_id_tarea, reverse=True)

        for tarea in tareas_del_dia:
            print(f"El trabajador {trabajador.get_nombre()} realizo la tarea {tarea.get_id_tarea()} {tarea.get_descripcion()} con herramienta: {util.get_nombre()}")
            tarea.set_completada(True)

        return True

    @staticmethod
    def _obtener_id_tarea(tarea: 'Tarea') -> int:
        return tarea.get_id_tarea()



################################################################################
# DIRECTORIO: servicios\terrenos
################################################################################

# ==============================================================================
# ARCHIVO 64/67: __init__.py
# Directorio: servicios\terrenos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos\__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 65/67: plantacion_service.py
# Directorio: servicios\terrenos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos\plantacion_service.py
# ==============================================================================

from typing import TYPE_CHECKING
from python_forestacion.patrones.factory.cultivo_factory import CultivoFactory
from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry
from python_forestacion.excepciones.superficie_insuficiente_exception import SuperficieInsuficienteException
from python_forestacion.excepciones.agua_agotada_exception import AguaAgotadaException
from python_forestacion.constantes import AGUA_CONSUMIDA_RIEGO

if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.plantacion import Plantacion
    from python_forestacion.entidades.cultivos.cultivo import Cultivo

class PlantacionService:
    """Servicio para la gestion de Plantacion."""

    def __init__(self):
        self._cultivo_registry = CultivoServiceRegistry.get_instance()

    def plantar(self, plantacion: 'Plantacion', especie: str, cantidad: int) -> None:
        """Planta una cantidad de cultivos de una especie en la plantacion.

        Args:
            plantacion (Plantacion): La plantación donde se plantarán los cultivos.
            especie (str): El tipo de cultivo a plantar (ej. 'Pino', 'Olivo').
            cantidad (int): El número de cultivos a plantar.

        Raises:
            SuperficieInsuficienteException: Si no hay suficiente superficie.
        """
        superficie_ocupada = sum(c.get_superficie() for c in plantacion.get_cultivos_interno())
        superficie_disponible = plantacion.get_superficie() - superficie_ocupada

        # Crear un cultivo temporal para obtener su superficie
        cultivo_temporal = CultivoFactory.crear_cultivo(especie)
        superficie_requerida_total = cultivo_temporal.get_superficie() * cantidad

        if superficie_requerida_total > superficie_disponible:
            raise SuperficieInsuficienteException(superficie_requerida_total, superficie_disponible)

        for _ in range(cantidad):
            nuevo_cultivo = CultivoFactory.crear_cultivo(especie)
            plantacion.get_cultivos_interno().append(nuevo_cultivo)

    def regar(self, plantacion: 'Plantacion') -> None:
        """Riega todos los cultivos de la plantacion, consumiendo agua.

        Args:
            plantacion (Plantacion): La plantación a regar.

        Raises:
            AguaAgotadaException: Si no hay suficiente agua para el riego.
        """
        if plantacion.get_agua_disponible() < AGUA_CONSUMIDA_RIEGO:
            raise AguaAgotadaException(AGUA_CONSUMIDA_RIEGO, plantacion.get_agua_disponible())

        plantacion.set_agua_disponible(plantacion.get_agua_disponible() - AGUA_CONSUMIDA_RIEGO)

        for cultivo in plantacion.get_cultivos_interno():
            self._cultivo_registry.absorber_agua(cultivo)

    def cosechar(self, plantacion: 'Plantacion') -> None:
        """Cosecha todos los cultivos de la plantacion."""
        # En una implementacion real, esto deberia hacer algo mas util
        print(f"Cosechando todos los cultivos de {plantacion.get_nombre()}")
        plantacion.set_cultivos([]) # Simula la cosecha eliminando los cultivos


# ==============================================================================
# ARCHIVO 66/67: registro_forestal_service.py
# Directorio: servicios\terrenos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos\registro_forestal_service.py
# ==============================================================================

import os
import pickle
from typing import TYPE_CHECKING
from python_forestacion.constantes import DIRECTORIO_DATA, EXTENSION_DATA
from python_forestacion.excepciones.persistencia_exception import PersistenciaException, TipoOperacion
from python_forestacion.excepciones.mensajes_exception import MensajesException

if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal
    from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry

class RegistroForestalService:
    """Servicio para la persistencia de RegistroForestal. Similar a un "repositorio". """

    def __init__(self):
        from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry
        self._registry: 'CultivoServiceRegistry' = CultivoServiceRegistry.get_instance()

    def mostrar_datos(self, registro: 'RegistroForestal') -> None:
        """Imprime en consola los datos formateados de un registro forestal.

        Args:
            registro (RegistroForestal): El objeto de registro a mostrar.
        """
        print("\nREGISTRO FORESTAL")
        print("=================")
        print(f"Padron:      {registro.get_id_padron()}")
        print(f"Propietario: {registro.get_propietario()}")
        print(f"Avaluo:      {registro.get_avaluo()}")
        print(f"Domicilio:   {registro.get_tierra().get_domicilio()}")
        print(f"Superficie: {registro.get_tierra().get_superficie()}")
        
        plantacion = registro.get_plantacion()
        print(f"Cantidad de cultivos plantados: {len(plantacion.get_cultivos())}")
        print("Listado de Cultivos plantados")
        print("____________________________")
        for cultivo in plantacion.get_cultivos():
            print()
            self._registry.mostrar_datos(cultivo)

    def persistir(self, registro: 'RegistroForestal') -> None:
        """Guarda un objeto RegistroForestal en disco usando pickle.

        Args:
            registro (RegistroForestal): El registro a persistir.

        Raises:
            PersistenciaException: Si ocurre un error durante la escritura.
        """
        nombre_archivo = f"{registro.get_propietario()}{EXTENSION_DATA}"
        ruta_completa = os.path.join(DIRECTORIO_DATA, nombre_archivo)

        try:
            os.makedirs(DIRECTORIO_DATA, exist_ok=True)
            with open(ruta_completa, 'wb') as f:
                pickle.dump(registro, f)
            print(f"Registro de {registro.get_propietario()} persistido exitosamente en {ruta_completa}")
        except IOError as e:
            raise PersistenciaException(
                user_message=MensajesException.PERSISTENCIA_ESCRITURA_USER,
                technical_message=MensajesException.PERSISTENCIA_ESCRITURA_TECH.format(archivo=ruta_completa),
                nombre_archivo=ruta_completa,
                tipo_operacion=TipoOperacion.ESCRITURA
            ) from e

    @staticmethod
    def leer_registro(propietario: str) -> 'RegistroForestal':
        """Lee un objeto RegistroForestal desde disco.

        Args:
            propietario (str): El nombre del propietario para encontrar el archivo.

        Raises:
            ValueError: Si el nombre del propietario es nulo o vacío.
            PersistenciaException: Si el archivo no existe o está corrupto.

        Returns:
            RegistroForestal: El objeto recuperado desde el archivo.
        """
        if not propietario:
            raise ValueError("El nombre del propietario no puede ser nulo o vacio")

        nombre_archivo = f"{propietario}{EXTENSION_DATA}"
        ruta_completa = os.path.join(DIRECTORIO_DATA, nombre_archivo)

        if not os.path.exists(ruta_completa):
            raise PersistenciaException(
                user_message=MensajesException.PERSISTENCIA_NOT_FOUND_USER,
                technical_message=MensajesException.PERSISTENCIA_NOT_FOUND_TECH.format(archivo=ruta_completa),
                nombre_archivo=ruta_completa,
                tipo_operacion=TipoOperacion.LECTURA
            )

        try:
            with open(ruta_completa, 'rb') as f:
                registro = pickle.load(f)
                print(f"Registro de {propietario} recuperado exitosamente desde {ruta_completa}")
                return registro
        except (IOError, pickle.UnpicklingError) as e:
            raise PersistenciaException(
                user_message=MensajesException.PERSISTENCIA_CORRUPTO_USER,
                technical_message=MensajesException.PERSISTENCIA_CORRUPTO_TECH.format(archivo=ruta_completa),
                nombre_archivo=ruta_completa,
                tipo_operacion=TipoOperacion.LECTURA
            ) from e


# ==============================================================================
# ARCHIVO 67/67: tierra_service.py
# Directorio: servicios\terrenos
# Ruta completa: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos\tierra_service.py
# ==============================================================================

from typing import TYPE_CHECKING
from python_forestacion.entidades.terrenos.tierra import Tierra
from python_forestacion.entidades.terrenos.plantacion import Plantacion
from python_forestacion.constantes import AGUA_INICIAL_PLANTACION

if TYPE_CHECKING:
    pass

class TierraService:
    """Servicio para la gestion de Tierra."""

    def crear_tierra_con_plantacion(
        self,
        id_padron_catastral: int,
        superficie: float,
        domicilio: str,
        nombre_plantacion: str
    ) -> Tierra:
        """Crea una Tierra y le asocia una Plantacion nueva."""
        if superficie <= 0:
            raise ValueError("La superficie debe ser mayor a cero")

        tierra = Tierra(id_padron_catastral, superficie, domicilio)
        plantacion = Plantacion(
            nombre=nombre_plantacion,
            superficie=superficie,
            agua=AGUA_INICIAL_PLANTACION
        )
        tierra.set_finca(plantacion)
        return tierra



################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 66
# Generado: 2025-10-21 19:58:16
################################################################################
