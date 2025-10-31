from gui.components import component
from pygame import draw, display as di

class component_handler:
    def __init__(self):
        self.components = []

        self.event_comps = {}

    def add(self, comp:component):
        self.components.append(comp)

        if (comp.event_listener):
            if (not (comp.event_listener in self.event_comps)):
                self.event_comps[comp.event_listener] = []

            self.event_comps[comp.event_listener].append(comp)

    def run(self, display):
        # draw the components
        for component in self.components:
            draw.rect(display, component.color, component.get_rect())
        di.flip()

    def has_event(self, event_name):
        return event_name in self.event_comps

    def run_event(self, listener):
        for comp in self.event_comps[listener.type]:
            if (listener.check(comp)):
                comp.event_function(comp)