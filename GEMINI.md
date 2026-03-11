# GEMINI.md - Project Context

## Project Overview
**new-aimaze** is an AI-powered, Zork-inspired text adventure game. It blends a deterministic game engine (rules, maps, puzzles) with a generative AI narrative layer (storytelling, NPC dialogue, dramatic pacing).

### Key Architecture Principles
- **Deterministic Core:** The game engine manages the "truth" (inventory, location, connectivity, puzzle status) without AI hallucination.
- **AI Narrative Layer:** AI interprets the engine's state to generate immersive descriptions and handle NPC interactions.
- **Strict JSON Rule (CRITICAL):** Every LLM output intended to modify game state or guide narrative MUST be validated with a specific Pydantic model before processing. Direct injection of raw LLM JSON into the engine or state is strictly forbidden.
- **Token Efficiency:** Uses a structured, three-tier JSON state management system (World, Session, Scene) instead of sending full chat histories to the LLM, achieving 10-20x token reduction.
- **Director AI:** A specialized AI agent that manages pacing, tension, and world events.

## Tech Stack
- **Language:** Python 3.12+
- **Environment Management:** `uv` (preferred over pip)
- **Data Validation:** `Pydantic` (for structured state models)
- **Testing:** `pytest`
- **Linting/Formatting:** `Ruff`, `Black`, `Mypy` (max line length: 88)

## Project Structure
```text
new_aimaze/
├── engine/         # Deterministic logic (map, puzzles, events, npcs)
├── ai/             # LLM clients and specialized agents (narrator, director)
├── models/         # Pydantic state models (WorldState, SessionState, SceneState)
├── gameplay/       # Command parser and main game loop
└── main.py         # Entry point
```

## Building and Running
### Setup
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Development Commands
- **Run Game:** `python main.py`
- **Run Tests:** `pytest`
- **Format Code:** `black .`
- **Lint:** `ruff check .`
- **Type Check:** `mypy .`

## Development Conventions
- **Surgical Logic:** Keep game logic separate from AI narrative generation.
- **State Integrity:** Spatial coherence is mathematical (e.g., if North leads to Room B, South from Room B must lead to Room A).
- **Code Quality:**
    - Max cyclomatic complexity: 10.
    - Use early returns for validations.
    - Mandatory docstrings for classes and public methods.
    - Max line length: 88 characters.
- **Workflow:**
    - Update `CHANGELOG.md` with every significant feature or fix.
    - Write unit tests for all engine logic before integrating AI.
    - Use tiered LLM strategies (cheaper models for logic/summarization, better models for narrative).

## Key Documentation
- `docs/planteamiento_ia.md`: Core AI patterns and token-saving strategies (CRITICAL).
- `docs/arquitectura.md`: Detailed system design.
- `docs/PROJECT_SUMMARY.md`: High-level roadmap and status.
- `.github/copilot-instructions.md`: Specific instructions for AI-assisted coding.
