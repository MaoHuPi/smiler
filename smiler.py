DES = '''
Developed by MaoHuPi
Copyright: 2023 © MaoHuPi
App Name: Smiler
Version: 1.0.0
'''

import os
import math
import cv2
import pygame
path = '.' if os.path.isfile('./'+os.path.basename(__file__)) else os.path.dirname(os.path.abspath(__file__))

[W, H] = [400, 400]
pygame.init()
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Smiler')
icon = pygame.image.load(f'{path}/image/icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

def rad(deg): return deg/360*(math.pi*2)
def deg(rad): return rad/(math.pi*2)*360
def cv2pg(image, rgbChannel=True):
    image = pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], 'BGR' if rgbChannel else 'RGB')
    return (image)
def pg2cv(image, bgrChannel=True):
    image = pygame.surfarray.array3d(image)
    image = image.transpose([1, 0, 2])
    if bgrChannel:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return (image)
def drawImage(surface, image, position, resize=False, rotation=False, origin='lt'):
        position = list(position)
        size = image.get_size()
        image = image.convert_alpha()
        if resize != False:
            resize = [int(n) for n in resize]
            image = pygame.transform.scale(image, resize)
            size = resize
        if rotation != False:
            image = pygame.transform.rotate(image, rotation)  # deg
            r = rad(rotation % 90)
            size = [
                math.sin(r)*size[1] + math.cos(r)*size[0],
                math.sin(r)*size[0] + math.cos(r)*size[1]
            ]
        origin = 'cc' if origin == 'c' else origin
        for i in range(2):
            if origin[i] in ['a', 'lt'[i]]:
                pass
            elif origin[i] in ['e', 'rb'[i]]:
                position[i] -= size[i]
            elif origin[i] in ['c', 'm']:
                position[i] -= size[i]/2
        surface.blit(image, position)
def textImage(text='', size=W*0.06, bold=False, fgc=(0, 0, 0), bgc=False, fontName='arial', isSysFont=True):
    size = int(size)
    # render image
    text = str(text)
    font = (pygame.font.SysFont if isSysFont else pygame.font.Font)(
        fontName, size, bold=bold)
    if bgc:
        image = font.render(text, True, fgc, bgc)
    else:
        image = font.render(text, True, fgc)
    return(image)

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
mask = pygame.image.load(f'{path}/image/smile.png')
def smile(name):
    img = cv2.imread(name)
    img_pg = cv2pg(img)
    board = pygame.Surface((img_pg.get_width(), img_pg.get_height()), pygame.SRCALPHA).convert_alpha()
    board.blit(img_pg, (0, 0))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faceList = detector.detectMultiScale(img_gray)
    for(x, y, w, h) in faceList:
        x = x + w/2
        y = y + h/2
        w = max(w, h)
        h = w
        x = x - w/2
        y = y - h/2
        [x, y, w, h] = [int(x), int(y), int(w), int(h)]
        drawImage(board, mask, (x, y), (w, h), False, 'lt')
    nameList = name.replace('\\', '/').split('/')
    if nameList[-1].find('.') > -1:
        nameList[-1] = nameList[-1].split('.')
        nameList[-1].pop()
        nameList[-1] = '.'.join(nameList[-1])
    name = '/'.join(nameList)
    pygame.image.save(board, f'{name}_smile.png')
    # img = pg2cv(board)
    # cv2.imshow('img', img)

drawImage(win, mask, (W/2, H/2), (W*0.8, H*0.8), False, 'c')
white = pygame.Surface((W, H), pygame.SRCALPHA).convert_alpha()
white.fill((255, 255, 255, 200))
win.blit(white, (0, 0))
title = textImage('Smiler', W*0.1, False, (0, 0, 0), False)
label = textImage('please drop an image file.', W*0.06, False, (0, 0, 0), False)
copyright = textImage('2023 © MaoHuPi', W*0.04, False, (0, 0, 0), False)
drawImage(win, title, (W/2, H*0.4), False, False, 'c')
drawImage(win, label, (W/2, H*0.6), False, False, 'c')
drawImage(win, copyright, (W-10, H-10), False, False, 'rb')

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.DROPFILE:
            path = event.file
            print(path)
            smile(path)
        if event.type == pygame.QUIT:
            pygame.display.quit()
            run = False
            # exit()
    if run:
        pygame.display.update()
        clock.tick(20)