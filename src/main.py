from drone.server.socket_server import server

from drone.drone_interfaces.drone_interface import drone as dr
from drone.drone_interfaces.mock_drone import mock_drone as mdr

from pygame import KEYDOWN, K_SPACE
from threading import Event

from drone.gui.screen import screen
from drone.gui.components.button import button
from drone.gui.components.text_field import textfield
from drone.gui.listeners import on_click
from drone.gui.event_listener import event_listener

from drone.recognition_wrapper import recognition_wrapper
from drone.tracker import tracker

import cv2

automatic_mode = False

# ======================== Mock Drone =========================

#quit_event = Event()

# mock_drone = mdr(quit_event)
# mock_drone.run()

#sleep(1)

# ======================= Socket Server =======================

Socket_server = server("0.0.0.0", "192.168.10.1")
Socket_server.listen()

# =========================== Drone ===========================

drone = dr(Socket_server)
Socket_server.send("streamon")

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

def manuall_controls(func, arg=None):
    def wrap(x):
        global automatic_mode

        automatic_mode = False
        if arg is None:
            func()
        else:
            func(arg)

    return wrap

TAKE_OFF = button(
    (BUTTON_START_X, TITLE_Y + BUTTON_Y_OFFSET), BUTTON_SIZE, 
    manuall_controls(drone.takeoff), 
    color=BUTTON_COLOR,
    text="Take Off"
)
LAND = button(
    (BUTTON_START_X, TITLE_Y + BUTTON_Y_OFFSET + 100), BUTTON_SIZE, 
    manuall_controls(drone.land),
    color=BUTTON_COLOR,
    text="Land"
)

UP = button(
    (BUTTON_START_X + 200, TITLE_Y + BUTTON_Y_OFFSET), BUTTON_SIZE, 
    manuall_controls(drone.up, arg=50), 
    color=BUTTON_COLOR,
    text="Up"
)
DOWN = button(
    (BUTTON_START_X + 200, TITLE_Y + BUTTON_Y_OFFSET + 100), BUTTON_SIZE, 
    manuall_controls(drone.down, arg=50), 
    color=BUTTON_COLOR,
    text="Down"
)
LEFT = button(
    (BUTTON_START_X + 400, TITLE_Y + BUTTON_Y_OFFSET), BUTTON_SIZE, 
    manuall_controls(drone.left, arg=50), 
    color=BUTTON_COLOR,
    text="Left"
)
RIGHT = button(
    (BUTTON_START_X + 400, TITLE_Y + BUTTON_Y_OFFSET + 100), BUTTON_SIZE, 
    manuall_controls(drone.right, arg=50), 
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

def switch_mode(comp):
    global automatic_mode
    print("Switching mode...")
    automatic_mode = not automatic_mode

FACE_TRACK = button(
    (FACE_B_START, START_Y - (FACE_B_SIZE[1] + 10)),                   
    FACE_B_SIZE,
    switch_mode,
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

STAT_TO_FIELD = {
    "bat": BATTERY,
    "time": TIME,
    "agx":ACC_X,
    "agy":ACC_Y,
    "agz":ACC_Z,
}

# ================== Face recognition ==================

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def get_next_image(cap):
    image_frag = cap.get_image()

    return not (image_frag is None), image_frag

def image_proc(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def detection(frame):
    return face_cascade.detectMultiScale(
        frame,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(120, 120),
    )

cam = recognition_wrapper(
    lambda:Socket_server, 
    get_next_image, 
    image_proc, 
    detection, 
    run_once=True,
)

WIDTH = 960
HEIGHT = 720

track = tracker((WIDTH, HEIGHT), drone)
timer = main_screen.get_timer(0.5)

def run_function():
    stats = Socket_server.get_text()

    if stats == None:
        return
    
    for stat in stats.keys():
        if stat in STAT_TO_FIELD:
            STAT_TO_FIELD[stat].change_text(f"{stat}: {stats[stat][0]}")

    data = cam.run()

    if data and len(data[0]) > 0:
        dominant_obj = cam.get_dominant_object(data[0])

        center_point_obj = track.get_center_of_object(dominant_obj)
        dx, dy = track.center_around_point(center_point_obj)

        print(track.get_distance_to_face(dominant_obj))

        cv2.line(cam.last_frame, (center_point_obj[0] - dx, center_point_obj[1] - dy), center_point_obj, (0,0,255))

        if automatic_mode and timer():
            print("Running tracker...")
            track.run(dominant_obj) # only send run the tracker once a second

    if data:
        cam.show_frame()

def on_quit():
    cv2.destroyAllWindows()
    cam.stop()

    Socket_server.stop()

    #mock_drone.stop()

print("opening GUI")

main_screen.run(run_func=run_function, quit_func=on_quit)