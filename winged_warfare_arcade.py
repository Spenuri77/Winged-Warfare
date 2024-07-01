import pygame
import math
import random
import time

vector = pygame.math.Vector2

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Winged Warfare")

SKY_BLUE = (60, 10, 81)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60

running = True
main_menu = True
score_menu = False
pause = False

score = 0
score_multiplier = 0

pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

play_img = pygame.image.load('buttons/play_button.png').convert_alpha()
quit_img = pygame.image.load('buttons/quit_button.png').convert_alpha()
game_over_img = pygame.image.load('buttons/game_over.png').convert_alpha()

play_img_main_menu = pygame.image.load('buttons/play_button_main_menu.png').convert_alpha()
quit_img_main_menu = pygame.image.load('buttons/quit_button_main_menu.png').convert_alpha()


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

def draw_text():
    global score, score_multiplier
    font_path = '8-bit Arcade in.ttf'
    font = pygame.font.Font(font_path, 125)
    score_text = font.render(f'{score}', True, (75, 0, 130))
    score_text_shadow = font.render(f'{score}', True, (180, 0, 255))
    font = pygame.font.Font(font_path, 75)
    score_multiplier_text = font.render(f'{score_multiplier}x', True, (75, 0, 130))
    score_multiplier_text_shadow = font.render(f'{score_multiplier}x', True, (180, 0, 255))
    screen.blit(score_text, (35, 10))
    screen.blit(score_text_shadow, (30, 10))
    screen.blit(score_multiplier_text, (35, 80))
    screen.blit(score_multiplier_text_shadow, (30, 80))


