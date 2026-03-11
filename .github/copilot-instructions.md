# Copilot Instructions for new_aimaze Project

## Project Overview

**new_aimaze** is an AI-powered interactive fiction game inspired by classic Zork. It's a command-line adventure game where each playthrough generates a unique world with dynamic narratives, autonomous NPCs, and procedurally generated puzzles.

The game runs entirely in the terminal and must be in **Spanish (Spain)**.

**Project Goal:** Create a scalable, cost-effective AI-driven game engine that maintains coherent gameplay while generating emergent narratives.

**Key Principle:** Separate game logic (deterministic) from AI narrative (generative).

---

## 1. Docs

Documentos funcionales Inalterables

main.py                        # Entry point (currently minimal)
pyproject.toml                 # Project configuration
README.md                      # Project purpose (Zork-like game with AI)
docs/arquitectura.md           # System architecture design
docs/general_ia.md             # General IA architecture principles
docs/planteamiento_ia.md       # IA design patterns and strategies
docs/Entorno_tecnologico.md    # Technology environment 
docs/PROJECT_SUMMARY.md        # Project summary


---

## 2. Project Configuration

### Python Version
- **Required:** Python 3.12+ (see .python-version)

### Dependencies
- **Current:** None (empty in pyproject.toml)
- **Expected additions:**
  - LLM client libraries (anthropic, openai, ollama)
  - Command parsing libraries
  - Data serialization (pydantic for state management)

### Project Metadata
```toml
[project]
name = "new_aimaze"
version = "0.1.0"
description = "AI-powered Zork-style adventure game"
readme = "README.md"
requires-python = ">=3.12"
```

### Commands

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

## 3. Architecture Overview

### Two-Layer Architecture

```
┌─────────────────────────────────────────┐
│      AI Narrative Layer                 │
├─────────────────────────────────────────┤
│  - Narrative Planner                    │
│  - Director AI                          │
│  - NPC Decision AI                      │
│  - Narrator AI                          │
│  - Memory Extractor                     │
├─────────────────────────────────────────┤
│      Game Engine (Deterministic)        │
├─────────────────────────────────────────┤
│  - World Generator                      │
│  - Map Engine                           │
│  - Puzzle Engine                        │
│  - Event Simulation Engine              │
│  - NPC Engine                           │
└─────────────────────────────────────────┘
```

**Key Principle:** Game engine provides deterministic rules; AI layer interprets and narrates.

### Game Loop Flow

```
1. Player Input
   ↓
2. Command Parser
   ↓
3. Game Engine Update
   ↓
4. NPC Decision Engine
   ↓
5. Event Simulation Engine
   ↓
6. Director AI (narrative decisions)
   ↓
7. Narrator AI (generate scene description)
   ↓
8. Memory Extractor (update structured state)
   ↓
9. Output to Player
```

---

## 4. Core Systems Architecture

### 4.1 Game Engine Subsystems

#### World Generator
- **Purpose:** Generate initial world blueprint for each game
- **Output:** Structured world configuration with setting, theme, goal, threat, puzzle style
- **Example Settings:**
  - Abandoned space station (tech terror theme)
  - Medieval dungeon (fantasy mystery theme)
  - Aztec temple (ritual puzzle theme)
  - Underground city (exploration theme)
  - Lunar base (science fiction theme)

#### Map Engine
- **Purpose:** Generate connected room graph
- **Structure:** Rooms as nodes, exits as edges
- **Guarantees:** Spatial coherence, connectivity
- **Data Model:**
  ```json
  {
    "rooms": [
      {"id": "engine_room", "exits": ["corridor"]},
      {"id": "corridor", "exits": ["engine_room", "bridge"]}
    ]
  }
  ```

#### Puzzle Engine
- **Purpose:** Generate logic puzzles procedurally
- **Strategy:** Template-based generation (not random combinations)
- **Puzzle Types:**
  - Key and lock
  - Machine repair
  - Activation sequences
  - Symbolic logic
  - Item transport
  - Deduction challenges
- **Structure:**
  ```json
  {
    "puzzle_type": "repair",
    "blocked_path": "bridge",
    "items_needed": ["fuse", "toolkit"],
    "solution_steps": [...]
  }
  ```

#### Event Simulation Engine
- **Purpose:** Simulate time-based world events
- **Mechanism:** Events have progress values (0.0-1.0)
- **Behavior:** Progress increases each turn; triggers at 1.0
- **Event Types:**
  - Global (world-affecting)
  - Local (location-specific)
  - Personal (NPC-specific)
- **Example:**
  ```json
  {
    "event": "oxygen_failure",
    "progress": 0.4,
    "trigger_condition": "progress >= 1.0"
  }
  ```

