from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep

IPS = 10 # iterations per second
BUFFER_SIZE = 2048

class mock_drone:
    """
    simulates the recieving and sending of data for the Tello drone.
    """
    def __init__(self, shut_event):
        self.x_acc = 0
        self.y_acc = 0
        self.z_acc = 0

        self.roll = 0
        self.yaw = 0
        self.pitch = 0

        self.height = 0

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(("192.168.10.1", 8889)) # Tello IP address

        self.shut_event = shut_event

    def send_data(self):
        self.socket.sendto(
            "agx:%2d;agy:%2d;agz%2d;roll:%2d;yaw:%2d;pitch:%2d;height:%2d" % (self.x_acc, self.y_acc, self.z_acc, self.roll, self.yaw, self.pitch, self.height),
            ("0.0.0.0", 8890)
        )

    def run(self):
        self.socket.settimeout(0.1)

        while (not self.shut_event.is_set()):
            try:
                data, a = self.socket.recvfrom(BUFFER_SIZE)

            except TimeoutError:
                continue

            self.send_data()

            sleep(60 / IPS)