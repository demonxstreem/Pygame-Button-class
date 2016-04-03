#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Licensing agreement:
#   Do as thou wilt and harm none
#
#
# -------- IMPORTS --------

import pygame, itertools, time, sys
from pygame.locals import *

from pygame.color import THECOLORS as COLORS
COL = [C for C in COLORS]; COL.sort()


# -------- CONSTANTS --------
# main surface dimensions
SCREEN_WIDTH  = 680
SCREEN_HEIGHT = 420

# button dimensions
# and space between buttons
BTN_WIDTH  = 85
BTN_HEIGHT = 35
BTN_SPACE  = 15

# main surface background color
BG_COLOR = COLORS[COL[170]]



class Button:
    """
           Pygame Button class

           Constructor accepts two optional positional arguments:
               title:  string:  --> text to be displayed on button
               size:    tuple:  --> button width & height
               
           and (12)? optional keyword arguments:
               align_text         string:  --> align title (left, center, right)
               font_name          string:  --> title font name
               font_size             int:  --> title font size
               unselected          tuple:  --> button title (rgb) color
               selected            tuple:  --> mouse over title (rgb) color
               amount              float:  --> used to calc button highlight
               button_color        tuple:  --> button (rgb) color
               button_color_sel:   tuple:  --> mouse over button (rgb) color
               highlight_button     bool:  --> if True highlight button on mouse over
               shadow_color        tuple:  --> button shadow (rgb) color
               offset              tuple:  --> used to calc shadow position
               v_attr             string:  --> set virtual (x,y) attribute

           Each button is assigned a unique identifier and tag.
            (Useful for event handling)

           Methods:
               draw()       :surface:  pygame surface:  --> draw button to surface
               rendTxt()    :no args:                   --> renders/returns button title surf/rect
               getColors()  :    txt:            bool:  --> return title or button color
               getSurf()    :no args:                   --> return main surface
               getRect()    :no args:                   --> return main surface rect
               makeButton() :no args:                   --> return shadow and/or button surf/rect
               clicked()    :no args:
        """
        
    nextid  = itertools.count().__next__
    hovered = False
    _clicked = None

    def __init__(self, title='button', size=[60,20], **kwargs):
        
        self.id = Button.nextid()
        
        if title == 'button':
            self.title = '%s %i' % (title, self.id)
        else: self.title = title

        self.tag = self.title

        self.size = size
        self.pos = kwargs.get('pos', [0,0])

        self.align_text = kwargs.get('align_text', 'center')
        font_name = kwargs.get('font_name', None)
        font_size = kwargs.get('font_size', int(((size[0]+size[1])/3))-len(title))
        self.font_unselected = kwargs.get('unselected', (215, 255, 255))
        self.font_selected = kwargs.get('selected', (225, 255, 255))
        self.font = pygame.font.SysFont(font_name, font_size)

        amount = kwargs.get('amount', 1.5)
        self.button_color = kwargs.get('button_color', (70, 130, 180))
        color = list(self.button_color)
        self.button_color_sel = kwargs.get('button_color_sel', tuple([min(255, int(c*amount)) for c in color]))
        self.highlight_button = kwargs.get('highlight_button', False)
        self.shadow_color = kwargs.get('shadow_color', (99, 184, 255))
        self.offset = kwargs.get('offset', [3,2])
        self.v_attr = kwargs.get('v_attr', 'topleft')

        self.getSurf()
        self.getRect()


    def draw(self, surface):
        align = self.align_text
        button = self.makeButton()
        titleS, titleR = self.rendTxt()
        if align == 'center': titleR.center = button[0][1].center
        elif align == 'left':
            titleR.left = button[0][1].left+4
            titleR.centery = button[0][1].centery
        elif align == 'right':
            titleR.right = button[0][1].right-4
            titleR.centery = button[0][1].centery
        button[0][0].blit(titleS, titleR)

        if len(button) == 2:
            self.surf.blit(button[1][0], button[1][1])
        self.surf.blit(button[0][0], button[0][1])

        surface.blit(self.surf, self.rect)


    def rendTxt(self):
        title_surf = self.font.render(self.title, True, self.getColors())
        return title_surf, title_surf.get_rect()


    def getColors(self, txt=True):
        if self.hovered:
            if txt: return self.font_selected
            else:   return self.button_color_sel
        else:
            if txt: return self.font_unselected
            else:   return self.button_color


    def getSurf(self):
        size, offset = self.size, self.offset
        if 0 not in offset:
            self.surf = pygame.Surface((size[0]+offset[0], size[1]+offset[1])).convert_alpha()
            self.surf.fill((0,0,0,0))
        else:
            self.surf = pygame.Surface(size).convert()


    def getRect(self):
        pos, v_attr = self.pos, self.v_attr
        self.rect = self.surf.get_rect()

        if   v_attr == 'center': self.rect.center = pos
        elif v_attr == 'topleft': self.rect.topleft = pos
        elif v_attr == 'topright': self.rect.topright = pos
        elif v_attr == 'bottomleft': self.rect.bottomleft = pos
        elif v_attr == 'bottomright': self.rect.bottomright = pos


    def makeButton(self):
        button=[]
        size, offset = self.size, self.offset
        button_surf = pygame.Surface(size).convert()
        if self.highlight_button:
            button_surf.fill(self.getColors(False))
        else:
            button_surf.fill(self.button_color)
        button_rect = button_surf.get_rect()
        button.append([button_surf, button_rect])

        if 0 not in offset:
            shadow_surf = pygame.Surface(size).convert()
            shadow_surf.fill(self.shadow_color)
            shadow_rect = shadow_surf.get_rect()
            (x,y) = button_rect.topleft; (x,y) = (x+offset[0], y+offset[1])
            shadow_rect.topleft = (x,y)
            button.append([shadow_surf, shadow_rect])

        return button


    def clicked(self):
        if not self._clicked:
            self._clicked = pygame.time.get_ticks()
            return False
        else:
            seconds = (pygame.time.get_ticks()-self._clicked)/1000
            if seconds > .5: self._clicked = None
        return True
            

        


