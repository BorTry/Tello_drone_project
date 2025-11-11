class drone:
    """
    digital equivalen of the tello drone
    """
    def __init__(self, sock):
        """
        digital equivalent of the tello drone, if given follows the real world drone

        required:
        - sock: A socket connection to send the data to the drone
        """
        self.sock = sock

        self.send("command") # gå i SDK modus for pre-programerte bevegelser i python

    # ================== Send Commands ==================
    def send(self, cmd):
        self.sock.send(cmd)

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