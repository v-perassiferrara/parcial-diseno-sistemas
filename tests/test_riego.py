
import unittest
from unittest.mock import Mock, patch
import threading

from python_forestacion.riego.control.control_riego_task import ControlRiegoTask
from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask
from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
from python_forestacion.excepciones.agua_agotada_exception import AguaAgotadaException
from python_forestacion.constantes import SENSOR_HUMEDAD_MIN, SENSOR_HUMEDAD_MAX, SENSOR_TEMP_MIN, SENSOR_TEMP_MAX, TEMP_MIN_RIEGO, HUMEDAD_MAX_RIEGO


class TestRiego(unittest.TestCase):

    def setUp(self):
        self.mock_plantacion = Mock()
        self.mock_plantacion_service = Mock()
        self.mock_sensor_temp = Mock(spec=TemperaturaReaderTask)
        self.mock_sensor_hum = Mock(spec=HumedadReaderTask)

        self.control_riego = ControlRiegoTask(
            sensor_temperatura=self.mock_sensor_temp,
            sensor_humedad=self.mock_sensor_hum,
            plantacion=self.mock_plantacion,
            plantacion_service=self.mock_plantacion_service
        )

    def test_sensor_temperatura_lee_en_rango(self):
        """Verifica que el sensor de temperatura genere valores dentro del rango."""
        sensor = TemperaturaReaderTask()
        temp = sensor._leer_temperatura()
        self.assertGreaterEqual(temp, SENSOR_TEMP_MIN)
        self.assertLessEqual(temp, SENSOR_TEMP_MAX)

    def test_sensor_humedad_lee_en_rango(self):
        """Verifica que el sensor de humedad genere valores dentro del rango."""
        sensor = HumedadReaderTask()
        humedad = sensor._leer_humedad()
        self.assertGreaterEqual(humedad, SENSOR_HUMEDAD_MIN)
        self.assertLessEqual(humedad, SENSOR_HUMEDAD_MAX)

    def test_control_riego_actualizar(self):
        """Verifica que el controlador actualice sus valores internos desde los sensores."""
        self.control_riego.actualizar(30.5)  # Simula temperatura
        self.assertEqual(self.control_riego._ultima_temperatura, 30.5)

        self.control_riego.actualizar(75.2)  # Simula humedad
        self.assertEqual(self.control_riego._ultima_humedad, 75.2)

    def test_evaluar_condiciones_riego_optimo(self):
        """Verifica que se inicie el riego bajo condiciones óptimas."""
        # Condiciones óptimas
        self.control_riego._ultima_temperatura = TEMP_MIN_RIEGO + 5
        self.control_riego._ultima_humedad = HUMEDAD_MAX_RIEGO - 10

        self.control_riego._evaluar_condiciones_y_regar()

        self.mock_plantacion_service.regar.assert_called_once_with(self.mock_plantacion)

    def test_evaluar_condiciones_no_regar_por_temperatura(self):
        """Verifica que no se riegue si la temperatura no es la adecuada."""
        # Temperatura demasiado alta
        self.control_riego._ultima_temperatura = 50
        self.control_riego._ultima_humedad = 50

        self.control_riego._evaluar_condiciones_y_regar()

        self.mock_plantacion_service.regar.assert_not_called()

    def test_evaluar_condiciones_no_regar_por_humedad(self):
        """Verifica que no se riegue si la humedad es demasiado alta."""
        self.control_riego._ultima_temperatura = 20
        self.control_riego._ultima_humedad = 90

        self.control_riego._evaluar_condiciones_y_regar()

        self.mock_plantacion_service.regar.assert_not_called()

    def test_manejo_excepcion_agua_agotada(self):
        """Verifica que se maneje la excepción AguaAgotadaException."""
        # Condiciones optimas para que se llame a regar
        self.control_riego._ultima_temperatura = 10
        self.control_riego._ultima_humedad = 40

        self.mock_plantacion_service.regar.side_effect = AguaAgotadaException(agua_requerida=50, agua_disponible=10)

        try:
            self.control_riego._evaluar_condiciones_y_regar()
        except Exception as e:
            self.fail(f"_evaluar_condiciones_y_regar() lanzó una excepción no esperada: {e}")

        self.mock_plantacion_service.regar.assert_called_once()

    @patch('time.sleep')
    def test_run_y_detener_sensores(self, mock_sleep):
        """Verifica que los hilos de los sensores puedan iniciarse y detenerse."""
        sensor_temp = TemperaturaReaderTask()
        sensor_hum = HumedadReaderTask()

        # Mock para evitar que el bucle se ejecute más de una vez en el test
        sensor_temp._detenido.set()
        sensor_hum._detenido.set()

        sensor_temp.start()
        sensor_hum.start()

        sensor_temp.join(timeout=1)
        sensor_hum.join(timeout=1)

        self.assertFalse(sensor_temp.is_alive())
        self.assertFalse(sensor_hum.is_alive())


if __name__ == '__main__':
    unittest.main()
