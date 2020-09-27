import pygame
import random
import math

# Initialize pygame and screen
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Caption, Icon, Background
pygame.display.set_caption("Snake")
icon = pygame.image.load("images/snake.png")
pygame.display.set_icon(icon)
background = pygame.image.load("images/KD.jpg")

# Colors
green = (0, 255, 0)

# Starting snake position and changes
snake_x = screen_width / 2
snake_y = screen_height / 2
x_change = 0
y_change = 0
snake_size = 40

# Food
russ = pygame.image.load("images/russ.png")
russ = pygame.transform.scale(russ, (snake_size, snake_size))
russ_x = random.randint(0, 790 - snake_size)
russ_y = random.randint(0, 590 - snake_size)

# Detect food collision
def isCollision(snake_x, snake_y, russ_x, russ_y):
    distance = math.sqrt(math.pow((snake_x - russ_x), 2) + math.pow((snake_y - russ_y), 2))
    if distance < 39:
        return True
    return False

# Detect Self-collision
def selfCollide(snake_x, snake_y, snake):
    if len(snake) > 1:
        for point in snake[:-30]:
            russ_x = point[0]
            russ_y = point[1]
            distance = math.sqrt(math.pow((snake_x - russ_x), 2) + math.pow((snake_y - russ_y), 2))
            if distance < 20:
                return True
    return False

# Show score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 10
textY = 10
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

# Game over
over_font = pygame.font.Font("freesansbold.ttf", 64)
def game_over():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
    play_again = font.render("Press SPACE to play again", True, (255, 0, 0))
    screen.blit(play_again, (280, 400))

# Draw the snake
def ourSnake(snake):
    for x in snake:
        pygame.draw.rect(screen, green, [x[0], x[1], snake_size, snake_size])

snake = [(snake_x, snake_y)]
snake_length = 1

# Game loop
running = True
over = False
moved = False
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        # User quit
        if event.type == pygame.QUIT:
            running = False
            continue
        # User controls using WASD
        elif event.type == pygame.KEYDOWN and not over:
            if event.key == pygame.K_a:
                x_change = -1
                y_change = 0
            elif event.key == pygame.K_d:
                x_change = 1
                y_change = 0
            elif event.key == pygame.K_w:
                y_change = -1
                x_change = 0
            elif event.key == pygame.K_s:
                y_change = 1
                x_change = 0
            moved = True
    # Move snake
    snake_x += x_change
    snake_y += y_change

    # Adjusts snake length, score, and food location if snake collides with food
    if isCollision(snake_x, snake_y, russ_x, russ_y):
        snake_length += 1
        score_value += 1
        russ_x = random.randint(0, 790 - snake_size)
        russ_y = random.randint(0, 590 - snake_size)
        for position in snake:
            if isCollision(position[0], position[1], russ_x, russ_y):
                russ_x = random.randint(0, 790 - snake_size)
                russ_y = random.randint(0, 590 - snake_size)
    screen.blit(russ, (russ_x, russ_y))

    snake_head = (snake_x, snake_y)
    snake.append(snake_head)
    # Maintains correct snake length
    if len(snake) > snake_length * (snake_size - snake_size / 2) and not over:
        del snake[0]

    ourSnake(snake)

    # Self collisions
    if moved and selfCollide(snake_x, snake_y, snake):
        over = True
        x_change = 0
        y_change = 0

    # Borders
    if snake_x < 0 or snake_x > 800 - snake_size:
        x_change = 0
        over = True
    if snake_y < 0 or snake_y > 600 -snake_size:
        y_change = 0
        over = True
    # Game over screen
    if over:
        game_over()
        for event in pygame.event.get():
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE:
                     over = False
                     snake_x = 400
                     snake_y = 300
                     snake = [(snake_x, snake_y)]
                     snake_length = 1
                     score_value = 0

    show_score(textX, textY)
    pygame.display.update()