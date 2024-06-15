'''
Author: Edward Drobnis
Date: June 14, 2024
Title: Main
Description: Replication of Slither.io, a snake game, where you consume food and avoid colliding with others, with the goal of being the biggest in the game!
'''

# Imports pygame, system, math, and random
import pygame
import sys
import math
import random

# Initializes Pygame and clock
pygame.init()
clock = pygame.time.Clock()

# Sets the width and height to 700 by 600 (respectively)
WIDTH = 700
HEIGHT = 600
pygame.display.set_caption('Slither.io')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Defines the RGBs (or RGBAs) of colours
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

# Defines the options of food colour
FOOD_COLOUR = [LIGHT_GREEN, DARK_GREEN, LIGHT_RED, LIGHT_BLUE, YELLOW, LIGHT_PURPLE, LIGHT_PINK, PINK, ORANGE]

# Loads and resizes images
background = pygame.transform.scale(pygame.image.load("./Graphics/background.png").convert_alpha(), (WIDTH, HEIGHT))
menu_background = pygame.transform.scale(pygame.image.load("./Graphics/menu.png").convert_alpha(), (WIDTH, HEIGHT))
play_button = pygame.image.load("./Graphics/play.png").convert_alpha()
skin_button = pygame.image.load("./Graphics/skin.png").convert_alpha()
save_button = pygame.image.load("./Graphics/save.png").convert_alpha()

# Defines fonts
menu_font = pygame.font.Font(None, 28)
score_font = pygame.font.Font(None, 24)

# Creates a class, food, that manages all the foods in the game
class Food(pygame.sprite.Sprite):
    def __init__(self):
        '''
        Initializes the food class
        :return: Randomly generated food throughout the map
        '''
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
        '''
        Spawns food all over the map
        :return: Adds the position of the foods to self.foods
        '''
        self.x = random.randint(-WIDTH, WIDTH * 2)
        self.y = random.randint(-HEIGHT, HEIGHT * 2)
        self.foods.append([self.x, self.y])
        self.foods_move.append([0, 0])
        self.colours.append(random.choice(FOOD_COLOUR))

    def speed_food(self, x, y):
        '''
        Adds the positions of speed_foods to self.speed_foods
        :param x: The x position of the tail of the snake
        :param y: The y position of the tail of the snake
        :return: Adds the positions to self.speed_foods
        '''
        self.speed_foods.append([x, y])
        self.speed_foods_move.append([0, 0])

    def snake_to_food(self, snake):
        '''
        Converts each segment in a snake into food
        :param snake: A list of all the positions of each segment
        :return: Adds the position of each food to self.snake_foods
        '''
        for segment in snake:
            self.snake_foods.append(segment)
            self.snake_foods_colour.append(random.choice(FOOD_COLOUR))
            self.snake_foods_move.append([0, 0])

    def move(self, dx, dy, speed):
        '''
        Moves the food in the direction of the snake
        :param dx: The x direction the snake is heading
        :param dy: The y direction the snake is heading
        :param speed: The speed of the snake
        :return: Moves the food towards the snake
        '''
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
        '''
        Removes a food from self.foods and adds a new one
        :param x: The x value of the food
        :param y: The y value of the food
        :return: Removes the food and adds a new value to self.foods
        '''
        for i in range(len(self.foods)):
            if self.foods[i] == [x, y]:
                self.foods.pop(i)
                self.colours.pop(i)
                self.foods_move.pop(i)
                break
        while len(self.foods) < 500:
            self.spawn_food()

    def draw(self, food_type, snake_colour):
        '''
        Draws the food with the size depending on the type of food
        :param food_type: The type of food (speed, snake, normal)
        :param snake_colour: The colour of the snake
        :return: Draws the foods in the foods lists
        '''
        if food_type == 'speed':
            for food in self.speed_foods:
                pygame.draw.circle(screen, snake_colour, food, 3)
        elif food_type == 'snake':
            for i in range(len(self.snake_foods)):
                pygame.draw.circle(screen, self.snake_foods_colour[i], self.snake_foods[i], 8)
        else:
            for i in range(len(self.foods)):
                pygame.draw.circle(screen, self.colours[i], self.foods[i], 5)


