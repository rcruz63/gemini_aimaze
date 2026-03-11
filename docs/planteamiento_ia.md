# Contextos estructurados

## Planteamiento 

Un remake de Zork con IA.

Este patrón se usa bastante en **juegos narrativos con LLM** porque reduce muchísimo el número de tokens que mandas a la API.
La idea es **no enviar toda la historia cada vez**, sino **mantener un estado estructurado del mundo** y que el modelo solo escriba la escena usando ese estado.

Dicho de forma simple:

> El modelo no recuerda la historia → **tú mantienes la memoria del mundo en formato estructurado**.

Eso reduce tokens **10-20×** fácilmente.

---

## 1️⃣ El problema típico en juegos con IA

Muchos juegos hacen algo así:

```text
Historia hasta ahora:
- Llegaste a la ciudad
- Hablaste con el tabernero
- Descubriste un mapa
- Un asesino te persigue
- ...

Describe lo que ocurre ahora.
```

Cada turno:

* el contexto crece
* el coste sube
* la latencia aumenta

Después de 50 turnos es un desastre.

---

## 2️⃣ El patrón: **Game State + Scene Prompt**

En lugar de enviar toda la historia, mantienes un **estado del mundo estructurado**.

Ejemplo:

```json
{
  "location": "Taberna del Dragón Dormido",
  "time": "noche",
  "player_goal": "descubrir quien envió al asesino",
  "player_status": {
    "health": "herido",
    "gold": 12
  },
  "important_npcs": [
    {
      "name": "Rurik",
      "role": "tabernero",
      "attitude": "sospechoso"
    },
    {
      "name": "Lysa",
      "role": "mercenaria",
      "attitude": "amigable"
    }
  ],
  "current_threat": "asesino buscando al jugador"
}
```

Eso **no crece con la historia**.

---

## 3️⃣ El prompt narrativo

Luego haces algo como esto:

```text
SYSTEM
Eres el narrador de un RPG de fantasía oscura.
Escribe descripciones breves y evocadoras.

GAME STATE
{json_state}

PLAYER ACTION
"Pregunto al tabernero si ha visto al asesino"

TASK
Describe lo que ocurre ahora.
Máximo 120 palabras.
```

El modelo inventa la escena usando **solo el estado actual**.

---

## 4️⃣ El truco importante: **Memory extractor**

Después de generar la escena, haces otra llamada **barata** para actualizar el estado.

Usando `gpt-4o-mini` por ejemplo:

```text
Analiza la escena y actualiza el estado del mundo.

Estado actual:
{json_state}

Escena:
{scene}

Devuelve SOLO el JSON actualizado.
```

Resultado:

```json
{
  "location": "Taberna del Dragón Dormido",
  "time": "noche",
  "player_goal": "descubrir quien envió al asesino",
  "important_events": [
    "Rurik afirma no haber visto nada",
    "Lysa observa al jugador desde una mesa"
  ],
  "current_threat": "asesino posiblemente dentro de la taberna"
}
```

---

## 5️⃣ Arquitectura típica de juegos IA

Muchos prototipos usan algo así:

```
player action
     │
     ▼
scene generator (modelo bueno)
     │
     ▼
memory extractor (modelo barato)
     │
     ▼
update game state
```

Modelo caro → **solo narrativa**
Modelo barato → **gestión del estado**

---

## 6️⃣ Optimización brutal (muy usada)

Divide el estado en tres niveles:

```json
{
  "world_state": {},
  "session_state": {},
  "scene_state": {}
}
```

### world_state

No cambia casi nunca.

```
reino
facciones
historia del mundo
```

### session_state

Estado de la partida.

```
misiones
NPC conocidos
relaciones
inventario
```

### scene_state

Solo la escena actual.

```
lugar
NPC presentes
peligro actual
```

En cada prompt solo envías:

```
scene_state + parte relevante de session_state
```

El `world_state` ni se manda.

---

## 7️⃣ Ahorro real de tokens

Sin estructura:

```
historia completa → 2000 tokens
respuesta → 200 tokens
```

