import os
import sys
import pygame

size = width, height = 1600, 1000
screen = pygame.display.set_mode(size)
FPS = 7
clock = pygame.time.Clock()
max_width = 0


class Background(pygame.sprite.Sprite):  # Фонновое изображение
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


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
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


tile_images = {
    'earth': load_image('single_earth.png'),
    'upper_back': load_image('upper.png'),
    'down_back': load_image('down.png'),
    'platform': load_image('platform.png'),
    'mid_back': load_image('mid.png')
}

tile_width = tile_height = 100


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


player_image = load_image('hero1.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5,
                                               tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0],
                                               tile_height * (self.pos[1]))


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '-':
                Tile('upper_back', x, y)
            elif level[y][x] == '?':
                Tile('mid_back', x, y)
            elif level[y][x] == '@':
                Tile('down_back', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
            elif level[y][x] == '_':
                Tile('down_back', x, y)
            elif level[y][x] == '=':
                Tile('platform', x, y)
            elif level[y][x] == '+':
                Tile('earth', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < level_x - 1 and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    player = None
    level_map = load_level('level1.txt')
    hero, level_x, level_y = generate_level(level_map)
    BackGround = Background(os.path.join('data', 'back.png'), [0, 0])
    up = False
    right = False
    left = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            move(hero, 'up')
        if keys[pygame.K_RIGHT]:
            move(hero, 'right')
        if keys[pygame.K_LEFT]:
            move(hero, 'left')
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
