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
