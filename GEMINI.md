# Análisis de Ingeniería Inversa: Proyecto Forestación

## 1. Resumen de Alto Nivel y Propósito

El proyecto "Forestación" es una aplicación de simulación de gestión agrícola y forestal. Su propósito principal es modelar las operaciones de una o varias fincas, abarcando desde la plantación y el cuidado de diversos tipos de cultivos (árboles y hortalizas) hasta la gestión de personal y la persistencia de datos. La aplicación simula un dominio de negocio complejo, aplicando principios de diseño de software para separar responsabilidades y gestionar la complejidad.

Las funcionalidades clave son:
1.  **Gestión de Cultivos:** Permite plantar diferentes tipos de cultivos (Pinos, Olivos, Lechugas, Zanahorias), validando la superficie disponible y gestionando su ciclo de vida.
2.  **Sistema de Riego Automatizado:** Simula un sistema de riego concurrente que monitorea sensores de temperatura y humedad para decidir cuándo regar, gestionando el consumo de agua.
3.  **Gestión de Personal:** Modela trabajadores con tareas asignadas y certificaciones médicas (apto médico), y simula la ejecución de sus labores.
4.  **Persistencia de Datos:** Guarda y recupera el estado de un "Registro Forestal" (que agrupa la tierra, la plantación y sus cultivos) en archivos `.dat` mediante serialización de objetos Java.
5.  **Orquestación de Fincas:** A través de `FincasService`, coordina operaciones complejas que involucran múltiples dominios, como fumigar o cosechar cultivos específicos de una finca.

---

### **2. Arquitectura General y Patrones de Diseño**

#### **Patrón Arquitectónico Principal: Arquitectura en Capas (Layered Architecture)**

El proyecto sigue una arquitectura en capas clásica, con una clara separación entre la presentación (simulada por `Main.java`), la lógica de negocio (servicios) y los datos (entidades). Aunque no hay una capa de acceso a datos formal (como un ORM), la lógica de persistencia está encapsulada en `RegistroForestalService`, actuando como un símil de Repositorio/DAO.

**Diagrama de Capas (ASCII):**

```
+------------------------------------------------+
|         Capa de Presentación (Simulada)        |
|              (Main.java)                       |
|   - Orquesta el flujo principal de la demo.    |
|   - Inicia y coordina los servicios.           |
+----------------------+-------------------------+
                       |
                       v
+----------------------+-------------------------+
|      Capa de Lógica de Negocio (Servicios)     |
| (servicios.cultivos, servicios.terrenos, etc.) |
|   - Contiene la lógica de negocio principal.   |
|   - Ej: plantar, regar, cosechar, trabajar.    |
|   - Coordina interacciones entre entidades.    |
+----------------------+-------------------------+
                       |
                       v
+----------------------+-------------------------+
|          Capa de Dominio (Entidades)           |
|      (entidades.cultivos, entidades.terrenos)  |
|   - POJOs (Plain Old Java Objects).            |
|   - Representan el estado del sistema.         |
|   - Contienen datos, pero no lógica de negocio.|
+------------------------------------------------+
```

#### **Patrones de Diseño (GoF y otros)**

- **Nombre del Patrón:** **Service Layer**
  - **Propósito:** Abstraer y encapsular la lógica de negocio. Las clases de servicio (ej. `PlantacionService`, `TrabajadorService`) contienen los "verbos" del sistema, operando sobre las entidades (los "sustantivos"). Esto centraliza la lógica y la hace reutilizable.
  - **Implementación:** Se encuentra en todo el paquete `servicios`. Cada subpaquete (`cultivos`, `personal`, `terrenos`) tiene servicios dedicados a manipular las entidades de su dominio.

- **Nombre del Patrón:** **Factory Method**
  - **Propósito:** Encapsular la lógica de creación de objetos complejos, permitiendo crear diferentes tipos de `Cultivo` sin exponer la lógica de instanciación al cliente.
  - **Implementación:** En `PlantacionService`, el método `crearCultivo(String especie)` actúa como una fábrica. El cliente solo pide "Pino" y el método se encarga de `new Pino(...)`.

    ```java
    // En servicios.terrenos.PlantacionService
    private Cultivo crearCultivo(String especie) {
        return switch (especie) {
            case "Pino"      -> new Pino("cedro");
            case "Olivo"     -> new Olivo(TipoAceituna.NEGRA);
            case "Lechuga"   -> new Lechuga("Mantecosa");
            case "Zanahoria" -> new Zanahoria(true);
            default          -> null;
        };
    }
    ```

