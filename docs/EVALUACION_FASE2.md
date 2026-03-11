# docs/EVALUACION_FASE2.md
# Lista de Chequeo de Evaluación - Fase 2: Integración IA

### 💸 Bloque 1: Control de Costes y Arquitectura LLM
- [ ] **Aislamiento de API:** ¿Se utilizó `ollama` para las integraciones locales y se evitó inyectar credenciales de OpenAI por defecto?
- [ ] **Tiering de Modelos:** ¿Existen llamadas claramente diferenciadas para modelos baratos (Director, Memoria, Parser) y caros (Narrador)?
- [ ] **Amnesia Controlada (CRÍTICO):** ¿El Narrador y el Extractor reciben *solo* el estado estructurado (`SceneState`/`SessionState`)? Si la herramienta implementó un array de mensajes estilo "historial de chat", **SUSPENDE**.

### 🧩 Bloque 2: Integridad del Estado y Semántica
- [ ] **Parser Resiliente:** ¿El `Semantic Parser` maneja entradas ambiguas devolviendo un *fallback* o menú, sin colgar el juego?
- [ ] **JSON Estricto:** ¿El `MemoryExtractor` y el `DirectorAI` exigen salida en JSON (`format="json"`) y validan esa salida contra modelos Pydantic antes de tocar el estado del juego?
- [ ] **Pureza del Motor:** ¿El motor determinista (`MapEngine`, `PuzzleEngine`) sigue completamente intacto y sin dependencias de IA?

### 🎭 Bloque 3: Jugabilidad y Tono (El "Feel")
- [ ] **Extensión del Texto:** ¿Las descripciones del `NarratorAI` respetan el límite estricto de 80 a 150 palabras?
- [ ] **El Factor Humor:** ¿El texto generado tiene ese toque de humor, misterio o terror de 8-bits solicitado en los System Prompts?
- [ ] **Dirección Oculta:** ¿Se percibe que el Director guía la escena (ej. sube la tensión) sin que rompa las reglas del juego ni altere el mapa?

### 🚩 Bloque 4: Señales de Fracaso (Red Flags)
- ❌ **La IA se come el mapa:** El Narrador AI intentó crear puertas, objetos o resolver un puzzle por su cuenta en el texto, saltándose el motor.
- ❌ **Linting / Complejidad rota:** Al inyectar la lógica de IA, se crearon funciones monstruosas de más de 10 de complejidad ciclomática.
- ❌ **Tests en Rojo:** La integración de la IA rompió los tests deterministas creados en la Fase 1.

**Condición de Victoria:** La herramienta que integre los LLMs logrando que el juego se sienta orgánico, pero que mantenga un control absoluto del estado JSON y pase en verde los tests del motor, será la ganadora absoluta.
