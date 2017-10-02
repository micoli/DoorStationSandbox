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
pygame.display.set_caption("ADV-MENU Test")
icon = pygame.Surface((1,1)); 
icon.set_alpha(0); 
pygame.display.set_icon(icon)
Surface = pygame.display.set_mode((320,200))

'''Items = [('Abc', 'abc', 'button'),
    ('Do something', 'x', 'slider', (2, 0, 10)),
    ('Done', 'p', 'checkbox', True),
    ('Test', 'name', 'disabled'),
    ('Cancel', 'cancel', 'cancelbutton'),
    ('Quit', 'exit', 'button'),
    ('Useless button 1', 'btn', 'button'),
    ('Useless button 2', 'btn', 'button'),
    ('Useless button 3', 'btn', 'button'),
    ('Useless button 4', 'btn', 'button'),
    ('Useless button 5', 'btn', 'button'),
    ('Useless button 6', 'btn', 'button'),
    ('Useless button 7', 'btn', 'button'),
    ('Useless button 8', 'btn', 'button'),
]'''

contacts=[
    ("01 Jaime"                  ,"01234567"),
    ("02 Velvet Frida Vowell"    ,"01234567"),
    ("03 Frida Forne"            ,"01234567"),
    ("04 Marlyn Muldowney 12"    ,"01234567"),
    ("05 America Ausmus"         ,"01234567"),
    ("06 Alissa Aberle"          ,"01234567"),
    ("07 Clarissa Coltuithar"    ,"01234567")
]

title=[
    "-- L'ORATOIRE --",
    "   873, Rapine  "
]
font = pygame.font.Font("mksanstallx.ttf",12)
ajfont = pygame.font.Font("mksanstallx.ttf",19)
Items = [(contact[0],contact,"button") for contact in contacts]

def contactDisplay():
    Surface.blit(ajfont.render(contact[0][0], True, (200, 200,0)),(15, 40 ),None)

displayMode="contactList"
while True:
    if displayMode=="contactList":
        contact = menu(Surface, Items, 10, 180, 10, 30, 50, 300, font,focus=3,frontcolor=(255, 255, 0),halfcolor=(200, 200, 0),disabledcolor=(155, 155, 0))
        displayMode="contactConfirmation"
    elif displayMode=="contactConfirmation":
        confirmationResult = menu(Surface, [('Appeler','call','button'),('Retour','exit','button')], 140, 180, 100, 30, 50, 150, font,frontcolor=(255, 255, 0),halfcolor=(200, 200, 0),disabledcolor=(155, 155, 0),additionalFunc = contactDisplay)
        print confirmationResult[0]
        if confirmationResult[0]=="call":
            displayMode="call"
        else:
            displayMode="contactList"
    elif displayMode=="call":
        confirmationResult = menu(Surface, [('Retour','exit','button')], 140, 180, 100, 30, 50, 150, font,frontcolor=(255, 255, 0),halfcolor=(200, 200, 0),disabledcolor=(155, 155, 0),additionalFunc = contactDisplay)
        displayMode="contactList"
pygame.quit()