- **Nombre del Patrón:** **Registry**
  - **Propósito:** Centralizar la selección de un servicio o handler basado en un tipo, eliminando la necesidad de cadenas `if/else` o `instanceof`. Es una implementación del principio Abierto/Cerrado.
  - **Implementación:** La clase `CultivoServiceRegistry` es un ejemplo perfecto. Mapea cada clase de `Cultivo` (ej. `Pino.class`) a la función de servicio correspondiente (ej. `pinoService::absorberAgua`). Esto permite que `PlantacionService` pueda regar cualquier tipo de cultivo sin conocer su implementación específica.

    ```java
    // En servicios.cultivos.CultivoServiceRegistry
    public CultivoServiceRegistry(...) {
        // ...
        absorberAguaHandlers.put(Pino.class, c -> pinoService.absorberAgua((Pino) c));
        absorberAguaHandlers.put(Olivo.class, c -> olivoService.absorberAgua((Olivo) c));
        // ...
    }

    public int absorberAgua(Cultivo cultivo) {
        Function<Cultivo, Integer> handler = absorberAguaHandlers.get(cultivo.getClass());
        // ...
        return handler.apply(cultivo);
    }
    ```

- **Nombre del Patrón:** **Data Access Object (DAO) / Repository (simulado)**
  - **Propósito:** Abstraer la lógica de persistencia de los datos. Separa cómo se guardan los datos (serialización, base de datos, etc.) de la lógica de negocio que los utiliza.
  - **Implementación:** `RegistroForestalService` actúa como un DAO. Sus métodos `persistir()` y `leerRegistro()` encapsulan la serialización y deserialización de objetos `RegistroForestal`, ocultando los detalles de `ObjectOutputStream` y `FileInputStream` al resto de la aplicación.

- **Nombre del Patrón:** **Generics y Bounded Wildcards**
  - **Propósito:** Proporcionar seguridad de tipos (type-safety) en colecciones y métodos, especialmente en operaciones como la cosecha.
  - **Implementación:** La clase `Box<T extends Cultivo>` es un DTO (Data Transfer Object) genérico que solo puede contener objetos que sean `Cultivo`. El método `FincasService.cosecharYempaquetar(Class<T> tipoCultivo)` utiliza generics para devolver una caja (`Box<T>`) que contiene solo el tipo de cultivo solicitado, garantizando la seguridad de tipos en tiempo de compilación.

---

### **3. Estructura Detallada del Proyecto**

```
/
├── data/
│   └── Juan Perez.dat  (Archivos de datos serializados)
└── src/
    ├── Main.java       (Punto de entrada y orquestación de la demo)
    ├── entidades/      (Paquete raíz para los modelos de dominio)
    │   ├── cultivos/   (Clases como Arbol, Hortaliza, Pino, Olivo)
    │   ├── personal/   (Clases como Trabajador, Tarea, AptoMedico)
    │   └── terrenos/   (Clases como Tierra, Plantacion, RegistroForestal)
    ├── excepciones/    (Clases de excepciones personalizadas)
    │   ├── AguaAgotadaException.java
    │   ├── ForestacionException.java (Excepción base)
    │   └── ...
    ├── riego/          (Lógica del sistema de riego concurrente)
    │   ├── control/    (ControlRiegoTask: decide cuándo regar)
    │   └── sensores/   (HumedadReaderTask, TemperaturaReaderTask: simulan sensores)
    └── servicios/      (Paquete raíz para la lógica de negocio)
        ├── cultivos/   (Servicios para cada tipo de cultivo: PinoService, etc.)
        ├── negocio/    (Servicios de orquestación: FincasService)
        ├── personal/   (TrabajadorService)
        └── terrenos/   (PlantacionService, RegistroForestalService)
```

- **`entidades`**: Contiene las clases que representan el **estado** y la **identidad** de los objetos del dominio (los "sustantivos"). Son POJOs, con campos y getters/setters. No contienen lógica de negocio.
- **`servicios`**: Contiene las clases que implementan la **lógica de negocio** (los "verbos"). Manipulan las entidades para ejecutar las operaciones del sistema. Esta es la capa más importante.
- **`excepciones`**: Define una jerarquía de excepciones personalizadas (`ForestacionException` como base) para un manejo de errores de negocio robusto y específico.
- **`riego`**: Un módulo autocontenido que demuestra el uso de concurrencia (`Runnable`, `ExecutorService`) para simular un proceso en segundo plano (el sistema de riego).

---

### **4. Componentes Clave y sus Responsabilidades**

- **Modelos/Entidades:**
  - **`Cultivo`**: Interfaz base para todo lo que se puede plantar. `Arbol` y `Hortaliza` son implementaciones abstractas, y `Pino`, `Olivo`, `Lechuga`, `Zanahoria` son las clases concretas.
  - **`Tierra`**: Representa una parcela de tierra física.
  - **`Plantacion`**: Representa la finca que está *en* una `Tierra`. Contiene listas de `Cultivo` y `Trabajador`. Es una de las entidades centrales.
  - **`Trabajador`**: Modela a un empleado, con sus `Tarea`s y su `AptoMedico`.
  - **`RegistroForestal`**: Una entidad agregadora que agrupa `Tierra`, `Plantacion` y `Propietario`. Es el objeto que se persiste.

