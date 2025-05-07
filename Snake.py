import pygame
import random
import sys
import time
import Menu

SNAKE_SIZE = 10
WIDTH, HEIGHT = 600, 400

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

        self.snake = Snake()
        self.enemy = EnemySnake()
        self.apple = Apple(amount=3)
        self.score = 0
        self.clock = pygame.time.Clock()
        self.running = True
        self.window = pygame.display.set_mode((self.width, self.height))

        self.menu = Menu.Menu(self.window)

        self.difficulty = self.menu.difficulty
        self.difficulty_speed = DIFFICULTY[self.difficulty]

        self.main_loop()
    
    def event_handler(self):
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
        self.window.fill(WHITE)
        for segment in self.snake.body:
            pygame.draw.rect(self.window, GREEN, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        for segment in self.enemy.body:
            pygame.draw.rect(self.window, BLUE, (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))
        self.apple.draw(self.window)
        self.update_score()
        pygame.display.flip()

    def check_apple_collision(self):
        for apple in self.apple.position:
            if self.snake.body[0] == apple or self.enemy.body[0] == apple:
                self.apple.position.remove(apple)
                self.apple.spawn()
                if self.snake.body[0] == apple:
                    self.snake.grow = True
                    self.score += 1
                    self.update_score()

    def check_enemy_collision(self):            
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
    def __init__(self, body=[(100, 100), (90, 100), (80, 100)]):
        self.body = body
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
        #self.check_apple_collision()

    def check_boundaries(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            Game.game_over()
        if head_x < 0:
            head_x = WIDTH - SNAKE_SIZE
        elif head_x >= WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = HEIGHT - SNAKE_SIZE
        elif head_y >= HEIGHT:
            head_y = 0
        self.body[0] = (head_x, head_y)

    def check_self_collision(self):
        head = self.body[0]
        if head in self.body[1:]:
            Game.game_over()

class EnemySnake(Snake):
    def __init__(self):
        super().__init__(body=[(500, 300), (510, 300), (520, 300)])
        self.direction = "LEFT"

    def find_direction(self):
        pass

    def find_closest_apple(self, apples):
        closest_apple = None
        min_distance = float('inf')
        for apple in apples:
            distance = ((self.body[0][0] - apple[0]) ** 2 + (self.body[0][1] - apple[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_apple = apple
        return closest_apple
    
    def move(self, apples):
        closest_apple = self.find_closest_apple(apples)
        self.move_towards(closest_apple)

    def move_towards(self, target):
        head_x, head_y = self.body[0]
        target_x, target_y = target

        if abs(target_x - head_x) > abs(target_y - head_y):
            self.direction = "RIGHT" if target_x > head_x else "LEFT"
        else:
            self.direction = "DOWN" if target_y > head_y else "UP"

        super().move()


class Apple:
    def __init__(self,amount):
        self.position = []
        for _ in range(amount):
            self.spawn()

    def spawn(self):
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        self.position.append((x, y)) 

    def draw(self, window):
        for apple in self.position:
            pygame.draw.rect(window, RED, (apple[0], apple[1], SNAKE_SIZE, SNAKE_SIZE))
        

if __name__ == "__main__":
    game = Game()
    pygame.quit()