
import pytest
from python_forestacion.entidades.terrenos.plantacion import Plantacion
from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService
from python_forestacion.excepciones.superficie_insuficiente_exception import SuperficieInsuficienteException
from python_forestacion.excepciones.agua_agotada_exception import AguaAgotadaException
from python_forestacion.patrones.factory.cultivo_factory import CultivoFactory

@pytest.fixture
def plantacion_service():
    """Fixture for the PlantacionService."""
    return PlantacionService()

@pytest.fixture
def plantacion_pequena():
    """Fixture for a small plantation."""
    return Plantacion(nombre="Finca Chica", superficie=10.0, agua=100)

def test_plantar_exitosamente(plantacion_service, plantacion_pequena):
    """Tests that crops can be planted successfully when there is enough space."""
    plantacion_service.plantar(plantacion_pequena, "Pino", 2)  # 2 Pinos * 2.0 m2/u = 4.0 m2
    assert len(plantacion_pequena.get_cultivos()) == 2

def test_plantar_sin_superficie_suficiente(plantacion_service, plantacion_pequena):
    """Tests that a SuperficieInsuficienteException is raised when there is not enough space."""
    with pytest.raises(SuperficieInsuficienteException) as excinfo:
        plantacion_service.plantar(plantacion_pequena, "Olivo", 4)  # 4 Olivos * 3.0 m2/u = 12.0 m2 > 10.0 m2
    assert excinfo.value.get_superficie_requerida() == 12.0
    assert excinfo.value.get_superficie_disponible() == 10.0

def test_regar_exitosamente(plantacion_service, plantacion_pequena):
    """Tests that watering works correctly when there is enough water."""
    initial_water = plantacion_pequena.get_agua_disponible()
    plantacion_service.regar(plantacion_pequena)
    assert plantacion_pequena.get_agua_disponible() < initial_water

def test_regar_sin_agua_suficiente(plantacion_service, plantacion_pequena):
    """Tests that an AguaAgotadaException is raised when there is not enough water."""
    plantacion_pequena.set_agua_disponible(5)  # Less than AGUA_CONSUMIDA_RIEGO (10)
    with pytest.raises(AguaAgotadaException):
        plantacion_service.regar(plantacion_pequena)

def test_plantar_cultivo_desconocido(plantacion_service, plantacion_pequena):
    """Tests that planting an unknown crop type raises a ValueError."""
    with pytest.raises(ValueError):
        plantacion_service.plantar(plantacion_pequena, "CultivoRaro", 1)
