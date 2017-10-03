#ADV-MENU TEST 1.1
#(C) 2008 Robin Wellner
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#Released under GPL (see http://www.gnu.org/licenses/)

from menu import menu, pygame
pygame.init()
pygame.display.set_caption("DoorStation Tester")
Surface = pygame.display.set_mode((320,200))

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
    "-- L'ORATOIRE --",
    "   873, Rapine  "
]

font = pygame.font.Font("mksanstallx.ttf",12)
bigFont = pygame.font.Font("mksanstallx.ttf",19)
Items = [(contact[0],k,"button") for k,contact in enumerate(contacts)]

contactIndex = 0
displayMode = "contactList"
frontColor = (255, 255, 0)
halfColor = (200, 200, 0)
disabledColor = (155, 155, 0)
foreverLoop = True

def contactDisplay():
    Surface.blit(bigFont.render(contact[0], True, (200, 200, 0)),(15, 40),None)

while foreverLoop:
    if displayMode == "contactList":
        contactIndex = menu(Surface, Items, 10, 180, 10, 30, 50, 300, font,focus=contactIndex,frontcolor=frontColor,halfcolor=halfColor,disabledcolor=disabledColor)
        if contactIndex[0] == "exit" or contactIndex[0] == "cancel":
            foreverLoop = False
        else:                        
            contactIndex=contactIndex[0]
            contact=Items[contactIndex]
            displayMode="contactConfirmation"
    elif displayMode == "contactConfirmation":
        confirmationResult = menu(Surface, [('Appeler','call','button'),('Retour','cancel','button')], 140, 180, 100, 30, 50, 150, font,frontcolor=frontColor,halfcolor=halfColor,disabledcolor=disabledColor,additionalFunc = contactDisplay)
        if confirmationResult[0] == "call":
            displayMode="call"
        else:
            displayMode="contactList"
    elif displayMode == "call":
        confirmationResult = menu(Surface, [('Retour','cancel','button')], 140, 180, 150, 30, 50, 150, font,frontcolor=frontColor,halfcolor=halfColor,disabledcolor=disabledColor,additionalFunc = contactDisplay)
        displayMode="contactList"
        
pygame.quit()