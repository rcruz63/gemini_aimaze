# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Motor de puzzles (`PuzzleEngine`) y plantilla de Llave y Cerradura (Fase 5).
- Parser de comandos determinista y Bucle de juego MVP (Fase 4).
- Motor de mapas (`MapEngine`) con validación de coherencia espacial matemática (Fase 3).
- Modelos de estado estructurado (WorldState, SessionState, SceneState, Room) con Pydantic.
- Estructura base del proyecto (engine, ai, models, gameplay, tests).
- Configuración de `pyproject.toml` con Pydantic y Pytest.
- Herramientas de formateo y linting (Ruff, Black) configuradas a 88 caracteres.
- Inicialización del entorno con `uv`.