# Creates a snake class
class Snake:
    def __init__(self, snake_colour):
        '''
        Initializes the snake class
        :param snake_colour: The colour of the snake
        '''
        self.snake = []
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.snake.append([self.x, self.y])
        self.snake_colour = snake_colour
        self.speed = 3

        for i in range(1, 11):
            self.snake.append([self.x, self.y + (8 * i)])

    def update_colour(self, snake_colour):
        '''
        Changes the colour of the snake
        :param snake_colour: The colour to change the snake to
        :return: Recolours the snake
        '''
        self.snake_colour = snake_colour

    def move(self):
        '''
        Moves each segment of the snake in the direction its heading
        :return: Returns a list with the updated positions
        '''
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
        '''
        Adds a new segment to the snake
        :return: Adds a new position to self.snake
        '''
        tail_x, tail_y = self.snake[-1]
        new_segment = [tail_x, tail_y]
        self.snake.append(new_segment)

    def shrink(self, food):
        '''
        Removes the last segment from the snake
        :param food: The position the speed food should be drawn in
        :return: Removes the last segment and adds its position to the speed_foods list in the foods class
        '''
        food.speed_foods.append([self.snake[-1][0], self.snake[-1][1]])
        food.speed_foods_move.append([0, 0])
        self.snake.pop()

    def eyes(self, radius):
        '''
        Draws the eyes of the snake
        :param radius: The radius of the snake
        :return: Positions the eyes in the direction of the cursor
        '''
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
        '''
        Draws the snake
        :param radius: The size of the snake
        :param speed: The speed of the snake
        :return: Draws each segment of the snake with shading
        '''
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

# Creates a BotSnake class for the bots
class BotSnake:
    def __init__(self, snake_colour):
        '''
        Initializes the bot class
        :param snake_colour: The colour of the snake
        '''
        self.snake_colour = snake_colour
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.speed = 2
        self.snake = []
        self.dx = 0
        self.dy = 0
        self.spawn_bot()

    def spawn_bot(self):
        '''
        Positions the bot around the screen and avoids placing it on the snake
        :return: A position for the bot
        '''
        while True:
            x = random.randint(100, WIDTH - 100)
            y = random.randint(100, HEIGHT - 100)
            potential_position = [x, y]
            if all(math.sqrt((segment[0] - x) ** 2 + (segment[1] - y) ** 2) >= 10 for segment in self.snake):
                self.snake = [potential_position]
                for _ in range(9):
                    self.snake.append([self.snake[-1][0] - self.dx, self.snake[-1][1] - self.dy])
                break

    def move_towards(self, target_x, target_y):
        '''
        Moves the snake towards food
        :param target_x: The x value of the food
        :param target_y: The y value of the food
        :return: Updates the positions of each segment in self.snake
        '''
        angle_to_target = math.atan2(target_y - self.snake[0][1], target_x - self.snake[0][0])
        self.dx = self.speed * math.cos(angle_to_target)
        self.dy = self.speed * math.sin(angle_to_target)
        new_head = [self.snake[0][0] + self.dx, self.snake[0][1] + self.dy]
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = list(self.snake[i - 1])
        self.snake[0] = new_head

    def seek_food(self, foods):
        '''
        Looks for the closet foods
        :param foods: The positions of all the foods
        :return: The closet foods to the snake
        '''
        closest_food = None
        closest_dist = float('inf')
        for food in foods:
            dist = math.sqrt((food[0] - self.snake[0][0]) ** 2 + (food[1] - self.snake[0][1]) ** 2)
            if dist < closest_dist:
                closest_dist = dist
                closest_food = food
        if closest_food:
            self.move_towards(closest_food[0], closest_food[1])

    def move(self, player_head, foods):
        '''
        Moves the snake
        :param player_head: The position of the head of the user's snake
        :param foods: The position of the foods
        :return:
        '''
        self.seek_food(foods)

    def draw_eyes(self, radius):
        '''
        Draws the eyes on the bots
        :param radius: The size of the snake
        :return: Draws eyes on the snakes
        '''
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
        '''
        Draws the bots
        :param radius:
        :return:
        '''
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
        '''
        Randomly speeds up the snake
        :return: Speeds up the snake randomly
        '''
        if len(self.snake) > 15:
            self.snake.pop()

    def grow(self):
        '''
        Grows the snake when it consumes food
        :return: A new position in self.snake
        '''
        tail_x, tail_y = self.snake[-1]
        new_segment = [tail_x, tail_y]
        self.snake.append(new_segment)

