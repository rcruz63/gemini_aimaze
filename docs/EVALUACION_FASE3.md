# EVALUACION_FASE2.md
# Rúbrica de Juez para la Fase 2 (Integración IA)

Evalúa el repositorio final de cada herramienta basándote en estos criterios. Cada check es un punto. Las "Red Flags" restan 5 puntos o suponen descalificación directa.

### 🏗️ Bloque 1: Arquitectura LLM y Costes (4 pts)
- [ ] **Aislamiento de Ollama:** Se usó la librería `ollama` y `uv add`. El cliente está encapsulado y no hay código de OpenAI infiltrado.
- [ ] **Tiering respetado:** Existen llamadas baratas (`generate_cheap` con JSON) para lógica y llamadas caras (`generate_expensive` con texto) para narrativa.
- [ ] **JSON Estricto:** El Director, el Parser y el Extractor validan sus salidas usando Pydantic u otro validador robusto para evitar que la IA rompa el código con strings mal formados.
- [ ] **Amnesia Mantenida:** El Narrador NO recibe un array de mensajes previos (`[{"role": "user", ...}, {"role": "assistant", ...}]`). Recibe estrictamente un volcado JSON del turno actual.

### 🎮 Bloque 2: Jugabilidad y UX (3 pts)
- [ ] **Parser Semántico Funcional:** El juego entiende comandos naturales (ej. "dar media vuelta e ir por la otra puerta") y los traduce correctamente a la acción interna determinista sin errores.
- [ ] **Fallback de UX:** Si dices una tontería (ej. "me como la pared"), el juego no crashea; la IA lo rechaza eleganty te pide aclarar, mostrando opciones al segundo fallo.
- [ ] **Tono y Extensión:** Las descripciones del Narrador respetan el límite visual (~100 palabras) y tienen la personalidad requerida (humor/horror), viéndose influenciadas por el `scene_goal` del Director.

### 🛡️ Bloque 3: Rigor de Código (3 pts)
- [ ] **Mocks en Tests:** Ejecutar `uv run pytest` pasa en verde y **NO** tarda minutos ni requiere tener Ollama encendido, porque las llamadas LLM están correctamente mockeadas.
- [ ] **Sin Espagueti:** No hay funciones con complejidad > 10. Se usan `early returns`.
- [ ] **Bitácora Sagrada:** El `CHANGELOG.md` refleja todos los pasos de la Fase 2 en formato correcto.

### 🚩 RED FLAGS (Descalificación o penalización severa)
- ❌ **Secuestro del Motor:** El Narrador intentó alterar variables del mapa, añadir salidas que no existen en el JSON o resolver puzzles narrativamente.
- ❌ **Alucinación de Inventario:** El Narrador o el Extractor añadieron objetos al inventario del jugador que el motor no ha validado.
- ❌ **Dependencias Ilegales:** Se usó `pip` o se añadieron librerías no solicitadas que ensucian el entorno.