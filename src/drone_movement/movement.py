import time

class drone:
    """
    Interface for the Tello drone
    """
    def __init__(self, sock, tello_address):
        """
        Tello drone

        required:
        - sock: A socket connection to send the data to the drone
        - tello_address: The drone address (IP, PORT)
        """
        self.sock = sock
        self.tello_address = tello_address

        sock.sendto(b"command", tello_address) # gå i SDK modus for pre-programerte bevegelser i python

    def send(self, cmd, wait = 0):
        self.sock.sendto(cmd.encode("utf-8"), self.tello_address)
        if wait > 0: # i tilfelle vi ønsker delay
            time.sleep(wait)

    def takeoff(self):
        self.send("takeoff")
  
    def land(self):
        self.send("land")

    def flip(self):
        self.send("flip")

    def forward(self, amount):
        self.send(f"forward {amount}")

    def back(self, amount):
        self.send(f"back {amount}")

    def left(self, amount):
        self.send(f"left {amount}")

    def right(self, amount):
        self.send(f"right {amount}")

    def up(self, amount):
        self.send(f"up {amount}")

    def down(self, amount):
        self.send(f"down {amount}")

    def rotation_clock(self, deg): #clockwise rotation
        self.send(f"cw {deg}")

    def rotation_counter(self, deg): #counter clockwise rotation
        self.send(f"ccw {deg}")

    def speed(self, cms): #cm per sekund
        self.send(f"speed {cms}")

