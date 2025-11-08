from drone.gui.screen import screen
from drone.gui.components.button import button
from drone.gui.components.text_field import textfield
from drone.gui.listeners import on_click

import pygame as p

main_screen = screen(1000, 562, (on_click, ), BGC=(25, 25, 25))

TITLE_WIDTH = 400
TITLE_Y = 25 # the titles position in the y direction

TITLE = textfield(
    ((main_screen.size[0]//2) - (TITLE_WIDTH//2), TITLE_Y), 
    (TITLE_WIDTH, 75),
    "Tello Drone Controller",
    color=(75, 75, 75)
)

BUTTON_COLOR = (255, 255, 0)
BUTTON_Y_OFFSET = 100

BUTTON_START_X = 200

TAKE_OFF = button(
    (BUTTON_START_X, TITLE_Y + BUTTON_Y_OFFSET), (175, 75), 
    lambda x: print("ooga"), 
    color=BUTTON_COLOR,
    text="Take Off"
)
LAND = button(
    (BUTTON_START_X, TITLE_Y + BUTTON_Y_OFFSET + 100), (175, 75), 
    lambda x: print("ooga"), 
    color=BUTTON_COLOR,
    text="Land"
)

UP = button(
    (BUTTON_START_X + 200, TITLE_Y + BUTTON_Y_OFFSET), (175, 75), 
    lambda x: print("ooga"), 
    color=BUTTON_COLOR,
    text="Up"
)
DOWN = button(
    (BUTTON_START_X + 200, TITLE_Y + BUTTON_Y_OFFSET + 100), (175, 75), 
    lambda x: print("ooga"), 
    color=BUTTON_COLOR,
    text="Down"
)
LEFT = button(
    (BUTTON_START_X + 400, TITLE_Y + BUTTON_Y_OFFSET), (175, 75), 
    lambda x: print("ooga"), 
    color=BUTTON_COLOR,
    text="Left"
)
RIGHT = button(
    (BUTTON_START_X + 400, TITLE_Y + BUTTON_Y_OFFSET + 100), (175, 75), 
    lambda x: print("ooga"), 
    color=BUTTON_COLOR,
    text="Right"
)

main_screen.add_component(TITLE)
main_screen.add_component(TAKE_OFF)
main_screen.add_component(LAND)
main_screen.add_component(UP)
main_screen.add_component(DOWN)
main_screen.add_component(LEFT)
main_screen.add_component(RIGHT)

main_screen.run()