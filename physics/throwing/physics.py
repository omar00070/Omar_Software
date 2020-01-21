import pygame
import math

width = 1500
height = 750
win = pygame.display.set_mode((width, height))
gray = (64, 64, 64)
white = (255, 255, 255)
black = (0, 0, 0)
gravity = 9.81/2

class Ball:
    def __init__(self, x, y, radius, color, material_coef):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.material_coef = material_coef
        self.x1 = 0
        self.y1 = 0
        self.bounce = False
        self.shoot = False
        self.time = 0
        self.time_x = 0
        self.timer_col = 0
        self.power = 0
        self. angle = 0
        self.velx = 0
        self.vely = 0
        self.colision = False
        self.dist_x = 0
        self.new_x = 0

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    @ staticmethod
    def motion(object):
        # collision
        if object.x < (width - object.radius) and not object.colision:
            object.dist_x = object.velx * object.time
            object.new_x = round(object.x1 + object.dist_x)
        if object.x >= width - object.radius:
            object.time_x = 0.1
            object.x1 = width - object.radius - 3
            object.colision = True
        if object.colision:
            object.dist_x = - object.velx * object.time_x
            object.new_x = round(object.x1 + object.dist_x)
        object.velx = object.power * math.cos(object.angle)
        vely = object.power * math.sin(object.angle)
        dist_y = vely * object.time - (gravity * object.time**2)/2
        new_y = round(object.y1 - dist_y)
        # shoot
        if object.shoot:
            object.time += 0.1
            object.time_x += 0.1
            if object.y <= 730 - object.radius:
                object.x = object.new_x
                object.y = new_y
                object.bounce = False
            if object.y > 730 - object.radius:
                object.y = 730 - object.radius
                object.shoot = False
                object.bounce = True
            if object.power < 5:
                object.y = 730 - object.radius
                object.bounce = False
                object.shoot = False
                object.colision = False
            if object.bounce:
                object.time = 0
                object.time_x = 0
                object.power = object.power/object.material_coef
                object.shoot = True
                object.x1 = object.x
                object.y1 = 730 - object.radius


def get_line(object, pos):
    line = [(object.x, object.y), (pos[0], pos[1])]
    return line


def redraw(line, line1, line3, object1, object2, object3):
    win.fill(gray)
    object1.draw()
    object2.draw()
    object3.draw()
    pygame.draw.line(win, black, (line[0][0], line[0][1]), (line[1][0], line[1][1]))
    pygame.draw.line(win, white, (line1[0][0], line1[0][1]), (line1[1][0], line1[1][1]))
    pygame.draw.line(win, black, (line3[0][0], line3[0][1]), (line3[1][0], line[1][1]))
    pygame.draw.rect(win, black, (0, height - 20, width, 20))


def get_angle(pos, ball):
    final_y = pos[1]
    start_y = ball.y1
    final_x = pos[0]
    start_x = ball.x1
    try:
        tan_angle = (final_y - start_y) / (final_x - start_x)
        angle = math.atan(tan_angle)
    except:
        angle = math.pi / 2
    if final_x > start_x and final_y < start_y:
        angle = abs(angle)
    elif final_x < start_x and final_y < start_y:
        angle = math.pi - angle
    elif final_x < start_x and final_y > start_y:
        angle = math.pi + abs(angle)
    elif final_x < start_x and final_y < start_y:
        angle = 2 * math.pi - angle

    return angle


def motion_start(object, pos):
    object.x1 = object.x
    object.y1 = object.y
    power = math.sqrt((pos[1] - object.y)**2 + (pos[0] - object.x)**2)/8
    angle = get_angle(pos, object)
    return power, angle


clock = pygame.time.Clock()
run = True
ball2 = Ball(450, 723, 7, white, 3)
ball1 = Ball(500, 716, 14, black, 1.5)
ball3 = Ball(550, 709, 20, white, 1.2)
shoot = False
bounce = False


while run:
    ball1.motion(ball1)
    ball2.motion(ball2)
    ball3.motion(ball3)
    pos = pygame.mouse.get_pos()
    line1 = get_line(ball1, pos)
    line2 = get_line(ball2, pos)
    line3 = get_line(ball3, pos)
    redraw(line1, line2, line3, ball1, ball2, ball3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not ball1.shoot:
                ball1.shoot = True
                ball1.time = 0
                ball1.time_x = 0
                ball1.power, ball1.angle = motion_start(ball1, pos)
                print(ball1.power, ball1.angle)
            if not ball2.shoot:
                ball2.shoot = True
                ball2.time = 0
                ball2.time_x = 0
                ball2.power, ball2.angle = motion_start(ball2, pos)
                print(ball2.power, ball2.angle)
            if not ball3.shoot:
                ball3.shoot = True
                ball3.time = 0
                ball3.time_x = 0
                ball3.power, ball3.angle = motion_start(ball3, pos)
                print(ball3.power, ball3.angle)
    pygame.display.update()
    clock.tick(60)
pygame.quit()

if self.x - self.radius <= object.x + object.radius and self.x + self.radius >= object.x - object.radius:
    if self.y + self.radius >= object.y - object.radius and self.y - self.radius <= object.y + object.radius: