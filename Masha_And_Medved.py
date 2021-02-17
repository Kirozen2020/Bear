from pygame import *
import pygame
import sys

pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Маша и Миша')
VIOLET = (110,40,212)
LIGHT_BLUE = (0,201,255)
pygame.mixer.music.load('soundtrack.mp3')
pygame.mixer.music.play()
bear_image = pygame.image.load('bear.gif')
bear_image2 = pygame.transform.flip(bear_image, True, False)
font = pygame.font.SysFont('Comic Sans Ms', 24)
clock = pygame.time.Clock()

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, name):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def mouse_collision(self):
        is_collide = self.rect.collidepoint(pygame.mouse.get_pos())
        return is_collide
    def get_name(self):
        return self.name

class Masha(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('masha.gif')
        self.rect = self.image.get_rect()
    def update(self):
        m = pygame.mouse.get_pos()
        if m[0] > 10 and m[0] < 550:
            self.rect.x = m[0]
        if m[1] > 300 and m[1] < 550:
            self.rect.y = m[1]

class Bear(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('bear.gif')
        self.rect = self.image.get_rect()
        self.direction = 'left'
        self.speed = 10
    def reflect(self):
        self.image = pygame.transform.flip(self.image, True, False)
    def slow(self):
        self.speed -= 1
        return self.speed
    def update(self):
        if self.direction == "right":
            self.rect.move_ip(self.speed, 0)
            if self.rect.right > 600:
                self.reflect()
                self.direction = "left"
        else:
            self.rect.move_ip(-self.speed, 0)
            if self.rect.left < 30:
                self.reflect()
                self.direction = "right"

class Jar(pygame.sprite.Sprite):
    def __init__(self, hero, enemy, score = 0):
        super().__init__()
        self.image = pygame.image.load('jar.gif')
        self.rect = self.image.get_rect()
        self.fly = False
        self.hero = hero
        self.enemy = enemy
        self.score = score
        self.away = pygame.mixer.Sound('away.wav')
        self.target = pygame.mixer.Sound('target.ogg')
        self.signal = False
    def update(self):
        if self.fly:
            self.rect.move_ip(0, -5)
            if self.rect.top < 0:
                self.fly = False
                self.target.play()
            if self.rect.colliderect(self.enemy.rect):
                self.fly = False
                self.away.play()
                self.score += 1
                enemy_speed = self.enemy.slow()
                if enemy_speed == 0:
                    self.signal = True
        else:
            self.rect.x = self.hero.rect.x - 20
            self.rect.y = self.hero.rect.y + 40
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                self.fly = True


class Backgraund(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('bg.gif')
        self.rect = self.image.get_rect()

class TextObject(pygame.sprite.Sprite):
    def __init__(self, x, y, text_func, color):
        super().__init__()
        self.pos = (x,y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont('Comic Sans MS', 24)
    def update(self):
        self.image, self.rect = self.get_surface(self.text_func())
    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

def is_done(end_signal = False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
    if end_signal:
        return True
    return False

def render_group(group):
    window.fill(VIOLET)
    group.update()
    group.draw(window)
    pygame.display.update()
    clock.tick(60)

def buttons_pressed():
    choosed = ""
    for button in button_list.sprites():
        if button.mouse_collision():
            choosed = button.get_name()

    click = pygame.mouse.get_pressed()
    if click[0] == 1:
        if choosed == 'Выход':
            pygame.quit()
            sys.exit()
        if choosed == 'Опции':
            game_rules()
        if choosed == 'Игра':
            game()


def get_info():
    info = pygame.Surface((600, 600))
    info.fill(VIOLET)
    info.blit(bear_image, (440, 40))
    info.blit(bear_image2, (40, 40))
    info.blit(font.render('Твоя задача - скормить медведю 10 банок воренья', False, LIGHT_BLUE), (10, 250))
    info.blit(font.render('чем больше он съел, тем тяжелее ему убегать',False, LIGHT_BLUE), (30, 280))
    info.blit(font.render('огонь - ЛКМ', False, LIGHT_BLUE), (200, 350))
    info.blit(font.render('движение - курсор мыши', False, LIGHT_BLUE), (180, 420))
    info.blit(font.render('выход в меню - ESC', False, LIGHT_BLUE), (170, 500))
    return info

def game_rules():
    info = get_info()
    while True:
        if is_done():
            break
        window.blit(info, (0, 0))
        pygame.display.update()
        clock.tick(60)

def game():
    masha = Masha()
    bear = Bear()
    jar = Jar(masha, bear)
    bg = Backgraund()
    score_label = TextObject(5, 0, lambda: 'Съел: {}'.format(jar.score), LIGHT_BLUE)
    game_sprites = pygame.sprite.Group(bg, masha, bear, jar, score_label)
    pygame.mouse.set_visible(False)
    while True:
        if is_done(jar.signal):
            break
        render_group(game_sprites)
    pygame.mouse.set_visible(True)



close_b = Button(160, 400, 'b1.gif', 'Выход')
game_b = Button(170, 250, 'b2.gif', 'Игра')
options_b = Button(180, 130, 'b3.gif', 'Опции')

button_list = pygame.sprite.Group(close_b, game_b, options_b)

while True:
    if is_done():
        break
    buttons_pressed()
    render_group(button_list)