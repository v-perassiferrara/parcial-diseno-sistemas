import threading
import time
from typing import TYPE_CHECKING
from python_forestacion.patrones.observer.observer import Observer
from python_forestacion.patrones.observer.eventos.evento_sensor import EventoSensor
from python_forestacion.constantes import TEMP_MIN_RIEGO, TEMP_MAX_RIEGO, HUMEDAD_MAX_RIEGO, INTERVALO_CONTROL_RIEGO
from python_forestacion.excepciones.agua_agotada_exception import AguaAgotadaException

if TYPE_CHECKING:
    from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
    from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask
    from python_forestacion.entidades.terrenos.plantacion import Plantacion
    from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService

class ControlRiegoTask(threading.Thread, Observer[EventoSensor]):
    """Controlador de riego que observa los sensores y reacciona a eventos."""

    def __init__(
        self,
        sensor_temperatura: 'TemperaturaReaderTask',
        sensor_humedad: 'HumedadReaderTask',
        plantacion: 'Plantacion',
        plantacion_service: 'PlantacionService'
    ):
        threading.Thread.__init__(self, daemon=True)
        self._plantacion = plantacion
        self._plantacion_service = plantacion_service
        self._ultima_temperatura: float = 20.0  # Valor inicial seguro
        self._ultima_humedad: float = 60.0     # Valor inicial seguro
        self._detenido = threading.Event()

        # Suscribirse a los sensores
        sensor_temperatura.agregar_observador(self)
        sensor_humedad.agregar_observador(self)

    def actualizar(self, evento: EventoSensor) -> None:
        """Este metodo es llamado por los sensores (Observable) cuando hay un nuevo evento."""
        if evento.tipo_sensor == "temperatura":
            self._ultima_temperatura = evento.valor
        elif evento.tipo_sensor == "humedad":
            self._ultima_humedad = evento.valor

    def _evaluar_condiciones_y_regar(self) -> None:
        temp = self._ultima_temperatura
        hum = self._ultima_humedad

        print(f"[Control Riego] Evaluando: Temp={temp:.2f}°C, Hum={hum:.2f}%")

        if (TEMP_MIN_RIEGO <= temp <= TEMP_MAX_RIEGO) and (hum <= HUMEDAD_MAX_RIEGO):
            try:
                print(f"[Control Riego] *** CONDICIONES OPTIMAS - REGANDO ***")
                self._plantacion_service.regar(self._plantacion)
                print(f"[Control Riego] Riego finalizado. Agua restante: {self._plantacion.get_agua_disponible()} L")
            except AguaAgotadaException as e:
                print(f"[Control Riego] [!] ADVERTENCIA: {e.get_user_message()}")
        else:
            print("[Control Riego] Condiciones no optimas para riego.")

    def run(self) -> None:
        print("[INFO] Control de Riego iniciado. Esperando lecturas de sensores...")
        while not self._detenido.is_set():
            self._evaluar_condiciones_y_regar()
            # La evaluación ahora podría ser menos frecuente o incluso eliminarse si
            # la lógica de riego se moviera completamente dentro de 'actualizar'.
            # Por ahora, se mantiene para no alterar demasiado el flujo.
            time.sleep(INTERVALO_CONTROL_RIEGO)

    def detener(self) -> None:
        self._detenido.set()
