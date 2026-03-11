# FASE3_IMPLEMENTACION.md
# Guía de Ejecución para la Fase 3: Sistemas Autónomos (El Mundo Vivo)

**Objetivo:** Implementar el motor de decisión de NPCs y la simulación avanzada de eventos para que el mundo sea proactivo, sin disparar los costes de la API.

#### 🧬 Prompt 1: Evolución del Modelo NPC
> "Actualiza los modelos de datos en `models/state.py` para los NPCs. Un NPC ya no es solo un nombre; debe ser un agente estructurado. Añade los campos: `personality` (lista de strings), `goal` (string), `secret` (string, opcional), `attitude_to_player` (int de 1 a 5) y `current_plan` (string). Modifica el `WorldState` o `SessionState` inicial (el de prueba) para incluir un NPC llamado 'Lysa' (mercenaria, pragmática, objetivo: ganar dinero) y otro llamado 'Rurik' (tabernero, sospechoso). Actualiza los tests y el CHANGELOG."

#### 🧠 Prompt 2: El Motor de Decisión NPC (NPC Decision AI)
> "Crea el módulo `ai/npc_ai.py`. Crea una función que reciba el `SceneState` actual y los datos de un único NPC. Usa `LLMClient.generate_cheap(json_mode=True)`. El prompt debe pedirle a la IA que decida la próxima acción del NPC basándose en su personalidad y objetivos, reaccionando a la acción previa del jugador. Debe devolver estrictamente un JSON: `{"action": "<acción breve>", "intent": "<motivo oculto>"}`. Escribe tests con mocks. Actualiza CHANGELOG."

#### ⚙️ Prompt 3: Integración y Filtro de Costes (CRÍTICO)
> "Actualiza el `gameplay/game_loop.py` para integrar las decisiones de los NPCs. REGLA INNEGOCIABLE PARA CONTROL DE COSTES: El bucle de NPCs SOLO debe iterar y llamar a `npc_ai` para los NPCs que estén PRESENTES en la sala actual (los 'scene_npcs'). Los NPCs en otras habitaciones ignoran su turno o usan lógica dummy. Recopila las acciones de los NPCs presentes y añádelas al `SceneState` bajo la clave `npc_actions` para que el Narrador las vea. Actualiza tests y CHANGELOG."

#### ⏳ Prompt 4: El Motor de Simulación de Eventos Avanzado
> "Refactoriza el `EventEngine` de la Fase 1 (`engine/event_engine.py`). Permite que el `DirectorAI` o los propios NPCs puedan inyectar nuevos eventos con `progress = 0.0`. Cuando un evento llegue a `1.0`, debe generar un `event_triggered` (ej. 'Los guardias irrumpen en la sala') y añadirse al `SceneState`. Modifica el `NarratorAI` para que, si recibe `event_triggered` o `npc_actions` en el estado, los integre en la narrativa obligatoriamente. Haz tests unitarios."

#### 🎭 Prompt 5: La Prueba del "Turno de Espera"
> "Añade el comando 'esperar' (o 'pasar turno') al `CommandParser`. Configura un escenario de prueba en `main.py` donde haya un evento ('oxígeno disminuyendo' a 0.8 de progreso) y un NPC hostil en la sala. El humano solo debe pulsar 'esperar'. El sistema debe procesar las intenciones del NPC, avanzar el progreso del evento a 1.0 y obligar al Narrador a describir cómo el mundo reacciona sin que el jugador haya hecho nada. Comprueba linting, complejidad < 10 y haz el último commit en CHANGELOG."