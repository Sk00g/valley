# Describes the (abstract) base element for all suie ui controls
import pygame


class Element:
    def __init__(self, position):
        self._host_panel = None
        self._position = position
        self.visible = True

    def add_panel(self, new_host):
        new_host.add_child(self)

    # Probably shouldn't mess with this in child classes, use recursion for multi-panel
    def _get_final_position(self):
        if self._host_panel:
            hpos = self._host_panel._get_final_position()
            return hpos[0] + self._position[0], hpos[1] + self._position[1]
        else:
            return self._position

    # Mandatory override, should return Rect object
    def get_display_rect(self):
        raise Exception("This 'Element' function needs to be overridden")

    # Optional override
    def get_position(self):
        return self._position

    # Optional override
    def set_position(self, new_position):
        self._position = new_position

    # Optional override
    def update(self, event_list):
        pass

    # Mandatory override
    def draw(self, surf: pygame.Surface):
        raise Exception("This 'Element' function needs to be overriden")