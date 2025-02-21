"""Main entry point for the Hand Gesture Game."""

import sys

from .core.game import RockPaperScissors
from .exceptions.game_exceptions import HandGestureGameError


def main() -> None:
    """
    Main entry point for the game.

    This function initializes and runs the Rock Paper Scissors game.
    It handles any game-related exceptions and ensures proper cleanup.
    """
    try:
        game = RockPaperScissors()
        game.run()
    except HandGestureGameError as e:
        print(f"Game error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