class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.image = pygame.image.load('pixel art/0.png').convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (2880, 1620)
        self.hp = 100
        self.shoot_cooldown = 0
        self.angle = 0.0
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 10.0
        self.acceleration = 5
        self.rotation_speed = 0.1
        self.DECELERATION = 0.05
        self.gravity = 1.5
        self.current_sprite = 0
        self.effect_active = False
        self.effect_end_time = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.hp_reach_zero_time = None

    def move(self):
        keys = pygame.key.get_pressed()

        if math.degrees(self.angle) > 360:
            self.angle = 0
        elif math.degrees(self.angle) < -360:
            self.angle = 0

        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed

        if keys[pygame.K_UP]:
            self.speed += self.acceleration
            self.gravity = 0.5
            self.current_sprite += 0.15
        else:
            if self.speed > 0:
                self.speed -= self.DECELERATION
            elif self.speed < 0:
                self.speed += self.DECELERATION
            self.gravity = 1.5
            self.current_sprite = 0

        if keys[pygame.K_x]:
            self.shoot()

        if not self.effect_active:
            self.speed = max(-10.0, min(self.speed, 10.0))
            self.DECELERATION = 0.05
        elif self.effect_active:
            self.speed = max(-14.0, min(self.speed, 14.0))

        self.velocity.x = math.cos(self.angle) * self.speed
        self.velocity.y = -math.sin(self.angle) * self.speed

        self.velocity.y += self.gravity

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 18.0
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle, 'player_bullet.png')
            camera_group.add(bullet)
            player_bullets_group.add(bullet)

    def pseudo_3d(self):
        if self.current_sprite >= 9:
            self.current_sprite = 5

        if 0 <= abs(math.degrees(self.angle)) < 9:
            sprites = ['pixel art/0_0.png', 'pixel art/0_1.png', 'pixel art/0_2.png', 'pixel art/0_3.png',
                       'pixel art/0_4.png', 'pixel art/0_5.png', 'pixel art/0_6.png', 'pixel art/0_7.png',
                       'pixel art/0_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 9 <= abs(math.degrees(self.angle)) < 18:
            sprites = ['pixel art/1_0.png', 'pixel art/1_1.png', 'pixel art/1_2.png', 'pixel art/1_3.png',
                       'pixel art/1_4.png', 'pixel art/1_5.png', 'pixel art/1_6.png', 'pixel art/1_7.png',
                       'pixel art/1_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 18 <= abs(math.degrees(self.angle)) < 27:
            sprites = ['pixel art/2_0.png', 'pixel art/2_1.png', 'pixel art/2_2.png', 'pixel art/2_3.png',
                       'pixel art/2_4.png', 'pixel art/2_5.png', 'pixel art/2_6.png', 'pixel art/2_7.png',
                       'pixel art/2_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 27 <= abs(math.degrees(self.angle)) < 36:
            sprites = ['pixel art/3_0.png', 'pixel art/3_1.png', 'pixel art/3_2.png', 'pixel art/3_3.png',
                       'pixel art/3_4.png', 'pixel art/3_5.png', 'pixel art/3_6.png', 'pixel art/3_7.png',
                       'pixel art/3_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 36 <= abs(math.degrees(self.angle)) < 45:
            sprites = ['pixel art/4_0.png', 'pixel art/4_1.png', 'pixel art/4_2.png', 'pixel art/4_3.png',
                       'pixel art/4_4.png', 'pixel art/4_5.png', 'pixel art/4_6.png', 'pixel art/4_7.png',
                       'pixel art/4_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 45 <= abs(math.degrees(self.angle)) < 54:
            sprites = ['pixel art/5_0.png', 'pixel art/5_1.png', 'pixel art/5_2.png', 'pixel art/5_3.png',
                       'pixel art/5_4.png', 'pixel art/5_5.png', 'pixel art/5_6.png', 'pixel art/5_7.png',
                       'pixel art/5_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 54 <= abs(math.degrees(self.angle)) < 63:
            sprites = ['pixel art/6_0.png', 'pixel art/6_1.png', 'pixel art/6_2.png', 'pixel art/6_3.png',
                       'pixel art/6_4.png', 'pixel art/6_5.png', 'pixel art/6_6.png', 'pixel art/6_7.png',
                       'pixel art/6_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 63 <= abs(math.degrees(self.angle)) < 72:
            sprites = ['pixel art/7_0.png', 'pixel art/7_1.png', 'pixel art/7_2.png', 'pixel art/7_3.png',
                       'pixel art/7_4.png', 'pixel art/7_5.png', 'pixel art/7_6.png', 'pixel art/7_7.png',
                       'pixel art/7_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 72 <= abs(math.degrees(self.angle)) < 81:
            sprites = ['pixel art/8_0.png', 'pixel art/8_1.png', 'pixel art/8_2.png', 'pixel art/8_3.png',
                       'pixel art/8_4.png', 'pixel art/8_5.png', 'pixel art/8_6.png', 'pixel art/8_7.png',
                       'pixel art/8_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 81 <= abs(math.degrees(self.angle)) < 90:
            sprites = ['pixel art/10_0.png', 'pixel art/10_1.png', 'pixel art/10_2.png', 'pixel art/10_3.png',
                       'pixel art/10_4.png', 'pixel art/10_5.png', 'pixel art/10_6.png', 'pixel art/10_7.png',
                       'pixel art/10_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 90 <= abs(math.degrees(self.angle)) < 99:
            sprites = ['pixel art/9_0.png', 'pixel art/9_1.png', 'pixel art/9_2.png', 'pixel art/9_3.png',
                       'pixel art/9_4.png', 'pixel art/9_5.png', 'pixel art/9_6.png', 'pixel art/9_7.png',
                       'pixel art/9_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 99 <= abs(math.degrees(self.angle)) < 108:
            sprites = ['pixel art/8_0.png', 'pixel art/8_1.png', 'pixel art/8_2.png', 'pixel art/8_3.png',
                       'pixel art/8_4.png', 'pixel art/8_5.png', 'pixel art/8_6.png', 'pixel art/8_7.png',
                       'pixel art/8_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 108 <= abs(math.degrees(self.angle)) < 117:
            sprites = ['pixel art/7_0.png', 'pixel art/7_1.png', 'pixel art/7_2.png', 'pixel art/7_3.png',
                       'pixel art/7_4.png', 'pixel art/7_5.png', 'pixel art/7_6.png', 'pixel art/7_7.png',
                       'pixel art/7_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 117 <= abs(math.degrees(self.angle)) < 126:
            sprites = ['pixel art/6_0.png', 'pixel art/6_1.png', 'pixel art/6_2.png', 'pixel art/6_3.png',
                       'pixel art/6_4.png', 'pixel art/6_5.png', 'pixel art/6_6.png', 'pixel art/6_7.png',
                       'pixel art/6_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 126 <= abs(math.degrees(self.angle)) < 135:
            sprites = ['pixel art/5_0.png', 'pixel art/5_1.png', 'pixel art/5_2.png', 'pixel art/5_3.png',
                       'pixel art/5_4.png', 'pixel art/5_5.png', 'pixel art/5_6.png', 'pixel art/5_7.png',
                       'pixel art/5_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 135 <= abs(math.degrees(self.angle)) < 144:
            sprites = ['pixel art/4_0.png', 'pixel art/4_1.png', 'pixel art/4_2.png', 'pixel art/4_3.png',
                       'pixel art/4_4.png', 'pixel art/4_5.png', 'pixel art/4_6.png', 'pixel art/4_7.png',
                       'pixel art/4_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 144 <= abs(math.degrees(self.angle)) < 153:
            sprites = ['pixel art/3_0.png', 'pixel art/3_1.png', 'pixel art/3_2.png', 'pixel art/3_3.png',
                       'pixel art/3_4.png', 'pixel art/3_5.png', 'pixel art/3_6.png', 'pixel art/3_7.png',
                       'pixel art/3_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 153 <= abs(math.degrees(self.angle)) < 162:
            sprites = ['pixel art/2_0.png', 'pixel art/2_1.png', 'pixel art/2_2.png', 'pixel art/2_3.png',
                       'pixel art/2_4.png', 'pixel art/2_5.png', 'pixel art/2_6.png', 'pixel art/2_7.png',
                       'pixel art/2_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 162 <= abs(math.degrees(self.angle)) < 171:
            sprites = ['pixel art/1_0.png', 'pixel art/1_1.png', 'pixel art/1_2.png', 'pixel art/1_3.png',
                       'pixel art/1_4.png', 'pixel art/1_5.png', 'pixel art/1_6.png', 'pixel art/1_7.png',
                       'pixel art/1_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 171 <= abs(math.degrees(self.angle)) < 180:
            sprites = ['pixel art/0_0.png', 'pixel art/0_1.png', 'pixel art/0_2.png', 'pixel art/0_3.png',
                       'pixel art/0_4.png', 'pixel art/0_5.png', 'pixel art/0_6.png', 'pixel art/0_7.png',
                       'pixel art/0_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 180 <= abs(math.degrees(self.angle)) < 189:
            sprites = ['pixel art/1_0.png', 'pixel art/1_1.png', 'pixel art/1_2.png', 'pixel art/1_3.png',
                       'pixel art/1_4.png', 'pixel art/1_5.png', 'pixel art/1_6.png', 'pixel art/1_7.png',
                       'pixel art/1_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 189 <= abs(math.degrees(self.angle)) < 198:
            sprites = ['pixel art/2_0.png', 'pixel art/2_1.png', 'pixel art/2_2.png', 'pixel art/2_3.png',
                       'pixel art/2_4.png', 'pixel art/2_5.png', 'pixel art/2_6.png', 'pixel art/2_7.png',
                       'pixel art/2_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 198 <= abs(math.degrees(self.angle)) < 207:
            sprites = ['pixel art/3_0.png', 'pixel art/3_1.png', 'pixel art/3_2.png', 'pixel art/3_3.png',
                       'pixel art/3_4.png', 'pixel art/3_5.png', 'pixel art/3_6.png', 'pixel art/3_7.png',
                       'pixel art/3_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 207 <= abs(math.degrees(self.angle)) < 216:
            sprites = ['pixel art/4_0.png', 'pixel art/4_1.png', 'pixel art/4_2.png', 'pixel art/4_3.png',
                       'pixel art/4_4.png', 'pixel art/4_5.png', 'pixel art/4_6.png', 'pixel art/4_7.png',
                       'pixel art/4_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 216 <= abs(math.degrees(self.angle)) < 225:
            sprites = ['pixel art/5_0.png', 'pixel art/5_1.png', 'pixel art/5_2.png', 'pixel art/5_3.png',
                       'pixel art/5_4.png', 'pixel art/5_5.png', 'pixel art/5_6.png', 'pixel art/5_7.png',
                       'pixel art/5_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 225 <= abs(math.degrees(self.angle)) < 234:
            sprites = ['pixel art/6_0.png', 'pixel art/6_1.png', 'pixel art/6_2.png', 'pixel art/6_3.png',
                       'pixel art/6_4.png', 'pixel art/6_5.png', 'pixel art/6_6.png', 'pixel art/6_7.png',
                       'pixel art/6_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 234 <= abs(math.degrees(self.angle)) < 243:
            sprites = ['pixel art/7_0.png', 'pixel art/7_1.png', 'pixel art/7_2.png', 'pixel art/7_3.png',
                       'pixel art/7_4.png', 'pixel art/7_5.png', 'pixel art/7_6.png', 'pixel art/7_7.png',
                       'pixel art/7_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 243 <= abs(math.degrees(self.angle)) < 252:
            sprites = ['pixel art/8_0.png', 'pixel art/8_1.png', 'pixel art/8_2.png', 'pixel art/8_3.png',
                       'pixel art/8_4.png', 'pixel art/8_5.png', 'pixel art/8_6.png', 'pixel art/8_7.png',
                       'pixel art/8_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 252 <= abs(math.degrees(self.angle)) < 261:
            sprites = ['pixel art/9_0.png', 'pixel art/9_1.png', 'pixel art/9_2.png', 'pixel art/9_3.png',
                       'pixel art/9_4.png', 'pixel art/9_5.png', 'pixel art/9_6.png', 'pixel art/9_7.png',
                       'pixel art/9_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 261 <= abs(math.degrees(self.angle)) < 270:
            sprites = ['pixel art/10_0.png', 'pixel art/10_1.png', 'pixel art/10_2.png', 'pixel art/10_3.png',
                       'pixel art/10_4.png', 'pixel art/10_5.png', 'pixel art/10_6.png', 'pixel art/10_7.png',
                       'pixel art/10_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, True)
        elif 270 <= abs(math.degrees(self.angle)) < 279:
            sprites = ['pixel art/9_0.png', 'pixel art/9_1.png', 'pixel art/9_2.png', 'pixel art/9_3.png',
                       'pixel art/9_4.png', 'pixel art/9_5.png', 'pixel art/9_6.png', 'pixel art/9_7.png',
                       'pixel art/9_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 279 <= abs(math.degrees(self.angle)) < 288:
            sprites = ['pixel art/8_0.png', 'pixel art/8_1.png', 'pixel art/8_2.png', 'pixel art/8_3.png',
                       'pixel art/8_4.png', 'pixel art/8_5.png', 'pixel art/8_6.png', 'pixel art/8_7.png',
                       'pixel art/8_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 288 <= abs(math.degrees(self.angle)) < 297:
            sprites = ['pixel art/7_0.png', 'pixel art/7_1.png', 'pixel art/7_2.png', 'pixel art/7_3.png',
                       'pixel art/7_4.png', 'pixel art/7_5.png', 'pixel art/7_6.png', 'pixel art/7_7.png',
                       'pixel art/7_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 297 <= abs(math.degrees(self.angle)) < 306:
            sprites = ['pixel art/6_0.png', 'pixel art/6_1.png', 'pixel art/6_2.png', 'pixel art/6_3.png',
                       'pixel art/6_4.png', 'pixel art/6_5.png', 'pixel art/6_6.png', 'pixel art/6_7.png',
                       'pixel art/6_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 306 <= abs(math.degrees(self.angle)) < 315:
            sprites = ['pixel art/5_0.png', 'pixel art/5_1.png', 'pixel art/5_2.png', 'pixel art/5_3.png',
                       'pixel art/5_4.png', 'pixel art/5_5.png', 'pixel art/5_6.png', 'pixel art/5_7.png',
                       'pixel art/5_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 315 <= abs(math.degrees(self.angle)) < 324:
            sprites = ['pixel art/4_0.png', 'pixel art/4_1.png', 'pixel art/4_2.png', 'pixel art/4_3.png',
                       'pixel art/4_4.png', 'pixel art/4_5.png', 'pixel art/4_6.png', 'pixel art/4_7.png',
                       'pixel art/4_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 324 <= abs(math.degrees(self.angle)) < 333:
            sprites = ['pixel art/3_0.png', 'pixel art/3_1.png', 'pixel art/3_2.png', 'pixel art/3_3.png',
                       'pixel art/3_4.png', 'pixel art/3_5.png', 'pixel art/3_6.png', 'pixel art/3_7.png',
                       'pixel art/3_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 333 <= abs(math.degrees(self.angle)) < 342:
            sprites = ['pixel art/2_0.png', 'pixel art/2_1.png', 'pixel art/2_2.png', 'pixel art/2_3.png',
                       'pixel art/2_4.png', 'pixel art/2_5.png', 'pixel art/2_6.png', 'pixel art/2_7.png',
                       'pixel art/2_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 342 <= abs(math.degrees(self.angle)) < 351:
            sprites = ['pixel art/1_0.png', 'pixel art/1_1.png', 'pixel art/1_2.png', 'pixel art/1_3.png',
                       'pixel art/1_4.png', 'pixel art/1_5.png', 'pixel art/1_6.png', 'pixel art/1_7.png',
                       'pixel art/1_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
        elif 351 <= abs(math.degrees(self.angle)) <= 360:
            sprites = ['pixel art/0_0.png', 'pixel art/0_1.png', 'pixel art/0_2.png', 'pixel art/0_3.png',
                       'pixel art/0_4.png', 'pixel art/0_5.png', 'pixel art/0_6.png', 'pixel art/0_7.png',
                       'pixel art/0_8.png']
            self.image = pygame.image.load(sprites[int(self.current_sprite)]).convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)

        if self.hp <= 0:
            self.image = pygame.image.load('explosion/7.png')

    def activate_effect(self, duration):
        self.effect_active = True
        self.speed = 14.0
        self.DECELERATION = 0
        self.effect_end_time = time.time() + duration

    def update(self):
        self.move()
        self.pseudo_3d()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.effect_active and time.time() > self.effect_end_time:
            self.effect_active = False

        if self.rect.right < 0:
            self.hp -= 100
        elif self.rect.top > 3240:
            self.hp -= 100
        elif self.rect.left > 5760:
            self.hp -= 100
        elif self.rect.bottom < 0:
            self.hp -= 100

        if self.hp >= 100:
            self.hp = 100
        elif self.hp <= 0:
            if self.hp_reach_zero_time is None:
                self.hp_reach_zero_time = time.time()
                explosion = Explosion(self.rect.centerx, self.rect.centery)
                camera_group.add(explosion)
            elif time.time() - self.hp_reach_zero_time >= 1:
                self.alive = False


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera_offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left': 750, 'right': 750, 'top': 450, 'bottom': 450}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        self.sky = pygame.image.load('background.png').convert()
        self.sky_rect = self.sky.get_rect(topleft=(0, 0))

        self.sky_clouds = pygame.image.load('clouds.png').convert_alpha()
        self.sky_clouds_rect = self.sky_clouds.get_rect(topleft=(0, 0))

        self.rotated_sprite_number = 2

    def center_target_camera(self, target):
        if target.rect.centerx - self.half_w < 0:
            self.offset.x = 0
        elif target.rect.centerx + self.half_w > 5760:
            self.offset.x = self.offset.x
        else:
            self.offset.x = target.rect.centerx - self.half_w
            self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        if self.camera_rect.left < self.camera_borders['left'] and self.camera_rect.top < self.camera_borders['top']:
            self.camera_rect.left = self.camera_borders['left']
            self.camera_rect.top = self.camera_borders['top']
        elif self.camera_rect.left < self.camera_borders['left'] and self.camera_rect.bottom > 2790:
            self.camera_rect.left = self.camera_borders['left']
            self.camera_rect.bottom = 2790
        elif self.camera_rect.right > 5010 and self.camera_rect.top < self.camera_borders['top']:
            self.camera_rect.right = 5010
            self.camera_rect.top = self.camera_borders['top']
        elif self.camera_rect.right > 5010 and self.camera_rect.bottom > 2790:
            self.camera_rect.right = 5010
            self.camera_rect.bottom = 2790
        elif self.camera_rect.left < self.camera_borders['left']:
            self.camera_rect.left = self.camera_borders['left']
        elif self.camera_rect.top < self.camera_borders['top']:
            self.camera_rect.top = self.camera_borders['top']
        elif self.camera_rect.right > 5010:
            self.camera_rect.right = 5010
        elif self.camera_rect.bottom > 2790:
            self.camera_rect.bottom = 2790

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, player):
        self.box_target_camera(player)

        sky_offset = self.sky_rect.topleft - self.offset
        sky_clouds_offset = self.sky_clouds_rect.topleft - self.offset

        self.display_surface.blit(self.sky, sky_offset)
        self.display_surface.blit(self.sky_clouds, sky_clouds_offset)

        for sprite in self.sprites()[self.rotated_sprite_number:]:
            offset_pos_sprite = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos_sprite)

        for sprite in self.sprites():
            rotated_image = pygame.transform.rotate(sprite.image, math.degrees(sprite.angle))
            rotated_rect = rotated_image.get_rect(center=sprite.rect.center)
            offset_pos = rotated_rect.topleft - self.offset
            screen.blit(rotated_image, offset_pos)


camera_group = CameraGroup()

player = Plane()

camera_group.add(player)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.images = ['explosion/0.png', 'explosion/1.png', 'explosion/2.png', 'explosion/3.png', 'explosion/4.png',
                       'explosion/5.png', 'explosion/6.png', 'explosion/7.png']
        self.current_sprite = 0
        self.image = pygame.image.load(self.images[int(self.current_sprite)]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = 0

    def animation(self):
        if self.current_sprite >= len(self.images) - 1:
            self.current_sprite = 7
            self.kill()
        else:
            self.current_sprite += 0.2

        self.image = pygame.image.load(self.images[int(self.current_sprite)]).convert_alpha()

    def update(self):
        self.animation()


class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self, x, y, x_feint, y_feint, plane_img):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.x_feint = x_feint
        self.y_feint = y_feint
        self.plane_img = plane_img
        self.image = pygame.image.load(self.plane_img).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8
        self.shoot_cooldown = 0
        self.angle = 0.0
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 10.0
        self.acceleration = 5
        self.rotation_speed = 0.02
        self.DECELERATION = 0.05
        self.gravity = 1.5
        self.current_sprite = 0
        self.last_direction = pygame.Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 50
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle, 'enemy_bullet.png')
            camera_group.add(bullet)
            enemy_bullets_group.add(bullet)

    def ai_move(self):
        dx = player.rect.x - self.rect.x + self.x_feint
        dy = player.rect.y - self.rect.y + self.y_feint

        target_distance = math.hypot(dx, dy)
        target_angle = math.atan2(dx, dy) - math.radians(90)

        if abs(target_angle - self.angle) > self.rotation_speed:
            if target_angle > self.angle:
                self.angle += self.rotation_speed
            else:
                self.angle -= self.rotation_speed
        else:
            self.angle = target_angle

        self.speed += self.acceleration

        self.speed = max(-10.0, min(self.speed, 10.0))

        self.velocity.x = math.cos(self.angle) * self.speed
        self.velocity.y = -math.sin(self.angle) * self.speed

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if math.degrees(target_angle) - 5 < math.degrees(self.angle) < math.degrees(
                target_angle) + 5 and target_distance < 700:
            self.shoot()

        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            player.hp -= 20
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            camera_group.add(explosion)
            self.kill()

        if self.rect.right < 0:
            self.angle = 0
        elif self.rect.top > 3240:
            self.angle = math.radians(90)
        elif self.rect.left > 5760:
            self.angle = math.radians(180)
        elif self.rect.bottom < 0:
            self.angle = math.radians(270)

    def update(self):
        self.ai_move()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, img):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.img = img
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.velocity = pygame.Vector2(0, 0)
        self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

    def update(self):
        self.velocity.x = math.cos(self.angle) * self.speed
        self.velocity.y = -math.sin(self.angle) * self.speed

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.right < 0 or self.rect.left > 5760 or self.rect.bottom < 0 or self.rect.top > 3240:
            self.kill()

        for player_bullet in player_bullets_group:
            if pygame.sprite.spritecollide(player_bullet, enemy_plane_group, True, pygame.sprite.collide_mask):
                global score, score_multiplier
                score_multiplier += 1
                score += (10 * score_multiplier)
                explosion = Explosion(self.rect.centerx, self.rect.centery)
                camera_group.add(explosion)
                player_bullet.kill()

        for enemy_bullet in enemy_bullets_group:
            if pygame.sprite.spritecollide(enemy_bullet, player_group, False, pygame.sprite.collide_mask):
                player.hp -= 10
                enemy_bullet.kill()


class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('missile.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0.0
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 15.0
        self.acceleration = 5
        self.rotation_speed = 0.01
        self.direction = direction
        self.mask = pygame.mask.from_surface(self.image)
        self.path = []

    def ai_move(self):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y

        target_distance = math.hypot(dx, dy)
        target_angle = math.atan2(dx, dy) - math.radians(90)

        if abs(target_angle - self.angle) > self.rotation_speed:
            if target_angle > self.angle:
                self.angle += self.rotation_speed
            else:
                self.angle -= self.rotation_speed
        else:
            self.angle = target_angle

        self.speed += self.acceleration

        self.speed = max(-15.0, min(self.speed, 15.0))

        self.velocity.x = math.cos(self.angle) * self.speed
        self.velocity.y = -math.sin(self.angle) * self.speed

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.direction == 'left':
            if self.rect.x > player.rect.x + 200:
                explosion = Explosion(self.rect.centerx, self.rect.centery)
                camera_group.add(explosion)
                self.kill()

        if self.direction == 'right':
            if self.rect.x < player.rect.x - 200:
                explosion = Explosion(self.rect.centerx, self.rect.centery)
                camera_group.add(explosion)
                self.kill()

        for missile in missile_group:
            if pygame.sprite.spritecollide(missile, player_group, False, pygame.sprite.collide_mask):
                player.hp -= 10
                explosion = Explosion(self.rect.centerx, self.rect.centery)
                camera_group.add(explosion)
                missile.kill()

    def update(self):
        self.ai_move()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        pygame.sprite.Sprite.__init__(self)
        self.powerup_type = powerup_type
        self.image = pygame.image.load(f'powerups/{self.powerup_type}.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        for powerup in powerups_group:
            if pygame.sprite.spritecollide(powerup, player_group, False, pygame.sprite.collide_mask):
                if powerup.powerup_type == 'health':
                    player.hp = 100
                elif powerup.powerup_type == 'speed':
                    player.activate_effect(5)
                    print('speed powerup')
                self.kill()


class HealthBar:
    def __init__(self, x, y, w, h, hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = hp
        self.max_hp = 100

    def draw(self, surface):
        self.hp = player.hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, (60, 0, 80), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, (180, 0, 255), (self.x, self.y, self.w * ratio, self.h))


health_bar = HealthBar(0, 0, SCREEN_WIDTH, 5, player.hp)

player_group = pygame.sprite.Group()
enemy_plane_group = pygame.sprite.Group()
player_bullets_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
powerups_group = pygame.sprite.Group()

player_group.add(player)

current_time = pygame.time.get_ticks()
last_call_time = current_time

current_time_score = pygame.time.get_ticks()
last_call_time_score = current_time_score


def generate_enemy_plane():
    x = [-100, 2880, 5760, 3340, 2880, 5860]
    y = [-100, -100, -100, -100, 3340, 3340]
    x_feint = random.randint(0, 100)
    y_feint = random.randint(0, 100)
    planes = ['f18.png', 'jas39.png', 'mig29.png']
    plane_img_index = random.randint(0, 2)
    coordinates_index = random.randint(0, 5)
    plane_img = planes[plane_img_index]
    return EnemyPlane(x[coordinates_index], y[coordinates_index], x_feint, y_feint, plane_img)


def generate_missile():
    x = [-100, 5860]
    y = [-100, 3340]
    direction = ''
    coordinates_index = random.randint(0, 1)
    if coordinates_index == 0:
        direction = 'left'
    elif coordinates_index == 1:
        direction = 'right'
    return Missile(x[coordinates_index], y[coordinates_index], direction)


def generate_powerup():
    x = 0
    y = 0
    powerup_types = ['health', 'speed']
    powerup_type = powerup_types[random.randint(0, 1)]
    camera_edges = [camera_group.camera_rect.left - 600, camera_group.camera_rect.right + 600,
                    camera_group.camera_rect.top - 300, camera_group.camera_rect.bottom + 300]
    camera_edge = camera_edges[random.randint(0, 3)]
    if camera_edge == camera_edges[0]:
        x = camera_edge
        y = random.randint(camera_edges[2], camera_edges[3])
    elif camera_edge == camera_edges[1]:
        x = camera_edge
        y = random.randint(camera_edges[2], camera_edges[3])
    elif camera_edge == camera_edges[2]:
        x = random.randint(camera_edges[0], camera_edges[1])
        y = camera_edge
    elif camera_edge == camera_edges[3]:
        x = random.randint(camera_edges[0], camera_edges[1])
        y = camera_edge

    return PowerUp(x, y, powerup_type)


def set_score_multiplier():
    global score_multiplier
    score_multiplier -= 1
    if score_multiplier < 0:
        score_multiplier = 0


def restart_game():
    player.alive = True
    player.rect.center = (2880, 1620)
    player.hp = 100
    player.shoot_cooldown = 0
    player.angle = 0.0
    player.velocity = pygame.Vector2(0, 0)
    player.speed = 10.0
    player.hp_reach_zero_time = None

    for enemy in enemy_plane_group:
        enemy.kill()
    for player_bullet in player_bullets_group:
        player_bullet.kill()
    for enemy_bullet in enemy_bullets_group:
        enemy_bullet.kill()
    for missile in missile_group:
        missile.kill()
    for powerup in powerups_group:
        powerup.kill()

    global score, score_multiplier
    score = 0
    score_multiplier = 0


def draw_menu():
    bg = pygame.image.load('buttons/main_menu_background.png').convert()
    screen.blit(bg, (0, 0))

    play_button = Button(960, 909, play_img_main_menu, 0.6)
    quit_button = Button(1887, 1048, quit_img_main_menu, 0.6)

    if play_button.draw():
        global main_menu
        main_menu = False

    if quit_button.draw():
        global running
        running = False


def draw_score():
    with open('score.txt', 'r') as file:
        number_str = file.read()
    score_in_file = int(number_str)

    play_again_button = Button(960, 640, play_img_main_menu, 1)
    quit_button = Button(960, 754, quit_img, 1)
    game_over_text = Button(960, 352, game_over_img, 1)

    global score
    font_path = 'upheavtt.ttf'
    font = pygame.font.Font(font_path, 56)

    if score > score_in_file:
        score_text = font.render(f'Your new best score: {score}!', True, 'white')
        score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 475))
        screen.blit(score_text, score_text_rect)
        with open('score.txt', 'w') as file:
            file.write(str(score))
    elif score < score_in_file:
        score_text = font.render(f'Your score: {score}', True, 'white')
        score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 475))
        screen.blit(score_text, score_text_rect)

    with open('score.txt', 'r') as file:
        number_str = file.read()
    score_in_file = int(number_str)

    font = pygame.font.Font(font_path, 25)
    best_score_text = font.render(f'Your best score: {score_in_file}', True, 'white')
    best_score_text_rect = best_score_text.get_rect(center=(SCREEN_WIDTH / 2, 525))
    screen.blit(best_score_text, best_score_text_rect)

    game_over_text.draw()

    if play_again_button.draw():
        restart_game()

    if quit_button.draw():
        global main_menu
        main_menu = True


while running:

    clock.tick(FPS)

    if main_menu:
        draw_menu()
    elif not player.alive:
        draw_score()
    else:
        camera_group.update()
        camera_group.custom_draw(player)

        current_time = pygame.time.get_ticks()
        current_time_score = pygame.time.get_ticks()

        if current_time - last_call_time >= 1000 and len(enemy_plane_group) <= 8:
            new_enemy_plane = generate_enemy_plane()
            camera_group.add(new_enemy_plane)
            enemy_plane_group.add(new_enemy_plane)
            camera_group.rotated_sprite_number += 1
            player.hp += 5
            last_call_time = current_time

        if current_time_score - last_call_time_score >= 10000 and len(powerups_group) <= 1:
            set_score_multiplier()
            missile = generate_missile()
            camera_group.add(missile)
            missile_group.add(missile)
            camera_group.rotated_sprite_number += 1
            player.hp += 10
            powerup = generate_powerup()
            camera_group.add(powerup)
            powerups_group.add(powerup)
            last_call_time_score = current_time_score

        if player.alive:
            draw_text()
            health_bar.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if main_menu:
                    main_menu = False
                else:
                    main_menu = True
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
