import os
import sys
import pygame

size = WIDTH, HEIGHT = 1600, 1000
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
max_width = 0
pygame.init()
count_keys = 3


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


level_map = ['level1.txt', 'level2.txt', 'level3.txt']
heart_pos = []


class Level:
    def __init__(self):
        global order
        self.order = order
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()

        self.generate_level()

    def load_level(self, filename):  # Загрузка уровней
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            lvl_map = [line.strip() for line in mapFile]

        global max_width
        max_width = max(map(len, lvl_map))

        return list(map(lambda x: x.ljust(max_width, '.'), lvl_map))

    def generate_level(self):  # Создание уровня
        level = self.load_level(level_map[self.order])
        cactus_pos = []
        key_pos = []
        for y in range(len(level)):
            for x in range(len(level[y])):
                x_x = tile_size * x
                y_y = tile_size * y
                if level[y][x] == '=':
                    Tile('platform', (x_x, y_y), self.visible_sprites, self.collision_sprites)
                if level[y][x] == '+':
                    Tile('earth', (x_x, y_y), self.visible_sprites, self.collision_sprites)
                if level[y][x] == '|':
                    Sprite('cactus', (x_x, y_y), self.visible_sprites, self.sprites)
                    cactus_pos.append((x_x, y_y))
                if level[y][x] == '-':
                    Sprite('key', (x_x, y_y), self.visible_sprites, self.sprites)
                    key_pos.append((x_x, y_y))
                if level[y][x] == '@':
                    self.player = Player((x_x, y_y), self.visible_sprites, self.active_sprites,
                                         self.collision_sprites, self.sprites, cactus_pos, key_pos, heart_pos,
                                         load_image('running_character.png'), 8, 1,
                                         load_image('running_character1.png'),
                                         load_image('jumping_charachter.png'), 3, 1)
                if level[y][x] == '*':
                    for i in range(3):
                        if i > 0:
                            x_x += 50
                        Sprite('heart', (x_x, y_y), self.visible_sprites, self.sprites)
                        heart_pos.append((x_x, y_y))
                global width_x
                width_x = x * tile_size

    def run(self):
        self.active_sprites.update()
        self.visible_sprites.camera_configure(self.player)


tile_images = {
    'earth': load_image('single_earth.png'),
    'platform': load_image('platform.png')
}
sprite_images = {
    'heart': load_image('heart.png'),
    'cactus': load_image('cactus.png'),
    'key': load_image('key.png')
}

tile_size = 100
width_x = 0


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos, group1, group2):
        super().__init__(group1, group2)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect(topleft=pos)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos, group1, group2):
        super().__init__(group1, group2)
        self.image = sprite_images[tile_type]
        self.rect = self.image.get_rect(topleft=pos)


