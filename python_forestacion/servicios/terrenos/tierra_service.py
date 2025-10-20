from typing import TYPE_CHECKING
from python_forestacion.entidades.terrenos.tierra import Tierra
from python_forestacion.entidades.terrenos.plantacion import Plantacion
from python_forestacion.constantes import AGUA_INICIAL_PLANTACION

if TYPE_CHECKING:
    pass

class TierraService:
    """Servicio para la gestion de Tierra."""

    def crear_tierra_con_plantacion(
        self,
        id_padron_catastral: int,
        superficie: float,
        domicilio: str,
        nombre_plantacion: str
    ) -> Tierra:
        """Crea una Tierra y le asocia una Plantacion nueva."""
        if superficie <= 0:
            raise ValueError("La superficie debe ser mayor a cero")

        tierra = Tierra(id_padron_catastral, superficie, domicilio)
        plantacion = Plantacion(
            nombre=nombre_plantacion,
            superficie=superficie,
            agua=AGUA_INICIAL_PLANTACION
        )
        tierra.set_finca(plantacion)
        return tierra
