import sys

import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 32

COUNT_DEAD = COUNT_HIT = COUNT_SHOT = COUNT_TAKE_BONUS = COUNT_BRAKE_BLOCK = 0

with open('statistic.txt') as f:
    f = f.read().split()
    COUNT_DEAD += int(f[0])
    COUNT_HIT += int(f[1])
    COUNT_SHOT += int(f[2])
    COUNT_TAKE_BONUS += int(f[3])
    COUNT_BRAKE_BLOCK += int(f[4])

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)

imgBrick = pygame.image.load('images\\sandbagBrown.png')
imgTanksRed = [
    pygame.transform.scale(pygame.image.load('images\\red_tank_1_lvl.png'), (32, 32)),
    pygame.transform.scale(pygame.image.load('images\\red_tank_2_lvl.png'), (32, 32)),
    pygame.transform.scale(pygame.image.load('images\\red_tank_3_lvl.png'), (32, 32)),
]
imgTanksRed = [
    pygame.transform.rotate(imgTanksRed[0], 180),
    pygame.transform.rotate(imgTanksRed[1], 180),
    pygame.transform.rotate(imgTanksRed[2], 180)

]
imgTanksBlue = [
    pygame.transform.scale(pygame.image.load('images\\blue_tank_1_lvl.png'), (32, 32)),
    pygame.transform.scale(pygame.image.load('images\\blue_tank_2_lvl.png'), (32, 32)),
    pygame.transform.scale(pygame.image.load('images\\blue_tank_3_lvl.png'), (32, 32))
]

