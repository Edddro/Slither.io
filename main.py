'''
Author: Edward Drobnis
Date: June 14, 2024
Title: Main
Description:
'''
import pygame
import sys
import math
import random

pygame.init()
clock = pygame.time.Clock()
WIDTH = 700
HEIGHT = 600
pygame.display.set_caption('Slither.io')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

LIGHT_GREEN = (57, 255, 20)
GREEN = (162, 209, 73)
DARK_GREEN = (154, 203, 65)
LIGHT_RED = (255, 7, 58)
RED = (235, 64, 52)
RED_TRANSPARENT = (235, 64, 52, 200)
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
GRAY_TRANSPARENT = (128, 128, 128, 200)
BLACK = (0, 0, 0)

FOOD_COLOR = [LIGHT_GREEN, DARK_GREEN, LIGHT_RED, LIGHT_BLUE, YELLOW, LIGHT_PURPLE, LIGHT_PINK, PINK, ORANGE]
background = pygame.transform.scale(pygame.image.load("./Graphics/background.png").convert_alpha(), (WIDTH, HEIGHT))
menu_background = pygame.transform.scale(pygame.image.load("./Graphics/menu.png").convert_alpha(), (WIDTH, HEIGHT))
play_button = pygame.image.load("./Graphics/play.png").convert_alpha()
skin_button = pygame.image.load("./Graphics/skin.png").convert_alpha()
save_button = pygame.image.load("./Graphics/save.png").convert_alpha()

