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

WIDTH = 1000
HEIGHT = 480

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

    def shrink(self, x, y):
        food = Food()
        food.speed_foods(x, y)
        self.snake.remove([x, y])

    def eyes(self, radius, target_x=0, target_y=5):
        head_x, head_y = self.snake[0]
        distance = radius / 8
        direction = pygame.math.Vector2(target_x - head_x, target_y - head_y).normalize() * 2

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

    def draw(self, radius):
        for i, segment in enumerate(reversed(self.snake)):
            if (i // 3) % 2 == 0:
                shade_factor = 1 - (i / (len(self.snake) * 3.5))
            else:
                shade_factor = 1
            color = (int(self.snake_colour[0] * shade_factor), int(self.snake_colour[1] * shade_factor), int(self.snake_colour[2] * shade_factor))
            pygame.draw.circle(screen, color, (int(segment[0]), int(segment[1])), radius)
        self.eyes(radius)
def hexagon(x, y, radius):
    inner_points = []
    outer_points = []
    for i in range(6):
        angle = math.pi / 2 + math.pi / 3 * i
        hexagon_x = x + radius * math.cos(angle)
        hexagon_y = y + radius * math.sin(angle)
        hexagon_outer_x = x + (radius * 1.15) * math.cos(angle)
        hexagon_outer_y = y + (radius * 1.15) * math.sin(angle)
        inner_points.append((hexagon_x, hexagon_y))
        outer_points.append((hexagon_outer_x, hexagon_outer_y))
    pygame.draw.polygon(screen, BLACK, outer_points)
    pygame.draw.polygon(screen, DARK_GRAY, inner_points)

def background(height_offset, width_offset):
    screen.fill(LIGHT_BLACK)
    radius = 17.5
    hexagon_width = 0
    for y in range(-HEIGHT + height_offset, HEIGHT + 35, 40):
        hexagon_height = 0
        for x in range(-WIDTH + width_offset, WIDTH + 35, 40):
            hexagon(x - hexagon_width, y + hexagon_height, radius)

            hexagon_height += radius * math.sin(math.pi / 10)
        hexagon_width -= 25 * math.cos(math.pi / 3)

def main():
    radius = 10
    height_offset = 0
    width_offset = 0
    score = 0
    high_score = 0
    if score != 0 and score % 800 == 0:
        radius += 2
    background(height_offset, width_offset)
    food = Food()
    food.draw("normal")
    snake = Snake()
    snake.draw(radius)

main()
run = True
while run:
    #main()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            main()