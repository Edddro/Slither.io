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
RED_TRANSPARENT = (235, 64, 52, 127)
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
        for _ in range(1000):
            self.spawn_food()

    def spawn_food(self):
        self.x = random.randint(-WIDTH, WIDTH * 2)
        self.y = random.randint(-HEIGHT, HEIGHT * 2)
        self.foods.append([self.x, self.y])
        self.foods_move.append([0, 0])
        self.colours.append(random.choice(FOOD_COLOR))

    def speed_food(self, x, y):
        self.speed_foods.append([x, y])
        self.speed_foods_move.append([0, 0])

    def snake_to_food(self, snake):
        for segment in snake:
            self.snake_foods.append(segment)
            self.snake_foods_move.append([0, 0])

    def move(self, dx, dy):
        for i in range(len(self.foods)):
            velocity_x = -1.5 * dx
            velocity_y = -1.5 * dy

            self.foods_move[i][0] += (velocity_x - self.foods_move[i][0]) * 0.01
            self.foods_move[i][1] += (velocity_y - self.foods_move[i][1]) * 0.01
            self.foods[i][0] += self.foods_move[i][0]
            self.foods[i][1] += self.foods_move[i][1]

        for i in range(len(self.snake_foods)):
            velocity_x = -1.5 * dx
            velocity_y = -1.5 * dy

            self.snake_foods_move[i][0] += (velocity_x - self.snake_foods_move[i][0]) * 0.01
            self.snake_foods_move[i][1] += (velocity_y - self.snake_foods_move[i][1]) * 0.01
            self.snake_foods[i][0] += self.snake_foods_move[i][0]
            self.snake_foods[i][1] += self.snake_foods_move[i][1]

        for i in range(len(self.speed_foods)):
            velocity_x = -1.5 * dx
            velocity_y = -1.5 * dy

            self.speed_foods_move[i][0] += (velocity_x - self.speed_foods_move[i][0]) * 0.01
            self.speed_foods_move[i][1] += (velocity_y - self.speed_foods_move[i][1]) * 0.01
            self.speed_foods[i][0] += self.speed_foods_move[i][0]
            self.speed_foods[i][1] += self.speed_foods_move[i][1]

    def update(self, x, y):
        for i in range(len(self.foods)):
            if self.foods[i] == [x, y]:
                self.foods.pop(i)
                self.colours.pop(i)
                self.foods_move.pop(i)
                break
        while len(self.foods) < 1000:
            self.spawn_food()

    def draw(self, food_type, snake_colour):
        if food_type == 'speed':
            for food in self.speed_foods:
                pygame.draw.circle(screen, snake_colour, food, 3)
        elif food_type == 'snake':
            for food in self.snake_foods:
                pygame.draw.circle(screen, random.choice(FOOD_COLOR), food, 8)
        else:
            for i in range(len(self.foods)):
                pygame.draw.circle(screen, self.colours[i], self.foods[i], 5)

class Snake:
    def __init__(self, snake_colour):
        self.snake = []
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.snake.append([self.x, self.y])
        self.snake_colour = snake_colour

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

    def shrink(self, food):
        food.speed_foods.append([self.snake[-1][0], self.snake[-1][1]])
        food.speed_foods_move.append([0, 0])
        self.snake.pop()

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

def speed_eaten(snake, food):
    head_x, head_y = snake.snake[0]
    for i in range(len(food.speed_foods)):
        food_x, food_y = food.speed_foods[i]
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

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

radius = 10
speed = False
length = 10
high_score = 0
background_x = 0
background_y = 0
snake_width = random.randint(-WIDTH + 50, WIDTH * 2 -50)
snake_height = random.randint(-HEIGHT + 50, HEIGHT * 2 -50)
snake_colour = random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])
food = Food()
snake = Snake(snake_colour)
run = True

while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if length > 15:
                    speed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                speed = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x < WIDTH / 2:
        background_x += 2.5 if speed else 1.5
        snake_width -= 2 if speed else 1
    if mouse_x > WIDTH / 2:
        background_x -= 2.5 if speed else 1.5
        snake_width += 2 if speed else 1
    if mouse_y < HEIGHT / 2:
        background_y += 2.5 if speed else 1.5
        snake_height -= 2 if speed else 1
    if mouse_y > HEIGHT / 2:
        background_y -= 2.5 if speed else 1.5
        snake_height += 2 if speed else 1

    screen.fill(BLACK)

    for i in range(-1, 2):
        for j in range(-1, 2):
            screen.blit(background, (background_x + i * WIDTH, background_y + j * HEIGHT))

    if speed:
        length -= 2
        snake.shrink(food)
        if length <= 15:
            speed = False

    food.draw("normal", snake_colour)
    food.draw("speed", snake_colour)
    snake.move()
    snake.draw(radius, speed)
    food.move(snake.dx, snake.dy)
    map()


    def draw_rect_alpha(surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)

    if snake_width < -WIDTH:
        draw_rect_alpha(screen, RED_TRANSPARENT, (0, 0, 20 + (abs(snake_width) - WIDTH), HEIGHT))
        pygame.draw.rect(screen, RED, (20 + (abs(snake_width) - WIDTH), 0, 2, HEIGHT))

    if snake_width > WIDTH * 2:
        draw_rect_alpha(screen, RED_TRANSPARENT, (WIDTH - 20 - (abs(snake_width) - WIDTH * 2), 0, 20 + (abs(snake_width) - WIDTH * 2), HEIGHT))
        pygame.draw.rect(screen, RED, (WIDTH - 20 - (abs(snake_width) - WIDTH * 2), 0, 2, HEIGHT))

    if snake_height < -HEIGHT:
        draw_rect_alpha(screen, RED_TRANSPARENT, (0, 0, WIDTH, 20 + (abs(snake_height) - HEIGHT)))
        pygame.draw.rect(screen, RED, (0, 20 + (abs(snake_height) - HEIGHT), WIDTH, 2))

    if snake_height > HEIGHT * 2:
        draw_rect_alpha(screen, RED_TRANSPARENT, (0, HEIGHT - 20 - (abs(snake_height) - HEIGHT * 2), WIDTH, 20 + (abs(snake_height) - HEIGHT * 2)))
        pygame.draw.rect(screen, RED, (0, HEIGHT - 20 - (abs(snake_height) - HEIGHT * 2), WIDTH, 2))

    food_index = food_eaten(snake, food)
    if food_index != -1:
        snake.grow()
        food.update(food.foods[food_index][0], food.foods[food_index][1])
        length += 2

    speed_index = speed_eaten(snake, food)
    if speed_index != -1:
        food.speed_foods.pop(speed_index)
        length += 1
        if length % 2 == 0:
            snake.grow()

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