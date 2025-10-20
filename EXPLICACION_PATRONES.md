# Análisis Exhaustivo del Proyecto "PythonForestal"

## 1. Visión General del Proyecto

- **Propósito y Alcance:** El proyecto "PythonForestal" es un sistema de software diseñado para simular la gestión integral de fincas agrícolas y forestales. Su alcance abarca desde la administración de terrenos y la plantación de diversos tipos de cultivos hasta la gestión de personal, el monitoreo ambiental con un sistema de riego automatizado y la persistencia de datos. El proyecto sirve como un caso de estudio práctico y educativo para la aplicación de principios de arquitectura de software y patrones de diseño en un dominio de negocio complejo.

- **Problema que Resuelve:** Aborda la complejidad de la gestión agrícola moderna, que incluye la optimización del uso de la tierra, la gestión de recursos hídricos, el seguimiento de múltiples tipos de cultivos con diferentes ciclos de vida y necesidades, la administración de personal y la necesidad de mantener registros trazables y auditables.

- **Funcionalidades Principales (según User Stories):**
    - **Gestión de Terrenos y Plantaciones:** Registrar terrenos, crear plantaciones asociadas y agrupar todo en un `RegistroForestal`.
    - **Gestión de Cultivos:** Plantar y gestionar 4 tipos de cultivos (Pino, Olivo, Lechuga, Zanahoria), cada uno con características y requisitos de superficie específicos.
    - **Sistema de Riego:** Regar todos los cultivos de una plantación, consumiendo agua del reservorio de la plantación y aplicando diferentes lógicas de absorción de agua según el tipo de cultivo.
    - **Riego Automatizado:** Monitorear sensores de temperatura y humedad en tiempo real (simulados con hilos) y activar el riego automáticamente bajo condiciones específicas.
    - **Gestión de Personal:** Registrar trabajadores, asignarles tareas y validar su aptitud médica antes de permitirles trabajar.
    - **Operaciones de Negocio:** Gestionar múltiples fincas, realizar fumigaciones y cosechar cultivos de un tipo específico para empaquetarlos.
    - **Persistencia de Datos:** Guardar y recuperar el estado completo de un `RegistroForestal` en el disco utilizando serialización (`pickle`).

- **Tecnologías y Frameworks:**
    - **Lenguaje:** Python 3.13.
    - **Frameworks/Librerías Externas:** Ninguna. El proyecto se basa exclusivamente en la **biblioteca estándar de Python**, lo que demuestra un profundo conocimiento del lenguaje base.
    - **Concurrencia:** Módulo `threading` para simular el sistema de riego concurrente.
    - **Persistencia:** Módulo `pickle` para la serialización de objetos.
    - **Principios de Diseño:** Fuerte adhesión a los principios SOLID y de Código Limpio.

## 2. Arquitectura del Sistema

- **Arquitectura General:** El proyecto implementa una **Arquitectura en Capas (Layered Architecture)** clásica y bien definida. Esta elección es ideal para separar las responsabilidades y reducir el acoplamiento entre los diferentes componentes del sistema.

- **Organización de Directorios y Módulos:** La estructura del proyecto refleja claramente la arquitectura en capas:
    - `python_forestacion/entidades/`: **Capa de Dominio/Modelos**. Contiene los objetos de datos puros (POJOs/DTOs) que representan el estado del sistema (ej. `Cultivo`, `Plantacion`, `Trabajador`). No contienen lógica de negocio.
    - `python_forestacion/servicios/`: **Capa de Lógica de Negocio (Capa de Servicio)**. Contiene toda la lógica de negocio que opera sobre las entidades. Está subdividida por dominio (`cultivos`, `terrenos`, `personal`, `negocio`).
    - `python_forestacion/patrones/`: **Capa de Soporte/Utilidades**. Contiene implementaciones genéricas y reutilizables de los patrones de diseño (Factory, Observer, Strategy, Singleton).
    - `python_forestacion/riego/`: **Módulo de Concurrencia**. Un subsistema autocontenido que maneja la simulación del riego automatizado.
    - `python_forestacion/excepciones/`: **Módulo de Manejo de Errores**. Define una jerarquía de excepciones personalizadas para el dominio.
    - `main.py`: **Capa de Presentación (simulada)**. Actúa como el punto de entrada y el cliente del sistema, orquestando las llamadas a los servicios para demostrar la funcionalidad.

