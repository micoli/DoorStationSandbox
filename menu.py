#ADV-MENU 1.2.1
#(C) 2009 Robin Wellner
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

import pygame
from pygame.locals import *
from math import *


class sli(object):
    __slots__ = ('index', 'max', 'min')
    def __init__ (self, tup):
        self.index = tup[0]
        self.min = tup[1]
        self.max = tup[2]

class chk(object):
    __slots__ = ('checked')
    def __init__ (self, checked):
        self.checked = checked

class menu:
    __slots__ = ('Surface','Items','Xoffset','Xoffset2','Yoffset','itemheight','totalheight','boxwidth','Font','focus','frontcolor','halfcolor','disabledcolor','backcolor','additionalFunc')
    def __init__(self,Surface, Items, Xoffset, Xoffset2, Yoffset, itemheight, totalheight, boxwidth, Font, focus=0,frontcolor=(255, 255, 255),halfcolor=(200, 200, 200),disabledcolor=(155, 155, 155),backcolor=(200, 200, 200),additionalFunc=None):
        self.Surface=Surface
        self.Items=Items
        self.Xoffset=Xoffset
        self.Xoffset2=Xoffset2
        self.Yoffset=Yoffset
        self.itemheight=itemheight
        self.totalheight=totalheight
        self.boxwidth=boxwidth
        self.Font=Font
        self.focus=focus
        self.frontcolor=frontcolor
        self.halfcolor=halfcolor
        self.disabledcolor=disabledcolor
        self.backcolor=backcolor
        self.additionalFunc=additionalFunc

    def run(self):
        Clock = pygame.time.Clock()
        sliderdata = {}
        for item in self.Items:
            if item[2] == 'slider':
                sliderdata[item[1]] = sli(item[3])
            elif item[2] == 'checkbox':
                sliderdata[item[1]] = chk(item[3])
        while True:
            Clock.tick(10)
            keystate = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'exit', sliderdata
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return 'cancel', sliderdata
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button==1:
                        if self.Xoffset < event.pos[0] < self.Xoffset+self.boxwidth and self.Yoffset < event.pos[1] < self.totalheight*len(self.Items):
                            clicked_item = (event.pos[1] - 20)/self.totalheight
                            if self.Items[clicked_item][2] in ('button', 'cancelbutton'):
                                return self.Items[clicked_item][1], sliderdata
                            elif self.Items[clicked_item][2] == 'slider':
                                if self.Xoffset2 < event.pos[0]:
                                    p = sliderdata[self.Items[clicked_item][1]]
                                    p.index = int(round(float(event.pos[0] - self.Xoffset2)/(self.boxwidth-self.Xoffset2+self.Xoffset)*p.max + p.min))
                            elif self.Items[clicked_item][2] == 'checkbox':
                                if self.Xoffset + self.boxwidth - self.itemheight < event.pos[0]:
                                    p = sliderdata[self.Items[clicked_item][1]]
                                    p.checked = not p.checked
                elif event.type == MOUSEMOTION:
                    if self.Xoffset < event.pos[0] < self.Xoffset+self.boxwidth and self.Yoffset < event.pos[1] < self.totalheight*len(self.Items):
                        self.focus = (event.pos[1] - self.Yoffset)/self.totalheight
                elif event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        self.focus = (self.focus + 1) % len(self.Items)
                    if event.key == K_RIGHT:
                        if self.Items[self.focus][2] == 'slider':
                            if sliderdata[self.Items[self.focus][1]].index < sliderdata[self.Items[self.focus][1]].max:
                                sliderdata[self.Items[self.focus][1]].index += 1
                        else:
                            self.focus = (self.focus + 1) % len(self.Items)
                    elif event.key == K_UP:
                        self.focus = (self.focus - 1) % len(self.Items)
                    if event.key == K_LEFT:
                        if self.Items[self.focus][2] == 'slider':
                            if sliderdata[self.Items[self.focus][1]].index > sliderdata[self.Items[self.focus][1]].min:
                                sliderdata[self.Items[self.focus][1]].index -= 1
                        else:
                            self.focus = (self.focus - 1) % len(self.Items)
                    elif event.key in (K_RETURN, K_SPACE):
                        if self.Items[self.focus][2] in ('button', 'cancelbutton'):
                            return self.Items[self.focus][1], sliderdata
                        elif self.Items[self.focus][2] == 'checkbox':
                            p = sliderdata[self.Items[self.focus][1]]
                            p.checked = not p.checked
                    else:
                        pass
            self.Surface.fill((0,0,0))
            if self.additionalFunc:
                self.additionalFunc()
            if self.Yoffset + self.focus*self.totalheight + self.itemheight > self.Surface.get_height():
                Ymod = self.Yoffset + (self.focus+1)*self.totalheight + self.itemheight - self.Surface.get_height()
            else:
                Ymod = 0
            for n in range(len(self.Items)):
                draw_item = self.Items[n][0]
                draw_type = self.Items[n][2]
                if self.focus == n:
                    if draw_type == 'button':
                        pygame.draw.rect(self.Surface, self.frontcolor, (self.Xoffset, self.Yoffset + n*self.totalheight - Ymod, self.boxwidth, self.itemheight))
                        drawcolor = (0, 0, 0)
                    elif draw_type == 'cancelbutton':
                        pygame.draw.rect(self.Surface, self.halfcolor, (self.Xoffset, self.Yoffset + n*self.totalheight - Ymod, self.boxwidth, self.itemheight))
                        drawcolor = (0, 0, 0)
                    elif draw_type == 'disabled':
                        pygame.draw.rect(self.Surface, self.disabledcolor, (self.Xoffset, self.Yoffset + n*self.totalheight - Ymod, self.boxwidth, self.itemheight))
                        drawcolor = (0, 0, 0)
                    elif draw_type == 'slider':
                        pygame.draw.rect(self.Surface, self.frontcolor, (self.Xoffset2, self.Yoffset + n*self.totalheight - Ymod, self.boxwidth-self.Xoffset2+self.Xoffset, self.itemheight))
                        p = sliderdata[self.Items[n][1]]
                        if p.index > p.min:
                            pygame.draw.rect(self.Surface, self.halfcolor, (self.Xoffset2, self.Yoffset + n*self.totalheight - Ymod, float(p.index-p.min)/(p.max-p.min)*(self.boxwidth-self.Xoffset2+self.Xoffset), self.itemheight))
                        drawcolor = self.frontcolor
                    elif draw_type == 'checkbox':
                        pygame.draw.rect(self.Surface, self.frontcolor, (self.Xoffset+self.boxwidth-self.itemheight, self.Yoffset + n*self.totalheight - Ymod, self.itemheight, self.itemheight))
                        p = sliderdata[self.Items[n][1]]
                        if not p.checked:
                            pygame.draw.rect(self.Surface, (0, 0, 0), (self.Xoffset+self.boxwidth-self.itemheight+8, self.Yoffset + n*self.totalheight+8 - Ymod, self.itemheight-16, self.itemheight-16))
                        drawcolor = self.frontcolor
                else:
                    if draw_type == 'button':
                        pygame.draw.rect(self.Surface, self.frontcolor, (self.Xoffset, self.Yoffset + n*self.totalheight - Ymod, self.boxwidth, self.itemheight), 1)
                        drawcolor = self.frontcolor
                    elif draw_type == 'cancelbutton':
                        pygame.draw.rect(self.Surface, self.halfcolor, (self.Xoffset, self.Yoffset + n*self.totalheight - Ymod, self.boxwidth, self.itemheight), 1)
                        drawcolor = self.halfcolor
                    elif draw_type == 'disabled':
                        pygame.draw.rect(self.Surface, self.disabledcolor, (self.Xoffset, self.Yoffset + n*self.totalheight - Ymod, self.boxwidth, self.itemheight), 1)
                        drawcolor = self.disabledcolor
                    elif draw_type == 'slider':
                        pygame.draw.rect(self.Surface, self.frontcolor, (self.Xoffset2, self.Yoffset + n*self.totalheight - Ymod, self.boxwidth-self.Xoffset2+self.Xoffset, self.itemheight), 1)
                        p = sliderdata[self.Items[n][1]]
                        if p.index > p.min:
                            pygame.draw.rect(self.Surface, self.frontcolor, (self.Xoffset2, self.Yoffset + n*self.totalheight - Ymod, float(p.index-p.min)/(p.max-p.min)*(self.boxwidth-self.Xoffset2+self.Xoffset), self.itemheight))
                        drawcolor = self.frontcolor
                    elif draw_type == 'checkbox':
                        pygame.draw.rect(self.Surface, self.frontcolor, (self.Xoffset+self.boxwidth-self.itemheight, self.Yoffset + n*self.totalheight - Ymod, self.itemheight, self.itemheight), 1)
                        p = sliderdata[self.Items[n][1]]
                        if p.checked:
                            pygame.draw.rect(self.Surface, self.frontcolor, (self.Xoffset+self.boxwidth-self.itemheight+8, self.Yoffset + n*self.totalheight+8 - Ymod, self.itemheight-16, self.itemheight-16))
                        drawcolor = self.frontcolor
                self.Surface.blit(self.Font.render(draw_item, True, drawcolor),
                             (self.Xoffset+15, self.Yoffset+ 5 + n*self.totalheight - Ymod))
            pygame.display.flip()