Con estado estructurado:

```
game_state → 150 tokens
respuesta → 200 tokens
```

En juegos largos esto es **10-20× más barato**.

---

## 8️⃣ Otro truco que usan algunos juegos

Mantener una **memoria vectorial de eventos importantes**.

Solo se recuperan cuando hace falta:

```
"asesino"
"tabernero"
"mapa antiguo"
```

Eso evita mandar todo el lore cada vez.

---

## 9️⃣ Mini ejemplo real de loop

Pseudo-flujo:

```python
scene = narrator_llm(
    state=current_state,
    player_action=action
)

new_state = memory_llm(
    state=current_state,
    scene=scene
)

current_state = new_state
```

---

💡 **Opinión:**
Este patrón es probablemente **la arquitectura más importante para juegos con IA hoy**. Sin él el coste se dispara muy rápido.

---

## 10️⃣ Director AI pattern

Si quieres, puedo enseñarte también **otro patrón todavía más potente para juegos narrativos**:

**"director AI pattern"**

Es el que usan algunos prototipos tipo **AI dungeon avanzado**, donde una IA controla:

* tensión narrativa
* giros de guion
* aparición de NPCs
* eventos dramáticos

y mejora muchísimo la historia.
Es bastante interesante.

## 11️⃣ Director AI Pattern

El **Director AI Pattern** es una evolución del sistema anterior.
En vez de que la IA solo **reaccione a lo que hace el jugador**, añades una capa que **dirige la narrativa** como si fuese un **director de cine o un máster de rol**.

Esto mejora muchísimo:

* coherencia de la historia
* tensión dramática
* aparición de eventos interesantes
* sensación de mundo vivo

Muchos prototipos narrativos avanzados lo usan porque los LLM **tienden a ser demasiado pasivos** si solo les das acciones del jugador.

---

### 1️⃣ El problema sin “director”

Arquitectura básica:

```
Jugador → IA narrador → escena
```

Problemas típicos:

* historia plana
* no hay tensión
* los NPC reaccionan pero no **actúan**
* la narrativa no progresa

El juego se vuelve una conversación larga.

---

### 2️⃣ La solución: un **Director de historia**

Añades una IA que **controla el ritmo narrativo**.

Arquitectura:

```
Jugador
   │
   ▼
Director AI
   │
   ▼
Narrador AI
   │
   ▼
Escena final
```

El **director decide qué debería pasar narrativamente**.

El **narrador escribe la escena**.

---

### 3️⃣ Qué decide el Director

El director **no escribe narrativa**.
Solo toma decisiones dramáticas.

Ejemplo de output del director:

```json
{
  "tension_level": 7,
  "scene_goal": "introducir sospecha sobre el tabernero",
  "event": "un desconocido entra en la taberna",
  "npc_focus": "Lysa",
  "twist_probability": 0.2
}
```

Esto es **muy barato en tokens**.

---

### 4️⃣ Prompt del Director

Ejemplo:

```text
Eres el director narrativo de un RPG.

Tu trabajo es mantener la historia interesante.

Reglas:
- alterna exploración, misterio y peligro
- aumenta la tensión gradualmente
- introduce eventos inesperados ocasionalmente

Estado del juego:
{game_state}

Última acción del jugador:
{player_action}

Devuelve un JSON con:
- tension_level (1-10)
- scene_goal
- event
- npc_focus
```

---

### 5️⃣ Prompt del Narrador

El narrador usa las decisiones del director.

```text
Eres el narrador de un RPG.

Estado del mundo:
{game_state}

Dirección narrativa:
{director_output}

Acción del jugador:
{player_action}

Describe la escena en 120 palabras máximo.
```

---

### 6️⃣ Ejemplo real

### Jugador

```
Pregunto al tabernero sobre el asesino.
```

### Director decide

```json
{
  "tension_level": 6,
  "scene_goal": "crear desconfianza",
  "event": "alguien escucha la conversación",
  "npc_focus": "Rurik"
}
```

### Narrador escribe

