"""Custom exceptions for the Hand Gesture Game."""


class HandGestureGameError(Exception):
    """Base exception class for Hand Gesture Game."""

    pass


class CameraError(HandGestureGameError):
    """Raised when there are issues with camera initialization or access."""

    pass


class GestureDetectionError(HandGestureGameError):
    """Raised when gesture detection fails."""

    pass


class ResourceInitializationError(HandGestureGameError):
    """Raised when required resources cannot be initialized."""

    pass
