# Idea 3: El Motor de Mapas y el "Test de la Brújula Rota"

**El Prompt (La Idea para la herramienta):**

> "Implementa el `MapEngine` en la carpeta `engine/`. Este motor gestiona un grafo de instancias de `Room`. Debe tener una función para conectar habitaciones (ej. `connect(room_A, room_B, direction='north')`). REGLA INNEGOCIABLE: La coherencia espacial es matemática. Si conecto A con B hacia el 'north', el motor DEBE crear automáticamente la conexión de B hacia A por el 'south'. Crea un test en `pytest` llamado `test_brujula_rota` que valide estrictamente esto. Actualiza CHANGELOG y haz commit."

* **Qué debe hacer su plan:** Codificar la lógica de grafos bidireccionales en `engine/map_engine.py` y sus tests exhaustivos.
* **Qué observar al finalizar:**
* El `test_brujula_rota` pasa. Hemos blindado el proyecto contra el mayor trauma de las versiones anteriores: la pérdida de coherencia espacial.