```
Rurik limpia lentamente una jarra mientras escuchas tu propia pregunta
resonar en la taberna.

Durante un instante parece dudar.

—No he visto a nadie así —dice finalmente.

Pero su mirada se desvía hacia la puerta.

En ese momento entra un hombre con capa oscura que se queda inmóvil,
como si estuviera escuchando.
```

Mucho más interesante que una respuesta directa.

---

### 7️⃣ Control de tensión narrativa

Un truco muy usado es mantener una variable:

```json
{
  "story_arc": "misterio",
  "tension": 4,
  "phase": "investigation"
}
```

La IA director controla la curva:

```
tensión baja → exploración
tensión media → sospecha
tensión alta → peligro
tensión máxima → clímax
```

Esto crea **estructura dramática automática**.

---

### 8️⃣ Eventos dirigidos

El director también puede **inyectar eventos**:

```json
{
  "event": "guardias entran en la taberna",
  "purpose": "presionar al jugador"
}
```

o

```json
{
  "event": "Lysa revela información parcial"
}
```

Esto hace que el mundo **no dependa solo del jugador**.

---

### 9️⃣ Arquitectura completa recomendada

Un sistema bastante potente sería:

```
Player
  │
  ▼
Director AI (4o-mini)
  │
  ▼
Narrator AI (4o / 4.1)
  │
  ▼
Scene
  │
  ▼
Memory extractor (4o-mini)
```

Cada modelo hace algo distinto:

| Componente | Modelo |
| ---------- | ------ |
| Director   | barato |
| Narrador   | bueno  |
| Memoria    | barato |

Esto reduce mucho el coste.

---

### 🔟 Otra mejora brutal (poco conocida)

Separar **lógica del mundo** de **narrativa**.

Añades un módulo intermedio:

```
Player
  │
  ▼
Game Logic AI
  │
  ▼
Director AI
  │
  ▼
Narrator AI
```

El **Game Logic** decide cosas como:

* si un NPC miente
* si un ataque acierta
* si el jugador encuentra pistas

Luego el narrador solo **lo cuenta**.

Esto evita incoherencias.

---

### 1️⃣1️⃣ Opinión personal

Para juegos con LLM, las tres ideas más potentes son:

1️⃣ **Game State estructurado**
2️⃣ **Director AI**
3️⃣ **Memoria separada de narrativa**

Con estas tres cosas puedes hacer un juego **mucho más profundo sin disparar costes**.

---

Si quieres, en el siguiente mensaje puedo enseñarte algo **todavía más potente para juegos narrativos**:

👉 **el patrón “NPC autonomous agents”**

donde cada NPC tiene:

* personalidad
* objetivos
* memoria propia

y los NPC **actúan solos incluso si el jugador no interactúa**.

Eso crea mundos sorprendentemente vivos. Es bastante espectacular cuando lo ves funcionando.

## NPC Autonomous Agents

El patrón **NPC Autonomous Agents** es probablemente lo más interesante que se está haciendo ahora en juegos con LLM.
La idea es muy simple conceptualmente:

> Los NPC **no son respuestas preprogramadas**, sino **agentes con objetivos propios que toman decisiones**.

En lugar de esto:

```text
Jugador → pregunta → NPC responde
```

tienes algo más parecido a esto:

```text
Jugador
   │
   ▼
Mundo simulado
   │
   ├─ NPC 1 (objetivos)
   ├─ NPC 2 (objetivos)
   └─ NPC 3 (objetivos)
```

Los NPC **deciden qué hacer incluso si el jugador no interactúa**.

---

### 1️⃣ El modelo mental: NPC = agente

Cada NPC tiene un pequeño “estado mental”.

Ejemplo:

```json
{
  "name": "Lysa",
  "role": "mercenaria",
  "personality": ["pragmática", "observadora"],
  "goal": "ganar dinero",
  "secret": "trabaja para el asesino",
  "attitude_to_player": 3,
  "current_plan": "observar al jugador"
}
```

Esto es **muy pequeño en tokens**.

---

### 2️⃣ El loop del mundo

En cada turno ocurre algo así:

