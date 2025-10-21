"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\personal
Fecha: 2025-10-21 19:58:16
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\personal\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: trabajador_service.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\servicios\personal\trabajador_service.py
# ================================================================================

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


