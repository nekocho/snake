import pygame
import random

# Define game window size
width, height = 600, 600
block_size = 20

# Initialise and set fonts in pygame module
# score_font use to display score
pygame.font.init()
score_font = pygame.font.SysFont("consolas", 20)
score = 0

# Colour definitions using tuples
white = (255, 255, 255)
red = (255, 0, 0)

# Initialise Pygame
pygame.init()

# Setting up display
win = pygame.display.set_mode((width, height))

# Setting up clock
clock = pygame.time.Clock()

# snake and food initialisation

snake_pos = [[width // 2, height // 2]]
snake_speed = [0, block_size]

teleport_walls = True  # Enable wall teleporting


# Food generation

def generate_food():
    while True:
        x = random.randint(0, (width - block_size) // block_size) * block_size
        y = random.randint(0, (height - block_size) // block_size) * block_size
        food_pos = [x, y]
        if food_pos not in snake_pos:
            return food_pos


food_pos = generate_food()


def draw_objects():
    win.fill((0, 0, 0))  # Fills screen black
    for pos in snake_pos:
        pygame.draw.rect(win, white,
                         pygame.Rect(pos[0], pos[1], block_size, block_size))  # Draws snake using white squares
    pygame.draw.rect(win, red,
                     pygame.Rect(food_pos[0], food_pos[1], block_size, block_size))  # Draws food using red squares

    # Render the score
    score_text = score_font.render(f"Score: {score}", True, white)  # Text surface
    win.blit(score_text, (10, 10))  # Position of score drawn


def update_snake():
    global food_pos, score
    new_head = [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]]

    if teleport_walls:
        # if the new head position is outside the screen, wrap it to the other side
        if new_head[0] >= width:
            new_head[0] = 0
        elif new_head[0] < 0:
            new_head[0] = width - block_size
        if new_head[1] >= height:
            new_head[1] = 0
        elif new_head[1] < 0:
            new_head[1] = height - block_size

    if new_head == food_pos:
        food_pos = generate_food()  # Generate new food if head of snake is at food position
        score += 1  # increment score when food is eaten
    else:
        snake_pos.pop()  # Remove last element from the snake

    snake_pos.insert(0, new_head)  # add new head to the snake --> increase length


# GAME OVER CONDITION
def game_over():
    # game over when snake hits the boundaries or runs into itself

    if teleport_walls:
        return snake_pos[0] in snake_speed[1:]
    else:
        # game over if snake runs into wall
        # game over if snake runs into itself
        return snake_pos[0] in snake_pos[1:] or \
            snake_pos[0][0] > width - block_size or \
            snake_pos[0][0] < 0 or \
            snake_pos[0][1] > height - block_size or \
            snake_pos[0][1] < 0


# DISPLAY GAME OVER SCREEN
def game_over_screen():
    global score
    win.fill((0, 0, 0))
    game_over_font = pygame.font.SysFont("consolas", 50)
    game_over_text = game_over_font.render(f"GAME OVER! Score: {score}", True, white)
    win.blit(game_over_text,
             (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

    # Loop that waits for player to press a key
    # If "R" is pressed, restart game, "Q" quits the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()  # Replay the game
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()  # Quit the game
                    return


# HANDLE USER INPUT

# Main game loop
def run():
    global snake_speed, snake_pos, food_pos, score
    # Reset game state
    snake_pos = [[width // 2, height // 2]]
    snake_speed = [0, block_size]
    food_pos = generate_food()
    score = 0

    # Loop that runs as long as the game is running
    running = True
    while running:
        for event in pygame.event.get():
            # If the window is closed, running is set to False to end the game
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()

            # Set it so that the snake can't turn 180 degrees
            for key in keys:
                # When UP key is pressed but the snake is moving down, ignore input
                if keys[pygame.K_UP]:
                    if snake_speed[1] == block_size:
                        continue
                    snake_speed = [0, -block_size]
                # When DOWN key is pressed but the snake is moving up, ignore input
                if keys[pygame.K_DOWN]:
                    if snake_speed[1] == -block_size:
                        continue
                    snake_speed = [0, block_size]
                # When LEFT key is pressed but the snake is moving right, ignore input
                if keys[pygame.K_LEFT]:
                    if snake_speed[0] == block_size:
                        continue
                    snake_speed = [-block_size, 0]
                # When RIGHT key is pressed but snake is moving left, ignore input
                if keys[pygame.K_RIGHT]:
                    if snake_speed[0] == -block_size:
                        continue
                    snake_speed = [block_size, 0]
        # Check if game is over
        if game_over():
            game_over_screen()  # If game over, display game over screen
            return  # Exit function
        # If not game over - update snake position, draw objects and update display
        update_snake()
        draw_objects()
        pygame.display.update()
        clock.tick(15)  # Limit frame rate to 15 FPS


if __name__ == "__main__":
    run()
