import os

import pygame
import sys

FPS = 50
WIDTH = 800
HEIGHT = 800
size = 800, 800
screen = pygame.display.set_mode(size)
max_width = 0

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data1/" + filename
        # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
    global max_width
    max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
player_image = load_image('mar.png')

tile_width = tile_height = 50

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
clock = pygame.time.Clock()



class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)

    def change(self, direc):
        if direc == 1:
            if self.pos_y - 1 >= 0:
                self.pos_y -= 1
        if direc == 2:
            if self.pos_x + 1 < max_width:
                self.pos_x += 1
        if direc == 3:
            if self.pos_y + 1 < max_width:
                self.pos_y += 1
        if direc == 4:
            if self.pos_x - 1 >= 0:
                self.pos_y -= 1
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + 15, tile_height * self.pos_y + 5)


# основной персонаж
player = None


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

level_name = input()
player, level_x, level_y = generate_level(load_level(level_name))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            player.change(1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            player.change(2)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            player.change(3)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            player.change(4)
        tiles_group.draw(screen)
        player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)