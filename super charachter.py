import os
import sys
import pygame

size = width, height = 1600, 1000
screen = pygame.display.set_mode(size)
FPS = 20
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
    'platform': load_image('platform.png'),
    'mid_back': load_image('mid.png')
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
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.move_x = 0
        self.move_y = 0
        self.pos_x, self.pos_y = self.rect.x, self.rect.y

    def change(self, direc):
        px, py = self.move_x, self.move_y
        x1, x2 = 0, 0
        y1, y2 = 0, 0
        if direc == 1:
            if tile_height * self.pos_y + self.move_y - 200 >= 0:
                self.move_y -= 200
                for hero in player_group:
                    x1, y1 = hero.rect.x, hero.rect.y
                for sprite in tiles_group:
                    x2, y2 = sprite.rect.x, sprite.rect.y
                    if y1 - self.move_y - tile_height <= y2 - self.move_y and y1 >= y2 and \
                            (0 <= abs(x1 - x2) < tile_height):
                        self.move_y = py
                        self.move_x = px
        if direc == 2:
            if tile_width * self.pos_x + self.move_x + 10 < max_width * tile_width:
                self.move_x += 10
                for hero in player_group:
                    x1, y1 = hero.rect.x, hero.rect.y
                for sprite in tiles_group:
                    x2, y2 = sprite.rect.x, sprite.rect.y
                    if x1 + self.move_x + tile_width >= x2 + self.move_x and x1 <= x2 and \
                            (0 <= abs(y1 - y2) < tile_height):
                        self.move_x = px - 10
                        self.move_y = 0
                self.gravity(tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)
        if direc == 3:
            if tile_width * self.pos_x + self.move_x - 10 >= 0:
                self.move_x -= 10
                for hero in player_group:
                    x1, y1 = hero.rect.x, hero.rect.y
                for sprite in tiles_group:
                    x2, y2 = sprite.rect.x, sprite.rect.y
                    if x1 - self.move_x - tile_width <= x2 - self.move_x and x1 >= x2 and \
                            (0 <= abs(y1 - y2) < tile_height):
                        self.move_x = px + 10
                        self.move_y = 0
                self.gravity(tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)
        if direc == 4:
            if tile_height * self.pos_y + self.move_y - 200 >= 0 and \
                    tile_width * self.pos_x + self.move_x + 10 < max_width * tile_width:
                self.move_y -= 200
                self.move_x += 10
                for hero in player_group:
                    x1, y1 = hero.rect.x, hero.rect.y
                for sprite in tiles_group:
                    x2, y2 = sprite.rect.x, sprite.rect.y
                    if (y1 - self.move_y - tile_height <= y2 - self.move_y and y1 >= y2 and
                            (0 <= abs(x1 - x2) < tile_height)) and (x1 - self.move_x - tile_width <= x2 - self.move_x
                                                                    and x1 >= x2 and (0 <= abs(y1 - y2) < tile_height)):
                        self.move_x = px + 10
                        self.move_y = py
                self.gravity(tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)
        if direc == 5:
            if tile_height * self.pos_y + self.move_y - 200 >= 0 and \
                    tile_width * self.pos_x + self.move_x - 10 >= 0:
                self.move_y -= 200
                self.move_x -= 10
                for hero in player_group:
                    x1, y1 = hero.rect.x, hero.rect.y
                for sprite in tiles_group:
                    x2, y2 = sprite.rect.x, sprite.rect.y
                    if (y1 - self.move_y - tile_height <= y2 - self.move_y and y1 >= y2 and
                            (0 <= abs(x1 - x2) < tile_height)) and (x1 + self.move_x + tile_width >= x2 + self.move_x
                                                                    and x1 <= x2 and (0 <= abs(y1 - y2) < tile_height)):
                        self.move_x = px - 10
                        self.move_y = py
                self.gravity(tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x + self.move_x, tile_height * self.pos_y + self.move_y)

    def gravity(self, x, y):
        self.move_y = 0
        x1, y = x / tile_width, y // tile_height
        if x1 % 1 >= 0.5:
            x1 = int(x1 + 1)
        else:
            x1 = int(x1)
        try:
            coord = level_map[y + 1][x1]
            self.pos_y = y
            if coord == '.':
                self.pos_y = y + 1
                self.rect = self.image.get_rect().move(x / tile_width * tile_width, tile_height * (y + 1))
        except IndexError:
            for sprite in player_group:
                sprite.kill()


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if x == 0 and y == 7:
                new_player = Player(x, y)
            elif level[y][x] == '=':
                Tile('platform', x, y)
            elif level[y][x] == '+':
                Tile('earth', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


level_map = load_level('level1.txt')
player, level_x, level_y = generate_level(level_map)
BackGround = Background(os.path.join('data', 'back.png'), [0, 0])
up = False
right = False
down = False
left = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    keys = pygame.key.get_pressed()
    player.gravity(player.rect.x, player.rect.y)
    if keys[pygame.K_UP]:
        player.change(1)
    if keys[pygame.K_RIGHT]:
        player.change(2)
    if keys[pygame.K_LEFT]:
        player.change(3)
    if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
        player.change(4)
    if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
        player.change(5)
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)