player_image_right = load_image('hero1.png')
player_image_left = load_image('hero2.png')
did_ran_right = False
did_ran_left = False


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group1, group2, collision_sprites, sprites, cactus_pos, key_pos, pos_heart, sheet_run_right,
                 columns_run, rows_run, sheet_run_left, sheet_jump, columns_jump, rows_jump):
        super().__init__(group1, group2)
        self.image = player_image_right
        self.rect = self.image.get_rect(topleft=pos)
        self.y = self.rect.y
        self.x = self.rect.x
        self.on_ground = False
        self.on_start_y, self.on_start_x = False, False

        self.frames_run_right = []
        self.cut_sheet_right(sheet_run_right, columns_run, rows_run)
        self.cur_frame_run_right = 0

        self.frames_run_left = []
        self.cut_sheet_left(sheet_run_left, columns_run, rows_run)
        self.cur_frame_run_left = 0

        self.frames_jump = []
        self.cut_sheet_jump(sheet_jump, columns_jump, rows_jump)
        self.cur_frame_jump = 0

        self.direction = pygame.math.Vector2()
        self.speed = 10
        self.gravity_speed = 1.3
        self.jump_speed = 25
        self.collision_sprites = collision_sprites
        self.sprites, self.visible_sprites = sprites, group1
        self.cactus_pos, self.key_pos, self.heart_pos = cactus_pos, key_pos, pos_heart
        self.count, self.count_heart, self.count_key = 0, -1, 0

    def input(self):  # Получение информации о том какая из кнопок нажата / зажата
        global width_x
        keys = pygame.key.get_pressed()

        if self.rect.x < width_x - tile_size // 10 and keys[pygame.K_RIGHT]:
            self.direction.x = 1
            if self.count_key == len(self.key_pos) \
                    and self.rect.x >= (width_x - tile_size // 10) - 10:
                pygame.mixer.music.load('data/' + 'win.mp3')
                pygame.mixer.music.play(0)
                game_screen('win.png')
        elif 0 < self.rect.x and keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_ground:
            pygame.mixer.music.load('data/'+'jump.mp3')
            pygame.mixer.music.play(0)
            self.direction.y = -self.jump_speed

    def vertical_c(self):  # Вертикальное столкновение героя
        for tile in self.collision_sprites.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = tile.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                if self.direction.y < 0:
                    self.rect.top = tile.rect.bottom
                    self.direction.y = 0

        for sprite in self.sprites.sprites():  # Столкновение с кактусом
            sprite_pos = sprite.rect.x, sprite.rect.y
            for pos_c in self.cactus_pos:
                if pos_c == sprite_pos:
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top
                            self.direction.y = 0
                            self.on_ground = True
                            self.on_start_y = True
        global count_keys
        for sprite in self.sprites.sprites():  # Собираем ключи
            sprite_pos = sprite.rect.x, sprite.rect.y
            for pos_k in self.key_pos:
                if pos_k == sprite_pos:
                    if sprite.rect.colliderect(self.rect):
                        self.count_key += 1
                        sprite.kill()
                        count_keys -= 1
                        pygame.mixer.music.load('data/' + 'key.mp3')
                        pygame.mixer.music.play(0)

        if self.on_ground and self.direction.y != 0:
            self.on_ground = False

    def draw_keys(self):  # отрисовка кол-ва ключей которые еще не собраны
        for i in range(3 - self.count_key):
            key = load_image('key.png')
            screen.blit(key, (i * tile_size, 0))

    def horizontal_c(self):  # Горизонтальное столкновение героя
        collision = False
        for tile in self.collision_sprites.sprites():
            if tile.rect.colliderect(self.rect):
                if self.direction.x < 0:
                    self.rect.left = tile.rect.right
                if self.direction.x > 0:
                    self.rect.right = tile.rect.left

        for sprite in self.sprites.sprites():  # Столкновение с кактусом
            sprite_pos = sprite.rect.x, sprite.rect.y
            for pos in self.cactus_pos:
                if pos == sprite_pos:
                    if sprite.rect.colliderect(self.rect):
                        collision = True
                        if self.direction.x < 0:
                            self.rect.left = sprite.rect.left + 75
                            self.on_start_x = True
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.right - 75
                            self.on_start_x = True
        if collision:  # Уменьшаем кол-во жизней
            self.count_heart += 1
            for heart in self.sprites:
                sprite_pos = heart.rect.x, heart.rect.y
                if self.count_heart < 2:
                    pos = self.heart_pos[self.count_heart]
                    if pos == sprite_pos:
                        heart.kill()
                        pygame.mixer.music.load('data/' + 'heart.mp3')
                        pygame.mixer.music.play(0)

    def gravity(self):  # Гравитация
        self.direction.y += self.gravity_speed
        self.rect.y += self.direction.y
        if self.rect.y >= self.y + tile_size * 20:  # Возвращение на начальную позицию при подении в яму
            self.count_heart += 1
            self.direction.y = -self.jump_speed // 2
            self.rect = self.rect = self.image.get_rect(topleft=(self.x, self.y))
            for heart in self.sprites:  # Уменьшаем кол-во жизней
                sprite_pos = heart.rect.x, heart.rect.y
                if self.count_heart < 2:
                    pos = self.heart_pos[self.count_heart]
                    if pos == sprite_pos:
                        heart.kill()
                        pygame.mixer.music.load('data/' + 'heart.mp3')
                        pygame.mixer.music.play(0)

    def start(self):  # Возвращение на начальную позицию при столковении со спрайтом кактуса
        if self.count_heart > 1:
            pygame.mixer.music.load('data/' + 'game_over.mp3')
            pygame.mixer.music.play(0)
            game_screen('game_over.png')
        if self.on_start_y:
            self.direction.y = -self.jump_speed // 2
            self.count += 1
            if self.count == 2:
                self.rect = self.image.get_rect(topleft=(self.x, self.y))
                self.count = 0
            self.on_start_y = False
        if self.on_start_x:
            self.direction.y = -self.jump_speed // 2
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.on_start_x = False

    def cut_sheet_right(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_run_right.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet_left(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_run_left.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def cut_sheet_jump(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames_jump.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def animate(self):
        keys = pygame.key.get_pressed()
        global did_ran_right
        global did_ran_left
        if keys[pygame.K_RIGHT]:
            self.cur_frame_run_right = (self.cur_frame_run_right + 1) % len(self.frames_run_right)
            self.image = self.frames_run_right[self.cur_frame_run_right]
            did_ran_right = True
        if keys[pygame.K_LEFT]:
            self.cur_frame_run_left = (self.cur_frame_run_left + 1) % len(self.frames_run_left)
            self.image = self.frames_run_left[self.cur_frame_run_left]
            did_ran_left = True
        if not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            if did_ran_right:
                self.image = player_image_right
                did_ran_right = False
            if did_ran_left:
                self.image = player_image_left
                did_ran_left = False

    def update(self):
        self.input()
        self.rect.x += self.direction.x * self.speed
        self.horizontal_c()
        self.gravity()
        self.start()
        self.vertical_c()
        self.animate()
        self.draw_keys()


borders_camera = {
    'left': 0,
    'up': 50,
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
        if player.rect.x >= 0 and player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.x <= width_x - tile_size * 2 and player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            if player.rect.top >= 700:
                self.camera_rect.top = (player.rect.top - 650)
            else:
                self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        self.offset = pygame.math.Vector2(
            self.camera_rect.left - borders_camera['left'],
            self.camera_rect.top - borders_camera['up'])

        for sprite in self.sprites():
            sprite_pos = sprite.rect.x, sprite.rect.y
            if sprite_pos in heart_pos:
                for pos in heart_pos:
                    if pos == sprite_pos:
                        self.display_surface.blit(sprite.image, (sprite.rect.topleft + self.offset // tile_size))
            else:
                self.display_surface.blit(sprite.image, sprite.rect.topleft - self.offset)


def start_screen(name):  # Стартовый экран
    pygame.mixer.music.load(name)
    pygame.mixer.music.play(-1)
    if name == 'data/' + 'sound_start.mp3':
        pygame.mixer.music.set_volume(0.3)
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                pygame.mixer.music.pause()
                return  # начинаем игру
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos_m = event.pos
                if 453 < pos_m[0] < 1135 and 697 < pos_m[1] < 723:
                    pygame.mixer.music.pause()
                    return
        pygame.display.flip()
        clock.tick(FPS)


start_screen('data/' + 'sound_start.mp3')


def game_screen(name):  # Финальный экран
    global order
    fon = pygame.transform.scale(load_image(name), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render('CLICK ENTER TO START', True, (100, 255, 100))
    text_x = 550
    text_y = 900
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)
    pygame.display.flip()
    start = False
    if name == 'win.png' and order < 2:
        order += 1
    elif name == 'win.png' and order >= 2:
        order = 0
        start_screen('data/' + 'won.mp3')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                start = True
            if start:
                BackGround = Background(os.path.join('data', 'back.png'), [0, 0])
                pygame.display.set_caption('Super character')
                lvl = Level()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
                    pygame.mouse.set_visible(False)
                    # Мышка отключена, чтобы не мешать игровому процессу (* тк она не используется)
                    screen.fill([255, 255, 255])
                    screen.blit(BackGround.image, BackGround.rect)
                    lvl.run()
                    pygame.display.update()
                    clock.tick(FPS)
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


BackGround = Background(os.path.join('data', 'back.png'), [0, 0])
pygame.display.set_caption('Super character')
order = 0
lvl = Level()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    pygame.mouse.set_visible(False)  # Мышка отключена, чтобы не мешать игровому процессу (* тк она не используется)
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    lvl.run()
    pygame.display.update()
    clock.tick(FPS)
