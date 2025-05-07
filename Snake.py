import pygame
import random
import sys
import time

SNAKE_SIZE = 10
# Initialize Pygame
pygame.init()
# Set up display
WIDTH, HEIGHT = 600, 400
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
# Set up game variables

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = "RIGHT"
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "UP":
            new_head = (head_x, head_y - SNAKE_SIZE)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + SNAKE_SIZE)
        elif self.direction == "LEFT":
            new_head = (head_x - SNAKE_SIZE, head_y)
        elif self.direction == "RIGHT":
            new_head = (head_x + SNAKE_SIZE, head_y)

        if self.grow:
            self.body.insert(0, new_head)
            self.grow = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()
        self.check_boundaries()
        self.check_self_collision()
        self.check_apple_collision()

    def check_boundaries(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            self.game_over()
        if head_x < 0:
            head_x = WIDTH - SNAKE_SIZE
        elif head_x >= WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = HEIGHT - SNAKE_SIZE
        elif head_y >= HEIGHT:
            head_y = 0
        self.body[0] = (head_x, head_y)
        if head_x < 0:
            head_x = WIDTH - SNAKE_SIZE
    
    def check_self_collision(self):
        head = self.body[0]
        if head in self.body[1:]:
            self.game_over()

    def check_apple_collision(self):
        if self.body[0] == apple.position:
            self.grow = True
            apple.spawn()
            self.score += 1
            self.update_score()

    def game_over(self):
        print("Game Over!")
        pygame.quit()
        sys.exit()

