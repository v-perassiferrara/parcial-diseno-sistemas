"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos
Fecha: 2025-10-21 19:58:16
Total de archivos integrados: 4
"""

# ================================================================================
# ARCHIVO 1/4: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/4: plantacion_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos\plantacion_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/4: registro_forestal_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos\registro_forestal_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/4: tierra_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\terrenos\tierra_service.py
# ================================================================================

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


