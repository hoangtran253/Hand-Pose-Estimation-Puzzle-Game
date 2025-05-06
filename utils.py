# utils.py
import cv2
import pygame
import numpy as np
import os

def load_image(image_path):
    """
    Load an image file and handle common errors
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        pygame.Surface: Loaded image as a Pygame surface
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
        
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        raise Exception(f"Could not load image: {e}")

def resize_image(image, width, height):
    """
    Resize an image while maintaining aspect ratio
    
    Args:
        image (pygame.Surface): Image to resize
        width (int): Target width
        height (int): Target height
        
    Returns:
        pygame.Surface: Resized image
    """
    return pygame.transform.scale(image, (width, height))

def convert_cv_to_pygame_surface(cv_image):
    """
    Convert OpenCV image (BGR) to pygame surface (RGB)
    
    Args:
        cv_image (numpy.ndarray): OpenCV image
        
    Returns:
        pygame.Surface: Pygame surface
    """
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    return pygame.surfarray.make_surface(cv_image.swapaxes(0, 1))

def draw_text(surface, text, font, color, position):
    """
    Draw text on a pygame surface
    
    Args:
        surface (pygame.Surface): Surface to draw on
        text (str): Text to display
        font (pygame.font.Font): Font to use
        color (tuple): RGB color
        position (tuple): (x, y) position
    """
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def calculate_angle(point1, point2):
    """
    Calculate angle between two points
    
    Args:
        point1 (tuple): (x, y) coordinates of first point
        point2 (tuple): (x, y) coordinates of second point
        
    Returns:
        float: Angle in degrees
    """
    return np.degrees(np.arctan2(point2[1] - point1[1], point2[0] - point1[0]))

def distance(point1, point2):
    """
    Calculate Euclidean distance between two points
    
    Args:
        point1 (tuple): (x, y) coordinates of first point
        point2 (tuple): (x, y) coordinates of second point
        
    Returns:
        float: Distance between points
    """
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def normalize_value(value, min_val, max_val, new_min, new_max):
    """
    Normalize a value from one range to another
    
    Args:
        value (float): Value to normalize
        min_val (float): Minimum value in original range
        max_val (float): Maximum value in original range
        new_min (float): Minimum value in new range
        new_max (float): Maximum value in new range
        
    Returns:
        float: Normalized value
    """
    if max_val - min_val == 0:
        return new_min
    return new_min + (value - min_val) * (new_max - new_min) / (max_val - min_val)