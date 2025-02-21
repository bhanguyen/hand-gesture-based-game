"""Module for detecting and classifying hand gestures using MediaPipe."""

from enum import Enum
from typing import List, Optional, Tuple

import mediapipe as mp
import numpy as np

from ..exceptions.game_exceptions import GestureDetectionError


class Gesture(Enum):
    """Enumeration of possible hand gestures."""

    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class GestureDetector:
    """
    A class for detecting and classifying hand gestures using MediaPipe.

    This class handles the initialization of MediaPipe's hand detection model
    and provides methods for detecting and classifying hand gestures in real-time.

    Attributes:
        mp_hands: MediaPipe Hands solution
        hands: Configured MediaPipe Hands model instance
        min_detection_confidence: Minimum confidence for hand detection
        min_tracking_confidence: Minimum confidence for hand tracking
    """

    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.7,
    ) -> None:
        """
        Initialize the GestureDetector with MediaPipe configuration.

        Args:
            static_image_mode: Whether to treat input images as a video stream or independent images
            max_num_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking

        Raises:
            ResourceInitializationError: If MediaPipe resources cannot be initialized
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

    def detect_gesture(
        self, landmarks: mp.solutions.hands.HandLandmark
    ) -> Optional[Gesture]:
        """
        Detect the gesture based on hand landmarks.

        Args:
            landmarks: MediaPipe hand landmarks

        Returns:
            Optional[Gesture]: Detected gesture or None if no gesture is recognized

        Raises:
            GestureDetectionError: If gesture detection fails
        """
        try:
            # Get finger landmarks
            finger_tips = [
                landmarks.landmark[4],  # thumb
                landmarks.landmark[8],  # index
                landmarks.landmark[12],  # middle
                landmarks.landmark[16],  # ring
                landmarks.landmark[20],  # pinky
            ]
            finger_bases = [
                landmarks.landmark[2],  # thumb base
                landmarks.landmark[5],  # index base
                landmarks.landmark[9],  # middle base
                landmarks.landmark[13],  # ring base
                landmarks.landmark[17],  # pinky base
            ]

            fingers_extended = self._check_fingers_extended(finger_tips, finger_bases)
            return self._classify_gesture(fingers_extended)

        except Exception as e:
            raise GestureDetectionError(f"Failed to detect gesture: {str(e)}")

    def _check_fingers_extended(
        self,
        finger_tips: List[mp.solutions.hands.HandLandmark],
        finger_bases: List[mp.solutions.hands.HandLandmark],
    ) -> List[bool]:
        """
        Check which fingers are extended based on their landmarks.

        Args:
            finger_tips: List of finger tip landmarks
            finger_bases: List of finger base landmarks

        Returns:
            List[bool]: List indicating which fingers are extended
        """
        fingers_extended = []
        for i, (tip, base) in enumerate(zip(finger_tips, finger_bases)):
            if i == 0:  # Thumb
                fingers_extended.append(tip.x < base.x)
            else:  # Other fingers
                fingers_extended.append(tip.y < base.y)
        return fingers_extended

    def _classify_gesture(self, fingers_extended: List[bool]) -> Optional[Gesture]:
        """
        Classify the gesture based on extended fingers.

        Args:
            fingers_extended: List indicating which fingers are extended

        Returns:
            Optional[Gesture]: Classified gesture or None if no gesture is recognized
        """
        extended_count = sum(fingers_extended)

        if extended_count <= 1:
            return Gesture.ROCK
        elif extended_count == 2 and fingers_extended[1] and fingers_extended[2]:
            return Gesture.SCISSORS
        elif extended_count >= 4:
            return Gesture.PAPER

        return None

    def __del__(self) -> None:
        """Clean up MediaPipe resources."""
        if hasattr(self, "hands"):
            self.hands.close()
