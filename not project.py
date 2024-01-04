import sys

import pygame

w = int(input())
hue = int(input())
if 0 <= hue <= 360 and 4 <= w <= 100 and type(w) is int and type(hue) is int and w % 4 == 0:
    size = 300, 300
    left_top = (150 - w / 2, 150 - w / 2)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    hsva_color = (hue, 100, 75, 100)
    color = pygame.Color(0, 0, 0)
    color.hsva = hsva_color


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, color, (150 - w / 2, 150 - w / 2, w, w), 0)
        hsva_color = (hue, 100, 100, 100)
        color1 = pygame.Color(0, 0, 0)
        color1.hsva = hsva_color
        pygame.draw.polygon(screen, color1, [(150 - w / 2, 150 - w / 2), (150, 150 - w), (150 + w, 150 - w), (150 + w / 2, 150 - w / 2)], 0)
        hsva_color = (hue, 100, 50, 100)
        color2 = pygame.Color(0, 0, 0)
        color2.hsva = hsva_color
        pygame.draw.polygon(screen, color2, [(150 + w, 150 - w), (150 + w / 2, 150 - w / 2), (150 + w / 2, 150 + w / 2), (150 + w, 150)], 0)
        pygame.display.flip()
else:
    print('Некорретный ввод')