imgTanksBlue = [
    pygame.transform.rotate(imgTanksBlue[0], 180),
    pygame.transform.rotate(imgTanksBlue[1], 180),
    pygame.transform.rotate(imgTanksBlue[2], 180)

]
imgBangs = [
    pygame.transform.scale(pygame.image.load('images/explosion1.png'), (32, 32)),
    pygame.transform.scale(pygame.image.load('images/explosion2.png'), (32, 32)),
    pygame.transform.scale(pygame.image.load('images/explosion3.png'), (32, 32)),
    pygame.transform.scale(pygame.image.load('images/explosion4.png'), (32, 32)),
    pygame.transform.scale(pygame.image.load('images/explosion5.png'), (32, 32))
]
imgBulletRed = [
    pygame.transform.scale(pygame.image.load('images/bulletRed1_outline.png'), (7, 12)),
    pygame.transform.scale(pygame.image.load('images/bulletRed2_outline.png'), (7, 15)),
    pygame.transform.scale(pygame.image.load('images/bulletRed3_outline.png'), (11.5, 15))
]
imgBulletBlue = [
    pygame.transform.scale(pygame.image.load('images/bulletBlue1_outline.png'), (7, 12)),
    pygame.transform.scale(pygame.image.load('images/bulletBlue2_outline.png'), (7, 15)),
    pygame.transform.scale(pygame.image.load('images/bulletBlue3_outline.png'), (11.5, 15))
]

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = [""
                  ""
                  ""
                  ""
                  ""
                  ""
                  "               BATTLE TANKS"]

    fon = pygame.image.load('images/start_background.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    start_button = pygame.Rect(300, 300, 200, 50)  # прямоугольник для кнопки начать
    statistics_button = pygame.Rect(300, 380, 200, 50)  # прямоугольник для кнопки начать
    exit_button = pygame.Rect(300, 460, 200, 50)  # прямоугольник для кнопки выйти

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return "start"
                elif exit_button.collidepoint(mouse_pos):
                    terminate()
                    return "exit"
                elif statistics_button.collidepoint(mouse_pos):
                    statistics_result = statistics_screen()  # Call the statistics_screen function
                    if statistics_result == "back":  # Check if the result is "back" to transition back to start screen
                        return "statistics_back"

        pygame.draw.rect(screen, (0, 0, 0), start_button)  # рисуем кнопку начать
        pygame.draw.rect(screen, (0, 0, 0), statistics_button)  # рисуем кнопку статистики
        pygame.draw.rect(screen, (0, 0, 0), exit_button)  # рисуем кнопку выйти

        font = pygame.font.Font(None, 30)
        start_text = font.render("Начать игру", True, (255, 255, 255))
        statistics_text = font.render("Статистика", True, (255, 255, 255))
        exit_text = font.render("Выйти", True, (255, 255, 255))
        screen.blit(start_text, (320, 320))  # позиция текста на кнопке начать
        screen.blit(statistics_text, (320, 400))  # позиция текста на кнопке начать
        screen.blit(exit_text, (320, 480))  # позиция текста на кнопке выйти

        pygame.display.flip()
        clock.tick(FPS)


def statistics_screen():
    global COUNT_DEAD, COUNT_HIT, COUNT_SHOT, COUNT_TAKE_BONUS, COUNT_BRAKE_BLOCK
    with open('statistic.txt') as f:
        f = f.read().split()
        COUNT_DEAD += int(f[0])
        COUNT_HIT += int(f[1])
        COUNT_SHOT += int(f[2])
        COUNT_TAKE_BONUS += int(f[3])
        COUNT_BRAKE_BLOCK += int(f[4])

    # Create an exit button rectangle
    back_button = pygame.Rect(50, 380, 200, 50)

    # Choose a font and size for the text
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_button.collidepoint(mouse_pos):  # Check if the "Назад" button is clicked
                    return "back"

        screen.fill((0, 0, 0))  # Clear the screen

        text_surface_dead = font.render(f"Кол-во игр: {COUNT_DEAD}", True, text_color)
        screen.blit(text_surface_dead, (50, 50))

        text_surface_hit = font.render(f"Кол-во попаданий: {COUNT_HIT}", True, text_color)
        screen.blit(text_surface_hit, (50, 100))

        text_surface_shot = font.render(f"Кол-во выстрелов: {COUNT_SHOT}", True, text_color)
        screen.blit(text_surface_shot, (50, 150))

        text_surface_take_bonus = font.render(f"Кол-во собранных бонусов: {COUNT_TAKE_BONUS}", True, text_color)
        screen.blit(text_surface_take_bonus, (50, 200))

        text_surface_brake_block = font.render(f"Кол-во сломанных блоков: {COUNT_BRAKE_BLOCK}", True, text_color)
        screen.blit(text_surface_brake_block, (50, 250))
        back_text = font.render("Назад", True, (255, 255, 255))
        screen.blit(back_text, (70, 390))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def dead_screen(player_name):
    with open('statistic.txt', 'w') as f:
        f.write(f'{COUNT_DEAD} {COUNT_HIT} {COUNT_SHOT} {COUNT_TAKE_BONUS} {COUNT_BRAKE_BLOCK}')
    intro_text = [""
                  ""
                  ""
                  ""
                  ""
                  ""
                  "               GAME OVER"]

    fon = pygame.image.load('images/finish_background.png')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 36)
    text = font.render(f"{player_name} танк был повержен!", True, (255, 0, 0))
    screen.blit(text, (300, 280))
    pygame.display.flip()

    exit_button = pygame.Rect(300, 380, 200, 50)  # прямоугольник для кнопки выйти
    ui_instance = UI()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if exit_button.collidepoint(mouse_pos):
                    terminate()
                    return "exit"

        pygame.draw.rect(screen, (0, 0, 0), exit_button)  # рисуем кнопку выйти

        font = pygame.font.Font(None, 30)
        exit_text = font.render("Выйти", True, (255, 255, 255))
        screen.blit(exit_text, (320, 400))  # позиция текста на кнопке выйти
        pygame.display.flip()
        clock.tick(FPS)


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                tank_width = 22
                screen_width = 800

                if i % 2 == 0:
                    x_position = 5 + i * 70
                else:
                    x_position = screen_width - (5 + tank_width + (i - 1) * 70) - 20

                pygame.draw.rect(screen, obj.color, (x_position, 5, 22, 22))

                text = fontUI.render(str(obj.rank + 1), 1, 'black')
                rect = text.get_rect(center=(x_position + 11, 5 + 11))
                screen.blit(text, rect)

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(x_position + 32, 5 + 11))
                screen.blit(text, rect)
                i += 1


