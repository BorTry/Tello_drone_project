from pygame import mouse, MOUSEBUTTONDOWN
from gui.event_listener import event_listener

# A list of pre-defined listeners

def mouse_collides(comp):
    mouse_pos = mouse.get_pos()

    return (
        comp.pos[0] + comp.size[0] >= mouse_pos[0] and 
        comp.pos[0] <= mouse_pos[0] and
        comp.pos[1] + comp.size[1] >= mouse_pos[1] and 
        comp.pos[1] <= mouse_pos[1]
    )

on_click = event_listener("on_click", MOUSEBUTTONDOWN, check_func=mouse_collides)