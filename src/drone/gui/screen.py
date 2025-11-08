import pygame as p
from drone.gui.components.component_handler import component_handler as ch
from drone.gui.components.component import component

p.init()

class screen:
    def __init__(self, width, height, event_listeners, BGC=(0, 0, 0), fps=60):
        """
        Screen

        required:
        - width, height : the size of the screen
        - event_listeners : array of the different event listeners

        optional:
        - BGC : background color
        - fps : target fps
        """
        self.size = (width, height)

        self.comp_handler = ch()

        self.fps = fps
        self.clock = p.time.Clock()

        self.event_listeners = event_listeners

        self.screen = p.display.set_mode([width, height])
        self.screen.fill(BGC)
        pass

    def run(self, run_func=None):
        """
        runs the screen

        optional:
        - run_func: a function that is ran every frame
        """
        while True:
            if (self.handle_events()): break
            self.comp_handler.run(self.screen)

            if run_func:
                run_func()

            for event in p.event.get():
                    if event.type == p.QUIT:
                        return "quit"
            
            self.clock.tick(self.fps)
                    
    def add_component(self, comp:component):
        self.comp_handler.add(comp) 

    def handle_events(self):
        for event in p.event.get():
            for listener in self.event_listeners:
                if (listener.is_same(event.type)):
                    self.comp_handler.run_event(listener)
            
            if event.type == p.QUIT:
                p.quit()
                return True
        return False