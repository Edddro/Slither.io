import pygame
import sys
import math
import random

# Initialization
pygame.init()
clock = pygame.time.Clock()
WIDTH = 700
HEIGHT = 600
pygame.display.set_caption('Slither.io')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
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
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

FOOD_COLOR = [LIGHT_GREEN, DARK_GREEN, LIGHT_RED, LIGHT_BLUE, YELLOW, LIGHT_PURPLE, LIGHT_PINK, PINK, ORANGE]
background = pygame.transform.scale(pygame.image.load("./Graphics/background.png").convert_alpha(), (WIDTH, HEIGHT))

class Food(pygame.sprite.Sprite):
    def __init__(self):
        self.foods = []
        self.speed_foods = []
        self.snake_foods = []
        self.colours = []
        self.foods_move = []
        self.snake_foods_move = []
        self.speed_foods_move = []
        for _ in range(500):
            self.x = random.randint(-WIDTH, WIDTH * 2)
            self.y = random.randint(-HEIGHT, HEIGHT * 2)
            self.foods.append([self.x, self.y])
            self.foods_move.append([0, 0])
            self.colours.append(random.choice(FOOD_COLOR))

    def speed_food(self, x, y):
        self.speed_foods.append([x, y])

    def snake_to_food(self, snake):
        for segment in snake:
            self.snake_foods.append([segment])

    def move(self, snake_dx, snake_dy):
        for i in range(len(self.foods)):
            velocity_x = -1.5 * snake.dx
            velocity_y = -1.5 * snake.dy

            self.foods_move[i][0] += (velocity_x - self.foods_move[i][0]) * 0.01
            self.foods_move[i][1] += (velocity_y - self.foods_move[i][1]) * 0.01
            self.foods[i][0] += self.foods_move[i][0]
            self.foods[i][1] += self.foods_move[i][1]

            # if self.foods[i][0] > WIDTH or self.foods[i][0] < 0 or self.foods[i][1] > 0 or self.foods[i][1] > HEIGHT:
            #     self.update(self.foods[i][0], self.foods[i][1])

        for pos in self.snake_foods:
            self.snake_foods_move((pygame.mouse.get_pos() - pygame.math.Vector2(pos)))
        for i in range(len(self.snake_foods_move)):
            self.snake_foods[i] += self.snake_foods_move[i] * -0.01
        for pos in self.speed_foods:
            self.speed_foods_move((pygame.mouse.get_pos() - pygame.math.Vector2(pos)))
        for i in range(len(self.speed_foods_move)):
            self.speed_foods[i] += self.speed_foods_move[i] * -0.01

    def update(self, x, y):
        for i in range(len(self.foods)):
            if self.foods[i] == [x, y]:
                self.foods.pop(i)
                self.colours.pop(i)
                self.foods_move.pop(i)
                break
        while len(self.foods) < 500:
            self.x = random.randint(-WIDTH, WIDTH * 2)
            self.y = random.randint(-HEIGHT, HEIGHT * 2)
            self.foods.append([self.x, self.y])
            self.colours.append(random.choice(FOOD_COLOR))
            self.foods_move.append([0, 0])

    def draw(self, food_type):
        if food_type == 'speed':
            for food in self.speed_foods:
                pygame.draw.circle(screen, random.choice(FOOD_COLOR), food, 3)
        elif food_type == 'snake':
            for food in self.snake_foods:
                pygame.draw.circle(screen, random.choice(FOOD_COLOR), food, 8)
        else:
            for i in range(len(self.foods)):
                pygame.draw.circle(screen, self.colours[i], self.foods[i], 5)

