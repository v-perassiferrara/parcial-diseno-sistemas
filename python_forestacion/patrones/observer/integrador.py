"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: observable.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\observable.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/3: observer.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\observer\observer.py
# ================================================================================

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class Observer(Generic[T], ABC):
    """Interfaz para el patron Observer."""

    @abstractmethod
    def actualizar(self, evento: T) -> None:
        pass


