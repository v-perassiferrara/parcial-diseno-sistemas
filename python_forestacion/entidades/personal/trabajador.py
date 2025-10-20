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
