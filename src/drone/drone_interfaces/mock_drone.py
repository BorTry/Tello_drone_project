from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep

from threading import Thread

IPS = 10 # iterations per second
BUFFER_SIZE = 2048

COMMAND_TO_FUNC = {
    "takeoff" : "height",
    "land": "height",
    "forward": "x_acc",
    "back": "x_acc",
    "left": "z_acc",
    "right": "z_acc",
    "up": "y_acc",
    "down": "y_acc",
    "cw": "roll",
    "ccw": "roll"
}

REVERSE_FUNCTIONS = {
    "land"
    "back"
    "right"
    "down"
    "ccw"
}

class mock_drone:
    """
    simulates the recieving and sending of data for the Tello drone.
    """
    def __init__(self, shut_event):
        self.stats = {
            "x_acc":0,
            "y_acc":0,
            "z_acc":0,
            "roll":0,
            "yaw":0,
            "pitch":0,
            "height":0,
        }

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("192.168.10.1", 8889)) # Tello IP address

        self.shut_event = shut_event
        self.thread = None

    def send_data(self):
        self.socket.sendto(
            "agx:%2d;agy:%2d;agz%2d;roll:%2d;yaw:%2d;pitch:%2d;height:%2d" % (
                self.x_acc, self.y_acc, self.z_acc, self.roll, self.yaw, self.pitch, self.height
            ),
            ("0.0.0.0", 8890)
        )

    def run(self):
        def wrap():
            self.socket.settimeout(0.1)

            while (not self.shut_event.is_set()):
                try:
                    data, a = self.socket.recvfrom(BUFFER_SIZE)

                    if not data:
                        continue

                    data = data.decode(encoding="utf-8").split(" ")

                    if (data[0] in REVERSE_FUNCTIONS):
                        data[1] *= -1

                    self.stats[COMMAND_TO_FUNC[data[0]]] += data[1]

                except TimeoutError:
                    continue

                self.send_data()

                sleep(60 / IPS)
        
        self.thread = Thread(target=wrap)