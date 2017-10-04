#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pip install pygame
#pip install cyrusbus

from menu import menu
import pygame
import math
import random
import time
from cyrusbus import Bus

pygame.init()
pygame.display.set_caption("DoorStation Tester")
Surface = pygame.display.set_mode((320,200))

bus = Bus()

contacts = [
    ("01 Jaime"                  ,"01234567"),
    ("02 Velvet Frida Vowell"    ,"01234567"),
    ("03 Frida Forne"            ,"01234567"),
    ("04 Marlyn Muldowney 12"    ,"01234567"),
    ("05 America Ausmus"         ,"01234567"),
    ("06 Alissa Aberle"          ,"01234567"),
    ("07 Clarissa Coltuithar"    ,"01234567")
]

title = [
    "Adresse 1",
    "Adresse 2",
    "       ",
    "HH:II"
]

font = pygame.font.Font("mksanstallx.ttf",12)
bigFont = pygame.font.Font("mksanstallx.ttf",19)
largeFont = pygame.font.Font("mksanstallx.ttf",24)
Items = [(contact[0],k,"button") for k,contact in enumerate(contacts)]

contactIndex = 0
displayMode = "contactList"
#displayMode = "screensaver"
frontColor = (255, 255, 0)
halfColor = (200, 200, 0)
disabledColor = (155, 155, 0)
foreverLoop = True

def contactDisplay():
    Surface.blit(bigFont.render(contact[0], True, (200, 200, 0)),(15, 40),None)

screen_rect = Surface.get_rect()

def blit_text(surface, text, pos, font, justif=0,color=pygame.Color('black')):
    x, y = pos
    for line in text.splitlines():
        y = y-font.render(line,0,color).get_height()/2
        
    for line in text.splitlines():
        word_surface = font.render(line,0,color)
        word_width, word_height = word_surface.get_size()
        if justif==0:
            offsetx = word_width
        elif justif==1:
            offsetx = word_width/2
        elif justif==2:
            offsetx = 0
        surface.blit(word_surface, (x-offsetx, y))
        y += word_height  # Start on new row.

class Ball:
    __slots__ = ('x', 'y', 'v','angle','vx','vy','radius','screen_rect')
    def __init__ (self, screen_rect,radius):
        self.screen_rect = screen_rect
        self.radius=radius
        self.x = random.randint(self.screen_rect.width/4,self.screen_rect.width*3/4)
        self.y = random.randint(self.screen_rect.height/4,self.screen_rect.height*3/4)
        self.v = random.randint(5,10)
        self.angle = random.random()*2*math.pi
        self.init()
        
    def init(self):
        self.vx = self.v*math.cos(self.angle)
        self.vy = self.v*math.sin(self.angle)
        
    def move(self):
        ''' 1
        4       2
            3'''
        self.x += self.vx
        self.y += self.vy
        prms=(
            ('y', 1  , 2  , self.y<self.radius),
            ('x', 1/2, 3/2, self.x>screen_rect.width-self.radius),
            ('y', 0  , 1  , self.y>screen_rect.height-self.radius),
            ('x', 3/2, 5/2, self.x<self.radius)
        )
        for p in prms:
            if(p[3]):
                if p[0]=='y':
                    self.vy = -self.vy
                    self.y += self.vy
                else:
                    self.vx = -self.vx
                    self.x += self.vx
                if random.randrange(0,100)>80:
                    self.angle = random.uniform(p[1],p[2])*math.pi
                    self.init()
        return
        
balls=[]
for i in range(0,10):
    balls.append(Ball(screen_rect,6))


while foreverLoop:
    if displayMode == "screensaver" :
        Surface.fill((0,0,0))
        for i in range(0,10):
            balls[i].move()
            pygame.draw.circle(Surface, pygame.Color("blue"), (int(balls[i].x),int(balls[i].y)), balls[i].radius, 0)
        blit_text(Surface,"\n".join(title).replace('HH:II',time.strftime("%H:%M")),  (screen_rect.width/2, screen_rect.height/2), largeFont,1,frontColor)
        pygame.display.update()

        dt = pygame.time.Clock().tick(20) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        
    if displayMode == "contactList":
        menuContacts = menu(Surface, Items, 10, 180, 10, 30, 50, 300, font,focus=contactIndex,frontcolor=frontColor,halfcolor=halfColor,disabledcolor=disabledColor)
        contactIndex = menuContacts.run() 
        if contactIndex[0] == "exit" or contactIndex[0] == "cancel":
            foreverLoop = False
        else:                        
            contactIndex=contactIndex[0]
            contact=Items[contactIndex]
            displayMode="contactConfirmation"
    elif displayMode == "contactConfirmation":
        confirmationResultMenu = menu(Surface, [('Appeler','call','button'),('Retour','cancel','button')], 140, 180, 100, 30, 50, 150, font,frontcolor=frontColor,halfcolor=halfColor,disabledcolor=disabledColor,additionalFunc = contactDisplay)
        confirmationResult = confirmationResultMenu.run()
        if confirmationResult[0] == "call":
            displayMode="call"
        else:
            displayMode="contactList"
    elif displayMode == "call":
        confirmationResult = menu(Surface, [('Retour','cancel','button')], 140, 180, 150, 30, 50, 150, font,frontcolor=frontColor,halfcolor=halfColor,disabledcolor=disabledColor,additionalFunc = contactDisplay)
        displayMode="contactList"
        
pygame.quit()
