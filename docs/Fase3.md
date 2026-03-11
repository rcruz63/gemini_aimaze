# FASE3_IMPLEMENTACION.md
# Guía de Ejecución para la Fase 3: Autonomous Systems

**Objetivo:** Sustituir los *mocks* por llamadas reales a modelos de lenguaje locales usando la librería `ollama`, implementando el Parser Semántico, el Director, el Narrador y el Extractor de Memoria.

*Instrucción para el humano:* Pasa cada uno de estos "Prompts" a la herramienta CLI de forma secuencial. No pases al siguiente hasta que los tests del anterior estén en verde.

#### 🛠️ Prompt 1: El Cliente LLM (La Pasarela)
> "Añade la dependencia `ollama` usando `uv add` (prohibido pip). Crea el módulo `ai/llm_client.py`. Implementa una clase `LLMClient` con dos métodos: `generate_cheap(prompt, json_mode=False)` y `generate_expensive(prompt)`. Usa modelos locales genéricos (ej. 'llama3' o 'qwen2.5'). Implementa manejo de errores por si el servidor de Ollama está caído. Escribe tests unitarios usando `unittest.mock.patch` para simular las respuestas de Ollama y no depender de la red durante los tests. Actualiza el CHANGELOG y haz commit respetando Conventional Commits."

#### 🧠 Prompt 2: El Parser Semántico (Intent Extractor)
> "Actualiza el `CommandParser` en `engine/` para usar `LLMClient.generate_cheap(json_mode=True)`. Debe recibir el texto libre del jugador y la lista de `available_actions` del `SceneState`. El LLM debe devolver un JSON estricto: `{"matched_action": "accion_elegida"}` o `{"matched_action": "unknown"}`. Modifica el game loop: si devuelve 'unknown', pide aclaración; si falla 2 veces, imprime las acciones válidas. Asegura que el motor siga siendo determinista (solo recibe acciones validadas). Tests obligatorios (mockeando la IA). Actualiza CHANGELOG."

#### 🎬 Prompt 3: El Director Narrativo
> "Crea `ai/director_ai.py`. Usa `LLMClient.generate_cheap(json_mode=True)`. Debe recibir el `SessionState` y `SceneState` (en formato JSON) y decidir el rumbo dramático. Devuelve un JSON: `{"tension_level": <1-10>, "scene_goal": "<instrucción narrativa>"}`. El Director NO altera el inventario ni el mapa, solo dicta el tono. Modifica el `SceneState` para incluir este output del Director. Crea tests con mocks. Actualiza CHANGELOG."

#### 🗣️ Prompt 4: El Narrador AI (El Alma)
> "Refactoriza `ai/narrator_ai.py` para usar `LLMClient.generate_expensive()`. Elimina el texto hardcodeado. El System Prompt debe ser estricto: 'Eres un narrador de aventuras retro 8-bits. Usa humor oscuro. Límite: 80-150 palabras. REGLA INNEGOCIABLE: NO inventes salidas, puertas ni objetos que no estén explícitamente en el JSON provisto. Basate en el scene_goal del Director.' Pásale SOLAMENTE el `SceneState` al prompt del usuario (jamás envíes el historial del chat). Crea tests mockeando la salida. Actualiza CHANGELOG."

#### 💾 Prompt 5: El Extractor de Memoria
> "Crea `ai/memory_extractor.py`. Este módulo se llama *después* de que el Narrador hable. Usa `LLMClient.generate_cheap(json_mode=True)`. Le pasamos el texto narrado y el `SessionState`. Debe extraer información clave (ej. relaciones, pistas) y devolver un JSON con actualizaciones estructurales para aplicar al `SessionState`. Valida la salida JSON usando Pydantic para evitar errores de parseo. Tests mockeados. Actualiza CHANGELOG."

#### 🔄 Prompt 6: Orquestación Final
> "Integra todos los módulos en `gameplay/game_loop.py`. El flujo exacto por turno debe ser: 1) Input semántico del jugador -> 2) Motor actualiza estado -> 3) Eventos avanzan -> 4) Director decide tono -> 5) Narrador genera texto -> 6) Memory Extractor actualiza sesión -> 7) Imprimir texto en consola. Asegúrate de que la consola se limpia limpiamente entre turnos y de que todo funciona sin romper la coherencia del mapa. Haz una revisión de linting (max 88 chars, complejidad < 10). Último commit en CHANGELOG."