```text
1 jugador actúa
2 los NPC deciden acciones
3 el mundo se actualiza
4 el narrador describe la escena
```

Arquitectura:

```text
Player action
     │
     ▼
NPC decision engine
     │
     ▼
World state update
     │
     ▼
Narrator AI
```

---

### 3️⃣ Decisión de los NPC

Cada NPC recibe el estado del mundo y decide.

Prompt típico:

```text
Eres un personaje de un RPG.

Nombre: Lysa
Personalidad: pragmática, observadora
Objetivo: ganar dinero
Actitud hacia el jugador: neutral

Situación actual:
El jugador está interrogando al tabernero sobre un asesino.

Decide tu acción.

Responde en JSON:
{
 "action": "",
 "intent": ""
}
```

Respuesta:

```json
{
  "action": "escuchar desde la mesa cercana",
  "intent": "averiguar cuánto sabe el jugador"
}
```

---

### 4️⃣ No todos los NPC actúan cada turno

Para que el coste no explote, se usa un **selector de NPC activos**.

Ejemplo:

```json
{
  "scene_npcs": ["Rurik", "Lysa"]
}
```

Solo esos se evalúan.

Esto reduce muchísimo llamadas a la API.

---

### 5️⃣ El narrador combina todo

Una vez que tienes:

* acción del jugador
* acciones de NPC

el narrador genera la escena.

Prompt:

```text
Acción del jugador:
{player_action}

Acciones de NPC:
{npc_actions}

Estado del mundo:
{game_state}

Describe la escena.
```

---

### 6️⃣ Ejemplo completo

Jugador:

```text
Pregunto al tabernero por el asesino.
```

NPC decisiones:

```json
[
  {
    "npc": "Rurik",
    "action": "evitar responder directamente",
    "intent": "proteger a un cliente"
  },
  {
    "npc": "Lysa",
    "action": "escuchar atentamente",
    "intent": "evaluar al jugador"
  }
]
```

Narrador:

```text
Rurik frunce el ceño al escuchar tu pregunta.

—No sé de qué hablas —dice, demasiado rápido.

Desde una mesa cercana, Lysa levanta ligeramente la mirada de su copa.
Parece escuchar cada palabra con atención.
```

La escena surge de **decisiones de personajes**, no solo del prompt.

---

### 7️⃣ Comportamientos emergentes (lo interesante)

Cuando cada NPC tiene:

* objetivos
* secretos
* relaciones

empiezan a aparecer comportamientos emergentes.

Ejemplo:

```text
NPC A quiere dinero
NPC B quiere matar al jugador
NPC C protege al jugador
```

El sistema puede generar situaciones inesperadas sin script.

---

### 8️⃣ Memoria individual de NPC

Cada NPC puede tener su propia memoria.

```json
{
  "memories": [
    "el jugador preguntó por el asesino",
    "Rurik parecía nervioso"
  ]
}
```

Esto hace que recuerden cosas.

---

### 9️⃣ Optimización muy importante

No todos los NPC usan IA siempre.

Muchos sistemas usan esto:

```text
NPC simple → reglas
NPC importante → LLM
```

Ejemplo:

```text
guardias → reglas
villanos → IA
aliados importantes → IA
```

Esto reduce el coste brutalmente.

---

### 🔟 Arquitectura completa (potente)

Algo así funciona muy bien:

```text
Player
  │
  ▼
Director AI
  │
  ▼
NPC decision engine
  │
  ▼
World state update
  │
  ▼
Narrator AI
  │
  ▼
Memory extractor
```

---

### 1️⃣1️⃣ Juegos y demos que usan ideas similares

Este tipo de arquitectura aparece en proyectos como:

* AI Dungeon
* Dwarf Fortress (aunque sin LLM)
* The Sims (conceptualmente parecido)

La diferencia es que con LLM **las acciones se narran dinámicamente**.

---

### 1️⃣2️⃣ El problema real de este patrón

El mayor riesgo es:

**explosión de llamadas a la API**.

Por eso se suelen aplicar tres reglas:

