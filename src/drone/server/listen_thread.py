from threading import Thread, Event
from socket import socket, AF_INET, SOCK_DGRAM

BUFFER_SIZE = 2048

class listen_thread:
    def __init__(self, address:str, port:int, event_signal:Event, timeout=0.5, target=None, function_variables=None, id=0):
        """
        listen thread

        required:
        - address: The IP-address to listen to
        - port: The port for listening
        - event_signal: Signal to terminate the thread

        optional:
        - timeout: seconds before the socket times out
        - target: target function
            - required:
                - unproccessed data
        - function_variables: extra variables that the run function needs. sets them to 0
        - id: id of the thread, only used for print statements
        """
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((address, port))

        self.target = target
        self.kill_thread = event_signal
        self.timeout = timeout

        self.thread = None
        self.id = id

        self.function_variables = {}

        if function_variables != None:
            for var in function_variables:
                self.function_variables[var] = 0

        if (self.timeout > 0):
            self.socket.settimeout(self.timeout)

    def start(self):
        """
        Starts the thread with the function set to target.
        """
        if not self.target:
            print(f"There are no target function defined for thread {self.id}.")
            return

        def wrap():
            while not self.kill_thread.is_set():
                try:
                    data, _ = self.socket.recvfrom(BUFFER_SIZE)

                    self.target(self.function_variables, data)

                except TimeoutError:
                    continue

        self.thread = Thread(target=wrap)
        self.thread.start()

    def stop(self):
        if (self.thread.is_alive):
            print(f"Waiting for thread {self.id}...")
            self.thread.join()
        self.socket.close()