# Base GUI panel for placing and arranging UI elements, contains no visual elements
import pygame
import suie


class Panel(suie.Element):
    # Optionally give a new panel a list of starting children
    def __init__(self, position, size, child_list=None):
        suie.Element.__init__(self, position)
        self._size = size
        self._child_list = []

        if child_list:
            for child in child_list:
                self.add_child(child)

    def get_display_rect(self):
        return pygame.Rect(self._position + self._size)

    def add_child(self, child: suie.Element):
        self._child_list.append(child)
        child._host_panel = self

    def remove_child(self, child: suie.Element):
        self._child_list.remove(child)
        child._host_panel = None

    def update(self, event_list):
        for child in self._child_list:
            child.update(event_list)

    def draw(self, screen: pygame.Surface):
        for child in self._child_list:
            if child.visible:
                child.draw(screen)

