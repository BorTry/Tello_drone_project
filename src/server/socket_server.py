from queue import Queue
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread, Event

import time

BUFFER_SIZE = 2048

class server:
    """
    o

    Creates a UDP connection between a pc and a Tello drone.
    """

    def __init__(self, pipe:Queue, local_address:tuple[str, int], listen_address:tuple[str, int]=None):
        """
        Server
        - 
        """
        self.local_address = local_address
        self.listen_address = listen_address

        self.pipe = pipe

        self.socket = socket(AF_INET, SOCK_DGRAM)

        self.socket.bind(local_address)

        self.kill_thread = Event()
        self.listen_thread = None

    def listen(self):
        if not self.listen_address:
            print("listen address not defined.")
            return
        
        def wrap():
            self.socket.settimeout(0.5)

            while not self.kill_thread.is_set():
                try:
                    data, address = self.socket.recvfrom(BUFFER_SIZE)

                    self.pipe.put(data.decode(encoding="utf-8")) # put the recieved data into a pipe
                except TimeoutError:
                    continue

        self.listen_thread = Thread(target=wrap)
        self.listen_thread.start()

    def send(self, msg):
        self.socket.sendto(msg.encode(encoding="utf-8"), self.listen_address)

    def get_next(self):
        return None if self.pipe.empty() else self.pipe.get()
    
    def stop(self):
        print("Stopping socket server...")
        self.kill_thread.set()

        if (self.listen_thread.is_alive()):
            print("Waiting for thread...")
            self.listen_thread.join()

        self.socket.close()

        print("Successfully stopped socket server.")


if __name__ == "__main__":
    pipe = Queue(10)

    test = server(pipe, ("127.0.0.1", 8000), ("127.0.0.1", 8000))

    test.listen()

    test.send("oogabooga")
    test.send("oogabooga")
    test.send("oogabooga")
    test.send("oogabooga")

    print(test.get_next())

    test.stop()