import pygame as pyg
import sys
import effects

# Initialize Pygame
pyg.init()
pyg.mixer.init()

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

# Load Background Music
background_music = 'Pixel Dreams.mp3'
death_sound = 'Death_Sound.wav'
wall_bounce_sound = 'Bounce_Sound.wav'
game_over_music = 'game_over_ambience.wav'

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

player_score = 0

# Load and play background music
try:
    pyg.mixer.music.load(background_music)
    pyg.mixer.music.play(-1)
except Exception as e:
    print(f"Error loading background music: {e}")

def display_start_menu():
    screen.fill(BG_COLOR)
    title = font.render("Your Demise", True, TEXT_COLOR)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))
    
    start_button = pyg.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    pyg.draw.rect(screen, BUTTON_COLOR, start_button)
    button_text = button_font.render("Don't Click", True, TEXT_COLOR)
    screen.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 5))
    
    pyg.display.update()
    return start_button

def display_game_over():
    screen.fill(GAMEOVER_COLOR)
    text = font.render(f"u r dead - Your Score: {player_score}", True, TEXT_COLOR)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3))
    
    button = pyg.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    pyg.draw.rect(screen, BUTTON_COLOR, button)
    button_text = button_font.render("Die Again", True, TEXT_COLOR)
    screen.blit(button_text, (SCREEN_WIDTH // 2 - button_text.get_width() // 2, SCREEN_HEIGHT // 2 + 5))
    
    pyg.display.update()
    return button

def fade_transition_effect():
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
    fade_steps = 30  # Number of steps for the fade effect

    for idx, color in enumerate(colors):
        for alpha in range(0, 256, int(256 / fade_steps)):  # Fade in
            fade_surface = pyg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill(color)
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            
            if idx < len(colors) // 2:
                text = font.render("Are You Ready", True, TEXT_COLOR)
            else:
                text = font.render("To Die?", True, TEXT_COLOR)
                
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            
            pyg.display.update()
            pyg.time.delay(10)

        for alpha in range(255, -1, -int(256 / fade_steps)):  # Fade out
            fade_surface = pyg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.fill(color)
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            
            if idx < len(colors) // 2:
                text = font.render("Are You Ready", True, TEXT_COLOR)
            else:
                text = font.render("To Die?", True, TEXT_COLOR)
                
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            
            pyg.display.update()
            pyg.time.delay(10)

while run:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False
        if event.type == pyg.MOUSEBUTTONDOWN:
            if display_menu:
                start_button = display_start_menu()
                if start_button.collidepoint(event.pos):
                    fade_transition_effect()
                    display_menu = False
                    game_over = False
                    player.topleft = (300, 250)
                    enemy.topleft = (100, 100)
                    enemy_speed = [1, 1]
                    speed_timer = pyg.time.get_ticks()
            elif game_over:
                button = display_game_over()
                if button.collidepoint(event.pos):
                    fade_transition_effect()
                    # Reset game state
                    player.topleft = (300, 250)
                    enemy.topleft = (100, 100)
                    enemy_speed = [1, 1]
                    speed_timer = pyg.time.get_ticks()
                    game_over = False
                    player_score = 0
                    # Switch back to background music
                    try:
                        pyg.mixer.music.load(background_music)
                        pyg.mixer.music.play(-1)
                    except Exception as e:
                        print(f"Error loading background music: {e}")

    if display_menu:
        display_start_menu()
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
            try:
                pyg.mixer.Sound(wall_bounce_sound).play()  # Play bounce sound
            except Exception as e:
                print(f"Error playing wall bounce sound: {e}")
        if enemy.top < 0 or enemy.bottom > SCREEN_HEIGHT:
            enemy_speed[1] = -enemy_speed[1]
            try:
                pyg.mixer.Sound(wall_bounce_sound).play()  # Play bounce sound
            except Exception as e:
                print(f"Error playing wall bounce sound: {e}")

        # Increase enemy speed over time
        current_time = pyg.time.get_ticks()
        
        if current_time - speed_timer > INCREMENT_INTERVAL:
            speed_timer = current_time
            player_score += 1
            if player_score %20:
                effects.transition.difficulty_transition()
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
            pyg.mixer.music.stop()  # Stop background music
            try:
                pyg.mixer.Sound(death_sound).play()  # Play death sound
            except Exception as e:
                print(f"Error playing death sound: {e}")
            try:
                pyg.mixer.music.load(game_over_music)
                pyg.mixer.music.play(-1)
            except Exception as e:
                print(f"Error loading game over music: {e}")

        pyg.display.update()
        clock.tick(60)
    else:
        display_game_over()

pyg.quit()
sys.exit()
