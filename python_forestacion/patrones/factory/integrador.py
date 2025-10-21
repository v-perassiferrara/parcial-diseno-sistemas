"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\factory
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\factory\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: cultivo_factory.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\patrones\factory\cultivo_factory.py
# ================================================================================

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from python_forestacion.entidades.cultivos.cultivo import Cultivo
    from python_forestacion.entidades.cultivos.pino import Pino
    from python_forestacion.entidades.cultivos.olivo import Olivo
    from python_forestacion.entidades.cultivos.lechuga import Lechuga
    from python_forestacion.entidades.cultivos.zanahoria import Zanahoria

class CultivoFactory:
    """Factory para la creacion de cultivos."""

    @staticmethod
    def _crear_pino() -> 'Pino':
        from python_forestacion.entidades.cultivos.pino import Pino
        return Pino(variedad="Parana")

    @staticmethod
    def _crear_olivo() -> 'Olivo':
        from python_forestacion.entidades.cultivos.olivo import Olivo
        from python_forestacion.entidades.cultivos.tipo_aceituna import TipoAceituna
        return Olivo(tipo_aceituna=TipoAceituna.ARBEQUINA)

    @staticmethod
    def _crear_lechuga() -> 'Lechuga':
        from python_forestacion.entidades.cultivos.lechuga import Lechuga
        return Lechuga(variedad="Mantecosa")

    @staticmethod
    def _crear_zanahoria() -> 'Zanahoria':
        from python_forestacion.entidades.cultivos.zanahoria import Zanahoria
        return Zanahoria(is_baby=False)

    @staticmethod
    def crear_cultivo(especie: str) -> 'Cultivo':
        factories = {
            "Pino": CultivoFactory._crear_pino,
            "Olivo": CultivoFactory._crear_olivo,
            "Lechuga": CultivoFactory._crear_lechuga,
            "Zanahoria": CultivoFactory._crear_zanahoria
        }

        if especie not in factories:
            raise ValueError(f"Especie de cultivo desconocida: {especie}")

        return factories[especie]()