class Snake:
    def __init__(self):
        self.snake = []
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.snake.append([self.x, self.y])
        self.snake_colour = random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])

        for i in range(1, 11):
            self.snake.append([self.x, self.y + (8 * i)])

    def move(self):
        head_x, head_y = self.snake[0]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - HEIGHT // 2, mouse_x - WIDTH // 2)
        self.dx = 8 * math.cos(angle)
        self.dy = 8 * math.sin(angle)

        new_head = [head_x + self.dx, head_y + self.dy]
        self.snake = [new_head] + self.snake[:-1]

        offset_x = WIDTH // 2 - head_x
        offset_y = HEIGHT // 2 - head_y
        for i in range(len(self.snake)):
            self.snake[i][0] += offset_x
            self.snake[i][1] += offset_y

    def grow(self):
        tail_x, tail_y = self.snake[-1]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - HEIGHT // 2, mouse_x - WIDTH // 2)
        dx = 8 * math.cos(angle)
        dy = 8 * math.sin(angle)

        new_segment = [tail_x - dx, tail_y - dy]
        self.snake.append(new_segment)

    def eyes(self, radius):
        head_x, head_y = self.snake[0]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - HEIGHT // 2, mouse_x - WIDTH // 2)
        distance = radius / 1.5

        x_eye_left = head_x + distance * math.cos(angle - math.pi / 6)
        y_eye_left = head_y + distance * math.sin(angle - math.pi / 6)
        x_eye_right = head_x + distance * math.cos(angle + math.pi / 6)
        y_eye_right = head_y + distance * math.sin(angle + math.pi / 6)

        pygame.draw.circle(screen, WHITE, (int(x_eye_left), int(y_eye_left)), 4)
        pygame.draw.circle(screen, WHITE, (int(x_eye_right), int(y_eye_right)), 4)

        pygame.draw.circle(screen, BLACK, (int(x_eye_left + 2 * math.cos(angle)), int(y_eye_left + 2 * math.sin(angle))), 2)
        pygame.draw.circle(screen, BLACK, (int(x_eye_right + 2 * math.cos(angle)), int(y_eye_right + 2 * math.sin(angle))), 2)

    def draw(self, radius, speed):
        for i, segment in enumerate(self.snake):
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
        self.eyes(radius)

def food_eaten(snake, food):
    head_x, head_y = snake.snake[0]
    for i in range(len(food.foods)):
        food_x, food_y = food.foods[i]
        if math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2) < 15:
            return i
    return -1

def map():
    map_rect = pygame.Rect(WIDTH - 150, HEIGHT - 150, 100, 100)
    pygame.draw.rect(screen, GRAY, map_rect, 1)
    map_x = (snake_width + WIDTH) / (WIDTH * 2) * 100 + map_rect.left
    map_y = (snake_height + HEIGHT) / (HEIGHT * 2) * 100 + map_rect.top
    map_x = max(map_rect.left + 5, min(map_rect.right - 15, map_x))
    map_y = max(map_rect.top + 5, min(map_rect.bottom - 15, map_y))
    pygame.draw.circle(screen, WHITE, (int(map_x), int(map_y)), 5)

radius = 10
speed = False
length = 10
high_score = 0
food = Food()
snake = Snake()
background_x = 0
background_y = 0
snake_width = 0
snake_height = 0
run = True

while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x < WIDTH / 2:
        background_x += 1.5
        snake_width -= 1
    if mouse_x > WIDTH / 2:
        background_x -= 1.5
        snake_width += 1
    if mouse_y < HEIGHT / 2:
        background_y += 1.5
        snake_height -= 1
    if mouse_y > HEIGHT / 2:
        background_y -= 1.5
        snake_height += 1

    screen.fill(BLACK)

    for i in range(-1, 2):
        for j in range(-1, 2):
            screen.blit(background, (background_x + i * WIDTH, background_y + j * HEIGHT))

    food.draw("normal")
    snake.move()
    snake.draw(radius, speed)
    food.move(snake.dx, snake.dy)
    map()

    if snake_width < -WIDTH:
        pygame.draw.rect(screen, RED, (0, 0, 20 + (abs(snake_width) - WIDTH), HEIGHT))
    if snake_width > WIDTH * 2:
        pygame.draw.rect(screen, RED, (WIDTH - 20 - (abs(snake_width) - WIDTH * 2), 0, 20 + (abs(snake_width) - WIDTH * 2), HEIGHT))
    if snake_height < -HEIGHT:
        pygame.draw.rect(screen, RED, (0, 0, WIDTH, 20 + (abs(snake_height) - HEIGHT)))
    if snake_height > HEIGHT * 2:
        pygame.draw.rect(screen, RED, (0, HEIGHT - 20 - (abs(snake_height) - HEIGHT * 2), WIDTH, 20 + (abs(snake_height) - HEIGHT * 2)))

    food_index = food_eaten(snake, food)
    if food_index != -1:
        snake.grow()
        food.update(food.foods[food_index][0], food.foods[food_index][1])
        length += 2
        if length != 10 and length % 800 == 0:
            radius += 1.2

    pygame.display.update()

    if background_x <= -WIDTH:
        background_x = 0
    if background_x >= WIDTH:
        background_x = 0
    if background_y <= -HEIGHT:
        background_y = 0
    if background_y >= HEIGHT:
        background_y = 0