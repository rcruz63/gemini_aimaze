"""
Bucle principal determinista del juego (MVP).
"""

import os
from engine.map_engine import MapEngine
from engine.command_parser import CommandParser
from engine.event_engine import EventEngine, Event
from engine.puzzle_engine import PuzzleEngine, KeyAndLockPuzzle
from ai.narrator_ai import NarratorMock
from models.state import SessionState, SceneState
from models.room import Room


class GameLoop:
    """Clase principal que coordina los subsistemas del juego."""

    def __init__(self) -> None:
        self.map_engine = MapEngine()
        self.parser = CommandParser()
        self.event_engine = EventEngine()
        self.puzzle_engine = PuzzleEngine()
        self.narrator = NarratorMock()
        self.session_state = SessionState(location="")
        self._setup_world()

    def _setup_world(self) -> None:
        """Inicializa un mundo de prueba con puzzles y eventos."""
        room_a = Room(room_id="sala_A", description="Estás en la Sala A. Es oscura y fría. Hay una puerta al norte que parece cerrada.")
        room_b = Room(room_id="sala_B", description="Estás en la Sala B. Un antiguo reactor zumba en el centro.")
        
        self.map_engine.add_room(room_a)
        self.map_engine.add_room(room_b)
        
        # El mapa inicialmente no tiene la conexión norte, se desbloquea con la llave
        self.session_state.location = "sala_A"
        self.session_state.inventory.append("llave_oxidada") # Damos la llave para testear
        
        puzzle = KeyAndLockPuzzle("sala_A", "norte", "sala_B", "llave_oxidada")
        self.puzzle_engine.add_puzzle(puzzle)
        
        evento = Event(name="falla_reactor", description="El reactor de la sala B empieza a emitir un sonido preocupante...", speed=0.5)
        self.event_engine.add_event(evento)

    def _clear_console(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self) -> None:
        """Ejecuta el bucle principal interactivo."""
        self._clear_console()
        print("\033[92mIniciando ndd_aimaze (MVP) - Escribe 'salir' para terminar.\n\033[0m")
        
        while True:
            # 1. Evaluar puzzles
            self.puzzle_engine.evaluate_puzzles(self.session_state, self.map_engine)
            
            # 2. Construir estado de la escena
            current_room = self.map_engine.rooms[self.session_state.location]
            scene = SceneState(
                location_description=current_room.description,
                available_actions=[f"ir {d}" for d in current_room.exits.keys()]
            )
            
            # 3. Avanzar eventos e inyectar en la escena si corresponde
            self.event_engine.tick(scene)
            
            # 4. Generar narrativa con el NarradorMock
            narrative = self.narrator.generate_scene(scene)
            
            # Imprimir en consola verde (estilo retro)
            print(f"\033[92m--- {current_room.room_id.upper()} ---\033[0m")
            print(f"\033[92m{narrative}\033[0m")
            
            try:
                user_input = input("\n\033[92m> \033[0m")
            except EOFError:
                break
                
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("\033[92mSaliendo del juego...\033[0m")
                break
                
            self._clear_console()
                
            parsed = self.parser.parse(user_input)
            if not parsed:
                print("\033[92mComando vacío o no reconocido.\033[0m\n")
                continue
                
            self._handle_action(parsed)

    def _handle_action(self, parsed: dict) -> None:
        """Aplica la acción parseada al estado."""
        action = parsed.get("action")
        target = parsed.get("target")
        
        if action == "ir":
            current_room = self.map_engine.rooms[self.session_state.location]
            if target in current_room.exits:
                self.session_state.location = current_room.exits[target]
                print(f"\033[92m[Acción: Te mueves hacia el {target}.]\033[0m\n")
            else:
                print(f"\033[92m[Acción: No puedes ir hacia el {target} desde aquí.]\033[0m\n")
        elif action == "mirar":
            print("\033[92m[Acción: Observas tu entorno con detenimiento.]\033[0m\n")
        elif action == "coger":
            print(f"\033[92m[Acción: Recoges {target}.]\033[0m\n")
        else:
            print(f"\033[92m[Acción '{action}' no implementada en este MVP.]\033[0m\n")
