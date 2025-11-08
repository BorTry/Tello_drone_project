class drone_data:
    def __init__(self, sock, tello_address):
        self.sock = sock
        self.tello_address = tello_address

        sock.send(b"command") # gå i SDK modus for pre-programerte bevegelser i python

    def send(self, cmd): # send kommando for renere kode
        self.sock.send(cmd)

    def speed_check(self):
        self.sock("speed?")

    def battery_check(self):
        self.sock("battery?")

    def time_check(self): # Flytid
        self.sock("time?")

    def wifi_check(self): # sjekker Wi-fi SNR
        self.sock("wifi?")

