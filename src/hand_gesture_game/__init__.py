"""Hand Gesture Game package."""

from .core.game import RockPaperScissors
from .core.gesture_detector import Gesture, GestureDetector
from .exceptions.game_exceptions import (
    CameraError,
    GestureDetectionError,
    HandGestureGameError,
    ResourceInitializationError,
)

__version__ = "1.0.0"
__author__ = "An Nguyen"

__all__ = [
    "RockPaperScissors",
    "Gesture",
    "GestureDetector",
    "HandGestureGameError",
    "CameraError",
    "GestureDetectionError",
    "ResourceInitializationError",
]
