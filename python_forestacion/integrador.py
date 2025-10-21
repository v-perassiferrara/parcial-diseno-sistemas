"""
Archivo integrador generado automaticamente
Directorio: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion
Fecha: 2025-10-21 19:58:16
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: __init__.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\__init__.py
# ================================================================================



# ================================================================================
# ARCHIVO 2/2: constantes.py
# Ruta: C:\Users\Valen\Desktop\parcial-diseno-sistemas\python_forestacion\constantes.py
# ================================================================================

# Constantes del sistema de Gestion Forestal

# Agua
AGUA_MINIMA = 10
AGUA_INICIAL_PLANTACION = 500
AGUA_CONSUMIDA_RIEGO = 10

# Riego
TEMP_MIN_RIEGO = 8
TEMP_MAX_RIEGO = 15
HUMEDAD_MAX_RIEGO = 50
INTERVALO_CONTROL_RIEGO = 2.5  # segundos

# Sensores
INTERVALO_SENSOR_TEMPERATURA = 2.0  # segundos
SENSOR_TEMP_MIN = -25  # °C
SENSOR_TEMP_MAX = 50  # °C
INTERVALO_SENSOR_HUMEDAD = 3.0  # segundos
SENSOR_HUMEDAD_MIN = 0  # %
SENSOR_HUMEDAD_MAX = 100  # %

# Cultivos
# Pino
SUPERFICIE_PINO = 2.0
AGUA_INICIAL_PINO = 2
ALTURA_INICIAL_ARBOL = 1.0
CRECIMIENTO_PINO = 0.10

# Olivo
SUPERFICIE_OLIVO = 3.0
AGUA_INICIAL_OLIVO = 5
CRECIMIENTO_OLIVO = 0.01

# Lechuga
SUPERFICIE_LECHUGA = 0.10
AGUA_INICIAL_LECHUGA = 1

# Zanahoria
SUPERFICIE_ZANAHORIA = 0.15
AGUA_INICIAL_ZANAHORIA = 0

# Estrategia de absorcion
MES_INICIO_VERANO = 3  # Marzo
MES_FIN_VERANO = 8   # Agosto
ABSORCION_SEASONAL_VERANO = 5
ABSORCION_SEASONAL_INVIERNO = 2
ABSORCION_CONSTANTE_LECHUGA = 1
ABSORCION_CONSTANTE_ZANAHORIA = 2

# Persistencia
DIRECTORIO_DATA = "data"
EXTENSION_DATA = ".dat"

# Threading
THREAD_JOIN_TIMEOUT = 2.0  # segundos


