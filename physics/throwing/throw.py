import pygame
import math
from platforms.plateforms import Platform

width = 900
height = 600
platform_y = height - 20
win = pygame.display.set_mode((width, height))
gray = (64, 64, 64)
white = (255, 255, 255)
black = (0, 0, 0)
gravity = 9.81/2
red = (255, 0, 0)
platform_1 = Platform(2*width/3, height/2, width/3, 30)
power_reduction_factor = 8
platform_2 = Platform(width/3, height/4, width/3, 10)

class Ball:
    def __init__(self, x, y, radius, color, material_coef, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.material_coef = material_coef
        self.x1 = self.x
        self.y1 = self.y
        self.bounce = False
        self.shoot = False
        self.time_y = 0
        self.time_x = 0
        self.power = 0
        self. angle = 0
        self.velx = 0
        self.vely = 0
        self.collision_right = False
        self.collision_left = False
        self.selected = False
        self.dist_x = 0
        self.new_x = 0
        self.colored = False
        self.mass = mass

    def selection(self, click_pos):
        if self.x - self.radius <= click_pos[0] <= self.x + self.radius:
            if self.y - self.radius < click_pos[1] <= self.y + self.radius:
                return True

    def object_collision(self, object):
        line = self.radius + object.radius
        ball_distance = math.sqrt((self.x - object.x)**2 + (self.y - object.y)**2)
        if round(ball_distance) <= round(line):
            """collision_angle = math.atan((self.y - object.y)/(self.x - object.x))
            object.power = line * self.power/(8 * object.mass/self.mass)
            object.angle = math.pi - collision_angle
            object.shoot = True"""
            return True

    def update_vel(self, object):
        if self.x - self.radius < object.x + object.radius and self.y - self.radius < object.y + object.radius:
            object.x1 = self.x - self.radius - object.radius
            object.y1 = self.y - self.radius - object.radius
            object.velx += self.velx * 0.5 * self.mass/object.mass
            self.velx -= self.velx * 0.5
            object.time_x = 0
            object.time_y = 0
            object.shoot = True
            object.angle = self.angle

        if self.x + self.radius > object.x - object.radius and self.y + self.radius > object.y - object.radius:
            object.y1 = self.y + self.radius + object.radius
            object.vely += self.vely*0.5 * self.mass/object.mass
            object.x1 = self.x + self.radius + object.radius
            object.velx += self.velx * 0.5 * self.mass/object.mass
            object.shoot = True
            object.angle = self.angle

    def draw(self):
        ball = pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def motion(self):
        # collision with the walls check
        if self.x < (width - self.radius) and not self.collision_right and not self.collision_left:
            self.dist_x = self.velx * self.time_y
            self.new_x = round(self.x1 + self.dist_x)
        if self.x >= width - self.radius:
            self.time_x = 0
            self.x1 = width - self.radius - 1
            self.angle = math.pi - self.angle
            self.collision_right = True
        if self.x <= 0 + 7 + self.radius/2:
            self.time_x = 0
            self.x1 = self.radius/2 + 8
            self.collision_left = True
            self.angle = math.pi - self.angle
        self.velx = self.power * math.cos(self.angle)
        self.vely = self.power * math.sin(self.angle)

        if self.collision_right:
            self.dist_x = self.velx / self.material_coef * self.time_x
            self.new_x = round(self.x1 + self.dist_x)
        if self.collision_left:
            self.dist_x = (self.velx/self.material_coef) * self.time_x
            self.new_x = round(self.x1 + self.dist_x)

        dist_y = self.vely * self.time_y - (gravity * self.time_y ** 2) / 2
        new_y = round(self.y1 - dist_y)

        # shoot and bouncing (off the ground) check
        if self.shoot:
            self.time_y += 0.3
            self.time_x += 0.3
            if self.y <= platform_y - self.radius:
                self.x = self.new_x
                self.y = new_y
                self.bounce = False
            if self.y > platform_y - self.radius:
                self.y = platform_y - self.radius
                self.shoot = False
                self.bounce = True
            if self.power < 5 and not platform_1.platform_colision(self):
                self.y = platform_y - self.radius
                self.bounce = False
                self.shoot = False
                self.collision_right = False
                self.collision_left = False
            elif platform_1.platform_colision(self):
                platform_1.vel_update(self)
            elif platform_2.platform_colision(self):
                platform_2.vel_update(self)
            if self.bounce:
                self.time_y = 0
                self.time_x = 0
                self.power = self.power / self.material_coef
                self.shoot = True
                self.x1 = self.x
                self.y1 = self.y - self.radius
            print((self.power**2)/9.81)


def get_line(object, pos):
    line = [(object.x, object.y), (pos[0], pos[1])]
    return line


def draw_line(line):
    pygame.draw.line(win, white, (line[0][0], line[0][1]), (line[1][0], line[1][1]))


def redraw(object1, object2, object3):
    win.fill(gray)
    object1.draw()
    object2.draw()
    object3.draw()
    pygame.draw.rect(win, black, (0, height - 20, width, 20))
    platform_1.platform_draw(win)
    platform_2.platform_draw(win)


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
    elif final_x < start_x and final_y <= start_y:
        angle = math.pi - angle
    elif final_x < start_x and final_y > start_y:
        angle = math.pi + abs(angle)
    elif final_x < start_x and final_y < start_y:
        angle = 2 * math.pi - angle

    return angle


def motion_start(object, pos):
    object.x1 = object.x
    object.y1 = object.y
    power = math.sqrt((pos[1] - object.y)**2 + (pos[0] - object.x)**2)/power_reduction_factor
    angle = get_angle(pos, object)
    return power, angle


clock = pygame.time.Clock()
run = True
ball2 = Ball(450, platform_y - 7, 7, white, 2.5, 2)
ball1 = Ball(500, platform_y - 14, 14, black, 1.9, 4)
ball3 = Ball(550, platform_y - 20, 20, white, 3, 1.5)


while run:
    """if ball1.object_collision(ball3):
        ball1.update_vel(ball3)
    if ball3.object_collision(ball1):
        ball3.update_vel(ball1)
        print(ball1.object_collision(ball3))"""
    ball1.motion()
    ball2.motion()
    ball3.motion()
    pos = pygame.mouse.get_pos()
    line1 = get_line(ball1, pos)
    line2 = get_line(ball2, pos)
    line3 = get_line(ball3, pos)
    redraw(ball1, ball2, ball3)
    if ball1.selected:
        draw_line(line1)
    if ball2.selected:
        draw_line(line2)
    if ball3.selected:
        draw_line(line3)
    if ball1.selection(pos):
        ball1.color = red
    elif not ball1.colored and not ball1.selected:
        ball1.color = black
    if ball2.selection(pos):
        ball2.color = red
    elif not ball2.colored and not ball2.selected:
        ball2.color = white
    if ball3.selection(pos):
        ball3.color = red
    elif not ball3.colored and not ball3.selected:
        ball3.color = white
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                if not ball1.selection(pos) and not ball2.selection(pos) and not ball3.selection(pos):
                    ball1.selected = True
                    ball2.selected = True
                    ball3.selected = True
                    ball1.color = red
                    ball2.color = red
                    ball3.color = red
            if event.button == 3:
                ball1.selected = False
                ball2.selected = False
                ball3.selected = False
                ball1.colored = False
                ball2.colored = False
                ball3.colored = False
                ball1.color = black
                ball2.color = white
                ball3.color = white
            if event.button == 1:
                print(math.degrees(ball1.angle))
                if ball1.selection(pos):
                    ball1.color = red
                    if not ball1.selected:
                        ball1.colored = True
                        ball1.selected = True
                if ball2.selection(pos):
                    ball2.selected = True
                    ball2.color = red
                    if not ball2.selected:
                        ball2.colored = True
                        ball2.selected = True
                if ball3.selection(pos):
                    ball3.selected = True
                    ball3.color = red
                    if not ball3.selected:
                        ball3.colored = True
                        ball3.selected = True

                if not ball1.shoot:
                    if ball1.selected:
                        ball1.time_y = 0
                        ball1.time_x = 0
                        ball1.power, ball1.angle = motion_start(ball1, pos)
                        if not ball3.selection(pos) and not ball1.selection(pos) and not ball2.selection(pos):
                            ball1.shoot = True

                        if pos[0] >= platform_1.x and platform_1.y - 3 <= pos[1] <= platform_1.y + 3 + platform_1.height or ball1.power < 5:
                            ball1.shoot = False

                if not ball2.shoot:
                    if ball2.selected:
                        ball2.time_y = 0
                        ball2.time_x = 0
                        ball2.power, ball2.angle = motion_start(ball2, pos)
                        if not ball3.selection(pos) and not ball1.selection(pos) and not ball2.selection(pos):
                            ball2.shoot = True
                        if pos[0] >= platform_1.x and platform_1.y - 3 <= pos[1] <= platform_1.y + 3 + platform_1.height or ball2.power < 5:
                            ball2.shoot = False

                if not ball3.shoot:
                    if ball3.selected:
                        ball3.time_y = 0
                        ball3.time_x = 0
                        ball3.power, ball3.angle = motion_start(ball3, pos)
                        if not ball3.selection(pos) and not ball1.selection(pos) and not ball2.selection(pos):
                            ball3.shoot = True
                        if pos[0] >= platform_1.x and platform_1.y - 3 <= pos[1] <= platform_1.y + 3 + platform_1.height or ball3.power < 5:
                            ball3.shoot = False
    pygame.display.update()
    clock.tick(60)
pygame.quit()