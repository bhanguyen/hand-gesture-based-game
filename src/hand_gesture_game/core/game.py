"""Main game module for the Rock Paper Scissors hand gesture game."""

import random
import time
from typing import Dict, Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np

from ..exceptions.game_exceptions import CameraError, GestureDetectionError
from ..utils.logging_config import get_logger
from .gesture_detector import Gesture, GestureDetector

logger = get_logger(__name__)


class GameState:
    """Enumeration of possible game states."""

    WAITING = "WAITING"
    COUNTDOWN = "COUNTDOWN"
    PLAYING = "PLAYING"
    RESULT = "RESULT"


class RockPaperScissors:
    """
    Main game class for Rock Paper Scissors hand gesture game.

    This class handles the game logic, video capture, and display interface
    for the Rock Paper Scissors game using hand gestures.

    Attributes:
        gesture_detector: GestureDetector instance for hand gesture recognition
        cap: OpenCV video capture object
        game_state: Current state of the game
        countdown: Countdown timer value
        last_countdown_time: Timestamp of last countdown update
        computer_choice: Computer's gesture choice
        player_choice: Player's gesture choice
        result: Current game result
        score: Dictionary containing player and computer scores
    """

    def __init__(self) -> None:
        """
        Initialize the Rock Paper Scissors game.

        Raises:
            CameraError: If camera cannot be initialized
            ResourceInitializationError: If required resources cannot be initialized
        """
        logger.info("Initializing Rock Paper Scissors game")
        self.gesture_detector = GestureDetector()
        self.cap = self._initialize_camera()
        self.mp_draw = mp.solutions.drawing_utils

        # Game state
        self.game_state: str = GameState.WAITING
        self.countdown: int = 3
        self.last_countdown_time: float = 0
        self.computer_choice: Optional[Gesture] = None
        self.player_choice: Optional[Gesture] = None
        self.result: str = ""
        self.score: Dict[str, int] = {"player": 0, "computer": 0}
        logger.debug("Game initialized with default state")

    def _initialize_camera(self) -> cv2.VideoCapture:
        """
        Initialize the camera for video capture.

        Returns:
            cv2.VideoCapture: Initialized video capture object

        Raises:
            CameraError: If camera cannot be initialized
        """
        logger.info("Initializing camera")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            logger.error("Failed to initialize camera")
            raise CameraError("Failed to initialize camera")
        logger.debug("Camera initialized successfully")
        return cap

    def get_computer_choice(self) -> Gesture:
        """
        Generate random computer choice.

        Returns:
            Gesture: Randomly selected gesture
        """
        choice = random.choice(list(Gesture))
        logger.debug(f"Computer chose {choice.name}")
        return choice

    def determine_winner(self) -> str:
        """
        Determine the winner based on player and computer choices.

        Returns:
            str: Result message indicating the winner
        """
        if self.player_choice == self.computer_choice:
            logger.info("Game resulted in a tie")
            return "Tie!"

        winning_combinations = {
            (Gesture.ROCK, Gesture.SCISSORS),
            (Gesture.PAPER, Gesture.ROCK),
            (Gesture.SCISSORS, Gesture.PAPER),
        }

        if (self.player_choice, self.computer_choice) in winning_combinations:
            self.score["player"] += 1
            logger.info(
                f"Player wins! New score - Player: {self.score['player']}, Computer: {self.score['computer']}"
            )
            return "You Win!"
        else:
            self.score["computer"] += 1
            logger.info(
                f"Computer wins! New score - Player: {self.score['player']}, Computer: {self.score['computer']}"
            )
            return "Computer Wins!"

    def display_interface(self, frame: np.ndarray) -> None:
        """
        Display game interface on frame.

        Args:
            frame: Video frame to display interface on
        """
        h, w, _ = frame.shape

        if self.game_state == GameState.WAITING:
            cv2.putText(
                frame,
                "Show hand to start!",
                (int(w / 4), 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
        elif self.game_state == GameState.COUNTDOWN:
            cv2.putText(
                frame,
                str(self.countdown),
                (int(w / 2), int(h / 2)),
                cv2.FONT_HERSHEY_SIMPLEX,
                4,
                (255, 0, 0),
                4,
            )
        elif self.game_state == GameState.RESULT:
            player_choice_text = f"Your choice: {self.player_choice.name}"
            computer_choice_text = f"Computer: {self.computer_choice.name}"
            cv2.putText(
                frame,
                player_choice_text,
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.putText(
                frame,
                computer_choice_text,
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
            cv2.putText(
                frame,
                self.result,
                (int(w / 4), int(h / 2)),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 0, 0),
                3,
            )

        # Always display score
        score_text = (
            f"Score - You: {self.score['player']} Computer: {self.score['computer']}"
        )
        cv2.putText(
            frame,
            score_text,
            (10, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )

    def run(self) -> None:
        """
        Main game loop.

        Raises:
            CameraError: If there are issues with camera access
            GestureDetectionError: If gesture detection fails
        """
        logger.info("Starting game loop")
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    logger.error("Failed to capture video frame")
                    raise CameraError("Failed to capture video frame")

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = self.gesture_detector.hands.process(rgb_frame)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame,
                            hand_landmarks,
                            self.gesture_detector.mp_hands.HAND_CONNECTIONS,
                        )

                        if self.game_state == GameState.WAITING:
                            logger.debug("Hand detected, starting countdown")
                            self.game_state = GameState.COUNTDOWN
                            self.last_countdown_time = time.time()

                        elif self.game_state == GameState.COUNTDOWN:
                            current_time = time.time()
                            if current_time - self.last_countdown_time >= 1:
                                self.countdown -= 1
                                logger.debug(f"Countdown: {self.countdown}")
                                self.last_countdown_time = current_time
                                if self.countdown <= 0:
                                    logger.info("Countdown finished, starting game")
                                    self.game_state = GameState.PLAYING
                                    self.computer_choice = self.get_computer_choice()

                        elif self.game_state == GameState.PLAYING:
                            try:
                                gesture = self.gesture_detector.detect_gesture(
                                    hand_landmarks
                                )
                                if gesture:
                                    logger.info(f"Player chose {gesture.name}")
                                    self.player_choice = gesture
                                    self.result = self.determine_winner()
                                    self.game_state = GameState.RESULT
                                    self.countdown = 3
                            except GestureDetectionError as e:
                                logger.error(f"Gesture detection error: {e}")

                elif self.game_state == GameState.RESULT:
                    current_time = time.time()
                    if current_time - self.last_countdown_time >= 2:
                        logger.debug("Resetting game state to WAITING")
                        self.game_state = GameState.WAITING
                        self.countdown = 3

                self.display_interface(frame)

                cv2.putText(
                    frame,
                    "Press 'q' or 'ESC' to quit",
                    (10, frame.shape[0] - 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

                cv2.imshow("Rock Paper Scissors", frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q") or key == 27:  # 27 is ESC key
                    logger.info("Game terminated by user")
                    break

        except Exception as e:
            logger.error(f"Game error: {str(e)}")
            raise CameraError(f"Game error: {str(e)}")

        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up resources")
        if hasattr(self, "cap"):
            self.cap.release()
        cv2.destroyAllWindows()
