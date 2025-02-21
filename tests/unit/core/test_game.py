"""Unit tests for the RockPaperScissors game class."""

import unittest
from unittest.mock import Mock, patch

import cv2
import numpy as np

from hand_gesture_game.core.game import GameState, RockPaperScissors
from hand_gesture_game.core.gesture_detector import Gesture
from hand_gesture_game.exceptions.game_exceptions import CameraError


class TestRockPaperScissors(unittest.TestCase):
    """Test cases for the RockPaperScissors class."""

    @patch("cv2.VideoCapture")
    def setUp(self, mock_video_capture):
        """Set up test fixtures."""
        # Mock video capture
        mock_video_capture.return_value.isOpened.return_value = True
        self.game = RockPaperScissors()

    def tearDown(self):
        """Clean up test fixtures."""
        self.game.cleanup()

    def test_init_state(self):
        """Test initial game state."""
        self.assertEqual(self.game.game_state, GameState.WAITING)
        self.assertEqual(self.game.countdown, 3)
        self.assertEqual(self.game.score, {"player": 0, "computer": 0})
        self.assertIsNone(self.game.computer_choice)
        self.assertIsNone(self.game.player_choice)
        self.assertEqual(self.game.result, "")

    @patch("cv2.VideoCapture")
    def test_camera_initialization_error(self, mock_video_capture):
        """Test camera initialization error handling."""
        mock_video_capture.return_value.isOpened.return_value = False
        with self.assertRaises(CameraError):
            RockPaperScissors()

    def test_get_computer_choice(self):
        """Test computer choice generation."""
        choice = self.game.get_computer_choice()
        self.assertIn(choice, list(Gesture))

    def test_determine_winner_tie(self):
        """Test winner determination for tie."""
        self.game.player_choice = Gesture.ROCK
        self.game.computer_choice = Gesture.ROCK
        result = self.game.determine_winner()
        self.assertEqual(result, "Tie!")
        self.assertEqual(self.game.score["player"], 0)
        self.assertEqual(self.game.score["computer"], 0)

    def test_determine_winner_player_wins(self):
        """Test winner determination when player wins."""
        test_cases = [
            (Gesture.ROCK, Gesture.SCISSORS),
            (Gesture.PAPER, Gesture.ROCK),
            (Gesture.SCISSORS, Gesture.PAPER),
        ]

        for player_choice, computer_choice in test_cases:
            with self.subTest(player=player_choice, computer=computer_choice):
                self.game.score = {"player": 0, "computer": 0}
                self.game.player_choice = player_choice
                self.game.computer_choice = computer_choice
                result = self.game.determine_winner()
                self.assertEqual(result, "You Win!")
                self.assertEqual(self.game.score["player"], 1)
                self.assertEqual(self.game.score["computer"], 0)

    def test_determine_winner_computer_wins(self):
        """Test winner determination when computer wins."""
        test_cases = [
            (Gesture.SCISSORS, Gesture.ROCK),
            (Gesture.ROCK, Gesture.PAPER),
            (Gesture.PAPER, Gesture.SCISSORS),
        ]

        for player_choice, computer_choice in test_cases:
            with self.subTest(player=player_choice, computer=computer_choice):
                self.game.score = {"player": 0, "computer": 0}
                self.game.player_choice = player_choice
                self.game.computer_choice = computer_choice
                result = self.game.determine_winner()
                self.assertEqual(result, "Computer Wins!")
                self.assertEqual(self.game.score["player"], 0)
                self.assertEqual(self.game.score["computer"], 1)

    def test_display_interface(self):
        """Test game interface display."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Test WAITING state
        self.game.game_state = GameState.WAITING
        self.game.display_interface(frame)

        # Test COUNTDOWN state
        self.game.game_state = GameState.COUNTDOWN
        self.game.countdown = 3
        self.game.display_interface(frame)

        # Test RESULT state
        self.game.game_state = GameState.RESULT
        self.game.player_choice = Gesture.ROCK
        self.game.computer_choice = Gesture.SCISSORS
        self.game.result = "You Win!"
        self.game.display_interface(frame)

        # No assertions needed as we're just testing if the methods run without errors
        # In a real application, we might want to test the actual frame contents


if __name__ == "__main__":
    unittest.main()