def food_eaten(snake, food):
    '''
    Checks if a normal food has been eaten
    :param snake: Checks the snake's head position
    :param food: Checks the position of each food
    :return: Either the index of the food or -1 if the head is not near any of the foods
    '''
    head_x, head_y = snake.snake[0]
    for i in range(len(food.foods)):
        food_x, food_y = food.foods[i]
        if math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2) < 15:
            return i
    return -1

def speed_eaten(snake, food):
    '''
    Checks if a speed food has been eaten
    :param snake: Checks the snake's head position
    :param food: Checks the position of each food
    :return: Either the index of the food or -1 if the head is not near any of the foods
    '''
    head_x, head_y = snake.snake[0]
    for i in range(len(food.speed_foods)):
        food_x, food_y = food.speed_foods[i]
        if math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2) < 15:
            return i
    return -1

def snake_eaten(snake, food):
    '''
    Checks if a snake food has been eaten
    :param snake: Checks the snake's head position
    :param food: Checks the position of each food
    :return: Either the index of the food or -1 if the head is not near any of the foods
    '''
    head_x, head_y = snake.snake[0]
    for i in range(len(food.snake_foods)):
        food_x, food_y = food.snake_foods[i]
        if math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2) < 15:
            return i
    return -1

def map():
    '''
    Draws a minimap, showing the position of the snake relative to the map
    :return: Shows the position of the snake on the map
    '''
    map_rect = pygame.Rect(WIDTH - 150, HEIGHT - 150, 100, 100)
    pygame.draw.rect(screen, GRAY, map_rect, 1)
    map_x = (snake_width + WIDTH) / (WIDTH * 2) * 100 + map_rect.left
    map_y = (snake_height + HEIGHT) / (HEIGHT * 2) * 100 + map_rect.top
    map_x = max(map_rect.left + 5, min(map_rect.right - 15, map_x))
    map_y = max(map_rect.top + 5, min(map_rect.bottom - 15, map_y))
    pygame.draw.circle(screen, WHITE, (int(map_x), int(map_y)), 5)

def draw_rect_alpha(surface, colour, rect):
    '''
    Draws a rectangle that is semi-transparent
    :param surface: Surface to draw the rectangle
    :param colour: Colour of the rectangle
    :param rect: Dimensions of the rectangle
    :return: Draws a semi-transparent rectangle
    '''
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, colour, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

def draw_circle_alpha(surface, colour, center, radius):
    '''
    Draws a semi-transparent circle
    :param surface: Surface to draw the circle
    :param colour: Colour of the circle
    :param center: Center of the circle
    :param radius: Radius of the circle
    :return: Draws a semi-transparent circle
    '''
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, colour, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def count(food):
    '''
    Counts the number of foods on the user's screen and adds more if there is very few
    :param food: The positions of all the foods
    :return: Draws more foods if the positions of the foods are offscreen
    '''
    food_count = len(food.foods)
    for i in range(len(food.foods)):
        if food.foods[i][0] < -WIDTH or food.foods[i][0] > WIDTH * 2 or food.foods[i][1] < -HEIGHT or food.foods[i][1] > HEIGHT * 2:
            food_count -= 1

    while food_count < 45:
        food.spawn_food()
        food_count += 1

