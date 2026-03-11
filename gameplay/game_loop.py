"""
Bucle principal determinista del juego (MVP).
"""

from engine.map_engine import MapEngine
from engine.command_parser import CommandParser
from models.state import SessionState, SceneState
from models.room import Room


class GameLoop:
    """Clase principal que coordina los subsistemas del juego."""

    def __init__(self) -> None:
        self.map_engine = MapEngine()
        self.parser = CommandParser()
        self.session_state = SessionState(location="")
        self._setup_world()

    def _setup_world(self) -> None:
        """Inicializa un mundo de prueba diminuto."""
        room_a = Room(room_id="sala_A", description="Estás en la Sala A. Hay una puerta al norte.")
        room_b = Room(room_id="sala_B", description="Estás en la Sala B. Hay una puerta al sur.")
        
        self.map_engine.add_room(room_a)
        self.map_engine.add_room(room_b)
        self.map_engine.connect("sala_A", "sala_B", "norte")
        
        self.session_state.location = "sala_A"

    def run(self) -> None:
        """Ejecuta el bucle principal interactivo."""
        print("Iniciando ndd_aimaze (MVP) - Escribe 'salir' para terminar.\n")
        
        while True:
            current_room = self.map_engine.rooms[self.session_state.location]
            
            # Generar el SceneState básico
            scene = SceneState(
                location_description=current_room.description,
                available_actions=[f"ir {d}" for d in current_room.exits.keys()]
            )
            
            # Imprimir determinísticamente
            print(f"\n--- {current_room.room_id.upper()} ---")
            print(scene.model_dump_json(indent=2))
            
            try:
                user_input = input("\n¿Qué quieres hacer? > ")
            except EOFError:
                break
                
            if user_input.lower() in ["salir", "exit", "quit"]:
                print("Saliendo del juego...")
                break
                
            parsed = self.parser.parse(user_input)
            if not parsed:
                print("Comando vacío o no reconocido.")
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
                print(f"Te mueves hacia el {target}.")
            else:
                print(f"No puedes ir hacia el {target} desde aquí.")
        else:
            print(f"Acción '{action}' no implementada en este MVP.")
