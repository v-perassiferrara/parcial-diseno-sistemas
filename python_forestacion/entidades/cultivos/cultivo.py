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