#### NPC Engine
- **Purpose:** Manage NPC state and autonomous decisions
- **Model:** Each NPC is an autonomous agent with goals
- **NPC State:**
  ```json
  {
    "name": "Lysa",
    "role": "mercenary",
    "personality": ["pragmatic", "observant"],
    "goal": "earn money",
    "secret": "works for the assassin",
    "attitude_to_player": 3,
    "current_plan": "observe the player",
    "memory": []
  }
  ```

### 4.2 AI Layer Subsystems

#### Narrative Planner
- **Purpose:** Plan long-term story structure
- **Output:** Three-act structure with narrative arcs
- **Decisions:**
  - Story acts and goals
  - Key story turning points
  - Major conflicts
- **Replans:** When player significantly deviates

#### Director AI
- **Purpose:** Control narrative pacing and drama
- **Not:** A writer (only makes structural decisions)
- **Decisions:**
  ```json
  {
    "tension_level": 7,
    "scene_goal": "introduce suspicion",
    "event": "unknown enters tavern",
    "npc_focus": "Lysa",
    "twist_probability": 0.2
  }
  ```
- **Controls:**
  - Tension curve (exploration → suspicion → danger → climax)
  - Event injection
  - NPC highlighting
  - Clue placement

#### NPC Decision AI
- **Purpose:** Decide NPC actions each turn
- **Input:** Game state, NPC personality, NPC goals
- **Output:** Action and intent for each active NPC
- **Optimization:** Only evaluate "scene NPCs" (present in current location)
- **Example:**
  ```json
  {
    "npc": "Rurik",
    "action": "avoid answering directly",
    "intent": "protect a client"
  }
  ```

#### Narrator AI
- **Purpose:** Convert game state into evocative text descriptions
- **Input:**
  - Location description
  - Active events
  - Player action
  - NPC actions
  - Director output
- **Constraints:** Brief, evocative, 80-150 words
- **Not:** Should not break game rules or contradict state
- **Tone constraints:** Must include humor, 8-bit retro terror, and slight sarcasm. Never generic or overly polite assistant tone.
- **Hard limit:** Strictly 80-150 words.

#### Memory Extractor
- **Purpose:** Update structured game state after each scene
- **Input:** Current state, generated scene, events
- **Output:** Updated JSON state
- **Optimization:** Keeps state bounded (prevents token bloat)
- **Three-tier State Management:**
  - `world_state`: Permanent world information (never/rarely changes)
  - `session_state`: Game progress information (changes slowly)
  - `scene_state`: Current scene details (changes each turn)

---

## 5. State Management & Data Models

### Structured State Pattern

**Key Insight:** Don't send entire history to LLM each turn. Maintain structured state and only send relevant portions.

**Token Efficiency:** 10-20× reduction compared to full history approach.

### Three-Level State Hierarchy

#### world_state
```json
{
  "setting": "abandoned_space_station",
  "theme": "technological_terror",
  "goal": "reactivate navigation system",
  "main_threat": "corrupted AI",
  "puzzle_style": "electrical"
}
```
- Immutable or rarely changes
- Never sent to narrator in each prompt
- Contains: kingdom, factions, world history

#### session_state
```json
{
  "location": "engine_room",
  "inventory": ["lantern", "toolkit"],
  "known_npcs": {
    "Rurik": {"role": "tavern keeper", "attitude": "suspicious"},
    "Lysa": {"role": "mercenary", "attitude": "friendly"}
  },
  "completed_quests": [],
  "active_missions": [],
  "relationships": {},
  "story_progress": 0.3
}
```
- Changes slowly
- Contains: quests, known NPCs, relationships

#### scene_state
```json
{
  "location_description": "engine_room",
  "active_npcs": ["Rurik"],
  "immediate_danger": "reactor overheating",
  "current_objective": "find replacement fuse",
  "available_actions": ["examine", "take", "go"]
}
```
- Changes each turn
- Only this + relevant session_state sent to LLM

### Prompt Template Pattern

```text
SYSTEM ROLE
You are the narrator of an AI-driven RPG adventure.
Write brief, evocative descriptions (80-150 words).
Maintain consistency with the game state.

GAME STATE
{scene_state}
{relevant_session_state}

DIRECTOR GUIDANCE
{director_ai_output}

PLAYER ACTION
{parsed_player_action}

NPC ACTIONS
{active_npc_decisions}

TASK
Describe what happens next.
```

---

## 6. AI Strategy & Cost Control

### Model Assignment Strategy

