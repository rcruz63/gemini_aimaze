# Arquitectura para un Remake de Zork con IA

## 1. Introducción

Los juegos clásicos de ficción interactiva, como Zork, se basaban en:

* Exploración de localizaciones
* Interacción mediante comandos de texto
* Resolución de puzzles
* Descubrimiento progresivo del mundo

Un remake moderno apoyado en IA puede mantener ese espíritu, pero añadir:

* Mundos generados dinámicamente
* Historias emergentes
* NPC autónomos
* Eventos inesperados
* Ambientaciones diferentes en cada partida

Para que el sistema sea coherente, escalable y económicamente viable, es importante separar **lógica del juego** y **narrativa generada por IA**.

---

# 2. Principios de diseño

## 2.1 Separación entre lógica y narrativa

La IA **no debe controlar directamente la lógica del juego**.

Debe encargarse de:

* narrativa
* ambientación
* decisiones de alto nivel
* comportamiento de personajes

Mientras que el motor del juego debe controlar:

* mapa
* reglas
* puzzles
* estado del mundo

---

## 2.2 Estado estructurado del mundo

El mundo se representa mediante un estado estructurado.

Ejemplo:

```json
{
  "location": "engine_room",
  "inventory": ["lantern"],
  "known_npcs": ["android"],
  "active_events": ["oxygen_low"]
}
```

Esto evita enviar toda la historia al modelo en cada turno y reduce mucho el coste.

---

# 3. Generación del mundo (World Generation)

Al comenzar una partida se genera un **World Blueprint**.

Ejemplo:

```json
{
  "setting": "nave espacial abandonada",
  "theme": "terror tecnológico",
  "goal": "reactivar el sistema de navegación",
  "main_threat": "IA corrupta",
  "puzzle_style": "tecnológico"
}
```

Otros posibles escenarios:

* mazmorra medieval
* templo azteca
* estación polar
* ciudad submarina
* base lunar

Cada partida comienza con una ambientación distinta.

---

# 4. Generación del mapa

El mapa se genera como un **grafo de habitaciones**.

Ejemplo:

```json
{
  "rooms": [
    {
      "id": "engine_room",
      "exits": ["corridor"]
    },
    {
      "id": "corridor",
      "exits": ["engine_room", "bridge"]
    }
  ]
}
```

Esto garantiza coherencia espacial.

---

# 5. Sistema de puzzles (Procedural Puzzle Generator)

Los puzzles se generan mediante **plantillas estructuradas**.

Ejemplo:

```json
{
  "puzzle_type": "repair",
  "blocked_path": "bridge",
  "items_needed": ["fuse", "toolkit"]
}
```

La IA decide el concepto del puzzle y el motor del juego implementa la lógica.

Tipos de puzzles habituales:

* llave y cerradura
* reparación de máquinas
* secuencias de activación
* combinaciones
* deducción lógica
* transporte de objetos

La narrativa cambia según la ambientación, pero la mecánica permanece.

---

# 6. NPC Autonomous Agents

Cada NPC se modela como un agente con objetivos propios.

Ejemplo:

```json
{
  "name": "Lysa",
  "role": "mercenaria",
  "goal": "ganar dinero",
  "attitude_to_player": 1,
  "current_plan": "observar al jugador"
}
```

Los NPC pueden:

* moverse
* investigar
* mentir
* ayudar
* sabotear

Esto genera comportamientos emergentes.

---

# 7. Event Simulation Engine

El mundo contiene eventos que evolucionan con el tiempo.

Ejemplo:

```json
{
  "event": "oxígeno disminuyendo",
  "progress": 0.4
}
```

Cada turno el progreso aumenta.

Cuando llega a 1.0 el evento ocurre.

Esto permite que el mundo evolucione incluso si el jugador no actúa.

Tipos de eventos:

* globales (guerras, catástrofes)
* locales (problemas en una zona)
* personales (planes de NPC)

---

# 8. Director AI

El Director AI controla el ritmo narrativo.

Funciones principales:

* introducir tensión
* activar eventos
* destacar NPC
* crear pistas

Ejemplo de salida:

```json
{
  "scene_goal": "aumentar tensión",
  "event": "ruido en el pasillo",
  "npc_focus": "androide"
}
```

El director decide **qué debería pasar narrativamente**, pero no escribe la escena.

---

# 9. Narrative Planner

El Narrative Planner planifica la historia a largo plazo.

Ejemplo:

```json
{
  "acts": [
    {
      "goal": "descubrir amenaza"
    },
    {
      "goal": "investigar conspiración"
    },
    {
      "goal": "confrontación final"
    }
  ]
}
```

Define:

* arcos narrativos
* giros argumentales
* momentos clave

Si el jugador cambia mucho la historia, el plan se recalcula.

---

# 10. Narrador IA

El narrador convierte el estado del mundo en texto.

Entrada:

* ubicación
* eventos activos
* acciones del jugador
* acciones de NPC

Salida:

Descripción narrativa breve y evocadora.

Ejemplo:

```
La consola chisporrotea débilmente.

Entre los cables quemados encuentras un fusible
que parece haber explotado hace tiempo.

En el pasillo cercano algo metálico golpea el suelo.
```

---

# 11. Memoria del juego

El sistema mantiene una memoria estructurada:

### world_state

Información permanente del mundo.

### session_state

Progreso de la partida.

### scene_state

Estado de la escena actual.

Esto reduce el número de tokens enviados al modelo.

---

# 12. Flujo de un turno

El ciclo de juego típico sería:

1. jugador introduce acción
2. NPC toman decisiones
3. eventos del mundo avanzan
4. director ajusta la narrativa
5. narrador genera la escena
6. memoria se actualiza

---

# 13. Arquitectura completa

```
World Generator
        │
        ▼
Map Generator
        │
        ▼
Puzzle Generator
        │
        ▼
Event Simulation Engine
        │
        ├─ NPC Autonomous Agents
        └─ World State
        │
        ▼
Narrative Planner
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

---

# 14. Ventajas del enfoque

Este sistema permite:

* aventuras diferentes en cada partida
* mundos coherentes
* NPC con comportamiento creíble
* puzzles funcionales
* narrativa emergente
* control de costes de IA

El resultado sería un **motor de ficción interactiva generativa**, capaz de crear aventuras prácticamente infinitas manteniendo la jugabilidad clásica.