- **Diagrama Conceptual de la Arquitectura (Texto):**

    ```
    +------------------------------------------------+
    |         Capa de Presentación (main.py)         |
    | (Orquesta el flujo de la demo, inicia servicios)|
    +------------------------+-----------------------+
                             |
                             v
    +------------------------+-----------------------+
    | Capa de Lógica de Negocio (Servicios)          |
    | (servicios.negocio -> fincas_service.py)       |
    | (servicios.terrenos -> plantacion_service.py)  |
    | (Contiene la lógica de negocio principal)      |
    +------------------------+-----------------------+
                             |
                             v
    +------------------------+-----------------------+
    |    Capa de Dominio/Entidades (entidades)       |
    | (entidades.cultivos -> cultivo.py)             |
    | (POJOs que representan el estado del sistema)  |
    +------------------------+-----------------------+
                             |
                             v
    +------------------------+-----------------------+
    |   Capa de Patrones y Utilidades (patrones)     |
    | (patrones.factory, patrones.strategy, etc.)    |
    | (Componentes reutilizables y transversales)    |
    +------------------------------------------------+
    ```

- **Relación entre Componentes:** La comunicación es unidireccional y descendente. La capa de presentación llama a los servicios, los servicios operan sobre las entidades y utilizan los patrones/utilidades. Las entidades no conocen a los servicios, y los servicios no conocen a la capa de presentación, lo que respeta el **Principio de Inversión de Dependencias**.

## 3. Patrones de Diseño Implementados

### 1. **Singleton**
- **Tipo:** Creacional.
- **Implementación:** `python_forestacion/servicios/cultivos/cultivo_service_registry.py`.
    ```python
    class CultivoServiceRegistry:
        _instance = None
        _lock = Lock()

        def __new__(cls):
            if cls._instance is None:
                with cls._lock:  # Thread-safe
                    if cls._instance is None:
                        cls._instance = super().__new__(cls)
            return cls._instance
    ```
- **Por qué se utiliza:** Para garantizar que exista una única instancia del `CultivoServiceRegistry` en todo el sistema. Esto es crucial porque el *registry* mantiene un estado centralizado (los diccionarios de *handlers* para cada tipo de cultivo) que debe ser consistente y accesible globalmente por todos los servicios que lo necesiten.
- **Beneficios:**
    - **Punto de Acceso Global:** Proporciona un único punto de acceso a los servicios de cultivo.
    - **Consistencia de Estado:** Evita tener múltiples registros de servicios que podrían desincronizarse.
    - **Eficiencia:** La inicialización de los servicios internos se realiza una sola vez.
    - **Seguridad en Hilos (Thread-Safety):** La implementación con `threading.Lock` y el patrón de "double-checked locking" asegura que la creación de la instancia sea segura incluso en un entorno concurrente.

### 2. **Factory Method**
- **Tipo:** Creacional.
- **Implementación:** `python_forestacion/patrones/factory/cultivo_factory.py`.
    ```python

        # CultivoFactory es el Creator/Factory

        # crear_cultivo() es el FactoryMethod

        # Cultivo es el Product (genérico)

        # Pino, Olivo, ... son los ConcreteProduct


    class CultivoFactory:   
        @staticmethod
        def crear_cultivo(especie: str) -> 'Cultivo':

            factories = {
                "Pino": CultivoFactory._crear_pino,     
                "Olivo": CultivoFactory._crear_olivo,
                # ...
            }
            if especie not in factories:
                raise ValueError(...)
            return factories[especie]()
    ```

