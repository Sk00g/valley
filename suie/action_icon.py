import sys
import suie
import factory


class ActionIcon(suie.Panel):
    WIDTH = 80
    HEIGHT = 72
    FONT_SIZE = 10
    BKGR_COLOR = (10, 20, 30, 255)
    HOTKEY_COLOR = (255, 255, 255, 255)
    HOTKEY_BKGR_COLOR = (0, 0, 0, 255)
    HOTKEY_BORDER_COLOR = (255, 255, 255, 255)

    def __init__(self, position, action, hotkey, icon_index: int):
        suie.Panel.__init__(self, position, (ActionIcon.WIDTH, ActionIcon.HEIGHT))

        border = suie.Border((0, 0), (ActionIcon.WIDTH, ActionIcon.HEIGHT), ActionIcon.BKGR_COLOR)
        icon = factory.generate_wc_button_icon(icon_index, (ActionIcon.WIDTH - 6, ActionIcon.HEIGHT - 6), action)
        icon.set_position((6, 6))
        hotkey_rect = suie.Rectangle((ActionIcon.WIDTH - 18, ActionIcon.HEIGHT - 16), (20, 20),
                                     ActionIcon.HOTKEY_BKGR_COLOR, ActionIcon.HOTKEY_BORDER_COLOR, 1)
        hotkey_text = suie.Label((ActionIcon.WIDTH - 12, ActionIcon.HEIGHT - 12), hotkey, 8, ActionIcon.HOTKEY_COLOR)
        self.shadow = suie.Rectangle((0, 0), (ActionIcon.WIDTH + 6, ActionIcon.HEIGHT + 6), (30, 30, 30, 150))
        self.shadow.visible = False

        self.add_child(border)
        self.add_child(icon)
        self.add_child(hotkey_rect)
        self.add_child(hotkey_text)
        self.add_child(self.shadow)

    def enable(self, flag: bool):
        self.shadow.visible = not flag

