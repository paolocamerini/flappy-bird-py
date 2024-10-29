import pygame
import random

pygame.init()

BACKGROUND = pygame.image.load('assets/sfondo.png')
BIRD = pygame.image.load('assets/uccello.png')
BASE = pygame.image.load('assets/base.png')
GAMEOVER = pygame.image.load('assets/gameover.png')
PIPE_DOWN = pygame.image.load('assets/tubo.png')
PIPE_UP = pygame.transform.flip(PIPE_DOWN, False, True)

SCREEN = pygame.display.set_mode((288, 512))
FPS = 60
ADVANCE_SPEED = 3
FONT = pygame.font.SysFont('Comic Sans MS', 50, bold=True)

class Pipe:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75, 150)
    def advance_and_draw(self):
        self.x -= ADVANCE_SPEED
        SCREEN.blit(PIPE_DOWN, (self.x, self.y + 210))
        SCREEN.blit(PIPE_UP, (self.x, self.y - 210))
    def check_collision(self, BIRD, bird_x, bird_y):
        tolerance = 5
        bird_right = bird_x + BIRD.get_width() - tolerance
        bird_left = bird_x + tolerance
        pipe_right = self.x + PIPE_DOWN.get_width()
        pipe_left = self.x
        bird_top = bird_y + tolerance
        bird_bottom = bird_y + BIRD.get_height() - tolerance
        pipe_top = self.y + 110
        pipe_bottom = self.y + 210
        if bird_right > pipe_left and bird_left < pipe_right:
            if bird_top < pipe_top or bird_bottom > pipe_bottom:
                game_over()
    def is_passed(self, bird_x):
        return bird_x > self.x + PIPE_DOWN.get_width()

def draw_objects():
    SCREEN.blit(BACKGROUND, (0, 0))
    for p in pipes:
        p.advance_and_draw()
    SCREEN.blit(BIRD, (bird_x, bird_y))
    SCREEN.blit(BASE, (base_x, 400))
    points_render = FONT.render(str(points), True, (255, 255, 255))
    SCREEN.blit(points_render, (144, 0))

def update_screen():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)

def initialize():
    global bird_x, bird_y, bird_vel_y
    global base_x, pipes, points
    bird_x, bird_y = 60, 150
    bird_vel_y = 0
    base_x = 0
    points = 0
    pipes = [Pipe()]

def game_over():
    SCREEN.blit(GAMEOVER, (50, 180))
    update_screen()
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                initialize()
                restart = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

initialize()

while True:
    base_x -= ADVANCE_SPEED
    if base_x < -45:
        base_x = 0
    bird_vel_y += 1
    bird_y += bird_vel_y
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            bird_vel_y = -10
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if pipes[-1].x < 150:
        pipes.append(Pipe())
    for p in pipes:
        p.check_collision(BIRD, bird_x, bird_y)
    for p in pipes:
        if p.is_passed(bird_x) and not p.is_passed(bird_x - ADVANCE_SPEED):  # Increment only if fully passed
            points += 1
            break
    if bird_y > 380:
        game_over()
    draw_objects()
    update_screen()
