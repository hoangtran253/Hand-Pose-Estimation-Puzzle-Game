# config.py
"""
Configuration settings for the Hand Pose Puzzle Game
"""

# Window settings
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_TITLE = "Hand Controlled Puzzle Game"

# Colors
BACKGROUND_COLOR = (50, 50, 50)
GRID_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)
SELECTED_COLOR = (255, 0, 0)
COMPLETION_COLOR = (0, 255, 0)

# Game settings
DEFAULT_PUZZLE_SIZE = (2, 2)  # Grid size (columns, rows)
PIECE_POSITION_TOLERANCE = 150  # How close pieces need to be to correct position
ROTATION_TOLERANCE = 15  # Maximum angle difference for correct rotation
ROTATION_THRESHOLD = 5  # Minimum angle change to trigger rotation

# Hand gesture settings
GRAB_DISTANCE_THRESHOLD = 0.08  # Distance between thumb and index finger to register as grab

# UI settings
FONT_SIZE = 24
WEBCAM_DISPLAY_SIZE = (320, 240)
WEBCAM_POSITION = (10, 10)  # Top-left corner position

# MediaPipe hand detection settings
HAND_DETECTION_CONFIDENCE = 0.5
HAND_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1