>"Cabe destacar que esta implementación es una variación muy común conocida como 'Fábrica Simple' (o Static Factory). Se diferencia del patrón "Factory Method" clásico en que no utiliza herencia; en lugar de tener un Creator abstracto y ConcreteCreators (subclases) que deciden qué instanciar, esta versión centraliza toda la lógica de creación en una única clase (CultivoFactory) con un único método que decide qué producto crear."

- **Por qué se utiliza:** Para desacoplar el código cliente (como `PlantacionService`) de la lógica de creación de objetos `Cultivo`. El cliente solo necesita saber la *especie* que quiere crear (un string), y la fábrica se encarga de la instanciación concreta.
- **Beneficios:**
    - **Desacoplamiento:** El `PlantacionService` no necesita importar `Pino`, `Olivo`, etc. Solo interactúa con la fábrica y la interfaz `Cultivo`.
    - **Centralización:** La lógica de creación está en un solo lugar, facilitando su mantenimiento.
    - **Extensibilidad (Principio Abierto/Cerrado):** Para añadir un nuevo tipo de cultivo, solo es necesario modificar la fábrica, sin tocar el código cliente que la utiliza.>=

### 3. **Observer**
- **Tipo:** Comportamental.
- **Implementación:**
    - `patrones/observer/observable.py`: Clase base `Observable[T]`.
    - `patrones/observer/observer.py`: Interfaz `Observer[T]`.
    - `riego/sensores/`: Los sensores (`TemperaturaReaderTask`, `HumedadReaderTask`) son `Observable`.
    - `riego/control/control_riego_task.py`: El `ControlRiegoTask` es un `Observer`.
- **Por qué se utiliza:** Para permitir que el `ControlRiegoTask` reaccione a los cambios en los sensores de temperatura y humedad sin estar fuertemente acoplado a ellos. Los sensores notifican a cualquier observador suscrito cuando tienen una nueva lectura.
- **Beneficios:**
    - **Desacoplamiento:** Los sensores no saben quién los observa, solo que deben notificar eventos. El controlador no sabe cómo los sensores obtienen los datos, solo que recibirá actualizaciones.
    - **Difusión de Eventos:** Un sensor puede notificar a múltiples observadores simultáneamente.
    - **Tipo-Seguridad:** El uso de `Generic[T]` (`Observable[float]`) asegura en tiempo de análisis estático que los sensores solo pueden emitir eventos de tipo `float`, y los observadores esperan recibir ese tipo.

### 4. **Strategy**
- **Tipo:** Comportamental.
- **Implementación:**
    - `patrones/strategy/absorcion_agua_strategy.py` (**Strategy**): Interfaz `AbsorcionAguaStrategy`.
    - `patrones/strategy/impl/` (**ConcreteStrategies**): Implementaciones concretas (`AbsorcionSeasonalStrategy` para árboles, `AbsorcionConstanteStrategy` para hortalizas).
    - `servicios/cultivos/cultivo_service.py` (**Contexto**): El servicio base tiene una referencia a una estrategia.
    - `servicios/cultivos/pino_service.py`, `lechuga_service.py`, etc.: Inyectan la estrategia apropiada en el constructor.
    ```python
    # Inyección de la estrategia en el servicio
    class PinoService(ArbolService):
        def __init__(self):
            super().__init__(AbsorcionSeasonalStrategy())
    ```
- **Por qué se utiliza:** Para definir una familia de algoritmos (las formas de absorber agua), encapsular cada uno y hacerlos intercambiables. Esto permite que la lógica de absorción de agua varíe independientemente de los servicios de cultivo que la utilizan.
- **Beneficios:**
    - **Elimina Condicionales:** Evita tener un `if/elif/else` dentro del `CultivoService` para decidir cómo absorber agua según el tipo de cultivo.
    - **Principio Abierto/Cerrado:** Se pueden añadir nuevas estrategias de absorción sin modificar los servicios existentes.
    - **Flexibilidad:** La estrategia podría incluso cambiarse en tiempo de ejecución si fuera necesario.

