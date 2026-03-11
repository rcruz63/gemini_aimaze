# Idea 4: Parser de Comandos y Motor de Navegación Determinista

**El Prompt (La Idea para la herramienta):**

> "Implementa el `CommandParser` en `engine/` y un bucle de juego básico en `gameplay/game_loop.py`. El parser debe entender comandos simples verbo-sustantivo (ej. 'ir norte', 'coger llave'). Conecta el parser con el `MapEngine` y el `SessionState` para que el jugador pueda moverse entre dos habitaciones de prueba y su `SessionState.location` se actualice. El output por terminal debe ser puramente determinista de momento (imprimir el JSON del SceneState o un texto hardcodeado). Recuerda: complejidad < 10, CHANGELOG obligatorio."

* **Qué debe hacer su plan:** Crear el parseo básico, instanciar un mundo diminuto (2 habitaciones conectadas) y permitir que un input del usuario actualice la posición en el estado.
* **Qué observar al finalizar:** * Puedes ejecutar `uv run python main.py`, escribir "ir norte" y ver cómo la posición cambia de la Sala A a la Sala B. No hay IA, solo pura lógica.
