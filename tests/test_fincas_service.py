
import unittest
from unittest.mock import Mock, MagicMock

from python_forestacion.entidades.cultivos.pino import Pino
from python_forestacion.entidades.cultivos.zanahoria import Zanahoria
from python_forestacion.servicios.negocio.fincas_service import FincasService
from python_forestacion.servicios.negocio.paquete import Paquete


class TestFincasService(unittest.TestCase):

    def setUp(self):
        self.fincas_service = FincasService()

        # Mock para finca 1
        self.mock_registro1 = Mock()
        self.mock_plantacion1 = Mock()
        self.mock_registro1.get_id_padron.return_value = 1
        self.mock_registro1.get_plantacion.return_value = self.mock_plantacion1
        self.mock_plantacion1.get_nombre.return_value = "Finca 1"
        self.cultivos1 = [Pino("pino1"), Pino("pino2"), Zanahoria(True)]
        self.mock_plantacion1.get_cultivos_interno.return_value = self.cultivos1

        # Mock para finca 2
        self.mock_registro2 = Mock()
        self.mock_plantacion2 = Mock()
        self.mock_registro2.get_id_padron.return_value = 2
        self.mock_registro2.get_plantacion.return_value = self.mock_plantacion2
        self.mock_plantacion2.get_nombre.return_value = "Finca 2"
        self.cultivos2 = [Pino("pino3"), Zanahoria(False), Zanahoria(True)]
        self.mock_plantacion2.get_cultivos_interno.return_value = self.cultivos2

    def test_add_finca_y_buscar_finca(self):
        """Verifica que se pueda agregar y buscar una finca."""
        self.fincas_service.add_finca(self.mock_registro1)
        encontrado = self.fincas_service.buscar_finca(1)
        self.assertEqual(encontrado, self.mock_registro1)
        no_encontrado = self.fincas_service.buscar_finca(99)
        self.assertIsNone(no_encontrado)

    def test_fumigar(self):
        """Verifica la lógica de fumigación."""
        self.fincas_service.add_finca(self.mock_registro1)
        # No podemos verificar el print directamente sin más mocks,
        # pero podemos asegurar que no lance errores.
        try:
            self.fincas_service.fumigar(1, "plaguicida_test")
            self.fincas_service.fumigar(99, "plaguicida_test")  # Probar con finca no existente
        except Exception as e:
            self.fail(f"fumigar() lanzó una excepción inesperada: {e}")

    def test_cosechar_y_empaquetar_cultivo_existente(self):
        """Verifica que se cosechen y empaqueten los cultivos correctos."""
        self.fincas_service.add_finca(self.mock_registro1)
        self.fincas_service.add_finca(self.mock_registro2)

        paquete_pinos = self.fincas_service.cosechar_yempaquetar(Pino)

        self.assertIsInstance(paquete_pinos, Paquete)
        self.assertEqual(len(paquete_pinos.get_contenido()), 3)
        self.assertEqual(paquete_pinos.get_tipo_contenido(), Pino)

        # Verifica que los cultivos fueron removidos de las plantaciones
        self.assertEqual(len(self.cultivos1), 1)
        self.assertIsInstance(self.cultivos1[0], Zanahoria)
        self.assertEqual(len(self.cultivos2), 2)
        self.assertIsInstance(self.cultivos2[0], Zanahoria)
        self.assertIsInstance(self.cultivos2[1], Zanahoria)

    def test_cosechar_y_empaquetar_cultivo_inexistente(self):
        """Verifica el comportamiento al cosechar un tipo de cultivo que no existe."""
        self.fincas_service.add_finca(self.mock_registro1)

        # Mock de un tipo de cultivo no presente
        class FalsoCultivo:
            pass

        paquete_vacio = self.fincas_service.cosechar_yempaquetar(FalsoCultivo)

        self.assertIsInstance(paquete_vacio, Paquete)
        self.assertEqual(len(paquete_vacio.get_contenido()), 0)
        self.assertEqual(paquete_vacio.get_tipo_contenido(), FalsoCultivo)


if __name__ == '__main__':
    unittest.main()