### 5. **Registry** (Bonus)
- **Tipo:** Estructural (a menudo considerado un patrón arquitectónico).
- **Implementación:** `python_forestacion/servicios/cultivos/cultivo_service_registry.py`.
    ```python
    class CultivoServiceRegistry:
        def __init__(self):
            self._absorber_agua_handlers: Dict[Type['Cultivo'], Callable] = {
                Pino: self._absorber_agua_pino,
                Olivo: self._absorber_agua_olivo,
                # ...
            }
        def absorber_agua(self, cultivo: 'Cultivo') -> int:
            handler = self._absorber_agua_handlers.get(type(cultivo))
            return handler(cultivo)
    ```
- **Por qué se utiliza:** Para realizar un "despacho polimórfico" basado en el tipo de la clase. En lugar de usar una cadena de `isinstance(cultivo, Pino)`, `isinstance(cultivo, Olivo)`, etc., se utiliza un diccionario que mapea directamente el tipo de la clase (`Pino`) a la función que debe manejarlo.
- **Beneficios:**
    - **Código más Limpio y Mantenible:** Elimina las feas y frágiles cadenas de `isinstance`.
    - **Rendimiento:** El acceso a un diccionario (`O(1)`) es más rápido que una serie de comprobaciones de tipo.
    - **Extensibilidad:** Para soportar un nuevo tipo de cultivo, solo hay que añadir una nueva entrada al diccionario del *registry*.

## 4. Estructura de Capas y Responsabilidades

- **Capa de Presentación/UI:** Simulada por `main.py`. Su responsabilidad es orquestar el flujo de la demostración, instanciar los servicios (realizando inyección de dependencias manual) y llamar a sus métodos. Es el "cliente" de la capa de servicios.
- **Capa de Lógica de Negocio:** El corazón del sistema, ubicada en el paquete `servicios`.
    - **Servicios de Dominio** (`servicios.cultivos`, `servicios.terrenos`, `servicios.personal`): Contienen la lógica de negocio específica para un agregado o entidad del dominio. Por ejemplo, `PlantacionService` sabe cómo plantar, regar y cosechar.
    - **Servicios de Aplicación/Negocio** (`servicios.negocio`): Orquestan operaciones que involucran múltiples dominios. `FincasService`, por ejemplo, gestiona una colección de fincas y puede realizar operaciones transversales como `cosechar_yempaquetar`.
- **Capa de Acceso a Datos:** Simulada por `RegistroForestalService`. Su responsabilidad es abstraer la lógica de persistencia (serialización con `pickle`) del resto de la aplicación. Actúa como un **Patrón DAO (Data Access Object)** o **Repository**.
- **Capa de Modelos/Entidades:** Ubicada en `entidades`. Define la estructura de los datos del dominio. Son clases simples que contienen estado pero no lógica de negocio, siguiendo el principio de **Anemic Domain Model**, lo cual es apropiado para esta arquitectura basada en servicios.
- **Servicios y Utilidades:** El paquete `patrones` y `excepciones` actúan como capas de soporte transversales, proporcionando herramientas y definiciones comunes para todo el sistema.

**Comunicación entre Capas:** El flujo es estrictamente descendente: `main.py` -> `servicios` -> `entidades`. Los servicios también utilizan los componentes de `patrones` y `excepciones`. Las capas inferiores no tienen conocimiento de las superiores.

## 5. Modelos de Datos

