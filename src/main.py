from drone.gui.screen import screen
from drone.gui.components.button import button
from drone.gui.components.text_field import textfield
from drone.gui.listeners import on_click
from drone.drone_movement.drone_read import drone_data

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

buttons_b = BUTTON_Y_OFFSET + TITLE_Y + 200  #definerer at display-verdiene skal nederst på siden (relativt til knappene) 
center_x = (main_screen.size[0] // 2) - (TITLE_WIDTH // 2)
start_y = buttons_b + 50
ROW_HEIGHT = 60   

speed_val   = "No value"  # drone.speed_check() # må bruke disse
battery_val = "No value"  # drone.battery_check()
time_val    = "No value"  # drone.time_check()

FACE_BUTTON_W, FACE_BUTTON_H = 260, 60
FACE_TRACK = button(
    ((main_screen.size[0] // 2) - (FACE_BUTTON_W // 2),  
     start_y - (FACE_BUTTON_H + 5)),                   
    (FACE_BUTTON_W, FACE_BUTTON_H),
    lambda x: print("Face tracking on"),
    color=(0, 200, 255),
    text="Face Tracking"
)

SPEED   = textfield((center_x, start_y + ROW_HEIGHT * 0), (TITLE_WIDTH, 75), f"SPEED: {speed_val}", color=(255, 255, 255))
BATTERY = textfield((center_x, start_y + ROW_HEIGHT * 1), (TITLE_WIDTH, 75), f"BATTERY: {battery_val}", color=(255, 255, 255))
TIME    = textfield((center_x, start_y + ROW_HEIGHT * 2), (TITLE_WIDTH, 75), f"TIME: {time_val}", color=(255, 255, 255))

main_screen.add_component(TITLE)
main_screen.add_component(TAKE_OFF)
main_screen.add_component(LAND)
main_screen.add_component(UP)
main_screen.add_component(DOWN)
main_screen.add_component(LEFT)
main_screen.add_component(RIGHT)

main_screen.add_component(FACE_TRACK)

main_screen.add_component(SPEED)
main_screen.add_component(BATTERY)
main_screen.add_component(TIME)


main_screen.run()