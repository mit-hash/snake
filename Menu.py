import pygame
import random
import sys
import time

class Menu:
    def __init__(self, window):
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 30)
        self.running = True
        self.window = window
        self.current_option = 0
        self.options = ["Play", "Settings", "Exit"]
        self.main_menu()
    
    def main_menu(self):
        while self.running:
            self.window.fill((255, 255, 255))
            self.draw_menu()
            self.handle_events()
            pygame.display.flip()
    
    def start_game(self):
        self.running = False

    def settings(self):
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_option = (self.current_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.current_option = (self.current_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.current_option == 0:
                        self.start_game()
                    elif self.current_option == 1:  # Settings
                        self.settings()
                    elif self.current_option == 2:  # Exit
                        self.running = False                    


    def draw_menu(self):
        for i, option in enumerate(self.options):
            if i == self.current_option:
                text = self.font.render(option, True, (0, 0, 0))
                self.window.blit(text, (self.window.get_width() // 2 - text.get_width() // 2, 100 + i * 50))
            else:
                text = self.font.render(option, True, (100, 100, 100))
                self.window.blit(text, (self.window.get_width() // 2 - text.get_width() // 2, 100 + i * 50))
        pygame.display.flip()
        pygame.display.set_caption("Snake Game Menu")