# Idea 2: Modelos de Estado Estructurado (El Corazón de los Datos)

**El Prompt (La Idea para la herramienta):**

> "Implementa los modelos de datos base usando Pydantic en la carpeta `models/`. Necesitamos tres niveles de estado: `WorldState` (estático: setting, theme), `SessionState` (dinámico lento: location, inventory, npcs_conocidos) y `SceneState` (dinámico rápido: location_description, active_npcs, available_actions). Implementa también modelos básicos para `Room` (con id y exits). Recuerda: complejidad ciclomática máxima de 10, usa early returns si hay validaciones, documenta en docstrings, haz tests unitarios comprobando la serialización a JSON, y registra en CHANGELOG antes de hacer commit."

* **Qué debe hacer su plan:** Crear archivos en `models/` (ej. `state.py`, `room.py`), definir clases Pydantic que puedan exportarse a JSON (`model_dump_json()`), y crear tests en `tests/test_models.py`.
* **Qué observar al finalizar:** * Ejecutas `uv run pytest` y pasa en verde.
* Los modelos se exportan perfectamente a un JSON limpio y estructurado (esto es vital para no saturar los tokens después).