class Tank:
    global COUNT_HIT, COUNT_SHOT, COUNT_DEAD

    MOVE_SPEED = [1.5, 2, 3]
    BULLET_SPEED = [4, 6, 4]
    BULLET_DAMAGE = [1, 1, 2]
    SHOT_DELAY = [50, 40, 40]

    def __init__(self, color, px, py, direct, keyList, bulletList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.hp = 5
        self.shotTimer = 0

        self.moveSpeed = 2
        self.shotDelay = 60
        self.bulletSpeed = 10
        self.bulletDamage = 1
        self.bulletList = bulletList

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

        self.rank = 0

        if self.color == 'red':
            self.image = pygame.transform.rotate(imgTanksRed[self.rank], -self.direct * 90)
        elif self.color == 'blue':
            self.image = pygame.transform.rotate(imgTanksBlue[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        global COUNT_SHOT
        if self.color == 'red':
            self.image = pygame.transform.rotate(imgTanksRed[self.rank], -self.direct * 90)
        elif self.color == 'blue':
            self.image = pygame.transform.rotate(imgTanksBlue[self.rank], -self.direct * 90)

        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.moveSpeed = self.MOVE_SPEED[self.rank]
        self.shotDelay = self.SHOT_DELAY[self.rank]
        self.bulletSpeed = self.BULLET_SPEED[self.rank]
        self.bulletDamage = self.BULLET_DAMAGE[self.rank]

        oldX, oldY = self.rect.topleft

        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for obj in objects:
            if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            COUNT_SHOT += 1

            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage,
                   self.bulletList[self.rank],
                   self.direct)
            print(dx, dy)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def draw(self):
        screen.blit(self.image, self.rect)

    def damage(self, value):
        global COUNT_HIT, COUNT_DEAD
        COUNT_HIT += 1

        self.hp -= value
        if self.hp <= 0:
            COUNT_DEAD += 1
            objects.remove(self)
            dead_screen(self.color)


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage, image, direct):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
        self.image = image
        self.direct = direct
        self.image = pygame.transform.rotate(self.image, -self.direct * 90)

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        break

    def draw(self):
        screen.blit(self.image, pygame.Rect(self.px, self.py, 2, 5))


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        screen.blit(image, rect)


class Block:
    global COUNT_BRAKE_BLOCK

    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        screen.blit(imgBrick, self.rect)

    def damage(self, value):
        global COUNT_BRAKE_BLOCK
        COUNT_BRAKE_BLOCK += 1

        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


class Bonus:
    global COUNT_TAKE_BONUS

    imgBonusesRang = [
        pygame.transform.scale(pygame.image.load('images/crateWood.png'), (32, 32)),
        pygame.transform.scale(pygame.image.load('images/crateWood_side.png'), (32, 32)),
        pygame.transform.scale(pygame.image.load('images/crateWood_2.png'), (32, 32)),
        pygame.transform.scale(pygame.image.load('images/crateWood_side_2.png'), (32, 32))
    ]
    imgBonusesHP = [
        pygame.transform.scale(pygame.image.load('images/crateMetal.png'), (32, 32)),
        pygame.transform.scale(pygame.image.load('images/crateMetal_side.png'), (32, 32)),
        pygame.transform.scale(pygame.image.load('images/crateMetal_2.png'), (32, 32)),
        pygame.transform.scale(pygame.image.load('images/crateMetal_side_2.png'), (32, 32))
    ]

    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'
        if bonusNum == 0:
            self.image = self.imgBonusesRang[0]
            self.imgList = self.imgBonusesRang
        else:
            self.image = self.imgBonusesHP[0]
            self.imgList = self.imgBonusesHP
        self.rect = self.image.get_rect(center=(px, py))

        self.timer = 600
        self.bonusNum = bonusNum
        self.frame = 0

    def update(self):
        global COUNT_TAKE_BONUS
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    COUNT_TAKE_BONUS += 1

                    if obj.rank < len(imgTanksRed) - 1:
                        obj.rank += 1
                        objects.remove(self)
                        break
                elif self.bonusNum == 1:
                    obj.hp += 1
                    objects.remove(self)
                    break
        self.frame += 0.05

    def draw(self):
        image = self.imgList[int(self.frame) % 4]
        screen.blit(image, self.rect)


bullets = []
objects = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE), imgBulletBlue)
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER),
     imgBulletRed)
ui = UI()

for _ in range(50):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True

        if not fined:
            break

    Block(x, y, TILE)

bonusTimer = 180
start_screen()
play = True
while play:
    with open('statistic.txt', 'w') as f:
        f.write(f'{COUNT_DEAD} {COUNT_HIT} {COUNT_SHOT} {COUNT_TAKE_BONUS} {COUNT_BRAKE_BLOCK}')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    if bonusTimer > 0:
        bonusTimer -= 1
    else:
        Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, 1))
        bonusTimer = randint(120, 240)

    for bullet in bullets:
        bullet.update()
    for obj in objects:
        obj.update()
    ui.update()

    fon_game = pygame.image.load('images/background.png')
    screen.blit(fon_game, (0, 0))
    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()
    ui.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