- **Capa de Lógica de Negocio (Servicios):**
  - **`PlantacionService`**: Lógica central para `plantar` (con validación de superficie), `regar` (con validación de agua) y `consumir` (cosechar) cultivos de una plantación.
  - **`CultivoServiceRegistry`**: Componente clave que permite el despacho polimórfico a los servicios de cultivo específicos (`PinoService`, `OlivoService`, etc.), evitando `instanceof`.
  - **`FincasService`**: Servicio de orquestación que maneja operaciones a nivel de múltiples fincas, como `fumigar` o `cosecharYempaquetar`.
  - **`RegistroForestalService`**: Responsable de `persistir` y `leerRegistro`, encapsulando la serialización/deserialización.
  - **`TrabajadorService`**: Contiene la lógica para que un `Trabajador` `trabajar`, validando su `AptoMedico`.

- **Capa de Acceso a Datos (simulada):**
  - **`RegistroForestalService`**: Como se mencionó, sus métodos `persistir` y `leerRegistro` actúan como la capa de acceso a datos, manejando la serialización de objetos Java a archivos `.dat`.

- **Capa de Presentación (simulada):**
  - **`Main.java`**: Actúa como el cliente de la capa de servicios. Su rol es instanciar los servicios (realizando una "inyección de dependencias" manual), crear las entidades iniciales y llamar a los métodos de servicio para demostrar el flujo de la aplicación.

---

### **5. Flujo de Datos en un Caso de Uso Crítico: "Plantar un Cultivo"**

1.  **`Main.java` (Cliente):** Llama a `plantacionService.plantar(plantacion, "Pino", 5)`. La intención es plantar 5 pinos en la plantación.
2.  **`PlantacionService.plantar()`:**
    a.  Recibe la `plantacion`, la especie `"Pino"` y la cantidad `5`.
    b.  Primero, calcula la superficie ya ocupada iterando sobre los cultivos existentes en `plantacion.getCultivosInterno()`.
    c.  Calcula la `sup_disponible` restando la superficie ocupada a la superficie total de la `Tierra` asociada.
    d.  Inicia un bucle para plantar `5` veces.
    e.  En cada iteración, llama a su método privado `crearCultivo("Pino")` (**Factory Method**).
    f.  `crearCultivo` devuelve una nueva instancia de `Pino`.
    g.  Verifica si la `sup_disponible` es suficiente para el nuevo pino.
    h.  Si hay espacio, añade el nuevo objeto `Pino` a la lista de cultivos de la `plantacion` (`plantacion.getCultivosInterno().add(cultivo)`).
    i.  Si no hay espacio, lanza una `SuperficieInsuficienteException` con detalles del error, deteniendo el flujo.
3.  **`Main.java` (Cliente):** Si la operación es exitosa, la `plantacion` ahora contiene 5 nuevos objetos `Pino`. Si se lanza una excepción, el bloque `catch` correspondiente en `main` la captura y muestra un mensaje de error amigable.

---

### **6. Dependencias y Ecosistema**

Dado que no hay un archivo `pom.xml` o `build.gradle`, el proyecto depende únicamente de las librerías estándar del **JDK (Java Development Kit)**.

- **`java.io.*`**: Utilizado extensivamente para la persistencia de datos mediante serialización (`ObjectInputStream`, `ObjectOutputStream`, `FileInputStream`, `FileOutputStream`).
- **`java.time.*`**: Usado para manejar fechas, como la `fechaEmision` de un `AptoMedico` o para la lógica estacional en los servicios de cultivo.
- **`java.util.concurrent.*`**: Utilizado en el módulo de riego para gestionar hilos (`ExecutorService`, `Executors`) y para variables atómicas (`AtomicLong`).
- **`java.util.*`**: Clases de colecciones estándar como `List`, `ArrayList`, `Map`, `HashMap`.

---

### **7. Guía de Migración a Python ("La Receta")**

Esta es una guía para recrear la arquitectura y los principios del proyecto en Python de forma idiomática.

- **Estructura de Proyecto Python Equivalente:**

  ```
  /
  ├── data/
  │   └── juan_perez.pkl
  ├── forestacion/
  │   ├── __init__.py
  │   ├── main.py             # Punto de entrada y orquestación
  │   ├── domain/             # Equivalente a 'entidades'
  │   │   ├── __init__.py
  │   │   ├── cultivos.py     # Clases Pydantic: Cultivo, Pino, Olivo...
  │   │   └── personal.py     # Clases Pydantic: Trabajador, Tarea...
  │   │   └── terrenos.py     # Clases Pydantic: Tierra, Plantacion...
  │   ├── services/           # Equivalente a 'servicios'
  │   │   ├── __init__.py
  │   │   ├── plantacion_service.py
  │   │   ├── trabajador_service.py
  │   │   └── registro_service.py # Lógica de persistencia
  │   ├── exceptions.py       # Excepciones personalizadas
  │   └── riego/              # Módulo de riego con asyncio
  │       ├── __init__.py
  │       └── riego_manager.py
  └── tests/
      ├── __init__.py
      └── test_plantacion_service.py
  ```

