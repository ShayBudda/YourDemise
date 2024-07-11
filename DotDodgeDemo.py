import pygame as pyg
import sys

# Initialize Pygame
pyg.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (225, 225, 100)
PLAYER_COLOR = (0, 255, 255)
ENEMY_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 200, 0)
GAMEOVER_COLOR = (150, 0, 0)
SPEED_INCREMENT = 0.1
INCREMENT_INTERVAL = 2000

# Set up display
screen = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pyg.display.set_caption("Your Demise")

# Create player and enemy
player = pyg.Rect(300, 250, 25, 25)
enemy = pyg.Rect(100, 100, 25, 25)
enemy_speed = [1, 1]

# Set up fonts
font = pyg.font.Font(None, 74)
button_font = pyg.font.Font(None, 50)

# Game state
display_menu = True
run = True
game_over = False

# Clock
clock = pyg.time.Clock()

# Initialize speed timer
speed_timer = pyg.time.get_ticks()

def display_start_menu():
    screen.fill(BG_COLOR)
    title = font.render("Your Demise", True, TEXT_COLOR)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))
    
    start_button = pyg.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    pyg.draw.rect(screen, BUTTON_COLOR, start_button)
    button_text = button_font.render("Start", True, TEXT_COLOR)
    screen.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 5))
    
    pyg.display.update()
    return start_button

def display_game_over():
    screen.fill(GAMEOVER_COLOR)
    text = font.render(f"u r dead - Your Score: {speed_timer / 500:.0f}", True, TEXT_COLOR)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
    
    button = pyg.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    pyg.draw.rect(screen, BUTTON_COLOR, button)
    button_text = button_font.render("Restart", True, TEXT_COLOR)
    screen.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 5))
    
    pyg.display.update()
    return button

while run:
    if display_menu:
        start_button = display_start_menu()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False
            if event.type == pyg.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    display_menu = False
                    game_over = False
                    player.topleft = (300, 250)
                    enemy.topleft = (100, 100)
                    enemy_speed = [1, 1]
                    speed_timer = pyg.time.get_ticks()
    elif not game_over:
        screen.fill(BG_COLOR)
        
        # Draw player and enemy
        pyg.draw.rect(screen, PLAYER_COLOR, player)
        pyg.draw.rect(screen, ENEMY_COLOR, enemy)

        # Handle player movement
        key = pyg.key.get_pressed()
        if key[pyg.K_a] and player.left > 0:
            player.move_ip(-3, 0)
        if key[pyg.K_d] and player.right < SCREEN_WIDTH:
            player.move_ip(3, 0)
        if key[pyg.K_w] and player.top > 0:
            player.move_ip(0, -3)
        if key[pyg.K_s] and player.bottom < SCREEN_HEIGHT:
            player.move_ip(0, 3)

        # Move enemy
        enemy.move_ip(enemy_speed[0], enemy_speed[1])
        if enemy.left < 0 or enemy.right > SCREEN_WIDTH:
            enemy_speed[0] = -enemy_speed[0]
        if enemy.top < 0 or enemy.bottom > SCREEN_HEIGHT:
            enemy_speed[1] = -enemy_speed[1]

        # Increase enemy speed over time
        current_time = pyg.time.get_ticks()
        if current_time - speed_timer > INCREMENT_INTERVAL:
            speed_timer = current_time
            if enemy_speed[0] > 0:
                enemy_speed[0] += SPEED_INCREMENT
            else:
                enemy_speed[0] -= SPEED_INCREMENT
            if enemy_speed[1] > 0:
                enemy_speed[1] += SPEED_INCREMENT
            else:
                enemy_speed[1] -= SPEED_INCREMENT

        # Check for collision
        if player.colliderect(enemy):
            game_over = True

        pyg.display.update()
        clock.tick(60)
    else:
        button = display_game_over()
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                run = False
            if event.type == pyg.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    # Reset game state
                    player.topleft = (300, 250)
                    enemy.topleft = (100, 100)
                    enemy_speed = [1, 1]
                    speed_timer = pyg.time.get_ticks()
                    game_over = False

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False

pyg.quit()
sys.exit()
# I can't figure this out, but the scoring system is a little broken at the moment 
# It accumulates score rather than giving a new one every time the game resets
