# Idea 5: El Motor de Puzzles (Plantillas Deterministas)

**El Prompt (La Idea para la herramienta):**

> "Implementa el `PuzzleEngine` en `engine/`. Olvida la IA. Crea una plantilla de puzzle determinista tipo 'Key and Lock' (Llave y Cerradura). El motor debe verificar si un objeto requerido (ej. 'llave_oxidada') está en el `SessionState.inventory` del jugador para desbloquear una salida (exit) en el `MapEngine`. Escribe tests unitarios que simulen a un jugador intentando pasar sin la llave (falla) y con la llave (pasa). Actualiza el CHANGELOG."

* **Qué debe hacer su plan:** Crear la clase base para Puzzles y un caso de uso concreto de bloqueo de puerta basado en inventario, evitando tiradas de dados.
* **Qué observar al finalizar:**
* El test asegura que la lógica del puzzle es 100% infranqueable si no tienes el estado correcto en el inventario.