- **Mapeo de Tecnologías (Java -> Python):**

  - **Framework/Librería Java:** N/A (Aplicación de consola) -> **Equivalente en Python:** `asyncio` para la concurrencia del riego, y librerías estándar. Si se quisiera exponer como API, **FastAPI** sería la elección ideal.
  - **Acceso a Datos (Serialización Java):** -> **Equivalente en Python:** Módulo `pickle` para serialización binaria (equivalente directo) o `JSON` con serializadores personalizados para mayor interoperabilidad.
  - **Modelos/Entidades (Clases POJO):** -> **Equivalente en Python:** **`dataclasses`** del paquete estándar o, preferiblemente, **Pydantic `BaseModel`**. Pydantic ofrece validación de tipos en tiempo de ejecución, lo cual es una gran ventaja en Python.
  - **Testing (JUnit):** -> **Equivalente en Python:** **`pytest`**. Es el estándar de facto, más flexible y potente que `unittest`.
  - **Gestor de Dependencias (Maven/Gradle):** -> **Equivalente en Python:** **`pip`** con un archivo `requirements.txt` para dependencias. Para una gestión más robusta, **Poetry** es una excelente alternativa.

- **Plan de Implementación Sugerido:**

  1.  **Definir los modelos de datos (`domain/`) con Pydantic:**
      - Crear `cultivos.py`, `terrenos.py`, etc.
      - Usar `BaseModel` de Pydantic para definir las entidades (`Pino`, `Plantacion`, etc.) con tipos estrictos.

  2.  **Crear la capa de acceso a datos (`services/registro_service.py`):**
      - Crear funciones `persistir(registro: RegistroForestal)` y `leer_registro(propietario: str)`.
      - Usar el módulo `pickle` para guardar y cargar los objetos Pydantic en archivos `.pkl`.

  3.  **Implementar la lógica de negocio (`services/`):**
      - Crear `plantacion_service.py` con funciones como `plantar(plantacion, especie, cantidad)`.
      - Replicar la lógica de validación y las excepciones personalizadas (ej. `SuperficieInsuficienteError`).
      - Implementar el patrón **Registry** usando un diccionario de Python que mapee tipos de clase a funciones de servicio.

  4.  **Implementar el sistema de riego (`riego/`) con `asyncio`:**
      - Crear tareas asíncronas (`async def`) para leer sensores y controlar el riego, reemplazando los `Runnable` de Java.
      - Usar `asyncio.sleep()` en lugar de `Thread.sleep()`.

  5.  **Orquestar la aplicación en `main.py`:**
      - Replicar el flujo de la demo del `Main.java` original, instanciando los servicios y llamando a sus funciones.

  6.  **Escribir tests unitarios (`tests/`) con `pytest`:**
      - Crear tests para las funciones de servicio, usando `pytest.raises` para verificar que las excepciones se lanzan correctamente.

---

### **8. Puntos Críticos y Complejidades Ocultas**

- **Inyección de Dependencias Manual:** En `Main.java`, las dependencias se crean y se "inyectan" manualmente en los constructores de los servicios (ej. `new PlantacionService(cultivoServiceRegistry)`). Al migrar a Python, se puede seguir este enfoque simple o, para una aplicación más grande, usar un framework de inyección de dependencias como `dependency-injector`.

- **Persistencia por Serialización:** La serialización binaria (`.dat`, `pickle`) es frágil. Si se cambia la definición de una clase (se añade o elimina un campo), los archivos antiguos pueden volverse ilegibles. Una alternativa más robusta en Python sería usar una base de datos ligera como **SQLite** con un ORM como **SQLAlchemy**, o guardar los datos en formato **JSON**.

- **Gestión de Estado Mutable:** El código Java a menudo modifica el estado de los objetos directamente (ej. `plantacion.getCultivosInterno().add(...)`). En Python, aunque esto es posible, es común favorecer un estilo más funcional, donde las funciones devuelven nuevos objetos de estado en lugar de modificar los existentes. Sin embargo, para una migración directa, el estilo mutable es aceptable.

- **Concurrencia en el Riego:** El sistema de riego usa `ExecutorService` y `volatile` para la comunicación entre hilos. La traducción a Python con `asyncio` es más simple y segura, ya que evita muchos de los problemas de la concurrencia basada en hilos (como las race conditions), pero requiere un entendimiento del modelo asíncrono de Python.
