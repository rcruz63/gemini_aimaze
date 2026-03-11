"""
Motor de puzzles basado en plantillas deterministas.
"""

from abc import ABC, abstractmethod
from typing import List
from models.state import SessionState
from engine.map_engine import MapEngine


class PuzzleTemplate(ABC):
    """Clase base para todos los puzzles."""
    
    @abstractmethod
    def attempt_solve(self, session_state: SessionState, map_engine: MapEngine) -> bool:
        """Intenta resolver el puzzle. Devuelve True si se resuelve o ya estaba resuelto."""
        pass


class KeyAndLockPuzzle(PuzzleTemplate):
    """
    Puzzle de Llave y Cerradura.
    Desbloquea una salida específica en una habitación si el jugador tiene la llave.
    """
    
    def __init__(self, room_id: str, direction: str, target_room_id: str, required_item: str) -> None:
        self.room_id = room_id
        self.direction = direction
        self.target_room_id = target_room_id
        self.required_item = required_item
        self.solved = False

    def attempt_solve(self, session_state: SessionState, map_engine: MapEngine) -> bool:
        if self.solved:
            return True
            
        if session_state.location != self.room_id:
            return False
            
        if self.required_item in session_state.inventory:
            # Desbloqueamos conectando la habitación en el mapa
            map_engine.connect(self.room_id, self.target_room_id, self.direction)
            self.solved = True
            return True
            
        return False


class PuzzleEngine:
    """Gestiona los puzzles activos en el mundo."""
    
    def __init__(self) -> None:
        self.puzzles: List[PuzzleTemplate] = []
        
    def add_puzzle(self, puzzle: PuzzleTemplate) -> None:
        self.puzzles.append(puzzle)
        
    def evaluate_puzzles(self, session_state: SessionState, map_engine: MapEngine) -> None:
        """Evalúa todos los puzzles no resueltos para ver si el estado actual los resuelve."""
        for puzzle in self.puzzles:
            if not getattr(puzzle, 'solved', True):
                puzzle.attempt_solve(session_state, map_engine)
