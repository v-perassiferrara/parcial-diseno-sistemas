import time
from datetime import date

# Importaciones de entidades
from python_forestacion.entidades.personal.trabajador import Trabajador
from python_forestacion.entidades.personal.tarea import Tarea
from python_forestacion.entidades.personal.herramienta import Herramienta
from python_forestacion.entidades.terrenos.registro_forestal import RegistroForestal
from python_forestacion.entidades.cultivos.pino import Pino
from python_forestacion.entidades.cultivos.lechuga import Lechuga

# Importaciones de servicios
from python_forestacion.servicios.terrenos.tierra_service import TierraService
from python_forestacion.servicios.terrenos.plantacion_service import PlantacionService
from python_forestacion.servicios.terrenos.registro_forestal_service import RegistroForestalService
from python_forestacion.servicios.personal.trabajador_service import TrabajadorService
from python_forestacion.servicios.negocio.fincas_service import FincasService
from python_forestacion.servicios.cultivos.cultivo_service_registry import CultivoServiceRegistry

# Importaciones de riego
from python_forestacion.riego.sensores.temperatura_reader_task import TemperaturaReaderTask
from python_forestacion.riego.sensores.humedad_reader_task import HumedadReaderTask
from python_forestacion.riego.control.control_riego_task import ControlRiegoTask

# Importaciones de excepciones
from python_forestacion.excepciones.superficie_insuficiente_exception import SuperficieInsuficienteException
from python_forestacion.excepciones.persistencia_exception import PersistenciaException

# Importaciones de constantes
from python_forestacion.constantes import THREAD_JOIN_TIMEOUT


