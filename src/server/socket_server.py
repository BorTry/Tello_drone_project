from queue import Queue
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Event

from listen_thread import listen_thread

import time

BUFFER_SIZE = 2048

# porter hvor data kommer inn
TEXT_PORT = 9000 
IMAGE_PORT = 11111

TEXT_SEND_PORT = 8889

class server:
    """
    Socket server used for two-way communication.

    Creates a UDP connection between a pc and a Tello drone. Opening two different listen threads for both image
    and text communication.
    """

    def __init__(self, local_address:tuple[str, int], target_address:str, max_queue_size=10):
        """creates a socket server to recieve and send data
        
        required:
        - local address : the address to host the different listening threads on.
        - target address : The addres where data will be sent to.

        optional:
        - max queue size : The maximum size for both the text and image queue
        """
        self.local_address = local_address
        self.target_address = target_address

        self.text_pipe = Queue(max_queue_size)
        self.image_pipe = Queue(max_queue_size)

        self.send_socket = socket(AF_INET, SOCK_DGRAM)

        self.kill_thread = Event()
        self.text_thread = None
        self.image_thread = None

    def listen_text(self):
        """
        Opens the text socket and starts listening.
        """
        # put the recieved data into a pipe
        handle_data = lambda data : self.text_pipe.put(data.decode(encoding="utf-8")) 

        self.text_thread = listen_thread(self.local_address[0], TEXT_PORT, self.kill_thread, target=handle_data, id=0)
        self.text_thread.start()

    def listen_image(self):
        """
        Opens the image socket and starts listening.
        """
        handle_data = lambda data : self.image_pipe.put(data) 

        self.image_thread = listen_thread(self.local_address[0], IMAGE_PORT, self.kill_thread, target=handle_data, id=1)
        self.image_thread.start()

    def send(self, msg):
        """
        Sends a msg to the target address.
        """
        self.send_socket.sendto(msg.encode(encoding="utf-8"), (self.target_address, TEXT_PORT))

    def get_text(self):
        return None if self.text_pipe.empty() else self.text_pipe.get()
    
    def get_image(self):
        return None if self.image_pipe.empty() else self.image_pipe.get()
    
    def stop(self):
        print("Stopping socket server...")
        self.kill_thread.set()

        if (self.text_thread):
            self.text_thread.stop()

        if (self.image_thread):
            self.image_thread.stop()

        self.send_socket.close()

        print("Successfully stopped socket server.")

if __name__ == "__main__":
    test = server(("127.0.0.1", 8000), "127.0.0.1")

    test.listen_text()

    test.send("oogabooga")
    test.send("oogabooga")
    test.send("oogabooga")
    test.send("oogabooga")

    time.sleep(2)

    print(test.get_text())
    print(test.get_text())
    print(test.get_text())
    print(test.get_text())

    test.stop()