# Copilot Instructions — new-aimaze

## Project overview

AI-powered text adventure game in the style of Zork, written in Python 3.12.
Currently in early design phase — `main.py` is a placeholder. All implementation
detail is in the design docs (`docs/design_architecture.md`, `docs/general_ia.md`, `docs/planteamiento_ia.md`).

The game runs entirely in the terminal and must be in **Spanish (Spain)**.

---

## Commands

```bash
# Run the game
uv run python main.py

# Activate virtual environment
source .venv/bin/activate

# Add a dependency (never use pip install)
uv add <package>

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/path/to/test_file.py::test_function_name
```

---

## Architecture

Two strictly separated layers:

```
Game Engine (deterministic — controls rules, state, map, puzzles)
AI Narrative Layer (generative — interprets and narrates)
```

**The Game Engine always wins.** The AI only interprets, decides, and narrates.

### Planned module structure

```
ai_zork/
├── engine/       # world.py, map_engine.py, puzzle_engine.py, npc_engine.py, event_engine.py
├── ai/           # llm_client.py, narrative_planner.py, director_ai.py, npc_ai.py,
│                 # narrator_ai.py, memory_extractor.py
├── models/       # world_state.py, npc.py, puzzle.py, event.py
├── gameplay/     # command_parser.py, game_loop.py
└── main.py
```

### Main game loop (pseudocode from design docs)

```python
while game_running:
    action = get_player_input()
    parsed_action = command_parser(action)
    game_engine.apply_action(parsed_action)
    npc_engine.update()
    event_engine.update()
    director.update()
    scene = narrator.generate_scene()
    print(scene)
```

### Three-tier state (critical for token control)

World state is split into three levels sent to the LLM selectively:

- **`world_state`** — immutable world facts (setting, factions, lore). Sent rarely.
- **`session_state`** — game progress (inventory, known NPCs, completed quests). Sent contextually.
- **`scene_state`** — current scene only (location, present NPCs, active threat). Sent every turn.

This achieves **10–20× token reduction** versus naive full-history prompting.

### AI model tiering

| Function           | Model tier      |
|--------------------|-----------------|
| World generation   | Expensive model |
| Narrator AI        | Expensive model |
| Director AI        | Cheap model     |
| NPC decisions      | Cheap model     |
| Memory extractor   | Cheap model     |

- **Development:** Ollama (local)
- **Production:** OpenAI

One LLM call per turn is the target.

---

## Key conventions

### Package management
- Use `uv add <package>` exclusively — never `pip install`.
- Virtual environment lives at `.venv/` in project root.
- Always run code via `uv run ...` or with the venv activated.

### Code style
- Max line length: **88 characters**.
- Max cyclomatic complexity: **10**.
- Functions must be small and have a **single responsibility**.
- Extract helper functions to reduce complexity.
- Use **early returns** to avoid deep nesting.
- Split files into focused modules when they grow.

### Documentation
- Document **in the code**, not in external documents.
- Code comments and docstrings are for AI maintainability — be explicit about intent.

### Changelog (bitácora)
- **Every change must be logged in the changelog.** No exceptions.
- No commit without a changelog entry.

### Commits
Conventional Commits format: `tipo(scope): descripción`

Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`

Commit at atomic steps (frequently, small units).

### Testing
- Framework: `pytest`.
- Tests live in `tests/`.

---

## Core AI patterns (from design docs)

### Game State + Scene Prompt
Send structured JSON state instead of conversation history. State doesn't grow
over time, keeping token usage flat across the entire game session.

### Memory Extractor
After each narrator call, a cheap model call extracts and updates `scene_state`
from the generated scene. This keeps state accurate without manual tracking.

### Director AI
A cheap model evaluates `world_state + story_progress + player_action` and
returns a JSON decision (introduce tension, activate NPC, trigger event). The
narrator then writes the scene from that directive — it does not write the scene
itself.

### NPC Autonomous Agents
Each NPC has `goal`, `attitude_to_player`, and `current_plan`. Only NPCs
**present in the current scene** are evaluated by AI each turn.

### Narrative Planner
Plans the story in 3-act arcs. If the player derails the plan, it recalculates.
Controls pacing ratios (exploration / dialogue / danger).
