"""
Main game loop with AI orchestration (Phase 2).
"""

import os
from typing import Dict, Optional

from ai.director_ai import DirectorAI
from ai.llm_client import LLMClient
from ai.memory_extractor import MemoryExtractor
from ai.narrator_ai import NarratorAI
from ai.npc_ai import NPCDecisionAI
from engine.command_parser import CommandParser
from engine.event_engine import EventEngine, Event
from engine.map_engine import MapEngine
from engine.puzzle_engine import PuzzleEngine, KeyAndLockPuzzle
from models.room import Room
from models.state import NPCState, SceneState, SessionState


class GameLoop:
    """Main class coordinating game subsystems and AI agents."""

    def __init__(self, llm_client: Optional[LLMClient] = None) -> None:
        self.llm_client = llm_client or LLMClient()
        self.map_engine = MapEngine()
        self.parser = CommandParser(self.llm_client)
        self.event_engine = EventEngine()
        self.puzzle_engine = PuzzleEngine()
        self.director = DirectorAI(self.llm_client)
        self.narrator = NarratorAI(self.llm_client)
        self.memory_extractor = MemoryExtractor(self.llm_client)
        self.npc_ai = NPCDecisionAI(self.llm_client)

        self.session_state = SessionState(location="")
        self.last_action_result = "Welcome to ndd_aimaze."
        self._setup_world()

    def _setup_world(self) -> None:
        """Initializes a test world with puzzles and events."""
        room_a = Room(
            room_id="sala_A",
            description="Estás en la Sala A. Es oscura y fría. Hay una puerta al norte que parece cerrada.",
        )
        room_b = Room(
            room_id="sala_B",
            description="Estás en la Sala B. Un antiguo reactor zumba en el centro.",
        )

        self.map_engine.add_room(room_a)
        self.map_engine.add_room(room_b)

        self.session_state.location = "sala_A"
        self.session_state.inventory.append("llave_oxidada")

        # Initialize NPCs
        self.session_state.npcs["lysa"] = NPCState(
            name="Lysa",
            personality=["mercenaria", "pragmática", "observadora"],
            goal="ganar dinero",
            secret="trabaja para el asesino",
            attitude_to_player=3,
            current_plan="observar al jugador",
        )
        self.session_state.npcs["rurik"] = NPCState(
            name="Rurik",
            personality=["tabernero", "sospechoso", "nervioso"],
            goal="proteger a un cliente",
            attitude_to_player=2,
            current_plan="evitar responder directamente",
        )
        self.session_state.npcs_conocidos.extend(["lysa", "rurik"])

        puzzle = KeyAndLockPuzzle("sala_A", "norte", "sala_B", "llave_oxidada")
        self.puzzle_engine.add_puzzle(puzzle)

        # Event for testing "esperar"
        evento_oxigeno = Event(
            name="oxigeno_disminuyendo",
            description="El soporte vital de la Sala A falla, el oxígeno se agota por completo.",
            progress=0.8,
            speed=0.2,
        )
        self.event_engine.add_event(evento_oxigeno)

    def _clear_console(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def run(self) -> None:
        """Runs the interactive main loop."""
        self._clear_console()
        print(
            "\033[92mIniciando ndd_aimaze (Fase 2) - Escribe 'salir' para terminar.\n\033[0m"
        )

        while True:
            # 1. Engine Update (Puzzles)
            self.puzzle_engine.evaluate_puzzles(self.session_state, self.map_engine)

            # 2. Build Scene State
            current_room = self.map_engine.rooms[self.session_state.location]

            # For testing Phase 3, we put Lysa in sala_A
            active_npcs_in_room = []
            if self.session_state.location == "sala_A":
                active_npcs_in_room = ["lysa"]

            scene = SceneState(
                location_description=current_room.description,
                active_npcs=active_npcs_in_room,
                available_actions=[f"ir {d}" for d in current_room.exits.keys()]
                + ["mirar", "coger"],
            )

            # 3. Event Tick
            self.event_engine.tick(scene)

            # 3.5 NPC Decision Engine (Only for NPCs in the same room)
            for npc_id in scene.active_npcs:
                if npc_id in self.session_state.npcs:
                    npc_state = self.session_state.npcs[npc_id]
                    action = self.npc_ai.generate_action(
                        npc_state, scene, self.last_action_result
                    )
                    scene.npc_actions[npc_id] = (
                        f"{action.action} (Intención: {action.intent})"
                    )

            # 4. Director AI (Set tone and goals)
            scene.director_directives = self.director.generate_directives(
                self.session_state, scene
            )

            # 5. Narrator AI (Generate immersive text)
            narrative = self.narrator.generate_scene(scene, self.last_action_result)

            # 6. Memory Extractor (Update session memory based on narration)
            updates = self.memory_extractor.extract_updates(
                narrative, self.session_state
            )
            self.session_state.memory.update(updates)

            # Display output
            if (
                self.last_action_result
                and self.last_action_result != "Welcome to ndd_aimaze."
            ):
                print(f"\033[93m{self.last_action_result}\033[0m\n")

            print(f"\033[92m--- {current_room.room_id.upper()} ---\033[0m")
            print(f"\033[92m{narrative}\033[0m")

            # 7. Input Handling with Semantic Parser
            try:
                user_input = input("\n\033[92m> \033[0m")
            except EOFError:
                break

            if user_input.lower() in ["salir", "exit", "quit"]:
                print("\033[92mSaliendo del juego...\033[0m")
                break

            self._clear_console()

            # Semantic Parsing with Retry
            parsed = self.parser.parse(user_input, scene.available_actions)

            if parsed.get("action") == "unknown":
                # Retry 1: Ask again more clearly
                print(
                    "\033[92m[IA: No te he entendido bien. ¿Puedes ser más específico?]\033[0m"
                )
                user_input = input("\033[92m> \033[0m")
                parsed = self.parser.parse(user_input, scene.available_actions)

                if parsed.get("action") == "unknown":
                    # Retry 2: Show menu fallback
                    print(
                        "\033[92m[IA: Lo siento, sigo sin entenderte. Elige una de estas opciones:]\033[0m"
                    )
                    for i, action in enumerate(scene.available_actions, 1):
                        print(f"\033[92m{i}. {action}\033[0m")

                    choice = input("\033[92mSelección (número o texto): \033[0m")
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(scene.available_actions):
                            action_parts = scene.available_actions[idx].split()
                            parsed = {
                                "action": action_parts[0],
                                "target": (
                                    action_parts[1] if len(action_parts) > 1 else ""
                                ),
                            }
                        else:
                            parsed = {"action": "unknown"}
                    except ValueError:
                        parsed = self.parser.parse(choice, scene.available_actions)

            if parsed.get("action") == "unknown":
                self.last_action_result = "No has hecho nada útil."
                continue

            # 8. Apply action and update last_action_result
            self.last_action_result = self._handle_action(parsed)

    def _handle_action(self, parsed: Dict[str, str]) -> str:
        """Applies the parsed action to the state and returns the result string."""
        action = parsed.get("action")
        target = parsed.get("target", "")

        if action == "ir":
            current_room = self.map_engine.rooms[self.session_state.location]
            if target in current_room.exits:
                self.session_state.location = current_room.exits[target]
                return f"Te has movido al {target}."
            else:
                return f"No puedes ir al {target} desde aquí."
        elif action == "mirar":
            return "Observas tu entorno con detenimiento."
        elif action == "coger":
            return f"Intentas recoger {target}."
        elif action == "esperar":
            return "Decides esperar un momento y observar qué sucede."
        else:
            return f"Realizas la acción: {action} {target}."