| Component | Model | Reason |
|-----------|-------|--------|
| World Generation | Expensive (GPT-4o, Claude-3-opus) | One-time, high quality |
| Narrator | Expensive (GPT-4o) | Critical for player experience |
| Director | Cheap (GPT-4o-mini, Claude-3-haiku) | Structural decisions only |
| NPC Decisions | Cheap (GPT-4o-mini, Claude-3-haiku) | Low-stakes decisions |
| Memory Extractor | Cheap (GPT-4o-mini, Claude-3-haiku) | JSON parsing |

### Ideal Turn Cost
- Target: 1 expensive call per turn (narrator)
- Supporting: 2-3 cheap calls (director, NPC, memory)
- Result: 10-20× cheaper than naive approaches

### Token Efficiency Patterns

1. **Structured State:** Replace history with JSON state
   - Without: 2000 tokens (full history) + 200 tokens (response)
   - With: 150 tokens (state) + 200 tokens (response)

2. **Memory Vectorization:** Store important events as keywords
   - Only retrieve relevant memories on demand
   - Example: ["assassin", "tavern_keeper", "ancient_map"]

3. **NPC Selection:** Only active NPCs generate decisions
   - Absent NPCs use simple state transitions
   - Reduces API calls

---

## 7. Implementation Priorities

### Phase 1: MVP (Foundation)
1. Basic Zork-like command parser
2. Deterministic world state management
3. Simple room graph navigation
4. Basic event system
5. Template-based puzzle engine

### Phase 2: AI Integration
6. Narrator AI integration
7. Memory extractor
8. Basic Director AI
9. Scene state management

### Phase 3: Autonomous Systems
10. NPC autonomous agents
11. NPC decision engine
12. NPC memory tracking

### Phase 4: Advanced Features
13. Narrative planner
14. Dynamic event generation
15. Relationship tracking
16. World state generation for new games

---

## 8. Code Patterns & Conventions

### Architecture Principles

1. **Separation of Concerns**
   - Game logic separate from narrative
   - State management separate from rendering
   - AI layer doesn't modify game state directly

2. **Deterministic Game Engine**
   - All core mechanics are rule-based
   - No randomness in puzzle logic (puzzle rules are fixed)
   - Events progress predictably (unless randomized in design)

3. **State as Source of Truth**
   - Single, authoritative game state
   - All changes flow through state management
   - No hidden state between layers

4. **Efficiency First**
   - Minimize LLM calls per turn
   - Maximize cache hits for descriptions
   - Use structured state throughout

### Expected Project Structure

```
ai_zork/
├── engine/
│   ├── world.py              # World generation
│   ├── map_engine.py         # Room graph, navigation
│   ├── puzzle_engine.py      # Puzzle templates, logic
│   ├── event_engine.py       # Event simulation
│   ├── npc_engine.py         # NPC state management
│   └── command_parser.py     # Parse player input
│
├── ai/
│   ├── llm_client.py         # LLM API abstraction
│   ├── narrative_planner.py  # Story planning
│   ├── director_ai.py        # Narrative direction
│   ├── npc_decision_ai.py    # NPC decision making
│   ├── narrator_ai.py        # Scene description
│   └── memory_extractor.py   # State updates
│
├── models/
│   ├── world_state.py        # State data classes
│   ├── npc.py                # NPC data model
│   ├── puzzle.py             # Puzzle data model
│   └── event.py              # Event data model
│
├── gameplay/
│   ├── game_loop.py          # Main game loop
│   └── session_manager.py    # Session state
│
└── main.py                   # Entry point
```

### Naming Conventions

- **State classes:** Use clear, descriptive names (WorldState, NPCAgent, PuzzleTemplate)
- **AI functions:** Prefix with intent (generate_scene, decide_npc_action, extract_memory)
- **Event types:** Use snake_case (oxygen_failure, npc_hunting_player)
- **Functions:** Use verbs (update, generate, parse, extract)

---

## 9. Integration Points with AI Tools

### For Copilot/Cline/Cursor

When using AI tools for development, provide context about:

1. **Architecture Decisions:**
   - Two-layer design (deterministic engine + AI narrative)
   - Structured state (world/session/scene)
   - Token efficiency strategies

2. **Game Loop Flow:**
   - Player input → Parse → Update engine → NPC decisions → Director → Narrator → Output

3. **Cost Constraints:**
   - 1 expensive call per turn (narrator)
   - Use cheap models for NPC/Director/Memory
   - Minimize tokens sent to LLM

4. **State Management:**
   - Keep state JSON-serializable
   - Never send entire history to narrator
   - Use three-tier state hierarchy

5. **NPC Autonomy:**
   - NPCs make decisions independently
   - Only "scene NPCs" are evaluated each turn
   - Emergent behaviors expected

---

## 10. Key Design Files Reference

