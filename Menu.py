import pygame
import random
import sys
import time

class Menu:
    def __init__(self, window):
        self.font = pygame.font.SysFont("Arial", 30)
        self.running = True
        self.window = window
        self.current_option = 0
        self.current_menu = 0
        self.difficulty = "easy"
        self.options = [["Play", "Settings", "Exit"], 
                        ["Back", "Difficulty"], 
                        ["Back", "Easy", "Medium", "Hard"]]
        self.main_menu()
    
    def main_menu(self):
        while self.running:
            self.window.fill((255, 255, 255))
            self.draw_menu(self.current_menu)
            self.handle_events()
            pygame.display.flip()
    
    def start_game(self):
        self.running = False

    def draw_menu(self, menu):
        for i, option in enumerate(self.options[menu]):
            if i == self.current_option:
                text = self.font.render(option, True, (0, 0, 0))
                self.window.blit(text, (self.window.get_width() // 2 - text.get_width() // 2, 100 + i * 50))
            else:
                text = self.font.render(option, True, (100, 100, 100))
                self.window.blit(text, (self.window.get_width() // 2 - text.get_width() // 2, 100 + i * 50))
        pygame.display.flip()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_option = (self.current_option - 1) % len(self.options[self.current_menu])
                elif event.key == pygame.K_DOWN:
                    self.current_option = (self.current_option + 1) % len(self.options[self.current_menu])
                elif event.key == pygame.K_RETURN:
                    self.select_option()

    def select_option(self):
        if self.current_menu == 0:
            self.handle_main_menu_selection()
        elif self.current_menu == 1:
            self.handle_settings_menu_selection()
        elif self.current_menu == 2:
            self.handle_difficulty_menu_selection()

    def handle_main_menu_selection(self):
        if self.current_option == 0:
            self.start_game()
        elif self.current_option == 1:
            self.current_menu = 1
            self.current_option = 0
        elif self.current_option == 2:
            self.running = False

    def handle_settings_menu_selection(self):
        if self.current_option == 0:
            self.current_menu = 0
            self.current_option = 0
        elif self.current_option == 1:
            self.current_menu = 2
            self.current_option = 0

    def handle_difficulty_menu_selection(self):
        if self.current_option == 0:
            self.current_menu = 1
            self.current_option = 0
        elif self.current_option == 1:
            self.difficulty = "easy"
        elif self.current_option == 2:
            self.difficulty = "medium"
        elif self.current_option == 3:
            self.difficulty = "hard"