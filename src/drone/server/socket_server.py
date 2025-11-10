from queue import Queue
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Event

from drone.server.listen_thread import listen_thread
from drone.logger import LOGGER

import numpy as np

server_logger = LOGGER.get_logger("Socket server")

BUFFER_SIZE = 2048

# ports where data will be recieved
TEXT_PORT = 8890
IMAGE_PORT = 11111

RETURN_PORT = 9000

# ports where data will be sent to
TEXT_SEND_PORT = 8889

class server:
    """
    Socket server used for two-way communication.

    Creates a UDP connection between a pc and a Tello drone. Opening two different listen threads for both image
    and text communication.
    """

    def __init__(self, local_address:str, target_address:str, max_queue_size=10):
        """creates a socket server to recieve and send data
        
        required:
        - local address: the address to host the different listening threads on.
        - target address: The address where data will be sent to.

        optional:
        - max queue size: The maximum size for both the text and image queue
        """
        self.local_address = local_address
        self.target_address = target_address

        self.text_pipe = Queue(max_queue_size)
        self.image_pipe = Queue(max_queue_size)
        self.max_queue_size = max_queue_size

        self.send_socket = socket(AF_INET, SOCK_DGRAM)

        self.kill_thread = Event()

        self.recieve_thread = None
        self.text_thread = None
        self.image_thread = None

    def listen(self):
        """
        Opens all sockets and starts listening.
        """
        self.listen_text()
        self.listen_image()

    def listen_text(self):
        """
        Opens the text socket and starts listening.
        """
        def handle_data(ooga, data):
            # put the recieved data into a pipe
            decoded_data = data.decode(encoding="utf-8").split(";")

            # format data
            data_list = {}

            for values_pairs in decoded_data:
                if values_pairs == "\r\n":
                    continue
                pair = values_pairs.split(":")

                data_list[pair[0]] = [pair[1]]

            if self.text_pipe.qsize() < self.max_queue_size:
                self.text_pipe.put(data_list)

            server_logger.log_csv(data_list)

        def handle_return_data(self, data):
            decoded_data = data.decode(encoding="utf-8")
            print(f"recieved {decoded_data} from drone")

        self.recieve_thread = listen_thread(self.local_address, RETURN_PORT, self.kill_thread, target=handle_return_data, id=0)
        self.recieve_thread.start()

        self.text_thread = listen_thread(self.local_address, TEXT_PORT, self.kill_thread, target=handle_data, id=1)
        self.text_thread.start()

    def listen_image(self):
        """
        Opens the image socket and starts listening.
        """
        variable_data = [
            "packets"
        ]

        def handle_data(self, data):
            if self.variable_data["packets"] is None:
                self.variable_data["packets"] = ""

            self.variable_data["packets"] += data
            if len(data) != 1460:
                last_frame = None

                for frame in self.__h264decode(self.variable_data["packets"]):
                    last_frame = frame # get the last frame given to the server
                
                self.image_pipe.put(last_frame)
                self.variable_data["packets"] = ""

        self.image_thread = listen_thread(self.local_address, IMAGE_PORT, self.kill_thread, variable_data=variable_data, target=handle_data, id=2)
        self.image_thread.start()

        self.send("streamon")
    
    def __h264decode(self, packets):
        res_frame_list = []
        frames = (packets)
        
        for framedata in frames:
            (frame, w, h, ls) = framedata

            if frame is not None:
                # print 'frame size %i bytes, w %i, h %i, linesize %i' % (len(frame), w, h, ls)

                frame = np.fromstring(frame, dtype=np.ubyte, count=len(frame), sep='')
                frame = (frame.reshape((h, ls / 3, 3)))
                frame = frame[:, :w, :]
                res_frame_list.append(frame)

        return res_frame_list

    def send(self, msg):
        """
        Sends a msg to the target address.
        """

        print(f"Sending command '{msg}' to {self.target_address}:{TEXT_SEND_PORT}")
        self.send_socket.sendto(msg.encode(encoding="utf-8"), (self.target_address, TEXT_SEND_PORT))

    def get_text(self):
        """
        Returns the next text message in the queue
        """
        return None if self.text_pipe.empty() else self.text_pipe.get()
    
    def get_image(self):
        """
        Returns the next image data in the queue
        """
        return None if self.image_pipe.empty() else self.image_pipe.get()
    
    def stop(self):
        print("Stopping socket server...")
        self.kill_thread.set()

        if (self.text_thread):
            self.text_thread.stop()

        if (self.image_thread):
            self.image_thread.stop()

        if (self.recieve_thread):
            self.recieve_thread.stop()

        self.send_socket.close()

        print("Successfully stopped socket server.")