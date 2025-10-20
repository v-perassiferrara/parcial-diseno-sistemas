class MensajesException:
    """Clase que centraliza los mensajes de error del sistema."""

    # Superficie
    SUPERFICIE_INSUFICIENTE_USER = "No hay suficiente superficie disponible en la plantacion."
    SUPERFICIE_INSUFICIENTE_TECH = "La superficie requerida ({requerida} m²) es mayor que la disponible ({disponible} m²)."

    # Agua
    AGUA_AGOTADA_USER = "No hay suficiente agua en la plantacion para regar."
    AGUA_AGOTADA_TECH = "Se requieren {requerida} L de agua, pero solo hay {disponible} L disponibles."

    # Persistencia
    PERSISTENCIA_ESCRITURA_USER = "Ocurrio un error al intentar guardar el registro."
    PERSISTENCIA_ESCRITURA_TECH = "Error de I/O al escribir en el archivo: {archivo}."
    PERSISTENCIA_LECTURA_USER = "Ocurrio un error al intentar leer el registro."
    PERSISTENCIA_LECTURA_TECH = "Error de I/O al leer el archivo: {archivo}."
    PERSISTENCIA_NOT_FOUND_USER = "No se encontro el registro solicitado."
    PERSISTENCIA_NOT_FOUND_TECH = "El archivo de datos no existe: {archivo}."
    PERSISTENCIA_CORRUPTO_USER = "El archivo de registro parece estar corrupto."
    PERSISTENCIA_CORRUPTO_TECH = "Error de deserializacion (pickle) en el archivo: {archivo}."
