#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Licensing agreement:
#   Do as thou wilt and harm none
#
#
"""
    pygame_color_chart.py

        Created for the sole purpose of displaying all Pygame predefined
        colors (sorted and indexed).

        All other functionality added for my own amusement.
"""
# -------- IMPORTS --------

import pygame
from pygame.locals import *

from pygame.color import THECOLORS as COLORS
COL = [C for C in COLORS]; COL.sort()


# -------- CONSTANTS --------
TILE_WIDTH  = 40
TILE_HEIGHT = 40

NUM_X_TILES = 30
NUM_Y_TILES = 40

SCREEN_WIDTH  = TILE_WIDTH*NUM_X_TILES
SCREEN_HEIGHT = TILE_HEIGHT*(len(COLORS)//NUM_X_TILES)+ TILE_HEIGHT

BGC = (236,244,251)



class Tile(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, n=None):
        super().__init__()

        color_tile = pygame.Surface((width//2, height//2)).convert()
        color_tile.fill(color)
        color_rect = color_tile.get_rect()

        self.image = pygame.Surface((width, height)).convert_alpha()
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.image.fill((0,0,0,0))
        color_rect.centerx = self.rect.centerx
        self.image.blit(color_tile, color_rect)

        if n:
            font = pygame.font.SysFont('cooper black', 12)
            label_surf = font.render(str(n), False, COLORS['black'])
            label_rect = label_surf.get_rect()
            label_rect.left = self.rect.left + label_rect.width//2
            label_rect.bottom = self.rect.bottom - label_rect.height//2
            self.image.blit(label_surf, label_rect)

        self.rect.topleft = (x, y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, int(SCREEN_HEIGHT+TILE_HEIGHT/2)))
    pygame.display.set_caption('Pygame Colors')
    clock = pygame.time.Clock()

    tile_list = pygame.sprite.Group()
    shadow_list = pygame.sprite.Group()

    x, y, n = 0, TILE_HEIGHT/2, 0
    for i in range(len(COL)):
        tile = Tile(COLORS[COL[i]], x, y, TILE_WIDTH, TILE_HEIGHT, i)
        tile_list.add(tile)
        if n < NUM_X_TILES:
            n += 1
            x += TILE_WIDTH
        elif n >= NUM_X_TILES:
            n = 0
            x = 0
            y += TILE_HEIGHT

    x, y, n = 0, TILE_HEIGHT/2, 0
    shadows = []
    for i in range(len(COL)):
        tile = Tile((140,140,140), x, y, TILE_WIDTH, TILE_HEIGHT)
        tile.shadow_pos = [(x+4,y+3),(x-4,y+3),(x-4,y-3),(x+4,y-3)]
        tile.orig_pos = (x, y)
        shadow_list.add(tile)
        shadows.append(tile)
        if n < NUM_X_TILES:
            n += 1
            x += TILE_WIDTH
        elif n >= NUM_X_TILES:
            n = 0
            x = 0
            y += TILE_HEIGHT
    
    done = False
    i = 0
    j = 0
    mod = 0
    modKey = 'centered'
    MODDIC={K_0:0,K_1:1,K_2:2,K_3:3,K_4:4,K_5:5,K_6:6,K_7:7,K_8:8,K_9:9}
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True

                elif event.key in MODDIC:
                    mod=MODDIC[event.key]
                    for s in shadows:
                        modKeyD = {'left' :s.shadow_pos[0],'down' :s.shadow_pos[1],
                                   'right':s.shadow_pos[2],'up'   :s.shadow_pos[3]}
                        if modKey in modKeyD:
                            (x,y) = modKeyD[modKey]
                            if modKey == 'left':
                                (x,y) = (x+mod,y+mod)
                            elif modKey == 'down':
                                (x,y) = (x-mod,y+mod)
                            elif modKey == 'right':
                                (x,y) = (x-mod,y-mod)
                            else:
                                (x,y) = (x+mod,y-mod)
                            s.rect.topleft = (x,y)

                elif event.key == K_LEFT:
                    modKey = 'left'
                    for s in shadows:
                        s.rect.topleft = s.shadow_pos[0]
                elif event.key == K_DOWN:
                    modKey = 'down'
                    for s in shadows:
                        s.rect.topleft = s.shadow_pos[1]
                elif event.key == K_RIGHT:
                    modKey = 'right'
                    for s in shadows:
                        s.rect.topleft = s.shadow_pos[2]
                elif event.key == K_UP:
                    modKey = 'up'
                    for s in shadows:
                        s.rect.topleft = s.shadow_pos[3]
                elif event.key == K_SPACE:
                    for s in shadows:
                        modKey = 'centered'
                        s.rect.topleft = s.orig_pos


        screen.fill(BGC)
        shadow_list.draw(screen)
        tile_list.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__=='__main__':main()
