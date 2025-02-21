"""Main entry point for the Hand Gesture Game."""

import logging
import sys
from pathlib import Path

from hand_gesture_game import HandGestureGameError, RockPaperScissors
from hand_gesture_game.utils.logging_config import setup_logging


def main() -> None:
    """
    Main entry point for the game.

    This function initializes and runs the Rock Paper Scissors game.
    It handles any game-related exceptions and ensures proper cleanup.
    """
    # Set up logging
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "game.log"
    setup_logging(str(log_file), level=logging.INFO)

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
