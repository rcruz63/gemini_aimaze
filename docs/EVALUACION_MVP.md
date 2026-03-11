# Lista de Chequeo de Evaluación (MVP Phase 1)

### 🕵️‍♂️ Bloque 1: Inspección de Infraestructura y Estilo (El rigor)

Antes de ejecutar nada, abre el código de ambos proyectos y revisa esto:

* [ ] **El Veto a Pip:** Abre `pyproject.toml` o las instrucciones de instalación. ¿Se configuró todo usando `uv` o la IA hizo trampas y coló un `pip install`?
* [ ] **La Religión de la Bitácora:** Abre `CHANGELOG.md`. ¿Están registrados los pasos que dio la IA usando el formato *Conventional Commits* (`feat:`, `fix:`, etc.) o está vacío/ignorado?
* [ ] **Estructura de Carpetas:** ¿Existen los directorios `engine/`, `models/`, `gameplay/` y `tests/` separados limpiamente?
* [ ] **Complejidad Visual:** Abre cualquier archivo en `engine/` (ej. el parser o el mapa). ¿Hay funciones gigantescas con `if/else` anidados infinitos, o la IA respetó la regla de extraer a *helpers*, usar *early returns* y no pasar de 88 caracteres?

### 🧪 Bloque 2: La Verdad Automatizada (Tests)

Abre la consola en ambos directorios y ejecuta: `uv run pytest`.

* [ ] **Pasar en Verde:** ¿Pasan todos los tests o el código base ya nace roto?
* [ ] **El Test de la Brújula Rota (CRÍTICO):** Revisa el código de los tests del `MapEngine`. ¿Existe una prueba explícita que valide que si vas de la Sala A a la Sala B por el "Norte", la puerta "Sur" de la Sala B te devuelve a la Sala A de forma matemática?
* [ ] **Test del Puzzle Determinista:** ¿Hay un test que compruebe que no puedes abrir una puerta/resolver el *quest* si no tienes un objeto específico (ej. "llave") en tu inventario del `SessionState`?

### 🎮 Bloque 3: Jugabilidad Manual y Estado (El "Feel")

Ejecuta el juego con `uv run python main.py` y juega 2 o 3 turnos.

* [ ] **El Cero Absoluto (0 llamadas a API):** Durante tu partida de prueba, ¿el juego tardó milisegundos en responder? ¿El texto es claramente un *placeholder* (texto hardcodeado) o la IA intentó conectarse a Ollama/OpenAI prematuramente gastando tokens? (En la Fase 1 la IA debe estar 100% *mockeada*).
* [ ] **El Parser no explota:** Si escribes "ir norte", ¿el juego actualiza tu posición? Si escribes un comando basura ("asdasdasd"), ¿el juego lo maneja con gracia o lanza un error fatal de Python (Traceback)?
* [ ] **El Estado de Tres Niveles:** Revisa el código de `models/`. ¿Se crearon explícitamente las tres clases de estado (ej. usando `Pydantic`): `WorldState`, `SessionState` y `SceneState`?
* [ ] **El Reloj del Mundo:** Al pulsar "esperar" o meter varios comandos, ¿hay algún sistema (`EventEngine`) que esté sumando valores de `0.0` a `1.0` de fondo para simular el paso del tiempo?

### 🚩 Bloque 4: Las Señales de Fracaso Inmediato (Red Flags)

Si ves alguna de estas cosas, esa herramienta **pierde puntos gravemente**:

* ❌ Importó la librería `openai` o configuró un LLM real en el MVP (Violación de costes).
* ❌ El mapa se genera aleatoriamente en cada turno usando arrays sin conexiones fijas (Violación de la coherencia espacial).
* ❌ Guardó el "historial del chat" en una lista gigante dentro del estado en lugar de usar un JSON estructurado.
