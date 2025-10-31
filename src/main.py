from gui.screen import screen
from gui.components.component import component as comp

test = screen(500, 500)
ooga = comp((50, 50), (25, 25), 
        {"event": "on_click", "efunc": lambda: print("ooga")}, 
        color=(255, 255, 0)
    )

test.add_component(ooga)

test.run()