### arquitectura.md
- Two-layer architecture design
- Detailed subsystem descriptions
- Complete data model examples
- Suggested tech stack

### planteamiento_ia.md
- Game State + Scene Prompt pattern (most important)
- Token efficiency techniques
- Director AI pattern
- NPC Autonomous Agents pattern
- Memory management strategies
- Real code flow examples

### general_ia.md
- Design principles
- World generation approach
- Map generation algorithm
- Puzzle generation templates
- Event simulation mechanics
- NPC autonomy model
- Memory structure
- Turn flow

---

## 11. Important Patterns to Implement

### Pattern 1: Game State + Scene Prompt
**Why:** Reduces tokens 10-20× vs. full history
**How:** Maintain structured state, send only current state to narrator
**File Reference:** planteamiento_ia.md sections 2-6

### Pattern 2: Director AI Pattern
**Why:** Creates coherent, paced narratives automatically
**How:** AI makes structural decisions, narrator writes the scene
**File Reference:** planteamiento_ia.md section 11

### Pattern 3: NPC Autonomous Agents
**Why:** Makes world feel alive, creates emergent gameplay
**How:** Each NPC has goals, personality, makes independent decisions
**File Reference:** planteamiento_ia.md section on NPC Autonomous Agents

### Pattern 4: Memory Extractor
**Why:** Keeps state bounded, prevents token bloat
**How:** After each scene, extract relevant state updates with cheap model
**File Reference:** planteamiento_ia.md sections 4, 6

### Pattern 5: Three-Tier State
**Why:** Organizes state by change frequency
**How:** world_state (static), session_state (slow), scene_state (dynamic)
**File Reference:** planteamiento_ia.md section 6

---

## 12. Development Checklist

- [ ] Set up Python 3.12 environment
- [ ] Initialize project structure
- [ ] Implement command parser
- [ ] Build world state models (Pydantic)
- [ ] Implement game loop framework
- [ ] Build basic map engine
- [ ] Implement puzzle template engine
- [ ] Add event simulation
- [ ] Integrate LLM client
- [ ] Implement memory extractor
- [ ] Add narrator AI integration
- [ ] Add Director AI
- [ ] Implement NPC decision engine
- [ ] Add NPC autonomous behavior
- [ ] Build narrative planner
- [ ] Implement world generator
- [ ] Add save/load system
- [ ] Optimize token usage
- [ ] Add comprehensive logging

---

## 13. Testing & Validation

### Unit Testing
- Command parser correctness
- State transitions
- Event progression logic
- Puzzle solution validation

### Integration Testing
- LLM call flow
- State updates after narration
- NPC behavior consistency
- Event triggering

### Gameplay Testing
- Narrative coherence
- NPC believability
- Puzzle fairness
- Cost tracking

---

## 14. Current Status

**Main.py:** Minimal placeholder
**Architecture:** Fully designed in markdown documents
**Implementation:** Ready to begin Phase 1
**Key Files Created:** All design documentation complete

---

## 15. Contact & References

- See `docs/arquitectura.md` for system design details
- See `docs/general_ia.md` for design principles
- See `docs/planteamiento_ia.md` for AI patterns and strategies
- See `README.md` for project purpose

---

## 16. Key conventions

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

### Testing & Commits (The Iron Law)
- **Test de la Brújula Rota:** Map navigation MUST have tests proving spatial coherence (if player goes North from A to B, South from B MUST return to A).
- **No Red Commits:** If `uv run pytest` fails, DO NOT propose a commit.
- **Bug = Test:** Every time a logical bug is fixed, a new pytest must be created before the changelog entry.

---

### Strict Anti-Goals (DO NOT IMPLEMENT)
- **NO LLM Map Generation:** The AI MUST NOT generate maps, rooms, or connections. Spatial coherence is strictly mathematical (North to B means South to A).
- **NO Multiplayer:** Single-player only. Do not add session IDs for multiple users or networking code.
- **NO i18n (Internationalization):** Do not extract strings to JSON/YAML for localization. The game is exclusively in Spanish (Español de España).
- **NO GUI/Graphics:** Do not import UI libraries (Tkinter, PyQt) or web frameworks yet. Standard terminal output only.



**Next Steps:** Begin implementing Phase 1 (MVP foundation)

### Phase 1 Execution Rules (MOCK EVERYTHING)
- **Zero API Calls:** During Phase 1, the AI layer MUST BE MOCKED.
- Do not implement real `ollama` or `openai` calls yet to preserve quotas.
- The "Spike" for week 1: Create a simple dummy function that takes a static JSON `scene_state` and prints a hardcoded narrative response to validate the terminal output formatting.