1️⃣ solo NPC presentes en la escena
2️⃣ solo NPC importantes usan LLM
3️⃣ decisiones muy cortas (JSON)

---

💡 **Opinión personal:**
Si combinas:

* estado del mundo estructurado
* director narrativo
* NPC autónomos

puedes construir algo **muy cercano a un “máster de rol automático”**.
Y sorprendentemente funciona bastante bien.

---

Si quieres, puedo enseñarte también algo que **casi nadie explica pero cambia completamente este tipo de juegos**:

👉 **el patrón “event simulation engine”**, que permite que **el mundo evolucione incluso si el jugador no hace nada** (ciudades cambian, NPC viajan, conspiraciones avanzan…).
Es lo que realmente hace que el mundo parezca vivo.

😄 Sí… este tema es una madriguera de conejo bastante profunda. Pero el siguiente patrón realmente **merece la pena**, porque es el que convierte un juego narrativo con IA en **un mundo que evoluciona por sí mismo**.

Ese patrón se suele llamar **Event Simulation Engine**.

La idea básica:

> El mundo **no espera al jugador**.
> Los eventos ocurren igualmente.

Esto cambia completamente la sensación del juego.

---

## Event Simulation Engine

### 1️⃣ El problema de la mayoría de juegos narrativos con IA

En muchos prototipos ocurre esto:

```text
jugador actúa → mundo reacciona
```

Si el jugador no hace nada… **no pasa nada**.

Resultado:

* el mundo parece artificial
* los NPC parecen actores esperando turno
* no hay urgencia

---

### 2️⃣ La idea del Event Simulation Engine

El mundo tiene **eventos que avanzan con el tiempo**.

Arquitectura:

```text
Player
  │
  ▼
World Simulation
  │
  ├─ NPC actions
  ├─ World events
  └─ Story arcs
  │
  ▼
Narrator AI
```

---

### 3️⃣ Tipos de eventos

Normalmente se usan tres tipos.

### Eventos globales

Afectan al mundo.

```json
{
  "event": "guerra entre reinos",
  "progress": 0.3
}
```

---

### Eventos locales

Afectan a una zona.

```json
{
  "event": "guardias buscan al asesino",
  "location": "taberna",
  "progress": 0.5
}
```

---

### Eventos de personaje

Afectan a NPC.

```json
{
  "npc": "Lysa",
  "event": "sigue al jugador",
  "progress": 0.7
}
```

---

### 4️⃣ Los eventos tienen progreso

Esto es muy importante.

Un evento no ocurre instantáneamente.

```json
{
  "event": "asesino encuentra al jugador",
  "progress": 0.0
}
```

Cada turno:

```json
progress += 0.1
```

Cuando llega a **1.0 → ocurre**.

---

### 5️⃣ Ejemplo

Evento inicial:

```json
{
  "event": "asesino busca al jugador",
  "progress": 0.4
}
```

Turnos después:

```json
{
  "event": "asesino encuentra al jugador",
  "progress": 1.0
}
```

Ahora el narrador recibe:

```json
{
  "event_triggered": "asesino entra en la taberna"
}
```

El jugador **no lo provocó**, pero ocurre.

---

### 6️⃣ El director puede crear eventos

Aquí se conecta con el **Director AI**.

El director puede generar nuevos eventos:

```json
{
  "new_event": {
    "type": "npc_plan",
    "npc": "Lysa",
    "goal": "robar el mapa del jugador",
    "progress": 0
  }
}
```

Esto crea **subtramas dinámicas**.

---

### 7️⃣ Motor simple de simulación

Un ejemplo muy simple sería algo así:

```python
for event in world_events:
    event["progress"] += event["speed"]

    if event["progress"] >= 1:
        trigger_event(event)
```

Esto **no necesita IA**.

La IA solo decide **qué eventos crear**.

---

### 8️⃣ Cómo se conecta con los NPC autónomos

Los NPC pueden crear eventos.

Ejemplo:

NPC decide:

```json
{
  "action": "seguir al jugador"
}
```

El motor crea:

```json
{
  "event": "Lysa sigue al jugador",
  "progress": 0.2
}
```

Después de varios turnos:

```json
{
  "event_triggered": "Lysa descubre el escondite del jugador"
}
```

---

### 9️⃣ Mundos persistentes

Si guardas los eventos puedes hacer cosas muy interesantes.

Ejemplo:

Jugador abandona la ciudad.

Mientras tanto:

```json
{
  "event": "rebelión en la ciudad",
  "progress": 0.6
}
```

Cuando vuelve:

```text
La ciudad está en caos.
```

Esto crea **sensación de mundo vivo**.

---

### 🔟 Un truco brutal de diseño

Usar **relojes narrativos**.

Es un concepto de juegos de rol.

Ejemplo:

```json
{
  "clock": "asesino encuentra al jugador",
  "segments": 6,
  "filled": 3
}
```

Cada evento llena un segmento.

Cuando se llena → ocurre el evento.

Esto funciona muy bien con IA.

---

### 1️⃣1️⃣ Arquitectura completa (muy potente)

Si juntas todos los patrones que hemos visto:

```text
Player
  │
  ▼
World Simulation Engine
  │
  ├─ Event System
  ├─ NPC Autonomous Agents
  └─ World State
  │
  ▼
Director AI
  │
  ▼
Narrator AI
  │
  ▼
Memory Extractor
```

Esto ya es **casi un motor narrativo completo**.

---

### 1️⃣2️⃣ Opinión personal

La combinación que más me gusta (y que varios prototipos usan):

1️⃣ **World state estructurado**
2️⃣ **NPC agentes autónomos**
3️⃣ **Event simulation engine**
4️⃣ **Director narrativo**
5️⃣ **Narrador LLM**

Con eso puedes crear algo muy parecido a:

> un **máster de rol automático que improvisa historias**.

---

💡 Te dejo una curiosidad final.

Hay un patrón aún más avanzado que empieza a aparecer en juegos experimentales:

**“Narrative Planning AI”**

donde la IA **planifica la historia a largo plazo** como si escribiera una novela (actos, clímax, giros).

Es el paso siguiente al Director AI.

Si quieres, te lo explico también… aunque aviso: **ese ya es nivel arquitectura de juego serio** 😅.

## Narrative Planning AI

😄 Vale, vamos a cerrar el círculo con el patrón más “alto nivel” de todos: **Narrative Planning AI**.
Aquí la idea es que el sistema **no solo reaccione o dirija escenas**, sino que **planifique la historia a largo plazo**, como haría un escritor.

> El sistema sabe hacia dónde va la historia, aunque el jugador tenga libertad.

Esto resuelve uno de los mayores problemas de los juegos narrativos con IA:

* muchas escenas interesantes
* pero **sin arco narrativo claro**

---

### 1️⃣ El problema sin planificación narrativa

Si usas solo:

* NPC autónomos
* eventos del mundo
* director narrativo

obtienes historias **emergentes**, pero a menudo:

* no hay clímax
* no hay resolución
* todo se alarga indefinidamente

Es divertido… pero no parece una historia.

---

### 2️⃣ La idea del Narrative Planner

Añades un **planificador de historia** que define:

* estructura narrativa
* hitos importantes
* posibles giros

Arquitectura:

```text id="6eq78p"
Narrative Planner
        │
        ▼
Director AI
        │
        ▼
World Simulation
        │
        ▼
Narrator AI
```

El planner **no genera escenas**.
Define **hacia dónde debería ir la historia**.

---

### 3️⃣ Ejemplo de plan narrativo

El planner puede generar algo así:

```json id="yqewoa"
{
  "story_arc": "misterio y conspiración",
  "acts": [
    {
      "act": 1,
      "goal": "descubrir que hay un asesino",
      "twist": "el asesino trabaja para una facción"
    },
    {
      "act": 2,
      "goal": "investigar la conspiración",
      "twist": "un aliado traiciona al jugador"
    },
    {
      "act": 3,
      "goal": "enfrentar al líder de la conspiración"
    }
  ]
}
```

