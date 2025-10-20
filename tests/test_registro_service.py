import pytest
import os
from python_forestacion.servicios.terrenos.tierra_service import TierraService
from python_forestacion.servicios.terrenos.registro_forestal_service import RegistroForestalService
from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal
from python_forestacion.excepciones.persistencia_exception import PersistenciaException
from python_forestacion.constantes import DIRECTORIO_DATA, EXTENSION_DATA

@pytest.fixture
def registro_service():
    return RegistroForestalService()

@pytest.fixture
def registro_completo():
    """Fixture for a complete RegistroForestal object."""
    tierra_service = TierraService()
    terreno = tierra_service.crear_tierra_con_plantacion(
        id_padron_catastral=999,
        superficie=1000.0,
        domicilio="Testlandia",
        nombre_plantacion="Finca de Prueba"
    )
    return RegistroForestal(
        id_padron=999,
        tierra=terreno,
        plantacion=terreno.get_finca(),
        propietario="Tester",
        avaluo=100.0
    )

def test_persistir_y_leer_registro(registro_service, registro_completo):
    """Tests that a forestry register can be persisted and read successfully."""
    propietario = registro_completo.get_propietario()
    ruta_archivo = os.path.join(DIRECTORIO_DATA, f"{propietario}{EXTENSION_DATA}")

    try:
        registro_service.persistir(registro_completo)
        assert os.path.exists(ruta_archivo)

        registro_leido = registro_service.leer_registro(propietario)
        
        assert registro_leido is not None
        assert registro_leido.get_propietario() == propietario
        assert registro_leido.get_tierra().get_superficie() == 1000.0
    finally:
        # Cleanup
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)

def test_leer_registro_no_existente(registro_service):
    """Tests that a PersistenciaException is raised when the register file does not exist."""
    with pytest.raises(PersistenciaException) as excinfo:
        registro_service.leer_registro("PropietarioFantasma")
    assert "No se encontro el registro solicitado" in excinfo.value.get_user_message()

def test_leer_registro_propietario_vacio(registro_service):
    """Tests that a ValueError is raised if the owner's name is empty."""
    with pytest.raises(ValueError):
        registro_service.leer_registro("")

def test_leer_registro_corrupto(registro_service):
    """Tests that a PersistenciaException is raised when the data file is corrupt."""
    propietario = "Corrupto"
    ruta_archivo = os.path.join(DIRECTORIO_DATA, f"{propietario}{EXTENSION_DATA}")

    # Create a corrupted (empty) file
    os.makedirs(DIRECTORIO_DATA, exist_ok=True)
    with open(ruta_archivo, 'w') as f:
        f.write("datos corruptos")

    try:
        with pytest.raises(PersistenciaException) as excinfo:
            registro_service.leer_registro(propietario)
        assert "Error de deserializacion (pickle)" in excinfo.value.get_technical_message()
    finally:
        # Cleanup
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
