"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\sensores
Fecha: 2025-10-21 19:58:15
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\sensores\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/3: humedad_reader_task.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\sensores\humedad_reader_task.py
# ================================================================================

import threading
import time
import random
from datetime import datetime
from python_forestacion.patrones.observer.observable import Observable
from python_forestacion.patrones.observer.eventos.evento_sensor import EventoSensor
from python_forestacion.constantes import INTERVALO_SENSOR_HUMEDAD, SENSOR_HUMEDAD_MIN, SENSOR_HUMEDAD_MAX

class HumedadReaderTask(threading.Thread, Observable[EventoSensor]):
    """Sensor de humedad que se ejecuta en un hilo separado y notifica eventos."""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._detenido = threading.Event()

    def _leer_humedad(self) -> float:
        return random.uniform(SENSOR_HUMEDAD_MIN, SENSOR_HUMEDAD_MAX)

    def run(self) -> None:
        while not self._detenido.is_set():
            humedad = self._leer_humedad()
            evento = EventoSensor(
                tipo_sensor="humedad",
                valor=humedad,
                timestamp=datetime.now()
            )
            self.notificar_observadores(evento)
            time.sleep(INTERVALO_SENSOR_HUMEDAD)

    def detener(self) -> None:
        self._detenido.set()


# ================================================================================
# ARCHIVO 3/3: temperatura_reader_task.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\riego\sensores\temperatura_reader_task.py
# ================================================================================

import threading
import time
import random
from datetime import datetime
from python_forestacion.patrones.observer.observable import Observable
from python_forestacion.patrones.observer.eventos.evento_sensor import EventoSensor
from python_forestacion.constantes import INTERVALO_SENSOR_TEMPERATURA, SENSOR_TEMP_MIN, SENSOR_TEMP_MAX

class TemperaturaReaderTask(threading.Thread, Observable[EventoSensor]):
    """Sensor de temperatura que se ejecuta en un hilo separado y notifica eventos."""

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        self._detenido = threading.Event()

    def _leer_temperatura(self) -> float:
        return random.uniform(SENSOR_TEMP_MIN, SENSOR_TEMP_MAX)

    def run(self) -> None:
        while not self._detenido.is_set():
            temperatura = self._leer_temperatura()
            evento = EventoSensor(
                tipo_sensor="temperatura",
                valor=temperatura,
                timestamp=datetime.now()
            )
            self.notificar_observadores(evento)
            time.sleep(INTERVALO_SENSOR_TEMPERATURA)

    def detener(self) -> None:
        self._detenido.set()


