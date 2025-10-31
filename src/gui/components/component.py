class component:
    def __init__(self, pos: list[int, int], size:list[int, int], options, color=(0, 0, 0)):
        """
        screen component
        -
        pos : position of component (left, top).
        size : size of component (width, height).
        options : optionals such as "event", "efunc", etc.
        color : color of the component.
        """
        self.pos = pos
        self.size = size
        self.color = color

        self.event_function = None
        self.event_listener = None

        self.contains_text = False
        self.text = None

        self.id = None

        if "event" in options:
            self.event_listener = options["event"]
            self.event_function = options["efunc"]

        if "text" in options:
            self.text = options["text"]
            self.contains_text = True

    def get_rect(self):
        return (*self.pos, *self.size)
    
    def set_id(self, id):
        self.id = id