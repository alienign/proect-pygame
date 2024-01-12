import os
import sys
import pygame

size = WIDTH, HEIGHT = 1600, 1000
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
max_width = 0
pygame.init()


class Background(pygame.sprite.Sprite):  # Фонновое изображение
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def load_image(name, colorkey=None):  # Загрузка изображения
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
    return image


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()

        self.generate_level()

    def load_level(self, filename):  # Загрузка уровней
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        global max_width
        max_width = max(map(len, level_map))

        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self):  # Создание уровня
        level = self.load_level('level1.txt')
        for y in range(len(level)):
            for x in range(len(level[y])):
                x_x = tile_size * x
                y_y = tile_size * y
                if level[y][x] == '=':
                    Tile('platform', (x_x, y_y), self.visible_sprites, self.collision_sprites)
                if level[y][x] == '+':
                    Tile('earth', (x_x, y_y), self.visible_sprites, self.collision_sprites)
                if level[y][x] == '@':
                    self.player = Player((x_x, y_y), self.visible_sprites, self.active_sprites, self.collision_sprites)
                global width_x
                width_x = x * tile_size

    def run(self):
        self.active_sprites.update()
        self.visible_sprites.camera_configure(self.player)


tile_images = {
    'earth': load_image('single_earth.png'),
    'platform': load_image('platform.png')
}

tile_size = 100
width_x = 0


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos, group1, group2):
        super().__init__(group1, group2)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect(topleft=pos)


player_image = load_image('hero1.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group1, group2, collision_sprites):
        super().__init__(group1, group2)
        self.image = player_image
        self.rect = self.image.get_rect(topleft=pos)
        self.y = self.rect.y
        self.on_ground = False

        self.direction = pygame.math.Vector2()
        self.speed = 10
        self.gravity_speed = 1.3
        self.jump_speed = 25
        self.collision_sprites = collision_sprites

    def input(self):  # Получение информации о том какая из кнопок нажата / зажата
        global width_x
        keys = pygame.key.get_pressed()

        if self.rect.x < width_x - tile_size // 10 and keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif 0 < self.rect.x and keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_ground:
            self.direction.y = -self.jump_speed

    def vertical_c(self):  # Вертикальное столкновение героя
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

        if self.on_ground and self.direction.y != 0:
            self.on_ground = False

    def horizontal_c(self):  # Горизонтальное столкновение героя
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left

    def gravity(self):  # Гравитация
        self.direction.y += self.gravity_speed
        self.rect.y += self.direction.y
        # if self.rect.y >= self.y + tile_size * 10:
        # print('Game over')

    def update(self):
        self.input()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_c()
        self.gravity()
        self.vertical_c()


borders_camera = {
    'left': 0,
    'up': 100,
    'right': 200,
    'down': 50
}


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(100, 300)

        cam_left = borders_camera['left']
        cam_up = borders_camera['up']
        cam_right = self.display_surface.get_size()[0] - (cam_left + borders_camera['right'])
        cam_down = self.display_surface.get_size()[1] - (cam_up + borders_camera['down'])

        self.camera_rect = pygame.Rect(cam_left, cam_up, cam_right, cam_down)

    def camera_configure(self, player):  # Регулировка камеры
        if player.rect.x > 0 and player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.x <= width_x - tile_size * 2 and player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        self.offset = pygame.math.Vector2(
            self.camera_rect.left - borders_camera['left'],
            self.camera_rect.top - borders_camera['up'])

        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect.topleft - self.offset)


def start_screen():
    intro_text = ["CУПЕР ГЕРОЙ", "",
                  "Тут должны быть правила"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font(None, 50)
    text = font.render("Начать!", True, (100, 255, 100))
    text_x = 25
    text_y = 300
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                return  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_m = event.pos
                if 15 < pos_m[0] < 160 and 270 < pos_m[1] < 370:
                    return
        pygame.display.flip()
        clock.tick(FPS)

start_screen()
def terminate():
    pygame.quit()
    sys.exit()


BackGround = Background(os.path.join('data', 'back.png'), [0, 0])
pygame.display.set_caption('Super charachter')
lvl = Level()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    lvl.run()
    pygame.display.update()
    clock.tick(FPS)
