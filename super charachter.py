import os
import sys
import pygame

size = 1600, 1000
screen = pygame.display.set_mode(size)
FPS = 50
clock = pygame.time.Clock()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'earth': load_image('single_earth.png'),
    'upper_back': load_image('upper.png'),
    'middle_back': load_image('mid.png'),
    'down_back': load_image('down.png')
}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


player_image = load_image('hero.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '-':
                Tile('upper_back', x, y)
            elif level[y][x] == '|':
                Tile('middle_back', x, y)
            elif level[y][x] == '@':
                Tile('down_back', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '_':
                Tile('down_back', x, y)
            elif level[y][x] == '+':
                Tile('earth', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()

player, level_x, level_y = generate_level(load_level('level1.txt'))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        tiles_group.draw(screen)
        player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)