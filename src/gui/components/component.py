SUPPORTED_EVENTS = ["on_click"]

class component:
    def __init__(self, pos: list[int, int], size:list[int, int], options, color=(0, 0, 0)):
        self.pos = pos
        self.size = size
        self.color = color

        self.event_function = None
        self.event_listener = None

        if "event" in options:
            event_type = options["event"]
            self.event_listener = event_type
            
            if not (event_type in SUPPORTED_EVENTS):
                print(f"There is no event listener for {event_type}")
                self.event_listener = None # reset the event listener
            else:
                self.event_function = options["efunc"]

    def get_rect(self):
        return (*self.pos, *self.size)