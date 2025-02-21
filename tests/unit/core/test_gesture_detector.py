"""Unit tests for the GestureDetector class."""

import unittest
from unittest.mock import Mock, patch

import mediapipe as mp
import numpy as np

from hand_gesture_game.core.gesture_detector import Gesture, GestureDetector
from hand_gesture_game.exceptions.game_exceptions import GestureDetectionError


class TestGestureDetector(unittest.TestCase):
    """Test cases for the GestureDetector class."""

    def setUp(self):
        """Set up test fixtures."""
        self.detector = GestureDetector()

    def tearDown(self):
        """Clean up test fixtures."""
        self.detector = None

    def create_mock_landmark(self, x: float, y: float, z: float = 0.0) -> Mock:
        """Create a mock landmark with given coordinates."""
        landmark = Mock()
        landmark.x = x
        landmark.y = y
        landmark.z = z
        return landmark

    def test_init_default_values(self):
        """Test initialization with default values."""
        self.assertEqual(self.detector.min_detection_confidence, 0.7)
        self.assertEqual(self.detector.min_tracking_confidence, 0.7)

    def test_rock_gesture_detection(self):
        """Test detection of rock gesture (closed fist)."""
        # Mock landmarks for closed fist
        landmarks = Mock()
        landmarks.landmark = {
            # Finger tips (all below bases)
            4: self.create_mock_landmark(0.5, 0.6),  # thumb
            8: self.create_mock_landmark(0.5, 0.6),  # index
            12: self.create_mock_landmark(0.5, 0.6),  # middle
            16: self.create_mock_landmark(0.5, 0.6),  # ring
            20: self.create_mock_landmark(0.5, 0.6),  # pinky
            # Finger bases
            2: self.create_mock_landmark(0.4, 0.5),  # thumb
            5: self.create_mock_landmark(0.5, 0.5),  # index
            9: self.create_mock_landmark(0.5, 0.5),  # middle
            13: self.create_mock_landmark(0.5, 0.5),  # ring
            17: self.create_mock_landmark(0.5, 0.5),  # pinky
        }

        gesture = self.detector.detect_gesture(landmarks)
        self.assertEqual(gesture, Gesture.ROCK)

    def test_paper_gesture_detection(self):
        """Test detection of paper gesture (open palm)."""
        # Mock landmarks for open palm
        landmarks = Mock()
        landmarks.landmark = {
            # Finger tips (all above bases)
            4: self.create_mock_landmark(0.3, 0.4),  # thumb
            8: self.create_mock_landmark(0.5, 0.4),  # index
            12: self.create_mock_landmark(0.5, 0.4),  # middle
            16: self.create_mock_landmark(0.5, 0.4),  # ring
            20: self.create_mock_landmark(0.7, 0.4),  # pinky
            # Finger bases
            2: self.create_mock_landmark(0.4, 0.5),  # thumb
            5: self.create_mock_landmark(0.5, 0.5),  # index
            9: self.create_mock_landmark(0.5, 0.5),  # middle
            13: self.create_mock_landmark(0.5, 0.5),  # ring
            17: self.create_mock_landmark(0.5, 0.5),  # pinky
        }

        gesture = self.detector.detect_gesture(landmarks)
        self.assertEqual(gesture, Gesture.PAPER)

    def test_scissors_gesture_detection(self):
        """Test detection of scissors gesture (victory sign)."""
        # Mock landmarks for scissors gesture
        landmarks = Mock()
        landmarks.landmark = {
            # Finger tips (index and middle up, others down)
            4: self.create_mock_landmark(0.5, 0.6),  # thumb down
            8: self.create_mock_landmark(0.5, 0.4),  # index up
            12: self.create_mock_landmark(0.5, 0.4),  # middle up
            16: self.create_mock_landmark(0.5, 0.6),  # ring down
            20: self.create_mock_landmark(0.5, 0.6),  # pinky down
            # Finger bases
            2: self.create_mock_landmark(0.4, 0.5),  # thumb
            5: self.create_mock_landmark(0.5, 0.5),  # index
            9: self.create_mock_landmark(0.5, 0.5),  # middle
            13: self.create_mock_landmark(0.5, 0.5),  # ring
            17: self.create_mock_landmark(0.5, 0.5),  # pinky
        }

        gesture = self.detector.detect_gesture(landmarks)
        self.assertEqual(gesture, Gesture.SCISSORS)

    def test_invalid_gesture_detection(self):
        """Test detection of invalid gesture."""
        # Mock landmarks for invalid gesture (three fingers up)
        landmarks = Mock()
        landmarks.landmark = {
            # Finger tips (index, middle, and ring up, others down)
            4: self.create_mock_landmark(0.5, 0.6),  # thumb down
            8: self.create_mock_landmark(0.5, 0.4),  # index up
            12: self.create_mock_landmark(0.5, 0.4),  # middle up
            16: self.create_mock_landmark(0.5, 0.4),  # ring up
            20: self.create_mock_landmark(0.5, 0.6),  # pinky down
            # Finger bases
            2: self.create_mock_landmark(0.4, 0.5),  # thumb
            5: self.create_mock_landmark(0.5, 0.5),  # index
            9: self.create_mock_landmark(0.5, 0.5),  # middle
            13: self.create_mock_landmark(0.5, 0.5),  # ring
            17: self.create_mock_landmark(0.5, 0.5),  # pinky
        }

        gesture = self.detector.detect_gesture(landmarks)
        self.assertIsNone(gesture)

    def test_error_handling(self):
        """Test error handling for invalid landmarks."""
        landmarks = Mock()
        landmarks.landmark = {}  # Empty landmarks

        with self.assertRaises(GestureDetectionError):
            self.detector.detect_gesture(landmarks)


if __name__ == "__main__":
    unittest.main()
