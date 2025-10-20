import threading
import time
import random
from python_forestacion.patrones.observer.observable import Observable
from python_forestacion.constantes import INTERVALO_SENSOR_HUMEDAD, SENSOR_HUMEDAD_MIN, SENSOR_HUMEDAD_MAX

class HumedadReaderTask(threading.Thread, Observable[float]):
    """Sensor de humedad que se ejecuta en un hilo separado."""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._detenido = threading.Event()

    def _leer_humedad(self) -> float:
        return random.uniform(SENSOR_HUMEDAD_MIN, SENSOR_HUMEDAD_MAX)

    def run(self) -> None:
        while not self._detenido.is_set():
            humedad = self._leer_humedad()
            # print(f"[Sensor Humedad] Lectura: {humedad:.2f}%") # Descomentar para debug
            self.notificar_observadores(humedad)
            time.sleep(INTERVALO_SENSOR_HUMEDAD)

    def detener(self) -> None:
        self._detenido.set()
