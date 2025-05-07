import pygame
import random
import sys
import time
import Menu

SNAKE_SIZE = 10
WIDTH, HEIGHT = 600, 400

DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

DIFFICULTY = {
    "easy": 10,
    "medium": 15,
    "hard": 20
}

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        pygame.init()

        # Set up the game variables
        self.snake = Snake()
        self.enemy = EnemySnake()
        self.apple = Apple(amount=3)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.window = pygame.display.set_mode((self.width, self.height))
        #
        #
        self.menu = Menu.Menu(self.window)
        #
        self.difficulty = self.menu.difficulty
        self.difficulty_speed = DIFFICULTY[self.difficulty]

        self.main_loop()
    
    def event_handler(self):
        # Handle key input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                    self.snake.direction = "UP"
                elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                    self.snake.direction = "DOWN"
                elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                    self.snake.direction = "LEFT"
                elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                    self.snake.direction = "RIGHT"
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                
    def draw_window(self):
        """Draw the game window, including the snake, enemy snake, and apples."""
        self.window.fill(WHITE)
        for segment in self.snake.body:
            pygame.draw.rect(self.window, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        for segment in self.enemy.body:
            pygame.draw.rect(self.window, BLUE, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        self.apple.draw(self.window)
        self.update_score()
        pygame.display.flip()

    def check_apple_collision(self):
        """Check if the snake or enemy snake collides with an apple."""
        for apple in self.apple.position:
            if self.snake.body[0] == apple or self.enemy.body[0] == apple:
                self.apple.position.remove(apple)
                self.apple.spawn()
                if self.snake.body[0] == apple:
                    self.snake.grow = True
                    self.score += 1
                    self.update_score()
                else:
                    self.enemy.grow = True

    def check_enemy_collision(self):     
        """Check if the enemy snake collides with the snake."""       
        for segment in self.enemy.body:
            if self.snake.body[0] == segment:
                Game.game_over()

    def update_score(self):
        font = pygame.font.SysFont("Arial", 25)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.window.blit(score_text, (10, 10))

    def game_over():
        print("Game Over!")
        pygame.quit()
        sys.exit()

    def main_loop(self):
        while self.running:
            self.event_handler()
            self.snake.move()
            self.enemy.move(apples=self.apple.position)
            self.draw_window()
            self.check_apple_collision()
            self.check_enemy_collision()
            self.clock.tick(self.difficulty_speed)
    

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = "RIGHT"
        self.grow = False
        
    def move(self):
        """Move the snake in the current direction."""
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
        #self.check_apple_collision()

    def check_boundaries(self):
        """Check if the snake head is within the boundaries of the window."""
        head_x, head_y = self.body[0]
        if not self.within_boundaries(self.body[0]):
            Game.game_over()
        # if head_x < 0:
        #     head_x = WIDTH - SNAKE_SIZE
        # elif head_x >= WIDTH:
        #     head_x = 0
        # if head_y < 0:
        #     head_y = HEIGHT - SNAKE_SIZE
        # elif head_y >= HEIGHT:
        #     head_y = 0
        # self.body[0] = (head_x, head_y)

    def check_self_collision(self):
        """Check if the snake collides with itself."""
        head = self.body[0]
        if head in self.body[1:]:
            Game.game_over()

    def within_boundaries(self, head):
        """Check if the snake head is within the boundaries of the window."""
        head_x, head_y = head
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return False
        return True        

class EnemySnake(Snake):
    def __init__(self):
        super().__init__()
        self.body = [(500, 300), (510, 300), (520, 300)]
        self.direction = "LEFT"

    def find_closest_apple(self, apples):
        """Find the closest apple to the enemy snake based on Manhattan distance."""
        closest_apple = None
        min_distance = float('inf')
        head_x, head_y = self.body[0]

        for apple_x, apple_y in apples:
            distance = abs(head_x - apple_x) + abs(head_y - apple_y)  # Manhattan distance
            if distance < min_distance:
                min_distance = distance
                closest_apple = (apple_x, apple_y)

        return closest_apple
    
    def move(self, apples):
        """Move the enemy snake towards the closest apple."""
        if not apples:
            super().move()
            return
        closest_apple = self.find_closest_apple(apples)
        self.move_towards(closest_apple)

    def move_towards(self, target):
        """Move the enemy snake towards the target apple."""
        head_x, head_y = self.body[0]
        target_x, target_y = target

        # Priority directions toward target
        directions = []
        if target_x > head_x:
            directions.append("RIGHT")
        elif target_x < head_x:
            directions.append("LEFT")

        if target_y > head_y:
            directions.append("DOWN")
        elif target_y < head_y:
            directions.append("UP")

        # Fill remaining directions to try all if needed
        for d in directions:
            if d not in DIRECTIONS:
                directions.append(d)

        # Try directions in order, avoiding collisions with self
        for direction in directions:
            new_head = self.get_new_head_pos(direction)
            if new_head not in self.body and super().within_boundaries(new_head):
                self.direction = direction
                break  # Found a safe direction

        super().move()
    
    def get_new_head_pos(self, direction):
        head_x, head_y = self.body[0]
        if direction == "UP":
            return (head_x, head_y - SNAKE_SIZE)
        elif direction == "DOWN":
            return (head_x, head_y + SNAKE_SIZE)
        elif direction == "LEFT":
            return (head_x - SNAKE_SIZE, head_y)
        elif direction == "RIGHT":
            return (head_x + SNAKE_SIZE, head_y)

class Apple:
    def __init__(self,amount):
        self.position = []
        for _ in range(amount):
            self.spawn()

    def spawn(self):
        """Spawn an apple at a random position on the grid."""
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        self.position.append((x, y)) 

    def draw(self, window):
        """Draw the apples on the window."""
        for apple in self.position:
            pygame.draw.rect(window, RED, (apple[0], apple[1], SNAKE_SIZE, SNAKE_SIZE))
        

if __name__ == "__main__":
    game = Game()
    pygame.quit()