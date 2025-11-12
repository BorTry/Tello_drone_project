import pygame as p
from drone.gui.components.component_handler import component_handler as ch
from drone.gui.components.component import component

p.init()
font = p.font.SysFont(None, 24)

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
        self.clock = p.time.Clock()

        self.comp_handler = ch(self.clock, BGC)

        self.fps = fps

        self.event_listeners = event_listeners

        self.screen = p.display.set_mode([width, height])
        self.BGC = BGC
        self.screen.fill(BGC)

    def run(self, run_func=None, quit_func=None):
        """
        runs the screen

        optional:
        - run_func: a function that is ran every frame
        """
        run = True
        while run:
            if (self.handle_events()): 
                run = False

            self.screen.fill(self.BGC)
            self.comp_handler.run(self.screen)

            if run_func:
                run_func()

            if not run and quit_func:
                quit_func()
                p.quit()
            
            self.clock.tick(self.fps)
                    
    def add_component(self, comp:component):
        self.comp_handler.add(comp) 

    def handle_events(self):
        for event in p.event.get():
            for listener in self.event_listeners:
                if (listener.is_same(event.type)):
                    self.comp_handler.run_event(listener)
            
            if event.type == p.QUIT:
                return True
        return False
    
    class timer:
        def __init__(self, seconds_between_fire):
            self.secs = seconds_between_fire * 1000 # convert into milliseconds
            self.last_fired = p.time.get_ticks()

        def has_fired(self):
            curr_time = p.time.get_ticks()

            if curr_time - self.last_fired > self.secs:
                self.last_fired = curr_time
                return True
            return False

    def get_timer(self, seconds_between_fire):        
        return self.timer(seconds_between_fire).has_fired