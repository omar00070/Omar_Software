import pygame
import math
height, width = 700, 1200
white = (255, 255, 255)
win = pygame.display.set_mode((width, height))

class Ball:
    def __init__(self, x, y, radius):
        self.x = int(x)
        self.y = int(y)
        self.radius = radius

    def draw(self):
        pygame.draw.circle(win, white, (self.x, self.y), self.radius)

    @staticmethod
    def move(x1, y1, angle, power, time):
        velx = power * math.cos(angle)
        vely = power * math.sin(angle)
        dist_x = velx * time
        dist_y = vely * time - (9.81/2)*(time**2) / 2
        new_x1 = x1 + int(dist_x)
        new_y1 = y1 + int(dist_y)
        return (new_x1, new_y1)


def redraw():
    win.fill((0, 0, 0))
    ball1.draw()


def get_angle(pos):

    final_y = pos[1]
    start_y = ball1.y
    final_x = pos[0]
    start_x = ball1.x
    try:
        tan_angle = (final_y - start_y) / (final_x - start_x)
        angle = math.atan(tan_angle)
    except:
        angle = math.pi / 2

    if final_x > start_x and final_y < start_y:
        angle = abs(angle)
    elif final_x < start_x and final_y <= start_y:
        angle = math.pi - angle
    elif final_x < start_x and final_y > start_y:
        angle = math.pi + abs(angle)
    elif final_x < start_x and final_y < start_y:
        angle = 2 * math.pi - angle

    return angle


x1 = 0
y1 = 0
angle = 0
power = 0
time = 0
run = True
shoot = False

ball1 = Ball(height - 3, width*0.5, 15)

while run:

    if shoot:
        if ball1.y <= height:
            time += 0.3
            po = ball1.move(x1, y1, angle, power, time)
            ball1.x = po[0]
            ball1.y = po[1]
        else:
            ball1.y = height - 3
            shoot = False

    pos = pygame.mouse.get_pos()
    line = [pos, (ball1.x, ball1.y)]
    redraw()
    pygame.draw.line(win, white, (line[0][0], line[0][1]), (line[1][0], line[1][1]))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                x1 = ball1.x
                y1 = ball1.y
                time = 0
                power = math.sqrt((line[1][0] - line[0][0])**2 + (line[1][1] - line[0][1])**2)/8
                angle = get_angle(pos)
                shoot = True

    pygame.display.update()