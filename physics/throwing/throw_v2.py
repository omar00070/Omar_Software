import pygame
import math

print(math.cos(0.4), math.cos(math.pi - 0.4))
display_width = 1700
display_height = 600
size = (display_width, display_height)
display_bg = pygame.display.set_mode(size)
gravity = 9.81/1.5

class Ball:
    def __init__(self, x, y, radius, material_coef):
        self.x = x
        self.y = y
        self.radius = radius
        self.material_coef = material_coef

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.radius)

    @staticmethod
    def motion(startx, starty, power, angle, time):
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power
        distx = velx * time
        disty = vely * time + (- gravity * time**2)/2
        newx = round(distx + startx)
        newy = round(starty - disty)
        return (newx, newy)

lballx = 400
lbally = 590


lball = Ball(lballx, lbally, 7, 1.5)
another_ball = Ball(600, 590, 7, 2)

def get_angle(pos):
    start_x = lball.x
    start_y = lball.y
    final_x = pos[0]
    final_y = pos[1]

    try:
        tan_angle = (final_y - start_y) / (final_x - start_x)
        angle = math.atan(tan_angle)
    except:
        angle = math.pi/2
    if final_x > start_x and final_y < start_y:
        angle = abs(angle)
    elif final_x < start_x and final_y < start_y:
        angle = math.pi - abs(angle)
    elif final_x < start_x and final_y > start_y:
        angle = math.pi + abs(angle)
    elif final_x < start_x and final_y < start_y:
        angle = 2*math.pi - abs(angle)

    return angle


def shoot_init(object, pos):
    distance = [(object.x, object.y), pos]
    angle = get_angle(pos)
    power = math.sqrt((distance[1][1] - distance[0][1]) ** 2 + (distance[1][0] - distance[0][0]) ** 2) / 10
    return angle, power





def line(object):
    pos_find = pygame.mouse.get_pos()
    line = [(object.x, object.y), pos_find]
    return line


def redraw():
    display_bg.fill((64, 64, 64))
    lball.draw(display_bg)
    another_ball.draw(display_bg)
    pygame.draw.line(display_bg, (255, 255, 255), line_ball1[0], line_ball1[1])
    pygame.draw.line(display_bg, (0, 0, 0), line_ball2[0], line_ball2[1])


def move(object,time, power, x1, y1):
        time += 0.3
        po = object.motion(x1, y1, power, angle, time)
        object.x = po[0]
        object.y = po[1]
        return time, power

time = 0
x1 = 0
y1 = 0
power1 = 0
angle = 0
shoot = False
bounce = False
ti = pygame.time.Clock()

def bounce_fun(object, power):
    x1 = object.x
    y1 = object.y
    power = round(power/object.material_coef)
    return power, x1, y1

run = True
while run:
    if shoot:
        bounce = False
        if lball.y < (600 - lball.radius):
            move(lball, time, power1, x1, y1)
            time, power1 = move(lball, time, power1, x1, y1)
        else:
            bounce = True
            shoot = False
            lball.y = lbally
        if bounce and not shoot:
            power1, x1, y1 = bounce_fun(lball, power1)
            shoot = True
            print(x1, y1)
            time = 0
        if power1 <= 5:
            shoot = False
            bounce = False
            lball.y = lbally

    pos = pygame.mouse.get_pos()
    line_ball2 = line(another_ball)
    line_ball1 = line(lball)
    redraw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
               # return time, angle, shoot, power
               #angle, power = shoot_init(lball, pos1)
                time = 0
                angle = get_angle(pos)
                x1 = lball.x
                y1 = lball.y
                x2 = pos[0]
                y2 = pos[1]
                shoot = True
                power1 = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)/6
                print(angle, power1, math.cos(angle))
    ti.tick(60)
pygame.quit()