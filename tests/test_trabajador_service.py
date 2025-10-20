import pytest
from datetime import date
from python_forestacion.entidades.personal.trabajador import Trabajador
from python_forestacion.entidades.personal.tarea import Tarea
from python_forestacion.entidades.personal.herramienta import Herramienta
from python_forestacion.servicios.personal.trabajador_service import TrabajadorService

@pytest.fixture
def trabajador_service():
    return TrabajadorService()

@pytest.fixture
def herramienta_comun():
    return Herramienta(id_herramienta=1, nombre="Pala", certificado_hys=True)

@pytest.fixture
def tareas_diarias():
    return [
        Tarea(1, date.today(), "Desmalezar"),
        Tarea(2, date.today(), "Abonar"),
    ]

def test_trabajador_con_apto_trabaja(trabajador_service, tareas_diarias, herramienta_comun, capsys):
    """Tests that a worker with medical clearance can work and completes tasks."""
    trabajador = Trabajador(dni=123, nombre="Pepe", tareas=tareas_diarias)
    trabajador_service.asignar_apto_medico(trabajador, True, date.today(), "OK")
    
    resultado = trabajador_service.trabajar(trabajador, date.today(), herramienta_comun)
    
    assert resultado is True
    captured = capsys.readouterr()
    assert "realizo la tarea 2" in captured.out
    assert "realizo la tarea 1" in captured.out
    assert all(t.is_completada() for t in tareas_diarias)

def test_trabajador_sin_apto_no_trabaja(trabajador_service, tareas_diarias, herramienta_comun, capsys):
    """Tests that a worker without medical clearance cannot work."""
    trabajador = Trabajador(dni=123, nombre="Pepe", tareas=tareas_diarias)
    # No se asigna apto medico
    
    resultado = trabajador_service.trabajar(trabajador, date.today(), herramienta_comun)
    
    assert resultado is False
    captured = capsys.readouterr()
    assert "no tiene apto medico vigente" in captured.out
    assert not any(t.is_completada() for t in tareas_diarias)

def test_trabajador_con_apto_false_no_trabaja(trabajador_service, tareas_diarias, herramienta_comun, capsys):
    """Tests that a worker with a non-valid medical clearance cannot work."""
    trabajador = Trabajador(dni=123, nombre="Pepe", tareas=tareas_diarias)
    trabajador_service.asignar_apto_medico(trabajador, False, date.today(), "Enfermo")

    resultado = trabajador_service.trabajar(trabajador, date.today(), herramienta_comun)
    
    assert resultado is False
    captured = capsys.readouterr()
    assert "no tiene apto medico vigente" in captured.out