- **Entidades Principales:**
    - `Cultivo`: Interfaz base. `Arbol` y `Hortaliza` son subclases abstractas. `Pino`, `Olivo`, `Lechuga`, `Zanahoria` son las clases concretas.
    - `Tierra`: Representa la parcela física.
    - `Plantacion`: La finca que está *sobre* una `Tierra`. Contiene las listas de `Cultivo` y `Trabajador`. Es una entidad **agregadora**.
    - `Trabajador`: Modela a un empleado con sus `Tarea`s y `AptoMedico`.
    - `RegistroForestal`: La raíz del agregado principal, que agrupa `Tierra`, `Plantacion` y `Propietario`. Es el objeto que se serializa.

- **Relaciones entre Entidades:**
    - `Tierra` 1--1 `Plantacion` (Una tierra contiene una plantación).
    - `Plantacion` 1--* `Cultivo` (Una plantación tiene muchos cultivos).
    - `Plantacion` 1--* `Trabajador` (Una plantación tiene muchos trabajadores).
    - `Trabajador` 1--* `Tarea` (Un trabajador tiene muchas tareas).
    - `Trabajador` 1--1 `AptoMedico`.
    - `RegistroForestal` agrupa `Tierra` y `Plantacion`.

- **ORM:** No se utiliza un ORM. La persistencia se maneja manualmente a través de la serialización de objetos Python con el módulo `pickle`. `RegistroForestalService` actúa como la capa de abstracción para esta operación.

## 6. Flujo de Datos y Control

**Flujo Típico: "Plantar un Cultivo" (`plantacion_service.plantar`)**

1.  **`main.py` (Cliente):** Llama a `plantacion_service.plantar(plantacion, "Pino", 5)`.
2.  **`PlantacionService.plantar()`:**
    a. Calcula la superficie ya ocupada iterando sobre los cultivos existentes.
    b. Calcula la superficie disponible.
    c. Llama a `CultivoFactory.crear_cultivo("Pino")` para obtener una instancia temporal y calcular la superficie total requerida. **(Patrón Factory)**.
    d. **Validación:** Comprueba si la superficie requerida excede la disponible. Si es así, lanza `SuperficieInsuficienteException`.
    e. Si hay espacio, entra en un bucle y llama a `CultivoFactory.crear_cultivo("Pino")` 5 veces, añadiendo cada nuevo objeto `Pino` a la lista de cultivos de la `plantacion`.
3.  **`main.py` (Cliente):** La `plantacion` ahora contiene 5 nuevos objetos `Pino`. Si se lanzó una excepción, el bloque `try...except` la captura y muestra un mensaje de error.

**Manejo de Errores y Excepciones:**
- El proyecto define una jerarquía de excepciones personalizadas que heredan de `ForestacionException` (`excepciones/forestacion_exception.py`).
- Se utilizan excepciones específicas del dominio como `SuperficieInsuficienteException` y `AguaAgotadaException` para señalar errores de negocio de forma clara.
- Las excepciones de persistencia (`PersistenciaException`) encapsulan errores de I/O o de `pickle`, proporcionando mensajes claros para el usuario y detalles técnicos para el desarrollador.

## 7. Principios SOLID y Clean Code

El proyecto demuestra una aplicación rigurosa de los principios SOLID:

- **S (Single Responsibility Principle):** Cada clase tiene una única responsabilidad bien definida. Las `entidades` solo guardan datos, los `servicios` contienen lógica, las `factories` crean objetos, las `strategies` definen algoritmos.
- **O (Open/Closed Principle):** El sistema está abierto a la extensión pero cerrado a la modificación.
    - **Ejemplo (Strategy):** Se puede añadir una nueva `AbsorcionAguaStrategy` sin modificar los servicios que la usan.
    - **Ejemplo (Factory):** Se puede añadir un nuevo tipo de `Cultivo` modificando solo la `CultivoFactory` y añadiendo su servicio al `CultivoServiceRegistry`, sin tocar el código cliente.
