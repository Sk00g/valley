import suie
import factory
from avatar import Avatar


class AvatarIcon(suie.Panel):
    WIDTH = 90
    HEIGHT = 80
    FONT_SIZE = 10
    BKGR_COLOR = (10, 20, 30, 255)
    ACTION_COLOR = (120, 120, 220, 255)
    POWER_COLOR = (220, 120, 120, 255)
    STACK_COLOR = (120, 220, 120, 255)

    def __init__(self, position, avatar: Avatar):
        suie.Panel.__init__(self, position, (AvatarIcon.WIDTH, AvatarIcon.HEIGHT))

        self._avatar = avatar

        border = suie.Border((0, 0), (AvatarIcon.WIDTH, AvatarIcon.HEIGHT), AvatarIcon.BKGR_COLOR)
        icon = factory.generate_wc_icon(avatar.icon_index, (60, 62))
        icon.set_position((6, 6))
        self.life_bar = suie.ProgressBar((4, 69), (86, 11), suie.BAR_COLOR_GREEN)
        self.action = suie.Label((AvatarIcon.WIDTH - 17, 8), "", font_size=AvatarIcon.FONT_SIZE, color=AvatarIcon.ACTION_COLOR)
        self.power = suie.Label((AvatarIcon.WIDTH - 22, 28), str(avatar.power), font_size=AvatarIcon.FONT_SIZE, color=AvatarIcon.POWER_COLOR)
        self.stack = suie.Label((AvatarIcon.WIDTH - 22, 48), str(avatar.get_stack_count()), font_size=AvatarIcon.FONT_SIZE, color=AvatarIcon.STACK_COLOR)
        self.shadow = suie.Rectangle((0, 0), (AvatarIcon.WIDTH + 6, AvatarIcon.HEIGHT + 6), (0, 0, 0, 100))

        self.add_child(border)
        self.add_child(icon)
        self.add_child(self.life_bar)
        self.add_child(self.action)
        self.add_child(self.power)
        self.add_child(self.stack)
        self.add_child(self.shadow)

    def highlight(self, flag: bool):
        self.shadow.visible = not flag

    def get_avatar(self):
        return self._avatar

    def set_action(self, action):
        self.action.set_text(action)

    def update(self, event_list):
        self.life_bar.set_fill(self._avatar._current_life / self._avatar.max_life)
        self.power.set_text(str(self._avatar.power))
        self.stack.set_text(str(self._avatar.get_stack_count()))

        super().update(event_list)

