# new-aimaze Project Summary

## Quick Facts

- **Project Type:** AI-Powered Text Adventure Game (Zork-inspired)
- **Status:** Design Phase Complete, Implementation Phase 1 Ready
- **Python Version:** 3.12+
- **Code Files:** 1 (placeholder main.py)
- **Documentation:** ~57 KB across 5 markdown files
- **Generated Guides:** copilot-instructions.md (18 KB)
- **Git History:** Empty (no commits yet)

---

## Architecture at a Glance

```
┌─────────────────────────────────────┐
│  AI NARRATIVE LAYER (Generative)   │
│ - Narrator, Director, NPC AI       │
├─────────────────────────────────────┤
│  GAME ENGINE (Deterministic)       │
│ - World, Map, Puzzles, Events      │
└─────────────────────────────────────┘
```

**Key Principle:** Game engine (deterministic rules) + AI layer (narrative interpretation)

---

## The 5 Critical Design Patterns

### 1. Game State + Scene Prompt
**Impact:** 10-20× token reduction
**How:** Send structured JSON state instead of full history
**Cost:** 350 tokens/turn vs 5200 tokens/turn at turn 50

### 2. Director AI Pattern
**Impact:** Automatic pacing and drama
**How:** AI makes structural decisions (JSON), narrator writes scene
**Result:** Coherent narratives without passive gameplay

### 3. NPC Autonomous Agents
**Impact:** Living world with emergent behaviors
**How:** Each NPC has goals, makes independent decisions
**Cost:** Only "scene NPCs" evaluated

### 4. Memory Extractor
**Impact:** State stays bounded
**How:** Post-scene extraction with cheap model
**Result:** No token bloat regardless of game length

### 5. Three-Tier State Management
**Impact:** Efficient data organization
**How:** world_state (static) | session_state (slow) | scene_state (dynamic)
**Result:** Only send necessary tokens per turn

---

## Implementation Timeline

| Phase | Focus | Duration |
|-------|-------|----------|
| 1 | MVP Foundation | 2-3 weeks |
| 2 | AI Integration | 2-3 weeks |
| 3 | Autonomous Systems | 2-3 weeks |
| 4 | Advanced Features | 4-6 weeks |
| **Total** | **Full Product** | **~10-12 weeks** |

---

## File Reference Guide

| File | Size | Priority | Use For |
|------|------|----------|---------|
| **arquitectura.md** | 6.6 KB | High | System design overview |
| **general_ia.md** | 6.0 KB | High | Design principles |
| **planteamiento_ia.md** | 25.4 KB | ⭐⭐⭐ | Core AI patterns (MOST IMPORTANT) |
| **copilot-instructions.md** | 18 KB | High | AI tool integration guide |
| **README.md** | 384 bytes | Low | Project purpose |

---

## Key Numbers

- **Token Reduction:** 10-20× vs naive approaches
- **Cost Reduction:** 3-4× via model tiering
- **Ideal Turn Cost:** 1 expensive call + 2-3 cheap calls
- **Max State Size:** ~150 tokens (bounded)
- **NPC Evaluation:** Only active scene NPCs

---

## Core Systems

### Game Engine
- **World Generator:** Blueprint with setting/theme/goal/threat
- **Map Engine:** Room graphs with guaranteed connectivity
- **Puzzle Engine:** Template-based (repair, keys, sequences, logic)
- **Event Engine:** Time-based progression (0.0-1.0)
- **NPC Engine:** Autonomous agents with goals

### AI Layer
- **Narrative Planner:** Long-form story structure
- **Director AI:** Pacing and drama control
- **NPC Decision AI:** Autonomous agent actions
- **Narrator AI:** Scene generation (80-150 words)
- **Memory Extractor:** State update after each turn

---

## What's Not Done (Yet)

- ❌ No actual code (except placeholder)
- ❌ No dependencies configured
- ❌ No testing framework
- ❌ No LLM integration
- ❌ No game loop implementation

## What's Done

- ✅ Complete architecture design
- ✅ Five core AI patterns documented
- ✅ Data models specified with examples
- ✅ Implementation roadmap clear
- ✅ Cost control strategies detailed
- ✅ copilot-instructions.md created

---

## Next Steps

1. **Immediate:**
   - Set up Python 3.12 environment
   - Create project directory structure
   - Update pyproject.toml with dependencies

2. **Phase 1 (MVP):**
   - Implement command parser
   - Build state data models
   - Create game loop
   - Build map engine
   - Implement puzzle engine

3. **Phase 2 (AI):**
   - Add LLM client
   - Implement memory extractor
   - Add narrator AI
   - Add director AI

4. **Phase 3 (Life):**
   - NPC decision making
   - Emergent behaviors
   - Relationship tracking

5. **Phase 4 (Polish):**
   - World generator
   - Narrative planner
   - Optimization
   - Full product

---

## Important Design Decisions

1. **Separate concerns:** Game logic never touches narrative
2. **Structured state:** JSON-based, never send full history
3. **Model tiering:** Expensive for narrative, cheap for logic
4. **Template generation:** For coherence, not randomness
5. **NPC autonomy:** Independent decision-making per agent
6. **Scene-based evaluation:** Only active NPCs get LLM calls

---

## Cost Control Summary

| Area | Strategy | Savings |
|------|----------|---------|
| State | Structured instead of history | 10-20× |
| Models | Tiered by quality needs | 3-4× |
| NPCs | Only scene NPCs evaluated | 5-10× |
| Memory | Vectorized keywords | 2-5× |
| **Total** | **Combined strategies** | **50-100×** |

---

## Documentation Hierarchy

1. **Start here:** README.md (project purpose)
2. **Then read:** copilot-instructions.md (AI tool guide)
3. **Deep dive:** arquitectura.md + general_ia.md (design)
4. **Master:** planteamiento_ia.md (AI patterns - most critical)

---

## Quick Start Commands (Future)

```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .

# Development
pytest                      # Run tests
black .                     # Format code
ruff check .               # Lint
mypy .                     # Type check

# Run game
python -m new_aimaze       # Start game
```

---

## Contact Points

- **Architecture:** See arquitectura.md
- **AI Patterns:** See planteamiento_ia.md (CRITICAL)
- **Design Principles:** See general_ia.md
- **AI Tool Integration:** See copilot-instructions.md
- **Project Purpose:** See README.md

---

## Current Status Badge

**Design Phase:** ✅ Complete
**Documentation:** ✅ Comprehensive  
**Architecture:** ✅ Proven patterns
**Implementation:** 🚫 Not started

**Readiness:** 100% design, 0% code → Ready for Phase 1

---

*Last Updated: 2026*
*Analysis includes copilot-instructions.md creation*