- **L (Liskov Substitution Principle):** Los subtipos son perfectamente sustituibles por sus tipos base. Un `Pino` o una `Lechuga` pueden ser tratados como un `Cultivo` en cualquier parte del sistema (ej. en la lista `_cultivos` de `Plantacion`).
- **I (Interface Segregation Principle):** Se utilizan interfaces (clases base abstractas en Python) específicas y cohesivas. `AbsorcionAguaStrategy` es una interfaz para un propósito muy concreto. `Observer[T]` es una interfaz genérica pero enfocada en un solo comportamiento.
- **D (Dependency Inversion Principle):** Los módulos de alto nivel no dependen de los de bajo nivel; ambos dependen de abstracciones.
    - `PlantacionService` no depende de `Pino` o `Lechuga`, sino de la abstracción `Cultivo` y de `CultivoFactory`.
    - `CultivoService` no depende de `AbsorcionSeasonalStrategy`, sino de la abstracción `AbsorcionAguaStrategy`.

## 8. Gestión de Dependencias

- **Dependencias entre Módulos:** La inyección de dependencias se realiza **manualmente** a través de los constructores. Esto mantiene el sistema simple y sin la necesidad de un framework de DI.
    ```python
    # El servicio de Pino inyecta la estrategia que necesita
    class PinoService(ArbolService):
        def __init__(self):
            super().__init__(AbsorcionSeasonalStrategy())

    # El controlador de riego inyecta los sensores que necesita observar
    tarea_control = ControlRiegoTask(tarea_temp, tarea_hum, ...)
    ```
- **Dependencias Externas:** No hay. El proyecto se basa únicamente en la biblioteca estándar de Python, lo que lo hace portable y sin sobrecarga de dependencias.

## 9. Configuración y Entorno

- **Variables de Entorno:** No se utilizan.
- **Archivos de Configuración:** Toda la configuración del sistema (valores "mágicos") está centralizada en un único archivo: `python_forestacion/constantes.py`. Esta es una excelente práctica que evita el *hardcoding* y facilita la modificación de parámetros del sistema.
    ```python
    # python_forestacion/constantes.py
    AGUA_CONSUMIDA_RIEGO = 10
    TEMP_MIN_RIEGO = 8
    SUPERFICIE_PINO = 2.0
    ```
- **Manejo de Entornos:** No hay una distinción formal entre entornos (dev, test, prod), lo cual es aceptable para un proyecto de esta naturaleza y escala.

## 10. Testing y Calidad

- **Estrategia de Testing:** El archivo `main.py` actúa como un **test de integración** o un script de demostración de extremo a extremo. Ejecuta un flujo completo que involucra todos los componentes principales y valida la correcta implementación de los patrones de diseño.
- **Cobertura de Tests:** No hay tests unitarios formales (ej. con `pytest` o `unittest`). La validación se concentra en el flujo de `main.py`.
- **Herramientas de Calidad:** El código sigue estrictamente las convenciones de **PEP 8** y utiliza **type hints** de forma exhaustiva, lo que permite el uso de analizadores estáticos como `mypy` para garantizar la corrección de tipos.

## 11. Seguridad y Buenas Prácticas

- **Validación de Entrada:** Los *setters* en las clases de entidad realizan validaciones básicas para mantener el estado consistente (ej. `superficie > 0`, `agua >= 0`).
- **Manejo de Datos Sensibles:** No se manejan datos sensibles como contraseñas. La persistencia con `pickle` es una vulnerabilidad de seguridad conocida si los datos no son de confianza, pero es aceptable en el contexto de este proyecto educativo.
- **Buenas Prácticas Adicionales:**
    - **Inmutabilidad Defensiva:** Métodos como `get_cultivos()` en `Plantacion` devuelven una copia de la lista (`return self._cultivos.copy()`), lo que evita que el código cliente modifique el estado interno de la entidad de forma inesperada.
    - **Seguridad en Hilos (Thread-Safety):** Se utiliza `threading.Lock` para proteger la creación del Singleton y `threading.Event` para una finalización segura (*graceful shutdown*) de los hilos del sistema de riego.

