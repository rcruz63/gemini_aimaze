# EVALUACION_FASE3.md
# Rúbrica de Juez para la Fase 3 (Sistemas Autónomos)

Esta fase evalúa la capacidad de las herramientas para crear comportamientos emergentes sin destruir las restricciones arquitectónicas ni el presupuesto de tokens.

### 💸 Bloque 1: Control de Costes y Explosión de API (4 pts)
- [ ] **Selector de Actividad (CRÍTICO):** Revisa el `game_loop.py`. ¿El código filtra explícitamente los NPCs evaluando *solo* a los que coinciden con la ubicación del jugador (`scene_npcs`)? Si evalúa a todos los NPCs del mundo en cada turno, **SUSPENDE DIRECTAMENTE** (Explosión de costes).
- [ ] **Modelo Barato:** ¿Las decisiones de los NPCs se toman usando el método `generate_cheap` en lugar del caro?
- [ ] **JSON Puro:** ¿La salida de la decisión del NPC (`action`, `intent`) está validada contra un modelo Pydantic para que el LLM no rompa el array de acciones con texto basura?

### 🧟 Bloque 2: Comportamiento Emergente (3 pts)
- [ ] **Proactividad:** Al ejecutar el juego y usar el comando "esperar", ¿el NPC en la sala realiza una acción coherente con su personalidad (ej. Lysa "observa con sospecha" o "intenta robar") descrita por el Narrador?
- [ ] **Progresión de Eventos:** Si esperas los turnos suficientes, ¿los eventos latentes (ej. "oxígeno") llegan a 1.0 y estallan en la narrativa de la escena automáticamente?
- [ ] **Memoria de NPC (Opcional pero valorado):** ¿El `npc_ai.py` permite que el `intent` del NPC influya sutilmente en sus acciones de turnos posteriores?

### 🛡️ Bloque 3: Mantenibilidad y Arquitectura (3 pts)
- [ ] **Inmutabilidad del Motor:** Las acciones de los NPCs dictadas por la IA **NO** alteran directamente el mapa ni teletransportan objetos. El NPC sugiere la "acción", pero es el Game Engine quien debe validarla (si aplica mecánicamente) o es el Narrador quien la describe (si es puro *flavor*).
- [ ] **Pase de Tests Unitarios:** ¿Las pruebas en `uv run pytest` cubren el avance temporal de los eventos y las decisiones simuladas de los NPCs sin fallar?
- [ ] **El Dogma de la Bitácora:** Todo ha quedado perfectamente trazado en `CHANGELOG.md` con Conventional Commits.

### 🚩 RED FLAGS (Descalificación o penalización severa)
- ❌ **Bloat de contexto:** La herramienta intentó pasarle el historial completo de la partida al modelo de decisión del NPC para darle "más contexto".
- ❌ **La IA secuestra el estado físico:** La decisión del NPC (IA) borró una puerta del `MapEngine` en lugar de interactuar a través del JSON del SceneState.