import csv
import pygame
import numpy as np
import random
import os


class LettersCheck:

    with open(os.path.join("game_assets", "word_choice.txt")) as sample:
        words = csv.reader(sample, delimiter=',', quotechar='"')
        data = []

        for row in data:
            data.append(row)

    def __init__(self, data):
        self.x = 200
        self.y = 300
        self.press = np.zeros(27)
        self.word = data[random.randint(0, 6)][random.randint(0, 5)]



    def letter_load(self, letter):
        font = pygame.font.sysFont("comicsansms", 72)
        shown_letter = font.render(letter, True, (0, 128, 0))
        return shown_letter

    def letter_drawer(self, shown_letter):
        pass

    def letter_checker(self, event, letter):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if self.press[0] < 1:
                    LettersCheck.letter_drawer()



