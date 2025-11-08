from gui.components.component import component
from gui.listeners import on_click

class button(component):
    def __init__(self, pos, size, click_function, event_listener=on_click, text=None, color=tuple[int, int, int]):
        if text:
            super().__init__(pos, size, {"event": event_listener.type, "efunc": click_function, "text": text}, color)
        else:
            super().__init__(pos, size, {"event": event_listener.type, "efunc": click_function}, color)