
import pytest
from python_forestacion.entidades.cultivos.arbol import Arbol
from python_forestacion.entidades.cultivos.pino import Pino


def test_cultivo_set_superficie_negativa_falla():
    """Verifica que no se pueda asignar una superficie negativa a un cultivo."""
    with pytest.raises(ValueError):
        # Usamos Pino como una implementacion concreta de Cultivo/Arbol
        pino = Pino("pino_test")
        pino.set_superficie(-10.0)

def test_cultivo_set_agua_negativa_falla():
    """Verifica que no se pueda asignar una cantidad de agua negativa."""
    with pytest.raises(ValueError):
        pino = Pino("pino_test")
        pino.set_agua(-100)

def test_arbol_set_altura_negativa_falla():
    """Verifica que no se pueda asignar una altura negativa a un arbol."""
    with pytest.raises(ValueError):
        pino = Pino("pino_test")
        pino.set_altura(-1.0)
