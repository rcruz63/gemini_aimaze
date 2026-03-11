# Roadmap Fase 2: Integración de IA Real (ndd_aimaze)

**Objetivo Principal:** Conectar los modelos de lenguaje locales (Ollama) para dotar al juego de un Parser Semántico, un Director, un Narrador y un Extractor de Memoria, manteniendo la regla de oro: la IA interpreta, pero el motor determinista manda.

## 🗺️ Plan de Ideas (Prompts para la Herramienta)

### Idea 1: El Cliente LLM Agnóstico (La Pasarela)
**El Prompt:**
> "Añade la dependencia `ollama` usando `uv add`. Implementa el módulo `ai/llm_client.py`. Necesitamos una clase cliente que exponga dos métodos principales: `generate_cheap()` (para lógica JSON, ej. modelo `llama3.2:3b`) y `generate_expensive()` (para narrativa, ej. modelo `qwen2.5:7b` o el que tengamos local). Debe soportar el modo JSON estricto (`format='json'`) para los modelos baratos. Crea tests mockeando la respuesta de Ollama. Obligatorio: `CHANGELOG.md`, complejidad < 10, early returns."

* **Qué observar:** Que no use la librería `openai` (todavía) y que la estructura permita cambiar el modelo con variables de entorno o configuración simple.

### Idea 2: El Parser Semántico (Intent Extractor)
**El Prompt:**
> "Actualiza el `CommandParser`. En lugar de if/else rígidos, usa el `llm_client.generate_cheap()` en modo JSON. El prompt debe recibir el input del jugador y el array de `SceneState.available_actions`. Debe devolver un JSON con la acción elegida. Si el input es un disparate, devuelve 'unknown'. Implementa un sistema de reintentos: si falla dos veces, muestra un menú con las opciones disponibles. Haz tests comprobando entradas naturales como 'quiero abrir la maldita puerta norte'. Actualiza `CHANGELOG.md`."

* **Qué observar:** El jugador ya no tiene que hablar como un robot. El motor sigue recibiendo comandos estrictos, pero el parser actúa como traductor universal.

### Idea 3: El Extractor de Memoria (Memory Extractor)
**El Prompt:**
> "Implementa `ai/memory_extractor.py`. Este módulo se ejecuta DESPUÉS de cada escena. Usa `llm_client.generate_cheap()` en modo JSON. Recibe el texto narrado de la escena y el `SessionState` actual (solo lo relevante). Su trabajo es devolver un JSON con actualizaciones (ej. 'NPC_Lysa_attitude: suspicious' o descubrimientos clave). Usa modelos de Pydantic para asegurar que la salida de la IA tiene la estructura correcta. Escribe tests mockeando la IA y actualiza el `CHANGELOG.md`."

* **Qué observar:** Que el extractor sea capaz de leer un bloque de texto y convertirlo en variables estructuradas sin alucinar claves JSON inventadas.

### Idea 4: El Director Narrativo (Director AI)
**El Prompt:**
> "Implementa `ai/director_ai.py`. Usa `llm_client.generate_cheap()` en modo JSON. Este módulo lee el `SessionState` y `SceneState` e inyecta directrices narrativas. Devuelve un JSON con: `tension_level` (1-10) y `scene_goal` (ej. 'introducir sospecha sobre el tabernero'). No altera el mapa ni el inventario. Integra esta llamada en `game_loop.py` justo antes del Narrador. Escribe tests, documenta en docstrings y añade al `CHANGELOG.md`."

* **Qué observar:** El `SceneState` ahora debe tener un bloque de "instrucciones del director" que guiará el tono del siguiente texto.

### Idea 5: El Narrador AI (El Alma del Juego)
**El Prompt:**
> "Sustituye la clase `NarratorMock` en `ai/narrator_ai.py` por una conexión real usando `llm_client.generate_expensive()`. El System Prompt DEBE exigir: 1) Tono de aventura 8-bits, humor y ligero sarcasmo. 2) Límite estricto de 80 a 150 palabras. El prompt de usuario solo recibirá el JSON del `SceneState` (que ahora incluye la guía del Director) y el resultado de la acción del motor. El historial completo del chat está PROHIBIDO. Actualiza `CHANGELOG.md`."

* **Qué observar:** Textos inmersivos, divertidos y cortos. Si la IA empieza a contar la historia de su vida, el límite de palabras falló.

### Idea 6: Orquestación del Game Loop
**El Prompt:**
> "Refactoriza `gameplay/game_loop.py` para integrar todo el flujo de la Fase 2: 1) Input del jugador -> 2) Semantic Parser -> 3) Game Engine Update -> 4) Event/NPC tick -> 5) Director AI evalúa -> 6) Narrator AI genera texto -> 7) Memory Extractor actualiza sesión -> 8) Imprimir texto. Asegura que la consola se limpie entre turnos (efecto terminal clásica). Los tests de integración deben usar mocks para la IA. Commit con `CHANGELOG.md`."

* **Qué observar:** El ciclo de vida completo de un turno, demostrando que la arquitectura de dos capas (Motor -> IA) fluye a la perfección.