# main.py
import os
import sys
import argparse
import pygame
import cv2
from puzzle_game import PuzzleGame
from config import DEFAULT_PUZZLE_SIZE, WINDOW_SIZE, WINDOW_TITLE

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Hand Pose Estimation Puzzle Game')
    
    parser.add_argument('--image', type=str, default='puzzle_image.jpg',
                        help='Path to the image file for the puzzle')
    
    parser.add_argument('--columns', type=int, default=DEFAULT_PUZZLE_SIZE[0],
                        help='Number of columns in the puzzle grid')
    
    parser.add_argument('--rows', type=int, default=DEFAULT_PUZZLE_SIZE[1],
                        help='Number of rows in the puzzle grid')
    
    parser.add_argument('--width', type=int, default=WINDOW_SIZE[0],
                        help='Width of the game window')
    
    parser.add_argument('--height', type=int, default=WINDOW_SIZE[1],
                        help='Height of the game window')
    
    return parser.parse_args()

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import mediapipe
        import numpy
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Please install all required packages using:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    # Check OpenCV and camera access
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access webcam.")
            print("Please make sure your webcam is connected and not being used by another application.")
            sys.exit(1)
        cap.release()
    except Exception as e:
        print(f"Error with camera access: {e}")
        sys.exit(1)
        
    # Check Pygame
    try:
        pygame.init()
        pygame.quit()
    except pygame.error as e:
        print(f"Error initializing Pygame: {e}")
        sys.exit(1)

def print_instructions():
    """Print game instructions to the console"""
    print("\n" + "="*50)
    print("Hand Pose Estimation Puzzle Game")
    print("="*50)
    print("\nGame Controls:")
    print("- Use hand gestures to interact with puzzle pieces:")
    print("  * Pinch thumb and index finger to grab pieces")
    print("  * Move your hand to move the selected piece")
    print("  * Rotate your wrist to rotate the selected piece")
    print("  * Release the pinch to drop the piece")
    print("- Keyboard Controls:")
    print("  * ESC: Quit the game")
    print("  * R: Reset the puzzle")
    print("\nObjective: Arrange all puzzle pieces in the correct position to complete the image.")
    print("="*50 + "\n")

def main():
    """Main entry point of the application"""
    # Check if all dependencies are installed
    check_dependencies()
    
    # Parse command line arguments
    args = parse_args()
    
    # Check if the image file exists
    if not os.path.exists(args.image):
        print(f"Error: Image file '{args.image}' not found.")
        print("Please provide a valid image path with the --image argument.")
        print("Example: python main.py --image your_image.jpg")
        sys.exit(1)
    
    # Set up the game with the specified parameters
    puzzle_size = (args.columns, args.rows)
    window_size = (args.width, args.height)
    
    print(f"Starting game with image: {args.image}")
    print(f"Puzzle size: {puzzle_size[0]}x{puzzle_size[1]}")
    print(f"Window size: {window_size[0]}x{window_size[1]}")
    
    # Print instructions
    print_instructions()
    
    # Initialize pygame before creating the game
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    
    try:
        # Create and run the game
        game = PuzzleGame(args.image, puzzle_size, window_size)
        game.run()
    except Exception as e:
        print(f"Error during game execution: {e}")
    finally:
        # Clean up resources
        pygame.quit()
        cv2.destroyAllWindows()
        print("\nGame terminated.")

if __name__ == "__main__":
    main()