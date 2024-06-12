import pygame
import sys
import math
import random

# Initialization
pygame.init()
clock = pygame.time.Clock()
WIDTH, HEIGHT = 700, 600
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
BLACK = (0, 0, 0)

FOOD_COLOR = [LIGHT_GREEN, DARK_GREEN, LIGHT_RED, LIGHT_BLUE, YELLOW, LIGHT_PURPLE, LIGHT_PINK, PINK, ORANGE]
background = pygame.transform.scale(pygame.image.load("./Graphics/background.png").convert_alpha(), (WIDTH, HEIGHT))

class Food(pygame.sprite.Sprite):
    def __init__(self):
        self.foods = []
        self.speed_foods = []
        self.snake_foods = []
        self.colours = []
        for _ in range(50):
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.foods.append([self.x, self.y])
            self.colours.append(random.choice(FOOD_COLOR))

    def speed_food(self, x, y):
        self.speed_foods.append([x, y])

    def snake_to_food(self, snake):
        for segment in snake:
            self.snake_foods.append([segment])

    def move(self):
        self.foods_move = []
        self.snake_foods_move = []
        self.speed_foods_move = []
        for pos in self.foods:
            self.foods_move.append((pygame.mouse.get_pos() - pygame.math.Vector2(pos)))
        for i in range(len(self.foods_move)):
            self.foods[i] += self.foods_move[i] * -0.01

            if self.foods[i][0] < 0 or self.foods[i][0] > WIDTH or self.foods[i][1] < 0 or self.foods[i][1] > HEIGHT:
                self.update(self.foods[i][0], self.foods[i][1])
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
                break
        while len(self.foods) < 50:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.foods.append([self.x, self.y])
            self.colours.append(random.choice(FOOD_COLOR))

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
        dx = 8 * math.cos(angle)
        dy = 8 * math.sin(angle)

        new_head = [head_x + dx, head_y + dy]
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

        pygame.draw.circle(screen, BLACK,
                           (int(x_eye_left + 2 * math.cos(angle)), int(y_eye_left + 2 * math.sin(angle))), 2)
        pygame.draw.circle(screen, BLACK,
                           (int(x_eye_right + 2 * math.cos(angle)), int(y_eye_right + 2 * math.sin(angle))), 2)

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
                color = (
                min(int(self.snake_colour[0] * shade_factor), 255), min(int(self.snake_colour[1] * shade_factor), 255),
                min(int(self.snake_colour[2] * shade_factor), 255))
            else:
                color = (int(self.snake_colour[0] * shade_factor), int(self.snake_colour[1] * shade_factor),
                         int(self.snake_colour[2] * shade_factor))
            pygame.draw.circle(screen, color, (int(segment[0]), int(segment[1])), radius)
        self.eyes(radius)

def check_collision(snake, food):
    head_x, head_y = snake.snake[0]
    for i in range(len(food.foods)):
        food_x, food_y = food.foods[i]
        if math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2) < 15:
            return i
    return -1

# Main game loop
mouse_x, mouse_y = pygame.mouse.get_pos()
radius = 10
speed = False
score = 0
high_score = 0
food = Food()
snake = Snake()
background_x = 0
background_y = 0
run = True

while run:
    clock.tick(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x < WIDTH / 2:
        background_x -= 3
    if mouse_x > WIDTH / 2:
        background_x += 3
    if mouse_y < HEIGHT / 2:
        background_y -= 3
    if mouse_y > HEIGHT / 2:
        background_y += 3

    screen.fill(BLACK)
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            screen.blit(background, (background_x + i * WIDTH, background_y + j * HEIGHT))

    food.draw("normal")
    snake.move()
    snake.draw(radius, speed)
    food.move()

    # Check collision with food
    food_index = check_collision(snake, food)
    if food_index != -1:
        snake.grow()
        food.update(food.foods[food_index][0], food.foods[food_index][1])
        score += 10

    pygame.display.update()

    # Reset background position to create an infinite scrolling effect
    if background_x <= -WIDTH:
        background_x = 0
    if background_x >= WIDTH:
        background_x = 0
    if background_y <= -HEIGHT:
        background_y = 0
    if background_y >= HEIGHT:
        background_y = 0