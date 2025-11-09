from drone.server.socket_server import server
from drone.drone_interface import drone as dr

from drone.gui.screen import screen
from drone.gui.components.button import button
from drone.gui.components.text_field import textfield
from drone.gui.listeners import on_click

# ======================= Socket Server =======================

Socket_server = server("0.0.0.0", "0.0.0.0")
# Socket_server.listen_text()

# =========================== Drone ===========================

drone = dr(Socket_server)

# ============================ GUI ============================

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

BUTTON_SIZE = (175, 75)

BUTTON_START_X = 200

TAKE_OFF = button(
    (BUTTON_START_X, TITLE_Y + BUTTON_Y_OFFSET), BUTTON_SIZE, 
    lambda x: drone.takeoff(), 
    color=BUTTON_COLOR,
    text="Take Off"
)
LAND = button(
    (BUTTON_START_X, TITLE_Y + BUTTON_Y_OFFSET + 100), BUTTON_SIZE, 
    lambda x: drone.land(), 
    color=BUTTON_COLOR,
    text="Land"
)

UP = button(
    (BUTTON_START_X + 200, TITLE_Y + BUTTON_Y_OFFSET), BUTTON_SIZE, 
    lambda x: drone.up(), 
    color=BUTTON_COLOR,
    text="Up"
)
DOWN = button(
    (BUTTON_START_X + 200, TITLE_Y + BUTTON_Y_OFFSET + 100), BUTTON_SIZE, 
    lambda x: drone.down(), 
    color=BUTTON_COLOR,
    text="Down"
)
LEFT = button(
    (BUTTON_START_X + 400, TITLE_Y + BUTTON_Y_OFFSET), BUTTON_SIZE, 
    lambda x: drone.left(), 
    color=BUTTON_COLOR,
    text="Left"
)
RIGHT = button(
    (BUTTON_START_X + 400, TITLE_Y + BUTTON_Y_OFFSET + 100), BUTTON_SIZE, 
    lambda x: drone.right(), 
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

# ======================= State Display =======================

ROW_HEIGHT = 60   
B_X_OFFSET = 200
TEXT_SIZE = [175, 50]

FACE_B_SIZE = (BUTTON_SIZE[0] + 75, BUTTON_SIZE[1] - 10)
FACE_B_START = (main_screen.size[0] // 2) - (FACE_B_SIZE[0] // 2)

DISPLAY_Y = BUTTON_Y_OFFSET + TITLE_Y + 250  # definerer at display-verdiene skal nederst på siden (relativt til knappene) 
CENTER_X = (main_screen.size[0] // 2) - (BUTTON_SIZE[0] // 2)
START_Y = DISPLAY_Y + FACE_B_SIZE[1]

FACE_TRACK = button(
    (FACE_B_START, START_Y - (FACE_B_SIZE[1] + 10)),                   
    FACE_B_SIZE,
    lambda x: print("Automatic mode on"),
    color=(0, 200, 255),
    text="Automatic mode"
)

SPEED   = textfield((CENTER_X - B_X_OFFSET, START_Y), TEXT_SIZE, f"SPEED: 0", color=(255, 255, 255))
BATTERY = textfield((CENTER_X, START_Y), TEXT_SIZE, f"BATTERY: 0", color=(255, 255, 255))
TIME    = textfield((CENTER_X + B_X_OFFSET, START_Y), TEXT_SIZE, f"TIME: 0", color=(255, 255, 255))

# ==================== Acceleration ====================

ACC_X = textfield((CENTER_X - B_X_OFFSET, START_Y + ROW_HEIGHT * 1), TEXT_SIZE, f"X: 0", color=(255, 255, 255))
ACC_Y = textfield((CENTER_X, START_Y + ROW_HEIGHT * 1), TEXT_SIZE, f"Y: 0", color=(255, 255, 255))
ACC_Z = textfield((CENTER_X + B_X_OFFSET, START_Y + ROW_HEIGHT * 1), TEXT_SIZE, f"Z: 0", color=(255, 255, 255))

main_screen.add_component(FACE_TRACK)

main_screen.add_component(SPEED)
main_screen.add_component(BATTERY)
main_screen.add_component(TIME)

main_screen.add_component(ACC_X)
main_screen.add_component(ACC_Y)
main_screen.add_component(ACC_Z)

main_screen.run()