def main():
    """Punto de entrada principal de la aplicacion."""
    print("=" * 70)
    print("         SISTEMA DE GESTION FORESTAL - PATRONES DE DISENO")
    print("=" * 70)

    # ----------------------------------------------------------------------
    # PATRON SINGLETON: Inicializando servicios
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  PATRON SINGLETON: Inicializando servicios")
    print("-" * 70)

    tierra_service = TierraService()
    plantacion_service = PlantacionService()
    trabajador_service = TrabajadorService()
    registro_service = RegistroForestalService()
    fincas_service = FincasService()

    # Validar que el Registry es un Singleton
    registry1 = CultivoServiceRegistry.get_instance()
    registry2 = CultivoServiceRegistry.get_instance()
    if registry1 is registry2:
        print("[OK] Todos los servicios comparten la misma instancia del Registry")
    else:
        print("[ERROR] Las instancias del Registry son diferentes")

    # ----------------------------------------------------------------------
    # 1. Creacion de Entidades
    # ----------------------------------------------------------------------
    print("\n1. Creando tierra con plantacion...")
    terreno = tierra_service.crear_tierra_con_plantacion(
        id_padron_catastral=1,
        superficie=100.0,  # Superficie pequeña para probar limites
        domicilio="Agrelo, Mendoza",
        nombre_plantacion="Finca del Madero"
    )
    plantacion = terreno.get_finca()
    print(f"[OK] Plantacion '{plantacion.get_nombre()}' creada en '{terreno.get_domicilio()}' con {plantacion.get_superficie()} m².")

    registro = RegistroForestal(
        id_padron=1,
        tierra=terreno,
        plantacion=plantacion,
        propietario="Juan Perez",
        avaluo=50309233.55
    )
    print(f"[OK] Registro Forestal para '{registro.get_propietario()}' creado.")

    # ----------------------------------------------------------------------
    # 2. PATRON FACTORY: Plantando cultivos
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  PATRON FACTORY: Plantando cultivos")
    print("-" * 70)

    try:
        print("Plantando 5 Pinos...")
        plantacion_service.plantar(plantacion, "Pino", 5)
        print("Plantando 5 Olivos...")
        plantacion_service.plantar(plantacion, "Olivo", 5)
        print("Plantando 5 Lechugas...")
        plantacion_service.plantar(plantacion, "Lechuga", 5)
        print("Plantando 5 Zanahorias...")
        plantacion_service.plantar(plantacion, "Zanahoria", 5)
        print("[OK] Cultivos plantados exitosamente.")
    except SuperficieInsuficienteException as e:
        print(f"[!] ADVERTENCIA: {e.get_user_message()}")

    # ----------------------------------------------------------------------
    # 3. PATRON OBSERVER: Sistema de Riego Automatizado (20 segundos)
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  PATRON OBSERVER: Sistema de Riego Automatizado (20 segundos)")
    print("-" * 70)

    tarea_temp = TemperaturaReaderTask()
    tarea_hum = HumedadReaderTask()
    tarea_control = ControlRiegoTask(tarea_temp, tarea_hum, plantacion, plantacion_service)

    print("Iniciando sensores y control de riego...")
    tarea_temp.start()
    tarea_hum.start()
    tarea_control.start()

    time.sleep(20)

    print("\nDeteniendo sistema de riego...")
    tarea_temp.detener()
    tarea_hum.detener()
    tarea_control.detener()
    tarea_temp.join(timeout=THREAD_JOIN_TIMEOUT)
    tarea_hum.join(timeout=THREAD_JOIN_TIMEOUT)
    tarea_control.join(timeout=THREAD_JOIN_TIMEOUT)
    print("[OK] Sistema de riego detenido de forma segura.")

    # ----------------------------------------------------------------------
    # 4. Gestion de Personal
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  Gestion de Personal")
    print("-" * 70)

    tareas = [
        Tarea(1, date.today(), "Desmalezar"),
        Tarea(2, date.today(), "Abonar"),
        Tarea(3, date.today(), "Marcar surcos")
    ]
    trabajador = Trabajador(dni=43888734, nombre="Juan Perez", tareas=tareas)
    plantacion.set_trabajadores([trabajador])
    print(f"[OK] Trabajador '{trabajador.get_nombre()}' asignado a la plantacion.")

    print("\nAsignando apto medico...")
    trabajador_service.asignar_apto_medico(
        trabajador=trabajador,
        apto=True,
        fecha_emision=date.today(),
        observaciones="Estado de salud: excelente"
    )
    print("[OK] Apto medico asignado.")

    herramienta = Herramienta(id_herramienta=1, nombre="Pala", certificado_hys=True)
    print("\nEjecutando tareas del trabajador...")
    trabajador_service.trabajar(trabajador, date.today(), herramienta)

    # ----------------------------------------------------------------------
    # 5. Operaciones de Negocio y Persistencia
    # ----------------------------------------------------------------------
    print("\n" + "-" * 70)
    print("  Operaciones de Negocio y Persistencia")
    print("-" * 70)

    fincas_service.add_finca(registro)
    print("[OK] Finca agregada al servicio de gestion de fincas.")

    fincas_service.fumigar(id_padron=1, plaguicida="insecto organico")

    # Cosecha (usa Paquete generico)
    caja_lechugas = fincas_service.cosechar_yempaquetar(Lechuga)
    caja_lechugas.mostrar_contenido_caja()

    caja_pinos = fincas_service.cosechar_yempaquetar(Pino)
    caja_pinos.mostrar_contenido_caja()

    # Persistencia
    try:
        print("\nPersistiendo registro...")
        registro_service.persistir(registro)
    except PersistenciaException as e:
        print(f"[!] ERROR: {e.get_user_message()}")

    # Lectura
    try:
        print("\nLeyendo registro desde disco...")
        registro_leido = RegistroForestalService.leer_registro("Juan Perez")
        registro_service.mostrar_datos(registro_leido)
    except (PersistenciaException, ValueError) as e:
        print(f"[!] ERROR: {e}")

    # ----------------------------------------------------------------------
    # Finalizacion
    # ----------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("              EJEMPLO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
    print("  [OK] SINGLETON   - CultivoServiceRegistry (instancia unica)")
    print("  [OK] FACTORY     - Creacion de cultivos")
    print("  [OK] OBSERVER    - Sistema de sensores y eventos")
    print("  [OK] STRATEGY    - Algoritmos de absorcion de agua")
    print("=" * 70)

if __name__ == "__main__":
    main()