menu_font = pygame.font.Font(None, 28)
score_font = pygame.font.Font(None, 24)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        self.foods = []
        self.speed_foods = []
        self.snake_foods = []
        self.colours = []
        self.snake_foods_colour = []
        self.foods_move = []
        self.snake_foods_move = []
        self.speed_foods_move = []
        for _ in range(500):
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
            self.snake_foods_colour.append(random.choice(FOOD_COLOR))
            self.snake_foods_move.append([0, 0])

    def move(self, dx, dy, speed):
        if speed:
            movement = 0.1
        else:
            movement = 0.01
        for i in range(len(self.foods)):
            velocity_x = -1.5 * dx
            velocity_y = -1.5 * dy

            self.foods_move[i][0] += (velocity_x - self.foods_move[i][0]) * movement
            self.foods_move[i][1] += (velocity_y - self.foods_move[i][1]) * movement
            self.foods[i][0] += self.foods_move[i][0]
            self.foods[i][1] += self.foods_move[i][1]

        for i in range(len(self.snake_foods)):
            velocity_x = -1.5 * dx
            velocity_y = -1.5 * dy

            self.snake_foods_move[i][0] += (velocity_x - self.snake_foods_move[i][0]) * movement
            self.snake_foods_move[i][1] += (velocity_y - self.snake_foods_move[i][1]) * movement
            self.snake_foods[i][0] += self.snake_foods_move[i][0]
            self.snake_foods[i][1] += self.snake_foods_move[i][1]

        for i in range(len(self.speed_foods)):
            velocity_x = -1.5 * dx
            velocity_y = -1.5 * dy

            self.speed_foods_move[i][0] += (velocity_x - self.speed_foods_move[i][0]) * movement
            self.speed_foods_move[i][1] += (velocity_y - self.speed_foods_move[i][1]) * movement
            self.speed_foods[i][0] += self.speed_foods_move[i][0]
            self.speed_foods[i][1] += self.speed_foods_move[i][1]

    def update(self, x, y):
        for i in range(len(self.foods)):
            if self.foods[i] == [x, y]:
                self.foods.pop(i)
                self.colours.pop(i)
                self.foods_move.pop(i)
                break
        while len(self.foods) < 500:
            self.spawn_food()

    def draw(self, food_type, snake_colour):
        if food_type == 'speed':
            for food in self.speed_foods:
                pygame.draw.circle(screen, snake_colour, food, 3)
        elif food_type == 'snake':
            for i in range(len(self.snake_foods)):
                pygame.draw.circle(screen, self.snake_foods_colour[i], self.snake_foods[i], 8)
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
        self.speed = 3

        for i in range(1, 11):
            self.snake.append([self.x, self.y + (8 * i)])

    def update_colour(self, snake_colour):
        self.snake_colour = snake_colour

    def move(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle_to_mouse = math.atan2(mouse_y - HEIGHT // 2, mouse_x - WIDTH // 2)
        self.dx = self.speed * math.cos(angle_to_mouse)
        self.dy = self.speed * math.sin(angle_to_mouse)

        new_head = [self.snake[0][0] + self.dx, self.snake[0][1] + self.dy]

        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = list(self.snake[i - 1])
        self.snake[0] = new_head

        offset_x = WIDTH // 2 - new_head[0]
        offset_y = HEIGHT // 2 - new_head[1]
        for i in range(len(self.snake)):
            self.snake[i][0] += offset_x
            self.snake[i][1] += offset_y

    def grow(self):
        tail_x, tail_y = self.snake[-1]
        new_segment = [tail_x, tail_y]
        self.snake.append(new_segment)

    def shrink(self, food):
        food.speed_foods.append([self.snake[-1][0], self.snake[-1][1]])
        food.speed_foods_move.append([0, 0])
        self.snake.pop()

    def eyes(self, radius):
        head_x, head_y = self.snake[0]
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - head_y, mouse_x - head_x)
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
                    shade_factor = 1 + (i / (len(self.snake) * 5))
                else:
                    shade_factor = 1 - (i / (len(self.snake) * 3.5))
            else:
                shade_factor = 1
            if speed:
                colour = (min(int(self.snake_colour[0] * shade_factor), 255), min(int(self.snake_colour[1] * shade_factor), 255), min(int(self.snake_colour[2] * shade_factor), 255))
            else:
                colour = (int(self.snake_colour[0] * shade_factor), int(self.snake_colour[1] * shade_factor), int(self.snake_colour[2] * shade_factor))
            pygame.draw.circle(screen, colour, (int(segment[0]), int(segment[1])), radius)
        self.eyes(radius)

class BotSnake:
    def __init__(self, snake_colour):
        self.snake_colour = snake_colour
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.speed = 5
        self.snake = []
        self.dx = 0
        self.dy = 0
        self.spawn_bot()

    def spawn_bot(self):
        while True:
            x = random.randint(100, WIDTH - 100)
            y = random.randint(100, HEIGHT - 100)
            potential_position = [x, y]
            if all(math.sqrt((segment[0] - x) ** 2 + (segment[1] - y) ** 2) >= 10 for segment in self.snake):
                self.snake = [potential_position]
                for _ in range(9):
                    self.snake.append([self.snake[-1][0] - self.dx, self.snake[-1][1] - self.dy])
                break

    def move(self):
        if random.randint(0, 100) < 5:
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

        if self.direction == 'UP':
            self.dy = -self.speed
            self.dx = 0
        elif self.direction == 'DOWN':
            self.dy = self.speed
            self.dx = 0
        elif self.direction == 'LEFT':
            self.dx = -self.speed
            self.dy = 0
        elif self.direction == 'RIGHT':
            self.dx = self.speed
            self.dy = 0

        new_head = [self.snake[0][0] + self.dx, self.snake[0][1] + self.dy]

        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = list(self.snake[i - 1])
        self.snake[0] = new_head

    def draw_eyes(self, radius):
        head_x, head_y = self.snake[0]
        angle = math.atan2(self.dy, self.dx)
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

    def draw(self, radius):
        for i, segment in enumerate(self.snake):
            if i == 0:
                pygame.draw.circle(screen, WHITE, (int(segment[0] - radius // 2), int(segment[1] - radius // 2)), radius // 5)
                pygame.draw.circle(screen, WHITE, (int(segment[0] + radius // 2), int(segment[1] - radius // 2)), radius // 5)
            if (i // 3) % 2 == 0:
                shade_factor = 1 - (i / (len(self.snake) * 3.5))
            else:
                shade_factor = 1
            colour = (int(self.snake_colour[0] * shade_factor), int(self.snake_colour[1] * shade_factor), int(self.snake_colour[2] * shade_factor))
            pygame.draw.circle(screen, colour, (int(segment[0]), int(segment[1])), radius)
        self.draw_eyes(radius)

    def speed_up(self):
        if len(self.snake) > 15:
            self.snake.pop()

    def grow(self):
        tail_x, tail_y = self.snake[-1]
        new_segment = [tail_x, tail_y]
        self.snake.append(new_segment)

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

def snake_eaten(snake, food):
    head_x, head_y = snake.snake[0]
    for i in range(len(food.snake_foods)):
        food_x, food_y = food.snake_foods[i]
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

def draw_rect_alpha(surface, colour, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, colour, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, colour, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, colour, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def count(food):
    food_count = len(food.foods)
    for i in range(len(food.foods)):
        if food.foods[i][0] < -WIDTH or food.foods[i][0] > WIDTH * 2 or food.foods[i][1] < -HEIGHT or food.foods[i][1] > HEIGHT * 2:
            food_count -= 1

    while food_count < 45:
        food.spawn_food()
        food_count += 1

def check_collision(snake1, snake2):
    for segment in snake2.snake:
        if math.sqrt((snake1.snake[0][0] - segment[0]) ** 2 + (snake1.snake[0][1] - segment[1]) ** 2) < 10:
            return True
    return False

def handle_collision(user_snake, bots, food):
    for bot in bots:
        if check_collision(user_snake, bot):
            food.snake_to_food(user_snake.snake)
            return True
        if check_collision(bot, user_snake):
            food.snake_to_food(bot.snake)
            bots.remove(bot)
    return False

def menu(length, highest_length, first_game):
    screen.fill(BLACK)
    screen.blit(menu_background, (0, 0))

    if not first_game:
        score_text = menu_font.render(f"Your final length was {length}!", True, WHITE)
        score_text_width = score_text.get_width()
        score_text_x = (WIDTH - score_text_width) // 2
        score_text_y = HEIGHT // 4 * 1.75
        screen.blit(score_text, (score_text_x, score_text_y))

        highest_new_score = score_font.render("This is your best score so far!", True, WHITE)
        highest_score_text = score_font.render(f"Your best length ever was {highest_length}", True, WHITE)

        if length > highest_length:
            screen.blit(highest_new_score, (WIDTH / 2 - highest_new_score.get_width() // 2, HEIGHT // 4 * 2))
        else:
            screen.blit(highest_score_text, (WIDTH / 2 - highest_score_text.get_width() // 2, HEIGHT // 4 * 2))

    play_button_rect = play_button.get_rect(center=(WIDTH / 2, HEIGHT / 4 * 2.45))
    skin_button_rect = skin_button.get_rect(center=(WIDTH / 2, HEIGHT / 4 * 3.25))

    screen.blit(play_button, play_button_rect.topleft)
    screen.blit(skin_button, skin_button_rect.topleft)

    return play_button_rect, skin_button_rect, highest_length

    play_button_rect = play_button.get_rect(center=(WIDTH / 2, HEIGHT / 4 * 2.45))
    skin_button_rect = skin_button.get_rect(center=(WIDTH / 2, HEIGHT / 4 * 3.25))
    score_text_width = score_text.get_width()
    highest_score_text_width = highest_score_text.get_width()
    score_text_x = (WIDTH - score_text_width) // 2
    highest_score_text_x = (WIDTH - highest_score_text_width) // 2
    score_text_y = HEIGHT // 4 * 1.75
    highest_score_text_y = HEIGHT // 4 * 2

    screen.blit(play_button, play_button_rect.topleft)
    screen.blit(skin_button, skin_button_rect.topleft)
    screen.blit(score_text, (score_text_x, score_text_y))

    if length > highest_length:
        screen.blit(highest_new_score, (highest_score_text_x, highest_score_text_y))
        highest_length = length
    else:
        screen.blit(highest_score_text, (highest_score_text_x, highest_score_text_y))

    return play_button_rect, skin_button_rect, highest_length, length

def skin(preview_index):
    screen.fill(BLACK)
    preview_colours = [None, GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK]
    preview_snake = []
    for i in range(1, 11):
        preview_snake.append([WIDTH / 12 * 7 - (8 * i), HEIGHT / 2])

    for i, segment in enumerate(reversed(preview_snake)):
        if (i // 3) % 2 == 0:
            shade_factor = 1 - (i / (len(preview_snake) * 3.5))
        else:
            shade_factor = 1
        if preview_colours[preview_index] == None:
            draw_circle_alpha(screen, GRAY_TRANSPARENT, (int(segment[0]), int(segment[1])), 10)
        else:
            colour = (int(preview_colours[preview_index][0] * shade_factor), int(preview_colours[preview_index][1] * shade_factor), int(preview_colours[preview_index][2] * shade_factor))
            pygame.draw.circle(screen, colour, (int(segment[0]), int(segment[1])), 10)
    pygame.draw.circle(screen, WHITE, (preview_snake[0][0], preview_snake[0][1] + 2), 4)
    pygame.draw.circle(screen, WHITE, (preview_snake[0][0], preview_snake[0][1] - 2), 4)

    pygame.draw.circle(screen, BLACK, (preview_snake[0][0] + 2, preview_snake[0][1] + 2.5), 2)
    pygame.draw.circle(screen, BLACK, (preview_snake[0][0] + 2, preview_snake[0][1] - 2.5), 2)

    left_arrow_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 10, 20, 20)
    right_arrow_rect = pygame.Rect(WIDTH // 2 + 100, HEIGHT // 2 - 10, 20, 20)
    save_button_rect = save_button.get_rect(center=(WIDTH / 2, HEIGHT / 4 * 3 + 50))

    pygame.draw.polygon(screen, WHITE, [(left_arrow_rect.left + 10, left_arrow_rect.centery), (left_arrow_rect.right - 5, left_arrow_rect.top + 5), (left_arrow_rect.right - 5, left_arrow_rect.bottom - 5)])
    pygame.draw.polygon(screen, WHITE, [(right_arrow_rect.left + 5, right_arrow_rect.top + 5), (right_arrow_rect.right - 10, right_arrow_rect.centery), (right_arrow_rect.left + 5, right_arrow_rect.bottom - 5)])
    screen.blit(save_button, save_button_rect.topleft)

    return left_arrow_rect, right_arrow_rect, save_button_rect, preview_colours[preview_index]

radius = 10
speed = False
length = 10
speed_length = 0
highest_length = 0
background_x = 0
background_y = 0
snake_width = random.randint(-WIDTH + 100, WIDTH * 2 - 100)
snake_height = random.randint(-HEIGHT + 100, HEIGHT * 2 - 100)
preview_index = 0
food = Food()
snake_colour = random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])
snake = Snake(snake_colour)
num_bots = 15
bots = [BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])) for _ in range(num_bots)]
scene = "menu"
first_game = True
run = True

while run:
    clock.tick(30)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if length > 3:
                    speed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                speed = False
                speed_length = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if scene == "menu":
                if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    scene = "game"
                    if length > highest_length:
                        highest_length = length
                    length = 10
                if skin_button_rect.collidepoint(pygame.mouse.get_pos()):
                    scene = "skin"
            elif scene == "skin":
                if left_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    preview_index = (preview_index - 1) % 7
                elif right_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                    preview_index = (preview_index + 1) % 7
                elif save_button_rect.collidepoint(pygame.mouse.get_pos()):
                    scene = "menu"
                    if chosen_snake_colour != None:
                        snake_colour = chosen_snake_colour
                        snake.update_colour(snake_colour)

    if scene == "menu":
        play_button_rect, skin_button_rect, highest_length = menu(length, highest_length, first_game)
        snake_width = random.randint(-WIDTH + 100, WIDTH * 2 - 100)
        snake_height = random.randint(-HEIGHT + 100, HEIGHT * 2 - 100)
    elif scene == "skin":
        left_arrow_rect, right_arrow_rect, save_button_rect, chosen_snake_colour = skin(preview_index)
    elif scene == "game":
        first_game = False
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
            length -= 1
            speed_length += 1
            if speed_length % 2 == 0:
                snake.shrink(food)
            snake.speed = 4
            if length <= 30:
                speed = False

        food.draw("normal", snake_colour)
        food.draw("speed", snake_colour)
        food.draw("snake", snake_colour)
        snake.move()
        snake.draw(radius, speed)
        food.move(snake.dx, snake.dy, speed)
        map()
        count(food)
        length_text = score_font.render(f"Your length: {length}", True, WHITE)
        screen.blit(length_text, (WIDTH / 10 * 0.2, HEIGHT / 10 * 9.5))

        for bot in bots:
            bot.move()
            bot.draw(radius)

            food_index = food_eaten(bot, food)
            if food_index != -1:
                bot.grow()
                food.update(food.foods[food_index][0], food.foods[food_index][1])
                length += 2

            speed_index = speed_eaten(bot, food)
            if speed_index != -1:
                food.speed_foods.pop(speed_index)
                length += 1
                if length % 2 == 0:
                    bot.grow()

            snake_index = snake_eaten(bot, food)
            if snake_index != -1:
                food.snake_foods.pop(snake_index)
                food.snake_foods_colour.pop(snake_index)
                length += 4
                bot.grow()
                bot.grow()

            if handle_collision(bot, bots, food):
                pygame.display.update()
                bots.remove(bot)

        if handle_collision(snake, bots, food):
            pygame.display.update()
            pygame.time.delay(2000)
            scene = "menu"


        def draw_rect_alpha(surface, colour, rect):
            shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, colour, shape_surf.get_rect())
            surface.blit(shape_surf, rect)

        barriers = [-1, -1, -1, -1]
        if snake_width < -WIDTH:
            barriers[0] = (0, 0, 20 + (abs(snake_width) - WIDTH), HEIGHT)
            draw_rect_alpha(screen, RED_TRANSPARENT, (0, 0, 20 + (abs(snake_width) - WIDTH), HEIGHT))
            pygame.draw.rect(screen, RED, (20 + (abs(snake_width) - WIDTH), 0, 2, HEIGHT))

        if snake_width > WIDTH * 2:
            barriers[1] = (WIDTH - 20 - (abs(snake_width) - WIDTH * 2), 0, 20 + (abs(snake_width) - WIDTH * 2), HEIGHT)
            draw_rect_alpha(screen, RED_TRANSPARENT, (WIDTH - 20 - (abs(snake_width) - WIDTH * 2), 0, 20 + (abs(snake_width) - WIDTH * 2), HEIGHT))
            pygame.draw.rect(screen, RED, (WIDTH - 20 - (abs(snake_width) - WIDTH * 2), 0, 2, HEIGHT))

        if snake_height < -HEIGHT:
            barriers[2] = (0, 0, WIDTH, 20 + (abs(snake_height) - HEIGHT))
            draw_rect_alpha(screen, RED_TRANSPARENT, (0, 0, WIDTH, 20 + (abs(snake_height) - HEIGHT)))
            pygame.draw.rect(screen, RED, (0, 20 + (abs(snake_height) - HEIGHT), WIDTH, 2))

        if snake_height > HEIGHT * 2:
            barriers[3] = (0, HEIGHT - 20 - (abs(snake_height) - HEIGHT * 2), WIDTH, 20 + (abs(snake_height) - HEIGHT * 2))
            draw_rect_alpha(screen, RED_TRANSPARENT, (0, HEIGHT - 20 - (abs(snake_height) - HEIGHT * 2), WIDTH, 20 + (abs(snake_height) - HEIGHT * 2)))
            pygame.draw.rect(screen, RED, (0, HEIGHT - 20 - (abs(snake_height) - HEIGHT * 2), WIDTH, 2))

        snake_head_rect = pygame.Rect(snake.snake[0][0] - radius, snake.snake[0][1] - radius, radius * 2, radius * 2)
        for barrier in barriers:
            if barrier != -1:
                barrier_rect = pygame.Rect(barrier)
                if snake_head_rect.colliderect(barrier_rect):
                    food.snake_to_food(snake.snake)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    scene = "menu"
                else:
                    for bot in bots:
                        bot_head_rect = pygame.Rect(bot.snake[0][0] - radius, bot.snake[0][1] - radius, radius * 2, radius * 2)
                        if bot_head_rect.colliderect(barrier_rect):
                            food.snake_to_food(bot.snake)
                            bots.remove(bot)
                            break

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

        snake_index = snake_eaten(snake, food)
        if snake_index != -1:
            food.snake_foods.pop(snake_index)
            food.snake_foods_colour.pop(snake_index)
            length += 4
            snake.grow()
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