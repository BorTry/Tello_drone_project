from gui.components.component import component
from gui.listeners import on_click

class button(component):
    def __init__(self, pos, size, click_function, event_listener=on_click, color=...):
        super().__init__(pos, size, {"event": event_listener.type, "efunc": click_function}, color)