## 12. Puntos Clave para Defender el Proyecto

- **Decisiones de Arquitectura:**
    - Se eligió una **Arquitectura en Capas** para lograr una clara separación de responsabilidades, lo que hace que el sistema sea más fácil de entender, mantener y extender.
    - La **Inyección de Dependencias manual** fue una decisión consciente para mantener la simplicidad y evitar la sobrecarga de un framework, demostrando cómo se puede lograr el desacoplamiento con herramientas básicas.

- **Elección de Patrones:**
    - **Factory Method** se usó para centralizar la creación de cultivos, permitiendo añadir nuevos tipos sin modificar los servicios que los consumen.
    - **Strategy** fue clave para implementar diferentes algoritmos de absorción de agua de forma intercambiable, eliminando condicionales y adhiriendo al principio Abierto/Cerrado.
    - **Observer** desacopló el sistema de riego de los sensores, permitiendo una arquitectura basada en eventos para el monitoreo en tiempo real.
    - **Singleton** garantizó una única fuente de verdad para el registro de servicios, crucial para la consistencia del sistema.
    - **Registry** se implementó para un despacho polimórfico eficiente y limpio, una solución más elegante y mantenible que las cadenas de `isinstance`.

- **Escalabilidad y Mantenibilidad:**
    - La arquitectura modular y el bajo acoplamiento facilitan la **mantenibilidad**. Cambiar la lógica de un servicio no afecta a otros.
    - El sistema es **escalable en términos de funcionalidad**. Añadir un nuevo cultivo, una nueva estrategia o un nuevo servicio sigue un patrón claro y no requiere refactorizaciones masivas.
    - La centralización de constantes en `constantes.py` simplifica enormemente la reconfiguración del comportamiento del sistema.

- **Ventajas de la Implementación:**
    - **Código Limpio y Auto-documentado:** El uso estricto de PEP 8, nombres descriptivos y *type hints* hace que el código sea excepcionalmente legible.
    - **Robustez:** El manejo de excepciones personalizado y las validaciones de estado hacen que el sistema sea robusto ante entradas inválidas y errores de negocio.
    - **Demostración Práctica:** El proyecto no es solo teórico; implementa un dominio de negocio complejo de manera coherente, demostrando la aplicación práctica de los patrones en un contexto realista.

## 13. Áreas de Mejora y Deuda Técnica

- **Code Smells / Antipatrones:** El código está notablemente limpio. Un área menor de mejora podría ser la forma en que `ControlRiegoTask` distingue entre los eventos de temperatura y humedad, que actualmente se basa en el rango de valores. Una solución más robusta sería crear una clase de evento (`SensorEvent`) que contenga tanto el tipo de sensor como el valor.
    ```python
    # Sugerencia de mejora
    class SensorEvent:
        def __init__(self, tipo_sensor: str, valor: float):
            self.tipo = tipo_sensor
            self.valor = valor
    ```

- **Sugerencias para Refactoring:**
    - **Introducir Tests Unitarios:** La principal área de mejora es la falta de un conjunto de tests unitarios con `pytest`. Esto permitiría probar cada servicio y cada validación de forma aislada, mejorando la confianza al hacer cambios.
    - **Reemplazar `pickle` por una Base de Datos:** Para un sistema más cercano a producción, se debería reemplazar `pickle` por una base de datos (como **SQLite** con **SQLAlchemy**) para una persistencia más robusta, segura y consultable.
    - **Usar un Framework de Inyección de Dependencias:** Para proyectos más grandes, la inyección manual puede volverse tediosa. Introducir un framework como `dependency-injector` podría formalizar y automatizar la gestión de dependencias.
    - **Logging:** Implementar un sistema de logging (con el módulo `logging`) en lugar de usar `print()` permitiría un control más granular sobre los mensajes de salida (INFO, DEBUG, ERROR).
