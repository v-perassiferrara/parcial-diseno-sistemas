"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\negocio
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\negocio\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: fincas_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\negocio\fincas_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/3: paquete.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\negocio\paquete.py
# ================================================================================

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


