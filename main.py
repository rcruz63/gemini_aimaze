"""
Punto de entrada principal para el juego.
"""

from gameplay.game_loop import GameLoop


def main():
    game = GameLoop()
    game.run()


if __name__ == "__main__":
    main()
