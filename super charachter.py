import os
import sys
import pygame

size = width, height = 1600, 1000
screen = pygame.display.set_mode(size)
FPS = 50
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
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    global max_width
    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'earth': load_image('single_earth.png'),
    'upper_back': load_image('upper.png'),
    'down_back': load_image('down.png'),
    'platform': load_image('platform.png')
}

tile_width = tile_height = 100


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


player_image = load_image('hero1.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.move_x = 15
        self.move_y = 15

    def change(self, direc):
        if direc == 1:
            if tile_height * self.pos_y + self.move_y - 10 >= 0:
                self.move_y -= 10
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)
        if direc == 2:
            if tile_width * self.pos_x + self.move_x + 10 < max_width * tile_width:
                self.move_x += 10
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)
        if direc == 3:
            if tile_height * self.pos_y + self.move_y + 10 < max_width * tile_width:
                self.move_y += 10
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)
        if direc == 4:
            if tile_width * self.pos_x + self.move_x - 10 >= 0:
                self.move_x -= 10
                self.rect = self.image.get_rect().move(
                    tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)



all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()



def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '-':
                Tile('upper_back', x, y)
            elif level[y][x] == '@':
                Tile('down_back', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '_':
                Tile('down_back', x, y)
            elif level[y][x] == '=':
                Tile('platform', x, y)
            elif level[y][x] == '+':
                Tile('earth', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


player, level_x, level_y = generate_level(load_level('level1.txt'))
BackGround = Background(os.path.join('data', 'back.png'), [0, 0])
up = False
right = False
down = False
left = False
while True:
    for event in pygame.event.get():
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        if event.type == pygame.QUIT:
            terminate()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.change(1)
    if keys[pygame.K_RIGHT]:
        player.change(2)
    if keys[pygame.K_DOWN]:
        player.change(3)
    if keys[pygame.K_LEFT]:
        player.change(4)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
