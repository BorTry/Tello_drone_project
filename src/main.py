from gui.screen import screen
from gui.components.button import button
from gui.components.text_field import textfield
from gui.listeners import on_click

import pygame as p

test = screen(500, 500, (on_click, ))
ooga = button((50, 50), (25, 25), 
        lambda x: print("ooga"), 
        color=(255, 255, 0)
    )
dooga = textfield((200, 200), (150, 150), "hello world", color=(255, 255, 0))

test.add_component(ooga)
test.add_component(dooga)

test.run()