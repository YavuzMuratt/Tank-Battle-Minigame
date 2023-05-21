import pygame
import os

pygame.font.init()

# Set up window dimensions
WIDTH, HEIGHT = 1024, 768
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Bombastik Oyun 2")
Color = (125, 30, 30)
Brown = (102, 51, 0)
Blue = (0, 255, 255)
White = (255, 255, 255)

# Define fonts for displaying health and winner text
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)

# Initialize mixer for sound effects
pygame.mixer.init()
SHELL_FIRE = pygame.mixer.Sound('assets/Fire.mp3')
SHELL_HIT = pygame.mixer.Sound('assets/Hit.mp3')
CHEER = pygame.mixer.Sound('assets/Cheer.mp3')

FPS = 60
VEL = 2
BULLET_VEL = 7
MAX_BULLET = 7

# Define custom user events for bullet hits
RED_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2

# Set up border
BORDER = pygame.Rect(0, (HEIGHT / 2 - 5), WIDTH, 10)

# Set tank dimensions
tank_width = 60
tank_height = 65

# Load tank images
GREEN_TANK = pygame.image.load(
    os.path.join('assets', 'TankG.png'))
GREEN_TANK = pygame.transform.scale(GREEN_TANK, (tank_width, tank_height))

RED_TANK = pygame.image.load(
    os.path.join('assets', 'TankR.png'))
RED_TANK = pygame.transform.scale(RED_TANK, (tank_width, tank_height))
RED_TANK = pygame.transform.rotate(RED_TANK, 180)

BATTLEGROUND = pygame.image.load(
    os.path.join('assets', 'Background.png'))
BATTLEGROUND = pygame.transform.scale(BATTLEGROUND, (WIDTH, HEIGHT))


# Function to draw the game window
def draw_window(pred, pgreen, red_bullets, green_bullets, red_health, green_health):
    WIN.blit(BATTLEGROUND, (1, 1))
    pygame.draw.rect(WIN, Brown, BORDER)

    # Draw health text for red and green tanks
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, White)
    green_health_text = HEALTH_FONT.render("Health: " + str(green_health), 1, White)
    WIN.blit(red_health_text, (20, 20))
    WIN.blit(green_health_text, (20, 720))

    # Draw red and green tanks on the window
    WIN.blit(GREEN_TANK, (pgreen.x, pgreen.y))
    WIN.blit(RED_TANK, (pred.x, pred.y))

    # Draw bullets for red and green tanks
    for bullet in red_bullets:
        pygame.draw.rect(WIN, Blue, bullet)
    for bullet in green_bullets:
        pygame.draw.rect(WIN, White, bullet)

    pygame.display.update()


# Function to handle movement of the red tank
def red_movement(pressed_keys, pred):
    if pressed_keys[pygame.K_a] and pred.x - VEL > 0:  # Red Left
        pred.x -= VEL
    if pressed_keys[pygame.K_d] and pred.x + VEL < WIDTH - 45:  # Red Right
        pred.x += VEL
    if pressed_keys[pygame.K_s] and pred.y + VEL + pred.width < BORDER.y:  # Red Down
        pred.y += VEL
    if pressed_keys[pygame.K_w] and pred.y - VEL > 0:  # Red Up
        pred.y -= VEL


# Function to handle movement of the green tank
def green_movement(pressed_keys, pgreen):
    if pressed_keys[pygame.K_LEFT] and pgreen.x - VEL > 0:  # Green Left
        pgreen.x -= VEL
    if pressed_keys[pygame.K_RIGHT] and pgreen.x + VEL < WIDTH - 45:  # Green Right
        pgreen.x += VEL
    if pressed_keys[pygame.K_DOWN] and pgreen.y + VEL < HEIGHT - 65:  # Green Down
        pgreen.y += VEL
    if pressed_keys[pygame.K_UP] and pgreen.y - VEL > BORDER.y:  # Green Up
        pgreen.y -= VEL


# Function to handle movement of bullets
def bullet_movement(red_bullets, green_bullets, pred, pgreen):
    for bullet in red_bullets:
        bullet.y += BULLET_VEL
        if pgreen.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            red_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            red_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.y -= BULLET_VEL
        if pred.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            green_bullets.remove(bullet)
        elif bullet.y < 0:
            green_bullets.remove(bullet)


# Function to draw the winner text on the screen
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, White)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    CHEER.play()
    pygame.time.delay(5000)


# Main game loop
def main():
    pred = pygame.Rect(484, 28, tank_width, tank_height)
    pgreen = pygame.Rect(484, 688, tank_width, tank_height)

    red_bullets = []
    green_bullets = []

    red_health = 10
    green_health = 10

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(
                        pred.x + pred.width / 2 - 5, pred.y + pred.height // 2 - 2, 5, 10)
                    red_bullets.append(bullet)
                    SHELL_FIRE.play()

                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLET:
                    bullet = pygame.Rect(
                        pgreen.x + pgreen.width / 2 - 5, pgreen.height // 2 - 2 + pgreen.y, 5, 10)
                    green_bullets.append(bullet)
                    SHELL_FIRE.play()

            if event.type == RED_HIT:
                red_health -= 3
                SHELL_HIT.play()
            if event.type == GREEN_HIT:
                green_health -= 3
                SHELL_HIT.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Green Won!"
        if green_health <= 0:
            winner_text = "Red Won!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        pressed_keys = pygame.key.get_pressed()
        red_movement(pressed_keys, pred)
        green_movement(pressed_keys, pgreen)
        bullet_movement(red_bullets, green_bullets, pred, pgreen)

        draw_window(pred, pgreen, red_bullets, green_bullets, red_health, green_health)


# Run the main game loop
if __name__ == '__main__':
    main()