Esto es **muy barato en tokens** porque se genera una vez.

---

### 4️⃣ El planner define “story beats”

Los **story beats** son eventos clave.

Ejemplo:

```json id="1czv0i"
{
  "story_beats": [
    "jugador descubre el mapa",
    "NPC aliado traiciona",
    "asesino revela su identidad",
    "confrontación final"
  ]
}
```

El director intenta **hacer que el mundo evolucione hacia esos beats**.

---

### 5️⃣ Cómo se usa durante el juego

Cada turno el director recibe:

```json id="39gg7p"
{
  "story_arc": "act_1",
  "pending_beats": [
    "jugador descubre el mapa"
  ]
}
```

Entonces intenta crear situaciones que acerquen ese evento.

Ejemplo:

```json id="oqyr0c"
{
  "event": "Rurik menciona un mapa antiguo"
}
```

---

### 6️⃣ El truco importante: planificación flexible

El planner **no obliga al jugador**.

Si el jugador cambia la historia:

```text id="k7t92b"
jugador mata al asesino antes de tiempo
```

El planner se **recalcula**.

Prompt típico:

```text id="ksg82e"
El plan narrativo actual es este:
{story_plan}

El mundo ha cambiado así:
{world_state}

Actualiza el plan narrativo.
```

Esto mantiene coherencia.

---

### 7️⃣ Estructura narrativa clásica

Muchos planners usan la estructura clásica:

```text id="e0u7fc"
Acto 1 → introducción
Acto 2 → complicación
Acto 3 → clímax
```

O incluso la **estructura de 5 actos**.

---

### 8️⃣ Control de ritmo narrativo

El planner también controla ritmo.

Ejemplo:

```json id="r9qxtf"
{
  "pacing": {
    "exploration": 0.4,
    "dialogue": 0.3,
    "danger": 0.3
  }
}
```

Si hay demasiada acción:

→ introduce exploración o diálogo.

---

### 9️⃣ Planificación de subtramas

El planner también puede crear subtramas.

```json id="u4x7mq"
{
  "side_plot": {
    "npc": "Lysa",
    "arc": "conflicto de lealtad"
  }
}
```

Esto se integra con los **NPC autónomos**.

---

### 🔟 Arquitectura completa final

Si juntas todo lo que hemos visto:

```text id="z1ltyr"
Narrative Planner
        │
        ▼
Director AI
        │
        ▼
World Simulation Engine
        │
        ├─ NPC Autonomous Agents
        ├─ Event System
        └─ World State
        │
        ▼
Narrator AI
        │
        ▼
Memory Extractor
```

Esto ya es básicamente un **motor narrativo generativo completo**.

---

### 1️⃣1️⃣ Algo muy importante (que casi nadie menciona)

Los sistemas reales suelen tener **tres escalas de tiempo**.

### largo plazo

Narrative planner.

```text id="tv49y6"
actos
arcos narrativos
```

---

### medio plazo

Director.

```text id="hjwdid"
escenas
tensión
eventos
```

---

### corto plazo

NPC y narrador.

```text id="lsqgcm"
acciones
diálogo
descripción
```

Esta separación **es clave para que el sistema no se vuelva caótico**.

---

### 1️⃣2️⃣ Opinión sincera

La arquitectura que más sentido tiene ahora mismo para juegos con LLM sería algo así:

```text id="ajpmxy"
State Engine
NPC Agents
Event Simulation
Narrative Director
Narrative Planner
Narrator
```

Con eso puedes crear algo muy parecido a:

> un **RPG narrativo infinito dirigido por IA**.

---

💡 Y cierro con una idea curiosa.

Hay un patrón que **muy pocos prototipos usan todavía**, pero que probablemente será el siguiente salto:

**“player modeling AI”**

La IA intenta **entender el tipo de jugador**:

* explorador
* combatiente
* narrativo
* caótico

y **adapta la historia a su estilo**.

Eso hace que cada jugador tenga una historia completamente distinta.

Si te interesa, también puedo explicarte **cómo se implementa ese modelo de jugador**, que en realidad es bastante elegante.
