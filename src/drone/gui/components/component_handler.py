from drone.gui.components import component
from pygame import draw, display as di, font as f

f.init()
FONT_SIZE = 28
FONT = f.SysFont("arial", FONT_SIZE)

class component_handler:
    """
    Component handler

    handles all draw calls for the components given to it
    """
    def __init__(self, clock, BGC):
        self.clock = clock
        self.BGC = BGC

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
        display.fill(self.BGC)

        # draw the components
        for component in self.components:
            draw.rect(display, component.color, component.get_rect())

            # check if the component contains text
            if (component.contains_text):
                txt = FONT.render(component.text, True, (0, 0, 0))
                display.blit(txt, (
                    component.pos[0] + (component.size[0] // 2) - txt.get_width()//2, 
                    component.pos[1] + (component.size[1] // 2) - FONT_SIZE//2)
                )

        fps = self.clock.get_fps()
        fps_text = FONT.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
        display.blit(fps_text, (10, 10))

        di.flip()

    def has_event(self, event_name):
        return event_name in self.event_comps

    def run_event(self, listener):
        for comp in self.event_comps[listener.type]:
            if (listener.check(comp)):
                comp.event_function(comp)