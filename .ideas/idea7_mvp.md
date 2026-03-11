# Idea 7: El "Spike" (Validación Visual de la Consola)

**El Prompt (La Idea para la herramienta):**

> "Crea el 'Spike' de la Semana 1 en `ai/narrator_ai.py`. Crea una clase `NarratorMock` (sin llamadas reales a API para no gastar cuota). Esta clase recibe el `SceneState` JSON en cada turno y devuelve un string hardcodeado simulando a la IA (ej. 'Estás en una sala oscura. Huele a humedad. Opciones: ir norte'). Integra esto en el `game_loop.py` para que la terminal se limpie en cada turno y muestre este texto en verde (estilo 8-bits retro), ocultando el JSON por debajo. Haz tests visuales/manuales y actualiza el CHANGELOG."

* **Qué debe hacer su plan:** Enganchar todas las piezas deterministas y ponerles la capa de pintura visual (el texto en la terminal).
* **Qué observar al finalizar:**
* Ejecutas el juego, te mueves, resuelves un puzzle, pasan eventos... Todo funciona perfecto, no te has gastado ni 1 token de API, y la interfaz ya parece un juego clásico de Zork.
