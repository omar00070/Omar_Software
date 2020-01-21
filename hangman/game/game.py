import pygame
import os
from letters import letters_check


class Game:

    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.transparent = (0, 0, 0, 0)
        self.x = 0
        self.y = 0
        self.wrong = 0
        self.bg_width = 1200
        self.bg_height = 800
        self.win = pygame.display.set_mode((self.bg_width, self.bg_height))
        self.bg_image = pygame.image.load(os.path.join("game_assets", "background.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.bg_width, self.bg_height))
        self.background = self.win.blit(self.bg_image, (0, 0))
        background = self.background

    def dashes_drawer(self):
        for i in range(len(letters_check.LettersCheck.self.word)):
            pygame.draw.rect(self.background, self.black, (self.bg_width * 0.45 + i * 30, self.bg_height * 0.24, 20, 6))

    def game_run(self):
        clock = pygame.time.Clock()
        game_exit = False
        while not game_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                dashes = Game()
                dashes.dashes_drawer()
                pygame.display.update()
            clock.tick(60)

run = Game()
run.game_run()
