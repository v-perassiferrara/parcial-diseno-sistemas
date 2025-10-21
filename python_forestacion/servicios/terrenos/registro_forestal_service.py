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
