import cv2
import pygame
import sys
import random
from pygame.locals import *
from puzzle_piece import PuzzlePiece
from hand_pose_estimator import HandPoseEstimator

class PuzzleGame:
    def __init__(self, image_path, puzzle_size=(3, 3), window_size=(800, 600)):
        pygame.init()

        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Hand Controlled Puzzle Game")

        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, 
                                                    (window_size[0] // 2, window_size[1] // 2))

        self.puzzle_size = puzzle_size
        self.pieces = []
        self.create_puzzle_pieces()

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not open webcam")
            sys.exit()

        self.hand_estimator = HandPoseEstimator()

        self.selected_piece = None
        self.game_completed = False
        self.cursor_pos = None

        self.font = pygame.font.SysFont('Arial', 24)

    def create_puzzle_pieces(self):
        piece_width = self.original_image.get_width() // self.puzzle_size[0]
        piece_height = self.original_image.get_height() // self.puzzle_size[1]

        for y in range(self.puzzle_size[1]):
            for x in range(self.puzzle_size[0]):
                piece_surface = pygame.Surface((piece_width, piece_height))
                rect = pygame.Rect(x * piece_width, y * piece_height, piece_width, piece_height)
                piece_surface.blit(self.original_image, (0, 0), rect)

                original_x = self.window_size[0] // 4 + x * piece_width + piece_width // 2
                original_y = self.window_size[1] // 4 + y * piece_height + piece_height // 2

                rand_x = random.randint(piece_width, self.window_size[0] - piece_width)
                rand_y = random.randint(piece_height, self.window_size[1] - piece_height)

                rand_rotation = random.randint(0, 3) * 90

                piece = PuzzlePiece(piece_surface, rand_x, rand_y, original_x, original_y, rand_rotation)
                self.pieces.append(piece)
    def show_level_menu(self):
        selecting = True
        levels = [(2, 2), (3, 3), (4, 4), (5, 5)]
        buttons = []

        # Tạo các nút level
        for i, level in enumerate(levels):
            text = self.font.render(f"Level {i+1}: {level[0]}x{level[1]}", True, (255, 255, 255))
            rect = text.get_rect(center=(self.window_size[0] // 2, 100 + i * 80))
            buttons.append((rect, level))

        while selecting:
            self.screen.fill((30, 30, 30))

            # Tiêu đề
            title = self.font.render("Select Level", True, (0, 255, 255))
            self.screen.blit(title, (self.window_size[0] // 2 - 80, 30))

            # Vẽ các nút level
            for text_rect, level in buttons:
                # Thêm hiệu ứng hover
                mouse_pos = pygame.mouse.get_pos()
                if text_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, (100, 150, 255), text_rect.inflate(30, 20))
                else:
                    pygame.draw.rect(self.screen, (50, 50, 150), text_rect.inflate(30, 20))
                
                # Vẽ viền và văn bản
                pygame.draw.rect(self.screen, (255, 255, 255), text_rect.inflate(30, 20), 3)
                text = self.font.render(f"{level[0]}x{level[1]}", True, (255, 255, 255))
                self.screen.blit(text, text_rect)

            # Kiểm tra sự kiện người dùng
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for rect, level in buttons:
                        if rect.collidepoint(pos):
                            selecting = False
                            self.puzzle_size = level
                            self.pieces.clear()
                            self.create_puzzle_pieces()
                            return

            pygame.display.flip()


    def run(self):
        self.show_level_menu()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.cleanup()
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.cleanup()
                        return
                    elif event.key == K_r:
                        self.pieces.clear()
                        self.game_completed = False
                        self.selected_piece = None
                        self.last_rotation = 0
                        self.cursor_pos = None
                        self.show_level_menu()

            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture image")
                break

            frame = cv2.flip(frame, 1)
            processed_frame, results = self.hand_estimator.process_image(frame)

            index_finger = self.hand_estimator.get_index_finger_tip(results)
            is_grabbing = self.hand_estimator.is_grabbing(results)

            if index_finger:
                screen_x = int(index_finger.x * self.window_size[0])
                screen_y = int(index_finger.y * self.window_size[1])
                self.cursor_pos = (screen_x, screen_y)

                if is_grabbing:
                    if self.selected_piece is None:
                        for piece in self.pieces:
                            if piece.rect.collidepoint(screen_x, screen_y):
                                self.selected_piece = piece
                                piece.selected = True
                                break
                    else:
                        self.selected_piece.update_position(screen_x, screen_y)
                else:
                    if self.selected_piece:
                        self.selected_piece.selected = False
                        self.selected_piece = None
            else:
                self.cursor_pos = None

            self.check_puzzle_completion()
            self.draw()

            # Hiển thị webcam ở cửa sổ riêng
            cv2.imshow("Webcam Feed", processed_frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.cleanup()
                return

            pygame.display.flip()
            clock.tick(30)

    def draw(self):
        self.screen.fill((50, 50, 50))

        target_rect = pygame.Rect(
            self.window_size[0] // 4,
            self.window_size[1] // 4,
            self.original_image.get_width(),
            self.original_image.get_height()
        )
        pygame.draw.rect(self.screen, (200, 200, 200), target_rect, 2)

        for piece in self.pieces:
            piece.draw(self.screen)
            if piece.selected:
                pygame.draw.rect(self.screen, (255, 0, 0), piece.rect, 2)

        if self.cursor_pos:
            pygame.draw.circle(self.screen, (0, 255, 255), self.cursor_pos, 10)

        instructions = [
            "Use your hand to move puzzle pieces",
            "Grab: Pinch thumb and index finger",
            "Press ESC to quit, R to reset"
        ]

        y = 10
        for instruction in instructions:
            text = self.font.render(instruction, True, (255, 255, 255))
            self.screen.blit(text, (10, y))
            y += 30

        if self.game_completed:
            completion_text = self.font.render("WIN! Press 'r' to play again", True, (0, 255, 0))
            text_rect = completion_text.get_rect(center=(self.window_size[0] // 2, 50))
            self.screen.blit(completion_text, text_rect)

    def check_puzzle_completion(self):
        all_correct = all(piece.is_in_correct_position() for piece in self.pieces)
        if all_correct:
            self.game_completed = True
            print("Puzzle Completed!")

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        pygame.quit()
