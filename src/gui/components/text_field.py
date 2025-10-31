from gui.components.component import component

class textfield(component):
    def __init__(self, pos, size, text, listener=None, efunction=None, color=list[int, int, int]):
        if listener:
            super().__init__(pos, size, {"text": text, "event": listener, "efunc": efunction}, color)
        else:
            super().__init__(pos, size, {"text": text}, color)