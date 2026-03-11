# Idea 6: Event Simulation Engine (El Mundo Vivo)

**El Prompt (La Idea para la herramienta):**

> "Implementa el `EventEngine` en `engine/`. Debe manejar una lista de eventos con un progreso (`progress` de 0.0 a 1.0) y una velocidad (`speed`). Cada vez que se llama a `event_engine.tick()`, el progreso aumenta. Si llega a 1.0, el evento se marca como 'triggered' y se añade al `SceneState`. Escribe un test donde un evento 'bajada_oxigeno' avanza durante 3 turnos simulados (esperar, esperar, esperar) hasta que se dispara. CHANGELOG obligatorio."

* **Qué debe hacer su plan:** Crear la lógica de simulación de tiempo donde el mundo evoluciona aunque el jugador no haga nada.
* **Qué observar al finalizar:**
* Los tests demuestran que el mundo tiene un reloj interno independiente de las acciones resolutivas del jugador.

