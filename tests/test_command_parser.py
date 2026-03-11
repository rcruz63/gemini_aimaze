"""
Pruebas del parser de comandos.
"""

from engine.command_parser import CommandParser


def test_parse_basic_commands():
    parser = CommandParser()
    
    assert parser.parse("ir norte") == {"action": "ir", "target": "norte"}
    assert parser.parse("COGER llave") == {"action": "coger", "target": "llave"}
    assert parser.parse("mirar") == {"action": "mirar", "target": ""}
    assert parser.parse("") is None

def test_parse_synonyms():
    parser = CommandParser()
    
    assert parser.parse("moverse sur") == {"action": "ir", "target": "sur"}
    assert parser.parse("tomar espada") == {"action": "coger", "target": "espada"}
    assert parser.parse("examinar pared") == {"action": "mirar", "target": "pared"}
