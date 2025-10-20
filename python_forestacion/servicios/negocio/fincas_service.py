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
