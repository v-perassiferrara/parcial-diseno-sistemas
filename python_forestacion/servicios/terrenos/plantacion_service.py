from typing import TYPE_CHECKING
from python_forestacion.patrones.factory.cultivo_factory import CultivoFactory
from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry
from python_forestacion.excepciones.superficie_insuficiente_exception import SuperficieInsuficienteException
from python_forestacion.excepciones.agua_agotada_exception import AguaAgotadaException
from python_forestacion.constantes import AGUA_CONSUMIDA_RIEGO

if TYPE_CHECKING:
    from python_forestacion.entidades.terrenos.plantacion import Plantacion
    from python_forestacion.entidades.cultivos.cultivo import Cultivo

class PlantacionService:
    """Servicio para la gestion de Plantacion."""

    def __init__(self):
        self._cultivo_registry = CultivoServiceRegistry.get_instance()

    def plantar(self, plantacion: 'Plantacion', especie: str, cantidad: int) -> None:
        """Planta una cantidad de cultivos de una especie."""
        superficie_ocupada = sum(c.get_superficie() for c in plantacion.get_cultivos_interno())
        superficie_disponible = plantacion.get_superficie() - superficie_ocupada

        # Crear un cultivo temporal para obtener su superficie
        cultivo_temporal = CultivoFactory.crear_cultivo(especie)
        superficie_requerida_total = cultivo_temporal.get_superficie() * cantidad

        if superficie_requerida_total > superficie_disponible:
            raise SuperficieInsuficienteException(superficie_requerida_total, superficie_disponible)

        for _ in range(cantidad):
            nuevo_cultivo = CultivoFactory.crear_cultivo(especie)
            plantacion.get_cultivos_interno().append(nuevo_cultivo)

    def regar(self, plantacion: 'Plantacion') -> None:
        """Riega todos los cultivos de la plantacion."""
        if plantacion.get_agua_disponible() < AGUA_CONSUMIDA_RIEGO:
            raise AguaAgotadaException(AGUA_CONSUMIDA_RIEGO, plantacion.get_agua_disponible())

        plantacion.set_agua_disponible(plantacion.get_agua_disponible() - AGUA_CONSUMIDA_RIEGO)

        for cultivo in plantacion.get_cultivos_interno():
            self._cultivo_registry.absorber_agua(cultivo)

    def cosechar(self, plantacion: 'Plantacion') -> None:
        """Cosecha todos los cultivos de la plantacion."""
        # En una implementacion real, esto deberia hacer algo mas util
        print(f"Cosechando todos los cultivos de {plantacion.get_nombre()}")
        plantacion.set_cultivos([]) # Simula la cosecha eliminando los cultivos
