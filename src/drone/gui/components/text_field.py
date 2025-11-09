from drone.gui.components.component import component

class textfield(component):
    def __init__(self, pos, size, text, listener=None, efunction=None, color=tuple[int, int, int]):
        if listener:
            super().__init__(pos, size, {"text": text, "event": listener, "efunc": efunction}, color)
        else:
            super().__init__(pos, size, {"text": text}, color)

    def change_text(self, txt):
        """
        Change the text in a textfield
        """
        self.text = txt