import pygame
import math

blue = (0, 0, 255)
power_reduction_factor = 8


class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bounce = False

    def platform_draw(self, surface):
        pygame.draw.rect(surface, blue, (self.x, self.y, self.width, self. height))

    def platform_colision(self, object):
        if object.x + object. radius >= self.x and object.x <= self.x + self.width:
            if self.y - object.radius < object.y < self.y + self.height + object.radius:
                return True

    def vel_update(self, object):
        object.power *= (1.7 / object.material_coef)
        object.y1 = int(self.y - object.radius)
        object.x1 = object.x
        object.time_y = 0
        object.time_x = 0

        if object.power < 5:
            object.y = int(self.y) - object.radius
            object.shoot = False


