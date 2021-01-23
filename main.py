import pygame
import os 

pygame.font.init()
pygame.mixer.init()

width, height = 900, 500
spaceship_width, spaceship_height = 55, 40
WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("First game...")

BORDER = pygame.Rect(width//2 - 5, 0, 10, height)
FPS = 60
Velocity = 5
Bullet_velocity = 7
white = (255, 255, 255)
black = (0, 0, 0)
red_color = (255, 0, 0)
yellow_color = (255, 255, 0)
MAX_BULLETS = 4
health_font = pygame.font.SysFont("comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 70)

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

bullet_hit_sound = pygame.mixer.Sound("shoot.wav")
bullet_fire_sound = pygame.mixer.Sound("hit.wav")

yellow_spaceship_img = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_img, (spaceship_width, spaceship_height)), 90)
red_spaceship_img = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_img, (spaceship_width, spaceship_height)),270)
space_background = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space2.jpg")), (width, height))

class ParticleHandler:
    def __init__(self):
        self.particles = []

    def add_particles(self):
        pass #adds Particles

    def remove_particles(self):
        pass #removes Particles

def draw_win(red, yellow, RED_BULLETS, YELLOW_BULLETS, red_health, yellow_health):
    pygame.draw.rect(WIN, black, BORDER)
    WIN.blit(space_background, (0, 0))


    red_health_text = health_font.render(f"Health: {str(red_health)}", 1, white)
    yellow_health_text = health_font.render(f"Health: {str(yellow_health)}", 1, white)
    WIN.blit(red_health_text, (width - red_health_text.get_width()- 10, 10 ))
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(yellow_spaceship, (yellow.x, yellow.y))
    WIN.blit(red_spaceship, (red.x, red.y))

    for bullet in RED_BULLETS:
        pygame.draw.rect(WIN, red_color, bullet)

    for bullet in YELLOW_BULLETS:
        pygame.draw.rect(WIN, yellow_color, bullet)
    pygame.display.update()

def draw_winner(winner):
    winner_text = winner_font.render(winner, 1, white)
    WIN.blit(winner_text, (width // 2 - winner_text.get_width()//2, height // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    # pygame.time.delay(5000)

def yellow_movement_handle(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - Velocity > 0:  # LEFT
        yellow.x -= Velocity
    if keys_pressed[pygame.K_d] and yellow.x + Velocity + yellow.width < BORDER.x:  # RIGHT
        yellow.x += Velocity
    if keys_pressed[pygame.K_w] and yellow.y - Velocity > 0:  # UP
        yellow.y -= Velocity
    if keys_pressed[pygame.K_s] and yellow.y + Velocity + yellow.height < height - 20:  # down
        yellow.y += Velocity

def red_movement_handle(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - Velocity > BORDER.x + BORDER.width:  # LEFT
        red.x -= Velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + Velocity + red.width < width:  # RIGHT
        red.x += Velocity
    if keys_pressed[pygame.K_UP] and red.y - Velocity > 0:  # UP
        red.y -= Velocity
    if keys_pressed[pygame.K_DOWN] and red.y + Velocity + red.height < height - 20:  # down
        red.y += Velocity

def handle_bullets(YELLOW_BULLETS, RED_BULLETS, yellow, red):
    for bullet in YELLOW_BULLETS:
        bullet.x += Bullet_velocity
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            YELLOW_BULLETS.remove(bullet)
        elif bullet.x  > width:
            YELLOW_BULLETS.remove(bullet)
    for bullet in RED_BULLETS:
        bullet.x -= Bullet_velocity
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            RED_BULLETS.remove(bullet)
        elif bullet.x  < 0:
            RED_BULLETS.remove(bullet)


def main():
    red = pygame.Rect(700, 300, spaceship_width, spaceship_height)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)

    RED_BULLETS = []
    YELLOW_BULLETS = []

    red_health = 10
    yellow_health = 10


    clock = pygame.time.Clock()
    mode = True
    while mode:
        clock.tick(FPS)

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow won! \n press [R] to restart"


        if yellow_health <= 0 :
            winner_text = "Red won!" \
                          "press [R] to restart"

        if winner_text != "":
            draw_winner(winner_text)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode = False


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(YELLOW_BULLETS) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    YELLOW_BULLETS.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL and len(RED_BULLETS) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    RED_BULLETS.append(bullet)
                    bullet_fire_sound.play()

                if event.key == pygame.K_r:
                    main()

            if event.type == red_hit:
                red_health -= 2
                bullet_hit_sound.play()
            if event.type == yellow_hit:
                yellow_health -= 2
                bullet_hit_sound.play()

        # print(RED_BULLETS, YELLOW_BULLETS)
        keys_pressed = pygame.key.get_pressed()
        yellow_movement_handle(keys_pressed, yellow)
        red_movement_handle(keys_pressed, red)
        handle_bullets(YELLOW_BULLETS, RED_BULLETS, yellow, red)

            # red.x += 1
        draw_win(red, yellow, RED_BULLETS, YELLOW_BULLETS, red_health, yellow_health)

    pygame.quit()

if __name__ == "__main__":
    main()