from gui.components import component
from pygame import draw, display as di, font as f

f.init()
FONT = f.SysFont("consolas", 28)

class component_handler:
    def __init__(self):
        self.components = []

        self.event_comps = {}
        self.current_id = 0 # id of the next added component

    def add(self, comp:component):
        self.components.append(comp)
        
        comp.set_id(self.current_id)
        self.current_id += 1

        if (comp.event_listener):
            if (not (comp.event_listener in self.event_comps)):
                self.event_comps[comp.event_listener] = []

            self.event_comps[comp.event_listener].append(comp)

    def run(self, display):
        # draw the components
        for component in self.components:
            draw.rect(display, component.color, component.get_rect())

            # check if the component contains text
            if (component.contains_text):
                txt = FONT.render(component.text, True, (0, 0, 0))
                display.blit(txt, (component.pos[0], component.pos[1]))

        di.flip()

    def has_event(self, event_name):
        return event_name in self.event_comps

    def run_event(self, listener):
        for comp in self.event_comps[listener.type]:
            if (listener.check(comp)):
                comp.event_function(comp)