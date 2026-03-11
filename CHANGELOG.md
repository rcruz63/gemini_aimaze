# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- **Fase 3 - Sistemas Autónomos (El Mundo Vivo)**:
    - Actualizado `gameplay/game_loop.py` para procesar el motor de NPCs solo para los agentes presentes en la sala actual.
    - Refactorizado `engine/event_engine.py` para separar los eventos disparados y actualizar `SceneState` (Motor de simulación avanzado).
    - Actualizado System Prompt de `ai/narrator_ai.py` para obligar al narrador a tejer las acciones de los NPCs y eventos disparados.
    - Añadida acción semántica "esperar" en el parser y `game_loop` para observar el paso del tiempo.
    - Implementado `ai/npc_ai.py` (NPCDecisionAI) para que los NPCs decidan acciones de forma autónoma usando IA barata.
    - Evolución del modelo `NPC`: Creados `NPCState` y `NPCAction` en `models/state.py` para representar la mente de los agentes.
    - Actualizado `SceneState` para registrar `npc_actions` y `triggered_events`.
    - Inicializados NPCs (Lysa y Rurik) en `GameLoop`.
- **Fase 2 - Integración de IA Real**:
    - Implementación de `ai/llm_client.py` para interactuar con Ollama (Cliente Agnóstico).
    - Añadida dependencia `ollama` vía `uv`.
    - Actualizado `engine/command_parser.py` para usar IA (Parser Semántico) con soporte para lenguaje natural y modo JSON.
    - Implementado `ai/memory_extractor.py` para actualización persistente de la sesión basada en la narrativa.
    - Implementado `ai/director_ai.py` para orquestar tensión y tono narrativo.
    - Actualizado `ai/narrator_ai.py` con conexión real al modelo narrativo de Ollama, con tono humorístico de 8-bits y límite de palabras.
    - Refactorizado `gameplay/game_loop.py` para orquestar el flujo completo de la Fase 2: Parser -> Motor -> Director -> Narrador -> Extractor de Memoria.
    - Implementado sistema de reintentos y menú de fallback en el Parser Semántico.
    - Actualizado System Prompt de `ai/narrator_ai.py` con reglas estrictas anti-alucinaciones.
    - Corregido el orden de impresión en `gameplay/game_loop.py` para mostrar la resolución del motor antes de la descripción narrativa.
- Spike de validación visual de la consola y Narrador Mock (Fase 7).
- Motor de eventos temporales (`EventEngine`) para simular un mundo vivo (Fase 6).
- Motor de puzzles (`PuzzleEngine`) y plantilla de Llave y Cerradura (Fase 5).
- Parser de comandos determinista y Bucle de juego MVP (Fase 4).
- Motor de mapas (`MapEngine`) con validación de coherencia espacial matemática (Fase 3).
- Modelos de estado estructurado (WorldState, SessionState, SceneState, Room) con Pydantic.
- Estructura base del proyecto (engine, ai, models, gameplay, tests).
- Configuración de `pyproject.toml` con Pydantic y Pytest.
- Herramientas de formateo y linting (Ruff, Black) configuradas a 88 caracteres.
- Inicialización del entorno con `uv`.
