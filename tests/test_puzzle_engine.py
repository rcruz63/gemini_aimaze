"""
Pruebas del motor de puzzles.
"""

from engine.map_engine import MapEngine
from engine.puzzle_engine import PuzzleEngine, KeyAndLockPuzzle
from models.state import SessionState
from models.room import Room


def test_key_and_lock_puzzle():
    # Setup del mundo
    map_engine = MapEngine()
    room_a = Room(room_id="sala_A")
    room_b = Room(room_id="sala_B")
    map_engine.add_room(room_a)
    map_engine.add_room(room_b)
    
    # Setup del estado
    session_state = SessionState(location="sala_A")
    
    # Setup del puzzle
    puzzle_engine = PuzzleEngine()
    puzzle = KeyAndLockPuzzle(
        room_id="sala_A",
        direction="norte",
        target_room_id="sala_B",
        required_item="llave_oxidada"
    )
    puzzle_engine.add_puzzle(puzzle)
    
    # 1. Intento sin llave (falla)
    puzzle_engine.evaluate_puzzles(session_state, map_engine)
    assert "norte" not in map_engine.rooms["sala_A"].exits
    assert not puzzle.solved
    
    # 2. Intento con llave (pasa)
    session_state.inventory.append("llave_oxidada")
    puzzle_engine.evaluate_puzzles(session_state, map_engine)
    assert "norte" in map_engine.rooms["sala_A"].exits
    assert map_engine.rooms["sala_A"].exits["norte"] == "sala_B"
    assert puzzle.solved
