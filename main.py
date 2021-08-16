import pygame
import os

pygame.font.init()
pygame.mixer.init()


class Game():
    def __init__(WINDOW, self):
        WIDTH, HEIGHT = 900, 500
        SSW, SSH = 55, 40
        WIN = WINDOW
        pygame.display.set_caption("First Game")

        BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

        HEALTH_FONT = pygame.font.SysFont('helvetica', 40)
        WINNER_FONT = pygame.font.SysFont('helvetica', 100)

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)

        FPS = 60
        VELOCITY = 5
        MAX_BULLETS = 5
        BULLET_VELOCITY = 7

        BULLET_FIRE_SOUND = pygame.mixer.Sound(
            os.path.join('Assets', 'Gun+Silencer.mp3'))
        BULLET_HIT_SOUND = pygame.mixer.Sound(
            os.path.join('Assets', 'Grenade+1.mp3'))
        VICTORY_SOUND = pygame.mixer.Sound(
            os.path.join('Assets', 'Victory.mp3'))
        BACKGROUND_MUSIC = pygame.mixer.Sound(
            os.path.join('Assets', 'Blinding Lights.mp3'))

        YELLOW_HIT = pygame.USEREVENT + 1
        RED_HIT = pygame.USEREVENT + 2

        YELLOW_SPACESHIP_IMAGE = pygame.image.load(
            os.path.join('Assets', 'spaceship_yellow.png'))
        YELLOW_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SSW, SSH)), 90)
        RED_SPACESHIP_IMAGE = pygame.image.load(
            os.path.join('Assets', 'spaceship_red.png'))
        RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SSW, SSH))
        RED_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(RED_SPACESHIP_IMAGE, (SSW, SSH)), 270)
        SPACE_BACKGROUND = pygame.transform.scale(
            pygame.image.load(os.path.join('Assets', 'space.png')),
            (WIDTH, HEIGHT))

    def draw_window(red, yellow, red_bullets, yellow_bullets, red_health,
                    yellow_health, self):
        self.WIN.blit(self.SPACE_BACKGROUND, (0, 0))
        pygame.draw.rect(self.WIN, self.BLACK, self.BORDER)

        red_health_text = self.HEALTH_FONT.render("Health: " + str(red_health),
                                                  1, self.WHITE)
        yellow_health_text = self.HEALTH_FONT.render(
            "Health: " + str(yellow_health), 1, self.WHITE)
        self.WIN.blit(red_health_text,
                      (self.WIDTH - red_health_text.get_width() - 10, 10))
        self.WIN.blit(yellow_health_text, (10, 10))

        self.WIN.blit(self.YELLOW_SPACESHIP, (yellow.x, yellow.y))
        self.WIN.blit(self.RED_SPACESHIP, (red.x, red.y))

        for bullet in red_bullets:
            pygame.draw.rect(self.WIN, self.RED, bullet)

        for bullet in yellow_bullets:
            pygame.draw.rect(self.WIN, self.YELLOW, bullet)

        pygame.display.update()

    def draw_winner(text, Game):
        draw_text = Game.WINNER_FONT.render(text, 1, Game.WHITE)
        Game.WIN.blit(draw_text,
                      (Game.WIDTH // 2 - draw_text.get_width() // 2,
                       Game.HEIGHT // 2 - draw_text.get_height() // 2))
        pygame.display.update()
        Game.BACKGROUND_MUSIC.stop()
        Game.VICTORY_SOUND.play()
        pygame.time.delay(5000)

    def handle_yellow_movement(keys_pressed, yellow, Game):
        if keys_pressed[pygame.K_a] and yellow.x - Game.VELOCITY > 0:  #left
            yellow.x -= Game.VELOCITY
        if keys_pressed[pygame.K_d] and yellow.x + Game.VELOCITY < (
                Game.WIDTH / 2) - SSW + 15:  #right
            yellow.x += Game.VELOCITY
        if keys_pressed[pygame.K_w] and yellow.y - Game.VELOCITY > 0:  #up
            yellow.y -= Game.VELOCITY
        if keys_pressed[
                pygame.
                K_s] and yellow.y + Game.VELOCITY < Game.HEIGHT - Game.SSH - 15:  #down
            yellow.y += Game.VELOCITY

    def handle_red_movement(keys_pressed, red, Game):
        if keys_pressed[
                pygame.
                K_LEFT] and red.x - Game.VELOCITY > Game.WIDTH / 2:  #left
            red.x -= Game.VELOCITY
        if keys_pressed[
                pygame.K_RIGHT] and red.x + Game.VELOCITY < Game.WIDTH:  #right
            red.x += Game.VELOCITY
        if keys_pressed[pygame.K_UP] and red.y - Game.VELOCITY > 0:  #up
            red.y -= Game.VELOCITY
        if keys_pressed[
                pygame.
                K_DOWN] and red.y + Game.VELOCITY < Game.HEIGHT - Game.SSH - 15:  #down
            red.y += Game.VELOCITY

    def handle_bullets(yellow_bullets, red_bullets, yellow, red, Game):
        for bullet in yellow_bullets:
            bullet.x += Game.BULLET_VELOCITY
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(Game.RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x > Game.WIDTH:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets:
            bullet.x -= Game.BULLET_VELOCITY
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(Game.YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x < 0:
                red_bullets.remove(bullet)

    def main(self):
        Game.BACKGROUND_MUSIC.play(loops=0, fade_ms=0)
        red = pygame.Rect(700, 300, Game.SSW, Game.SSH)
        yellow = pygame.Rect(100, 300, Game.SSW, Game.SSH)

        red_bullets = []
        yellow_bullets = []

        yellow_health = 10
        red_health = 10

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(Game.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT and len(
                            yellow_bullets) < Game.MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width,
                                             yellow.y + yellow.height // 2 - 2,
                                             10, 5)
                        yellow_bullets.append(bullet)
                        Game.BULLET_FIRE_SOUND.play()

                    if event.key == pygame.K_RSHIFT and len(
                            red_bullets) < Game.MAX_BULLETS:
                        bullet = pygame.Rect(red.x - red.width,
                                             red.y + red.height // 2 - 2, 10,
                                             5)
                        red_bullets.append(bullet)
                        Game.BULLET_FIRE_SOUND.play()

                if event.type == Game.RED_HIT:
                    red_health -= 1
                    Game.BULLET_HIT_SOUND.play()

                if event.type == Game.YELLOW_HIT:
                    yellow_health -= 1
                    Game.BULLET_HIT_SOUND.play()

            winner_text = ""
            if red_health <= 0:
                winner_text = "Yellow Wins!"

            if yellow_health <= 0:
                winner_text = "Red Wins!"

            if winner_text != "":
                Game.draw_winner(winner_text)
                break

            print(red_bullets, yellow_bullets)
            keys_pressed = pygame.key.get_pressed()
            Game.handle_yellow_movement(keys_pressed, yellow)
            Game.handle_red_movement(keys_pressed, red)
            Game.handle_bullets(yellow_bullets, red_bullets, yellow, red)
            Game.draw_window(red, yellow, red_bullets, yellow_bullets,
                             red_health, yellow_health)

        Game.main(self)
