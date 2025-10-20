
import unittest
from unittest.mock import Mock

from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry


class TestRegistry(unittest.TestCase):

    def setUp(self):
        # Usamos get_instance() para asegurarnos de que el singleton está inicializado
        self.registry = CultivoServiceRegistry.get_instance()

    def test_absorber_agua_handler_no_existente(self):
        """Verifica que se lance un ValueError si no hay handler de absorción."""
        class CultivoFalso:
            pass

        cultivo_falso = CultivoFalso()
        with self.assertRaises(ValueError):
            self.registry.absorber_agua(cultivo_falso)

    def test_mostrar_datos_handler_no_existente(self):
        """Verifica que se lance un ValueError si no hay handler de mostrar datos."""
        class CultivoFalso:
            pass

        cultivo_falso = CultivoFalso()
        with self.assertRaises(ValueError):
            self.registry.mostrar_datos(cultivo_falso)


if __name__ == '__main__':
    unittest.main()
