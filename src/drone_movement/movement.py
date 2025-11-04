#import Tello3

import threading 
import socket
import sys
import time

class drone:
    def __init__(self, sock, tello_address):

        self.sock = sock
        self.tello_address = tello_address

        sock.sendto(b"command", tello_address) # gå i SDK modus for pre-programerte bevegelser i python

    def send(self, cmd, wait = 0):
        self.sock.sendto(cmd.encode("utf-8"), self.tello_address)
        if wait > 0: # i tilfelle vi ønsker delay
            time.sleep(wait)

    def takeoff(self):
        self.send("takeoff")
        pass
  
    def land(self):
        self.send("land")
        pass

    def flip(self):
        self.send("flip")
        pass

    def forward(self, amount):
        self.send(f"forward {amount}")
        pass

    def back(self, amount):
        self.send(f"back {amount}")
        pass

    def left(self, amount):
        self.send(f"left {amount}")
        pass

    def right(self, amount):
        self.send(f"right {amount}")
        pass

    def up(self, amount):
        self.send(f"up {amount}")
        pass

    def down(self, amount):
        self.send(f"down {amount}")
        pass

    def rotation_clock(self, deg): #clockwise rotation
        self.send(f"cw {deg}")
        pass

    def rotation_counter(self, deg): #counter clockwise rotation
        self.send(f"ccw {deg}")
        pass

    def speed(self, cms): #cm per sekund
        self.send(f"speed {cms}")
        pass