def menu(length, highest_length, first_game):
    '''
    Draws the menu screen
    :param length: The length of the snake
    :param highest_length: The highest length of the snake
    :param first_game: Checks if it is the first game played
    :return: The menu screen with a play button and change skin button
    '''
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
    '''
    Displays a screen to change the skin of the snake
    :param preview_index: The index number of the colours
    :return: Shows a preview of the colour on the snake
    '''
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

# Variables to set up the game
length = 10
preview_index = 0
highest_length = 0
background_x = 0
background_y = 0
# Generates random coordinates of the snake on the map
snake_width = random.randint(-WIDTH + 100, WIDTH * 2 - 100)
snake_height = random.randint(-HEIGHT + 100, HEIGHT * 2 - 100)
# Generates a random snake colour
snake_colour = random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])
# Creates 10 bots all over the screen
num_bots = 10
bots = [BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])) for _ in range(num_bots)]
scene = "menu"
first_game = True
run = True

# Main game loop
while run:
    # Tries running the code
    try:
        # Limits the frames to 30 fps
        clock.tick(30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Checks if the length of the snake is over 30 and speeds it up if so
                    if length > 30:
                        speed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    # Stops speeding the snake
                    speed = False
                    speed_length = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if scene == "menu":
                    # Checks if the play button is clicked
                    # If so, it changes the screen to the game screen and sets the highest length if needed
                    # It also generates 10 positions for the bots
                    if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                        scene = "game"
                        if length > highest_length:
                            highest_length = length
                        length = 10
                        bots = [BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])) for _ in range(num_bots)]
                    # Checks if the change skin button is clicked
                    if skin_button_rect.collidepoint(pygame.mouse.get_pos()):
                        scene = "skin"
                elif scene == "skin":
                    # Checks if the left, right, or save button are clicked
                    if left_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                        preview_index = (preview_index - 1) % 7
                    elif right_arrow_rect.collidepoint(pygame.mouse.get_pos()):
                        preview_index = (preview_index + 1) % 7
                    elif save_button_rect.collidepoint(pygame.mouse.get_pos()):
                        scene = "menu"
                        # Checks if the user chose a colour
                        # If so, it sets the snake's colour to the chosen colour, otherwise, it chooses a colour for the snake
                        if chosen_snake_colour != None:
                            snake_colour = chosen_snake_colour
                            snake.update_colour(snake_colour)
                        else:
                            snake_colour = random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])

        # Changes the values of variables if the screen is the menu screen
        if scene == "menu":
            radius = 10
            speed = False
            speed_length = 0
            play_button_rect, skin_button_rect, highest_length = menu(length, highest_length, first_game)
            snake_width = random.randint(-WIDTH + 100, WIDTH * 2 - 100)
            snake_height = random.randint(-HEIGHT + 100, HEIGHT * 2 - 100)
            food = Food()
            snake = Snake(snake_colour)
        elif scene == "skin":
            left_arrow_rect, right_arrow_rect, save_button_rect, chosen_snake_colour = skin(preview_index)
        elif scene == "game":
            first_game = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Moves the background image and manages the snake's position on the screen
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

            # Creates a tile board on the screen so the background is infinite
            for i in range(-1, 2):
                for j in range(-1, 2):
                    screen.blit(background, (background_x + i * WIDTH, background_y + j * HEIGHT))

            # Checks if the snake is speeding
            # If so, it will decrease the length and produce speed foods
            if speed:
                length -= 1
                speed_length += 1
                if speed_length % 2 == 0:
                    snake.shrink(food)
                snake.speed = 4
                # Checks if the length is equal to or less than 30 and sets speed to false, if not already
                if length <= 30:
                    speed = False


            # Draws the food, snake, map, and text on the screen
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

            # Loops through all the bots
            for bot in bots:
                # Moves the bots and draws them
                bot.move(snake.snake[0], food.foods)
                bot.draw(radius)

                # Checks if the bot consumed a normal food and increases its length if so
                food_index = food_eaten(bot, food)
                if food_index != -1:
                    bot.grow()
                    food.update(food.foods[food_index][0], food.foods[food_index][1])

                # Checks if the bot consumed a speed food and increases its length if so
                speed_index = speed_eaten(bot, food)
                if speed_index != -1:
                    food.speed_foods.pop(speed_index)
                    bot.grow()

                # Checks if the bot consumed a snake food and increases its length if so
                snake_index = snake_eaten(bot, food)
                if snake_index != -1:
                    food.snake_foods.pop(snake_index)
                    food.snake_foods_colour.pop(snake_index)
                    bot.grow()
                    bot.grow()


            # Loops through all the bots and calculates its head position, as well as the snake's head position
            for bot in bots:
                bot_head_rect = pygame.Rect(bot.snake[0][0] - radius, bot.snake[0][1] - radius, radius * 2, radius * 2)
                snake_head_rect = pygame.Rect(snake.snake[0][0] - radius, snake.snake[0][1] - radius, radius * 2, radius * 2)

                # Checks if the snake collided with the bot
                if snake_head_rect.colliderect(bot_head_rect):
                    food.snake_to_food(snake.snake)
                    food.draw("snake", snake_colour)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    scene = "menu"
                    break

                # Checks if any segment of the bot collided with the head of the snake
                for segment in bot.snake:
                    segment_rect = pygame.Rect(segment[0] - radius, segment[1] - radius, radius * 2, radius * 2)
                    if snake_head_rect.colliderect(segment_rect):
                        food.snake_to_food(snake.snake)
                        food.draw("snake", snake_colour)
                        pygame.display.update()
                        pygame.time.delay(2000)
                        scene = "menu"
                        break

                # Checks if any segment of the bot collided with the snake
                for segment in snake.snake:
                    segment_rect = pygame.Rect(segment[0] - radius, segment[1] - radius, radius * 2, radius * 2)
                    if bot_head_rect.colliderect(segment_rect):
                        food.snake_to_food(bot.snake)
                        food.draw("snake", snake_colour)
                        bots.remove(bot)
                        bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                        bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                        break

                # Checks if the bots collided with each other
                for other_bot in bots:
                    if bot != other_bot:
                        other_bot_head_rect = pygame.Rect(other_bot.snake[0][0] - radius, other_bot.snake[0][1] - radius, radius * 2, radius * 2)

                        if bot_head_rect.colliderect(other_bot_head_rect):
                            food.snake_to_food(bot.snake)
                            food.snake_to_food(other_bot.snake)
                            bots.remove(bot)
                            bots.remove(other_bot)
                            bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                            bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                            break

                        for segment in other_bot.snake:
                            segment_rect = pygame.Rect(segment[0] - radius, segment[1] - radius, radius * 2, radius * 2)
                            if bot_head_rect.colliderect(segment_rect):
                                food.snake_to_food(bot.snake)
                                food.snake_to_food(other_bot.snake)
                                bots.remove(bot)
                                bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                                bots.remove(other_bot)
                                bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                                break

            def draw_rect_alpha(surface, colour, rect):
                '''
                Draws a semi-transparent rectangle
                :param surface: surface to draw the rectangle
                :param colour: colour of the rectangle
                :param rect: position of the rectangle
                :return: draws a semi-transparent rectangle
                '''
                shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
                pygame.draw.rect(shape_surf, colour, shape_surf.get_rect())
                surface.blit(shape_surf, rect)

            # Draws barriers on the sides if the snake's position is near the end of the map
            # And calculates the dimensions of the barriers, which get larger the closer the snake is to the end
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


            # Checks if the snake or bots collided with the barrier
            snake_head_rect = pygame.Rect(snake.snake[0][0] - radius, snake.snake[0][1] - radius, radius * 2, radius * 2)
            for barrier in barriers:
                if barrier != -1:
                    barrier_rect = pygame.Rect(barrier)
                    if snake_head_rect.colliderect(barrier_rect):
                        food.snake_to_food(snake.snake)
                        food.draw("snake", snake_colour)
                        pygame.display.update()
                        pygame.time.delay(2000)
                        scene = "menu"
                    else:
                        for bot in bots:
                            bot_head_rect = pygame.Rect(bot.snake[0][0] - radius, bot.snake[0][1] - radius, radius * 2, radius * 2)
                            if bot_head_rect.colliderect(barrier_rect):
                                food.snake_to_food(bot.snake)
                                bots.remove(bot)
                                bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                                break

            # Checks if the snake consumed a normal food
            food_index = food_eaten(snake, food)
            if food_index != -1:
                snake.grow()
                food.update(food.foods[food_index][0], food.foods[food_index][1])
                length += 2

            # Checks if the snake consumed a speed food
            speed_index = speed_eaten(snake, food)
            if speed_index != -1:
                food.speed_foods.pop(speed_index)
                length += 1
                if length % 2 == 0:
                    snake.grow()

            # Checks if the snake consumed a snake food
            snake_index = snake_eaten(snake, food)
            if snake_index != -1:
                food.snake_foods.pop(snake_index)
                food.snake_foods_colour.pop(snake_index)
                length += 4
                snake.grow()
                snake.grow()

            # Increases the radius of the snake if its length is a multiple of 8--
            if length != 10 and length % 800 == 0:
                radius += 1.2

            pygame.display.update()

            # Sets the offset of the backgrounds if they are too much
            if background_x <= -WIDTH:
                background_x = 0
            if background_x >= WIDTH:
                background_x = 0
            if background_y <= -HEIGHT:
                background_y = 0
            if background_y >= HEIGHT:
                background_y = 0

    # Catches any potential errors in the code
    except Exception as e:
        print(e)

