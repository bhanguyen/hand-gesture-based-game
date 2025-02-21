# Hand Gesture-Based Rock Paper Scissors Game

A real-time interactive Rock Paper Scissors game that uses computer vision to detect hand gestures through your webcam. Play against the computer using natural hand movements!

## 🎮 Features

- Real-time hand gesture detection using MediaPipe
- Interactive gameplay with computer opponent
- Live webcam feed with hand landmark visualization
- Score tracking system
- Intuitive countdown system
- Clear visual feedback for game states
- Natural gesture recognition for Rock, Paper, and Scissors

## 🛠️ Requirements

- Python 3.8 or higher
- Webcam
- UV package manager (will be installed automatically)

## 🚀 Installation

### Quick Setup (Recommended)

1. Clone the repository:
```bash
# HTTPS
git clone https://github.com/yourusername/hand-gesture-based-game.git

# or SSH (if configured)
git clone git@github.com:yourusername/hand-gesture-based-game.git

cd hand-gesture-based-game
```

2. Run the setup script:
```bash
# On macOS
chmod +x setup-mac.sh
./setup-mac.sh
```

### Manual Setup

1. Install UV if not already installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix/MacOS
# or
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
# Install with exact versions from lock file (recommended)
uv pip sync uv.lock

# Or, install latest compatible versions
uv pip install -e ".[dev]"
```

## 🎯 How to Play

1. Run the game:
```bash
python main.py
```

2. Show your hand to the camera to start the game
3. When the countdown begins, prepare your gesture
4. Make one of the following gestures:
   - ✊ **Rock**: Make a fist
   - ✋ **Paper**: Show an open palm
   - ✌️ **Scissors**: Show index and middle fingers only
5. Hold your gesture until the result is displayed
6. The game will automatically restart for the next round
7. Press 'q' or 'ESC' to quit the game

## 🎲 Game Rules

- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
- Same gestures result in a tie
- Scores are tracked throughout the session

## 🔍 Gesture Detection Details

The game uses MediaPipe's hand landmark detection to track 21 different points on your hand. Gesture recognition is based on the relative positions of your finger joints:

- **Rock**: All fingers closed (0-1 fingers extended)
- **Paper**: Most fingers extended (4-5 fingers)
- **Scissors**: Only index and middle fingers extended

## 🛟 Troubleshooting

- Ensure your webcam is properly connected and accessible
- Make sure you have good lighting conditions
- Keep your hand within the camera frame
- If gestures aren't being detected, try adjusting your hand position or angle

### Common Issues

1. **Virtual Environment Issues**:
   ```bash
   # If venv activation fails, try:
   rm -rf .venv
   uv venv
   source .venv/bin/activate
   ```

2. **Dependency Issues**:
   ```bash
   # If dependencies are not working, try:
   uv pip sync uv.lock
   ```

3. **Camera Issues**:
   - Ensure no other application is using your camera
   - Try closing and reopening the game
   - Check system camera permissions

## 🔧 Development

For development work:

1. Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Check code style:
```bash
black .
flake8
mypy src tests
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- MediaPipe for providing the hand tracking solution
- OpenCV team for the computer vision framework 