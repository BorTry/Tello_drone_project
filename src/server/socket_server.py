from queue import Queue
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread


BUFFER_SIZE = 2048

class server:
    """
    o

    Creates a UDP connection between a pc and a Tello drone. Is meant to be ran on another Thread.
    """

    def __init__(self, pipe:Queue, local_address:list[str, int], listen_address:list[str, int]):
        """
        Server
        - 
        """
        self.local_address = local_address
        self.listen_address = listen_address

        self.pipe = pipe

        self.socket = socket(AF_INET, SOCK_DGRAM)

        self.socket.bind(local_address)

    def listen(self):
        data, address = self.socket.recvfrom(BUFFER_SIZE)

        pipe.put(data.decode(encoding="utf-8")) # put the recieved data into a pipe

    def send(self, msg):
        self.socket.sendto(msg.encode(encoding="utf-8"), self.listen_address)

    def get_next(self):
        return None if self.pipe.empty() else self.pipe.get()

if __name__ == "__main__":
    pipe = Queue(10)

    test = server(pipe, ("127.0.0.1", 8000), ("127.0.0.1", 9000))
    test2 = server(pipe, ("127.0.0.1", 9000), ("127.0.0.1", 8000))

    dooga = Thread(target=test.listen)

    dooga.start()

    test2.send("oogabooga")

    dooga.join()

    print(pipe.get())