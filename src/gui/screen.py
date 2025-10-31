import pygame as p
from gui.components.component_handler import component_handler as ch
from gui.components.component import component

p.init()

class screen:
    def __init__(self, width, height, BGC=(0, 0, 0), fps=60):
        self.comp_handler = ch()

        self.fps = fps
        self.clock = p.time.Clock()

        self.screen = p.display.set_mode([width, height])
        self.screen.fill(BGC)
        pass

    def run(self):
        while True:
            self.handle_events()
            self.comp_handler.run(self.screen)

            for event in p.event.get():
                    if event.type == p.QUIT:
                        return "quit"
            
            self.clock.tick(self.fps)
                    
    def add_component(self, comp:component):
        self.comp_handler.add(comp) 

    def handle_events(self):
        for event in p.event.get():
            match event.type:
                case p.MOUSEBUTTONDOWN:
                    if not self.comp_handler.has_event("on_click"):
                        continue
                    self.comp_handler.run_event("on_click")