def main():
    pygame.init() # initialize pygame and create main display surface
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Button class test')

    titles = ['Quit', 'New', 'Reset'] # button titles

    events = {} # initialize events dict and add custom events
    events[0] = Quit_event  = pygame.USEREVENT + 1
    events[1] = New_event   = pygame.USEREVENT + 2
    events[2] = Reset_event = pygame.USEREVENT + 3
    buttons = [] # initialize button list

    x, y = 30, 30 # set start position
    for title in titles:
        buttons.append( # define button and add it to the button list
            Button(title, (BTN_WIDTH, BTN_HEIGHT), pos=(x,y), font_name='broadway', font_size=25,
                   unselected=COLORS[COL[405]], selected=COLORS[COL[66]], highlight_button=True, amount=.7)
        )
        y += (BTN_HEIGHT + BTN_SPACE) # increment vert
    

        
    done = False
    while not done: # mainloop
        
        for evt in pygame.event.get(): # event handler loop
            # exit mainloop if user closes the application
            # or clicks on the escape key
            if evt.type ==  QUIT:
                done = True
            elif evt.type == KEYDOWN and evt.key == K_ESCAPE:
                done = True

            # check event queue for custom events
            elif evt.type == Quit_event:
                print('The Quit button was clicked')
            elif evt.type == New_event:
                print('The New button was clicked')
            elif evt.type == Reset_event:
                print('The Reset button was clicked')

            elif evt.type == MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos() # mouse position
                # check for collisions (mouse click) button
                for button in buttons:
                    if button.rect.collidepoint(m_pos) & pygame.mouse.get_pressed()[0] == 1:
                        # select action, call function, etc... by button ID
                        if button.id   == 0: # Quit
                            done = True
                        elif button.id == 1: # New
                            pass
                        elif button.id == 2: # reset
                            pass
                        

        # clear screen
        screen.fill(BG_COLOR)

        # check for collisions (mouse over) button
        # and set button and/or text color
        # check for collisions (mouse click) button
        # and post custom events to event queue
        for button in buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()): # (mouse over)
                if pygame.mouse.get_pressed()[0] == 1: # (mouse clicked)
                    # must wait .5 seconds between clicks
                    if not button.clicked():
                        pygame.event.post(
                            pygame.event.Event(events[button.id])
                        )
                button.hovered = True
            else:
                button.hovered = False

            # draw buttons using newly set colors
            button.draw(screen)

        # update screen
        pygame.display.flip()
        


if __name__=='__main__':
    
    main()
    pygame.quit()
    sys.exit()
