from socket import socket, AF_INET, SOCK_DGRAM

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
    "land",
    "back",
    "right",
    "down",
    "ccw"
}

ADDRESS = "0.0.0.0"

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
            "battery":100
        }

        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((ADDRESS, 8889)) # Tello IP address
        self.socket.settimeout(0.01)

        self.shut_event = shut_event
        self.thread = None

    def send_data(self):
        stat_string = "agx:%d;agy:%d;agz:%d;roll:%d;yaw:%d;pitch:%d;height:%d;battery:%d" % (
            self.stats["x_acc"], self.stats["y_acc"], self.stats["z_acc"], 
            self.stats["roll"], self.stats["yaw"], self.stats["pitch"], 
            self.stats["height"], self.stats["battery"]
        )

        self.socket.sendto(
            stat_string.encode(encoding="utf-8"),
            ("0.0.0.0", 8890)
        )

    def stop(self):
        print("Stopping mock drone...")
        self.shut_event.set()

        if self.thread.is_alive():
            print("Waiting for drone thread")
            self.thread.join()
        self.socket.close()
        print("Successfully stopped mock drone")

    def run(self):
        def wrap():
            from time import sleep

            while (not self.shut_event.is_set()):
                try:
                    data, a = self.socket.recvfrom(BUFFER_SIZE)

                    if not data or data == "command" or data == "streamon":
                        continue

                    data = data.decode(encoding="utf-8").split(" ")
                    
                    if (data[0] == "takeoff" or data[0] == "land"):
                        data.append(20)

                    data[1] = float(data[1])
                    print(f"Drone recieved '{data[0]} {data[1]}'")

                    if (data[0] in REVERSE_FUNCTIONS):
                        data[1] *= -1

                    self.stats[COMMAND_TO_FUNC[data[0]]] += data[1]

                except TimeoutError:
                    pass

                self.send_data()
                sleep(1 / IPS)
        
        self.thread = Thread(target=wrap)
        self.thread.start()