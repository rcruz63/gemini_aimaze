# MVP 

### Idea 1: Configuración del Entorno y Esqueleto del Proyecto

**El Prompt (La Idea para la herramienta):**

> "Inicia el proyecto `ndd_aimaze`. Configura `pyproject.toml` usando Python 3.12+ y añade `pytest` y `pydantic` como dependencias de desarrollo usando `uv` (prohibido usar `pip`). Crea la estructura de directorios base según la arquitectura: `engine/`, `ai/`, `models/`, y `gameplay/`. Configura el linter/formateador para respetar un máximo de 88 caracteres por línea. Finalmente, crea el archivo `CHANGELOG.md` inicial y haz el primer commit. Todo el código debe pasar linting y tests vacíos."

* **Qué debe hacer su plan:** Crear carpetas, inicializar el entorno virtual con `uv`, instalar `pydantic` y `pytest`, configurar herramientas (ej. Ruff/Black en pyproject.toml) y crear el CHANGELOG.
* **Qué observar al finalizar:** * El directorio `.venv` existe.
* Hay un `CHANGELOG.md` con la primera entrada.
* La estructura de carpetas es idéntica a la del documento de arquitectura.



---

### Idea 2: Modelos de Estado Estructurado (El Corazón de los Datos)

**El Prompt (La Idea para la herramienta):**

> "Implementa los modelos de datos base usando Pydantic en la carpeta `models/`. Necesitamos tres niveles de estado: `WorldState` (estático: setting, theme), `SessionState` (dinámico lento: location, inventory, npcs_conocidos) y `SceneState` (dinámico rápido: location_description, active_npcs, available_actions). Implementa también modelos básicos para `Room` (con id y exits). Recuerda: complejidad ciclomática máxima de 10, usa early returns si hay validaciones, documenta en docstrings, haz tests unitarios comprobando la serialización a JSON, y registra en CHANGELOG antes de hacer commit."

* **Qué debe hacer su plan:** Crear archivos en `models/` (ej. `state.py`, `room.py`), definir clases Pydantic que puedan exportarse a JSON (`model_dump_json()`), y crear tests en `tests/test_models.py`.
* **Qué observar al finalizar:** * Ejecutas `uv run pytest` y pasa en verde.
* Los modelos se exportan perfectamente a un JSON limpio y estructurado (esto es vital para no saturar los tokens después).



---

### Idea 3: El Motor de Mapas y el "Test de la Brújula Rota"

**El Prompt (La Idea para la herramienta):**

> "Implementa el `MapEngine` en la carpeta `engine/`. Este motor gestiona un grafo de instancias de `Room`. Debe tener una función para conectar habitaciones (ej. `connect(room_A, room_B, direction='north')`). REGLA INNEGOCIABLE: La coherencia espacial es matemática. Si conecto A con B hacia el 'north', el motor DEBE crear automáticamente la conexión de B hacia A por el 'south'. Crea un test en `pytest` llamado `test_brujula_rota` que valide estrictamente esto. Actualiza CHANGELOG y haz commit."

* **Qué debe hacer su plan:** Codificar la lógica de grafos bidireccionales en `engine/map_engine.py` y sus tests exhaustivos.
* **Qué observar al finalizar:**
* El `test_brujula_rota` pasa. Hemos blindado el proyecto contra el mayor trauma de las versiones anteriores: la pérdida de coherencia espacial.



---

### Idea 4: Parser de Comandos y Motor de Navegación Determinista

**El Prompt (La Idea para la herramienta):**

> "Implementa el `CommandParser` en `engine/` y un bucle de juego básico en `gameplay/game_loop.py`. El parser debe entender comandos simples verbo-sustantivo (ej. 'ir norte', 'coger llave'). Conecta el parser con el `MapEngine` y el `SessionState` para que el jugador pueda moverse entre dos habitaciones de prueba y su `SessionState.location` se actualice. El output por terminal debe ser puramente determinista de momento (imprimir el JSON del SceneState o un texto hardcodeado). Recuerda: complejidad < 10, CHANGELOG obligatorio."

* **Qué debe hacer su plan:** Crear el parseo básico, instanciar un mundo diminuto (2 habitaciones conectadas) y permitir que un input del usuario actualice la posición en el estado.
* **Qué observar al finalizar:** * Puedes ejecutar `uv run python main.py`, escribir "ir norte" y ver cómo la posición cambia de la Sala A a la Sala B. No hay IA, solo pura lógica.

---

### Idea 5: El Motor de Puzzles (Plantillas Deterministas)

**El Prompt (La Idea para la herramienta):**

> "Implementa el `PuzzleEngine` en `engine/`. Olvida la IA. Crea una plantilla de puzzle determinista tipo 'Key and Lock' (Llave y Cerradura). El motor debe verificar si un objeto requerido (ej. 'llave_oxidada') está en el `SessionState.inventory` del jugador para desbloquear una salida (exit) en el `MapEngine`. Escribe tests unitarios que simulen a un jugador intentando pasar sin la llave (falla) y con la llave (pasa). Actualiza el CHANGELOG."

* **Qué debe hacer su plan:** Crear la clase base para Puzzles y un caso de uso concreto de bloqueo de puerta basado en inventario, evitando tiradas de dados.
* **Qué observar al finalizar:**
* El test asegura que la lógica del puzzle es 100% infranqueable si no tienes el estado correcto en el inventario.



---

### Idea 6: Event Simulation Engine (El Mundo Vivo)

**El Prompt (La Idea para la herramienta):**

> "Implementa el `EventEngine` en `engine/`. Debe manejar una lista de eventos con un progreso (`progress` de 0.0 a 1.0) y una velocidad (`speed`). Cada vez que se llama a `event_engine.tick()`, el progreso aumenta. Si llega a 1.0, el evento se marca como 'triggered' y se añade al `SceneState`. Escribe un test donde un evento 'bajada_oxigeno' avanza durante 3 turnos simulados (esperar, esperar, esperar) hasta que se dispara. CHANGELOG obligatorio."

* **Qué debe hacer su plan:** Crear la lógica de simulación de tiempo donde el mundo evoluciona aunque el jugador no haga nada.
* **Qué observar al finalizar:**
* Los tests demuestran que el mundo tiene un reloj interno independiente de las acciones resolutivas del jugador.



---

### Idea 7: El "Spike" (Validación Visual de la Consola)

**El Prompt (La Idea para la herramienta):**

> "Crea el 'Spike' de la Semana 1 en `ai/narrator_ai.py`. Crea una clase `NarratorMock` (sin llamadas reales a API para no gastar cuota). Esta clase recibe el `SceneState` JSON en cada turno y devuelve un string hardcodeado simulando a la IA (ej. 'Estás en una sala oscura. Huele a humedad. Opciones: ir norte'). Integra esto en el `game_loop.py` para que la terminal se limpie en cada turno y muestre este texto en verde (estilo 8-bits retro), ocultando el JSON por debajo. Haz tests visuales/manuales y actualiza el CHANGELOG."

* **Qué debe hacer su plan:** Enganchar todas las piezas deterministas y ponerles la capa de pintura visual (el texto en la terminal).
* **Qué observar al finalizar:**
* Ejecutas el juego, te mueves, resuelves un puzzle, pasan eventos... Todo funciona perfecto, no te has gastado ni 1 token de API, y la interfaz ya parece un juego clásico de Zork.



---
