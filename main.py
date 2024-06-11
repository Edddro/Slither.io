'''
Name: Edward Drobnis
Date: May 30, 2024
Title:
Description:
'''
import pygame
import sys
import math
import random

pygame.init()

WIDTH = 700
HEIGHT = 600

pygame.display.set_caption('Slither.io')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

LIGHT_GREEN = (57, 255, 20)
GREEN = (162, 209, 73)
DARK_GREEN = (154, 203, 65)
LIGHT_RED = (255, 7, 58)
RED = (235, 64, 52)
LIGHT_BLUE = (0, 209, 255)
BLUE = (26, 115, 232)
DARK_BLUE = (0, 0, 139)
YELLOW = (252, 186, 3)
LIGHT_PURPLE = (177, 156, 217)
PURPLE = (128, 0, 128)
LIGHT_PINK = (255, 20, 147)
PINK = (255, 105, 180)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
LIGHT_BLACK = (27, 27, 27)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (45,45,45)

FOOD_COLOR = [LIGHT_GREEN, DARK_GREEN, LIGHT_RED, LIGHT_BLUE, DARK_GREEN, YELLOW, LIGHT_PURPLE, LIGHT_PINK, PINK, ORANGE]
background = pygame.transform.scale(pygame.image.load("./Graphics/background.png").convert_alpha(), (WIDTH, HEIGHT))

class Food(pygame.sprite.Sprite):
    def __init__(self):
        self.foods = []
        self.speed_foods = []
        self.snake_foods = []
        for _ in range(50):
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.foods.append([self.x, self.y])

    def speed_food(self, x, y):
        self.speed_foods.append([x, y])

    def snake_to_food(self, snake):
        for segment in snake:
            self.snake_foods.append([segment])

    def move(self):
        self.foods_move = []
        for pos in self.foods:
            self.foods_move.append((pygame.mouse.get_pos() - pygame.math.Vector2(pos)))
        for i in range(len(self.foods_move)):
            self.foods[i] += self.foods_move[i] * -0.1

    def update(self, x, y):
        self.foods = [food for food in self.foods if food != [x, y]]
        while len(self.foods) < 100:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.foods.append([self.x, self.y])

    def draw(self, food_type):
        if food_type == 'speed':
            for food in self.speed_foods:
                pygame.draw.circle(screen, random.choice(FOOD_COLOR), food, 3)
        elif food_type == 'snake':
            for food in self.snake_foods:
                pygame.draw.circle(screen, random.choice(FOOD_COLOR), food, 8)
        else:
            for food in self.foods:
                pygame.draw.circle(screen, random.choice(FOOD_COLOR), food, 5)

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        self.snake = []
        self.direction = ""
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.snake.append([self.x, self.y])
        self.snake_colour = random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])

        if self.direction == "up":
            for i in range(1, 11):
                self.snake.append([self.x, self.y + (8 * i)])
        elif self.direction == "down":
            for i in range(1, 11):
                self.snake.append([self.x, self.y - (8 * i)])
        elif self.direction == "right":
            for i in range(1, 11):
                self.snake.append([self.x - (8 * i), self.y])
        elif self.direction == "left":
            for i in range(1, 11):
                self.snake.append([self.x + (8 * i), self.y])
    def grow(self, direction, x, y):
        if direction == "up":
            self.snake.append([x, y + 8])
        elif direction == "down":
            self.snake.append([x, y - 10])
        elif direction == "right":
            self.snake.append([x - 10, y])
        elif direction == "left":
            self.snake.append([x + 10, y])

    def shrink(self):
        food = Food()
        food.speed_foods(self.snake[-1][0], self.snake[-1][1])
        self.snake.pop()

    def eyes(self, radius, mouse_x, mouse_y):
        head_x, head_y = self.snake[0]
        distance = radius / 8
        direction = pygame.math.Vector2(mouse_x - head_x, mouse_y - head_y).normalize() * 2

        if self.direction == "up" or self.direction == "down":
            x_eye_left = 4
            x_eye_right = -4
            y_eye_left = -3 * distance if self.direction == "up" else 3 * distance
            y_eye_right = -3 * distance if self.direction == "up" else 3 * distance
        else:
            x_eye_left = -3 * distance if self.direction == "left" else 3 * distance
            x_eye_right = -3 * distance if self.direction == "left" else 3 * distance
            y_eye_left = 4
            y_eye_right = -4

        pygame.draw.circle(screen, WHITE, (self.snake[0][0] + x_eye_left, self.snake[0][1] + y_eye_left), 4)
        pygame.draw.circle(screen, WHITE, (self.snake[0][0] + x_eye_right, self.snake[0][1] + y_eye_right), 4)

        pygame.draw.circle(screen, BLACK, (int(head_x + x_eye_left + direction.x), int(head_y + y_eye_left + direction.y)), 2.75)
        pygame.draw.circle(screen, BLACK, (int(head_x + x_eye_right + direction.x), int(head_y + y_eye_right + direction.y)), 2.75)

    def draw(self, radius, speed, mouse_x, mouse_y):
        for i, segment in enumerate(reversed(self.snake)):
            if (i // 3) % 2 == 0:
                if speed:
                    shade_factor = 1.0 + (i / (len(self.snake) * 5))
                else:
                    shade_factor = 1 - (i / (len(self.snake) * 3.5))
            else:
                shade_factor = 1
            if speed:
                color = (min(int(self.snake_colour[0] * shade_factor), 255), min(int(self.snake_colour[1] * shade_factor), 255), min(int(self.snake_colour[2] * shade_factor), 255))
            else:
                color = (int(self.snake_colour[0] * shade_factor), int(self.snake_colour[1] * shade_factor), int(self.snake_colour[2] * shade_factor))
            pygame.draw.circle(screen, color, (int(segment[0]), int(segment[1])), radius)
        self.eyes(radius, mouse_x, mouse_y)

def main():
    radius = 10
    speed = False
    score = 0
    high_score = 0
    if score != 0 and score % 800 == 0:
        radius += 2
    food = Food()
    food.draw("normal")
    snake = Snake()
    snake.draw(radius, speed, mouse_x, mouse_y)

mouse_x, mouse_y = pygame.mouse.get_pos()
background_x = 0
background_y = 0
main()
run = True
while run:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x < WIDTH / 2:
        background_x -= 0.1
    if mouse_x > WIDTH / 2:
        background_x += 0.1
    if mouse_y < HEIGHT / 2:
        background_y -= 0.1
    if mouse_y > HEIGHT / 2:
        background_y += 0.1

    screen.fill(BLACK)
    screen.blit(background, (background_x, background_y))
    screen.blit(background, (background_x + WIDTH, background_y))
    screen.blit(background, (background_x, background_y + HEIGHT))
    screen.blit(background, (background_x + WIDTH, background_y + HEIGHT))

    if background_x <= -WIDTH:
        background_x = 0
    if background_x >= 0:
        background_x = -WIDTH
    if background_y <= -HEIGHT:
        background_y = HEIGHT
    if background_y >= 0:
        background_y = -HEIGHT

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            main()