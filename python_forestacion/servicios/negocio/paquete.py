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