'''
Pseudo Code:

Functions:
spawn_food()
speed_food(x, y)
snake_to_food(snake)
move(dx, dy, speed)
update(x, y)
draw(food_type, snake_colour)
update_colour(snake_colour)
move()
grow()
shrink(food)
eyes(radius)
draw(radius, speed)
spawn_bot()
seek_food(foods)
move_towards(target_x, target_y)
draw_eyes(radius)
draw(radius)
speed_up()
grow()
food_eaten(snake, food)
snake_eaten(snake, food)
snake_eaten(snake, food)
map()
draw_circle_alpha(surface, colour, center, radius)
count()
menu(length, highest_length, first_game)
skin(preview_index)
draw_rect_alpha(surface, colour, rect)

start spawn_food():
    self.x = random.randint(-WIDTH, WIDTH * 2)
    self.y = random.randint(-HEIGHT, HEIGHT * 2)
    self.foods.append([self.x, self.y])
    self.foods_move.append([0, 0])
    self.colours.append(random.choice(FOOD_COLOUR))
end spawn_food

start speed_food(x, y):
    self.speed_foods.append([x, y])
    self.speed_foods_move.append([0, 0])
end speed_food

start snake_to_food(snake):
for segment in snake:
    self.snake_foods.append(segment)
    self.snake_foods_colour.append(random.choice(FOOD_COLOUR))
    self.snake_foods_move.append([0, 0])
end snake_to_food

start move(dx, dy, speed):
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
end move

start update(x, y):
for i in range(len(self.foods)):
    if self.foods[i] == [x, y]:
        self.foods.pop(i)
        self.colours.pop(i)
        self.foods_move.pop(i)
        break
while len(self.foods) < 500:
    self.spawn_food()
end update

start draw(food_type, snake_colour):
if food_type == 'speed':
for food in self.speed_foods:
    pygame.draw.circle(screen, snake_colour, food, 3)
elif food_type == 'snake':
for i in range(len(self.snake_foods)):
    pygame.draw.circle(screen, self.snake_foods_colour[i], self.snake_foods[i], 8)
else:
for i in range(len(self.foods)):
    pygame.draw.circle(screen, self.colours[i], self.foods[i], 5)
end draw

start update_colour(snake_colour):
        self.snake_colour = snake_colour
end update_colour
 
start move():
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
end move
start grow():
        tail_x, tail_y = self.snake[-1]
        new_segment = [tail_x, tail_y]
        self.snake.append(new_segment)
end grow

start shrink(food):
    food.speed_foods.append([self.snake[-1][0], self.snake[-1][1]])
    food.speed_foods_move.append([0, 0])
    self.snake.pop()
end shrink

start eyes(radius):
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
end eyes

start draw(radius, speed):
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
end draw

start spawn_bot():
    while True:
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        potential_position = [x, y]
        if all(math.sqrt((segment[0] - x) ** 2 + (segment[1] - y) ** 2) >= 10 for segment in self.snake):
            self.snake = [potential_position]
            for _ in range(9):
                self.snake.append([self.snake[-1][0] - self.dx, self.snake[-1][1] - self.dy])
            break
end spawn_bot
start move_towards(target_x, target_y):
    angle_to_target = math.atan2(target_y - self.snake[0][1], target_x - self.snake[0][0])
    self.dx = self.speed * math.cos(angle_to_target)
    self.dy = self.speed * math.sin(angle_to_target)
    new_head = [self.snake[0][0] + self.dx, self.snake[0][1] + self.dy]
    for i in range(len(self.snake) - 1, 0, -1):
        self.snake[i] = list(self.snake[i - 1])
    self.snake[0] = new_head
end move_towards
start seek_food(foods):
    closest_food = None
    closest_dist = float('inf')
    for food in foods:
        dist = math.sqrt((food[0] - self.snake[0][0]) ** 2 + (food[1] - self.snake[0][1]) ** 2)
        if dist < closest_dist:
            closest_dist = dist
            closest_food = food
    if closest_food:
        self.move_towards(closest_food[0], closest_food[1])
end seek_food
start move(player_head, foods):
    self.seek_food(foods)
end move
start draw_eyes(radius):
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
end draw_eyes
start draw(radius)
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
end draw
start speed_up():
    if len(self.snake) > 15:
        self.snake.pop()
end speed_up
start grow():
    tail_x, tail_y = self.snake[-1]
    new_segment = [tail_x, tail_y]
    self.snake.append(new_segment)
end grow
start food_eaten(snake, food):
    head_x, head_y = snake.snake[0]
    for i in range(len(food.foods)):
        food_x, food_y = food.foods[i]
        if math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2) < 15:
            return i
    return -1
end food_eaten
start speed_eaten(snake, food):
    head_x, head_y = snake.snake[0]
    for i in range(len(food.speed_foods)):
        food_x, food_y = food.speed_foods[i]
        if math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2) < 15:
            return i
    return -1
end speed_eaten
start snake_eaten(snake, food):
    head_x, head_y = snake.snake[0]
    for i in range(len(food.snake_foods)):
        food_x, food_y = food.snake_foods[i]
        if math.sqrt((head_x - food_x) ** 2 + (head_y - food_y) ** 2) < 15:
            return i
    return -1
end snake_eaten
start map():
    map_rect = pygame.Rect(WIDTH - 150, HEIGHT - 150, 100, 100)
    pygame.draw.rect(screen, GRAY, map_rect, 1)
    map_x = (snake_width + WIDTH) / (WIDTH * 2) * 100 + map_rect.left
    map_y = (snake_height + HEIGHT) / (HEIGHT * 2) * 100 + map_rect.top
    map_x = max(map_rect.left + 5, min(map_rect.right - 15, map_x))
    map_y = max(map_rect.top + 5, min(map_rect.bottom - 15, map_y))
    pygame.draw.circle(screen, WHITE, (int(map_x), int(map_y)), 5)
end map
start draw_circle_alpha(surface, colour, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, colour, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)
end draw_circle_alpha
start count(food):
    food_count = len(food.foods)
    for i in range(len(food.foods)):
        if food.foods[i][0] < -WIDTH or food.foods[i][0] > WIDTH * 2 or food.foods[i][1] < -HEIGHT or food.foods[i][1] > HEIGHT * 2:
            food_count -= 1

    while food_count < 45:
        food.spawn_food()
        food_count += 1
end count
start menu(length, highest_length, first_game):
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
end menu
start skin(preview_index):
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
end skin

Main loop
while run:
    try:
        clock.tick(30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Checks if the length of the snake is over 30 and speeds it up if so
                    if length > 30:
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
                        bots = [BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])) for _ in range(num_bots)]
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
                        else:
                            snake_colour = random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])

        if scene == "menu":
            radius = 10
            speed = False
            speed_length = 0
            play_button_rect, skin_button_rect, highest_length = menu(length, highest_length, first_game)
            snake_width = random.randint(-WIDTH + 100, WIDTH * 2 - 100)
            snake_height = random.randint(-HEIGHT + 100, HEIGHT * 2 - 100)
            food = Food()
            snake = Snake(snake_colour)
        elif scene == "skin":
            left_arrow_rect, right_arrow_rect, save_button_rect, chosen_snake_colour = skin(preview_index)
        elif scene == "game":
            first_game = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Moves the background image and manages the snake's position on the screen
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
                # Moves the bots and draws them
                bot.move(snake.snake[0], food.foods)
                bot.draw(radius)

                food_index = food_eaten(bot, food)
                if food_index != -1:
                    bot.grow()
                    food.update(food.foods[food_index][0], food.foods[food_index][1])

                speed_index = speed_eaten(bot, food)
                if speed_index != -1:
                    food.speed_foods.pop(speed_index)
                    bot.grow()

                snake_index = snake_eaten(bot, food)
                if snake_index != -1:
                    food.snake_foods.pop(snake_index)
                    food.snake_foods_colour.pop(snake_index)
                    bot.grow()
                    bot.grow()

            for bot in bots:
                bot_head_rect = pygame.Rect(bot.snake[0][0] - radius, bot.snake[0][1] - radius, radius * 2, radius * 2)
                snake_head_rect = pygame.Rect(snake.snake[0][0] - radius, snake.snake[0][1] - radius, radius * 2, radius * 2)

                if snake_head_rect.colliderect(bot_head_rect):
                    food.snake_to_food(snake.snake)
                    food.draw("snake", snake_colour)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    scene = "menu"
                    break

                for segment in bot.snake:
                    segment_rect = pygame.Rect(segment[0] - radius, segment[1] - radius, radius * 2, radius * 2)
                    if snake_head_rect.colliderect(segment_rect):
                        food.snake_to_food(snake.snake)
                        food.draw("snake", snake_colour)
                        pygame.display.update()
                        pygame.time.delay(2000)
                        scene = "menu"
                        break

                for segment in snake.snake:
                    segment_rect = pygame.Rect(segment[0] - radius, segment[1] - radius, radius * 2, radius * 2)
                    if bot_head_rect.colliderect(segment_rect):
                        food.snake_to_food(bot.snake)
                        food.draw("snake", snake_colour)
                        bots.remove(bot)
                        bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                        bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                        break

                for other_bot in bots:
                    if bot != other_bot:
                        other_bot_head_rect = pygame.Rect(other_bot.snake[0][0] - radius, other_bot.snake[0][1] - radius, radius * 2, radius * 2)

                        if bot_head_rect.colliderect(other_bot_head_rect):
                            food.snake_to_food(bot.snake)
                            food.snake_to_food(other_bot.snake)
                            bots.remove(bot)
                            bots.remove(other_bot)
                            bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                            bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                            break

                        for segment in other_bot.snake:
                            segment_rect = pygame.Rect(segment[0] - radius, segment[1] - radius, radius * 2, radius * 2)
                            if bot_head_rect.colliderect(segment_rect):
                                food.snake_to_food(bot.snake)
                                food.snake_to_food(other_bot.snake)
                                bots.remove(bot)
                                bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                                bots.remove(other_bot)
                                bots.append(BotSnake(random.choice([GREEN, RED, BLUE, YELLOW, ORANGE, PURPLE, PINK])))
                                break
'''