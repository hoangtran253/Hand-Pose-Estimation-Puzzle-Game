# puzzle_piece.py
import pygame
from config import PIECE_POSITION_TOLERANCE

class PuzzlePiece:
    def __init__(self, image, x, y, original_x, original_y, rotation=0):
        self.image = image
        self.original_image = image.copy()
        self.x = x
        self.y = y
        self.original_x = original_x
        self.original_y = original_y
        self.rotation = rotation
        self.rect = self.image.get_rect(center=(x, y))
        self.selected = False
        self.snap_threshold = PIECE_POSITION_TOLERANCE * 0.5  # Giảm độ nhạy của hút nam châm
        
    def update_position(self, x, y):
        self.x = x
        self.y = y
        
        # Kiểm tra nếu mảnh ghép gần đúng vị trí, tự động hút vào
        distance = ((self.x - self.original_x) ** 2 + (self.y - self.original_y) ** 2) ** 0.5
        if distance < self.snap_threshold:
            # Tạo hiệu ứng hút nam châm
            self.x = self.original_x
            self.y = self.original_y
            # Đặt lại góc quay về 0 (hướng ban đầu của ảnh)
            self.rotation = 0
            self.image = self.original_image.copy()
        
        self.rect.center = (self.x, self.y)
        
    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def is_in_correct_position(self, tolerance=20):
        distance = ((self.x - self.original_x) ** 2 + (self.y - self.original_y) ** 2) ** 0.5
        rotation_diff = min(abs(self.rotation % 360), 360 - abs(self.rotation % 360))
        return distance < tolerance and rotation_diff < 15

