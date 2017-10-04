#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#pip install pygame
#pip install cyrusbus

from menu import menu
import ScreenSaver
import pygame
import time
from cyrusbus import Bus

pygame.init()
pygame.display.set_caption("DoorStation Tester")
Surface = pygame.display.set_mode((320,200))

bus = Bus()
def bus_subscribe(eventName):
    def tags_decorator(func):
        bus.subscribe(eventName, func)
        return func
    return tags_decorator

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
displayMode = "contactsList"
#displayMode = "screensaver"
frontColor = (255, 255, 0)
halfColor = (200, 200, 0)
disabledColor = (155, 155, 0)
foreverLoop = True

def contactDisplay():
    Surface.blit(bigFont.render(contact[0], True, (200, 200, 0)),(15, 40),None)

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

screens={}
screens["contactsList"] = menu(Surface, "contactsList", bus, Items, 10, 180, 10,  30, 50, 300, font, focus=contactIndex, frontcolor=frontColor, halfcolor=halfColor, disabledcolor=disabledColor)
screens["callConfirmation"] = menu(Surface, "callConfirmation" ,bus , [('Appeler','call','button'),('Retour','cancel','button')], 140, 180, 100, 30, 50, 150, font,frontcolor=frontColor,halfcolor=halfColor,disabledcolor=disabledColor,additionalFunc = contactDisplay)
screens["call"] = menu(Surface,'call', bus, [('Retour','cancel','button')], 140, 180, 150, 30, 50, 150, font,frontcolor=frontColor,halfcolor=halfColor,disabledcolor=disabledColor,additionalFunc = contactDisplay)
screens["screenSaver"] = ScreenSaver.ScreenSaver(Surface,10,6)

def setScreen(screenName):
    global displayMode,screens
    displayMode=screenName
    screens[displayMode].needToUpdate=True
    
@bus_subscribe('gui.menu')
def menuCallback(bus,menuName,eventType,item=None,data=None,idx=0):
    global displayMode,callConfirmationMenu,contactsListMenu,contactsListMenu,contact
    if menuName == "contactsList":
        if eventType == "exit" or eventType == "cancel":
            foreverLoop = False
        elif eventType == "select" :   
            contactIndex = idx
            contact = Items[idx]
            setScreen("callConfirmation")
            screens["callConfirmation"].focus=0
            
    if menuName == "callConfirmation":
        if eventType == "select" and item[1] == "call":
            setScreen("call")
        else: 
            setScreen("contactsList")

    if menuName == "call":
        setScreen("contactsList")


setScreen("contactsList")
while foreverLoop:
    dt = pygame.time.Clock().tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bus.publish('gui.global',when=displayMode,eventType=pygame.QUIT)
        elif event.type == pygame.KEYDOWN:
            bus.publish('gui.key',when=displayMode,eventKey=event.key)
               
    screens[displayMode].run()
        
pygame.quit()




