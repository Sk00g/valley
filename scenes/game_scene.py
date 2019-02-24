

# Base class for scenes, list is statically handled
class GameScene:
    scene_stack = []

    def __init__(self):
        GameScene.scene_stack.append(self)

    @staticmethod
    def pop_scene():
        scene = GameScene.scene_stack.pop()
        scene.cleanup()

    @staticmethod
    def clear_and_switch(new_scene):
        while len(GameScene.scene_stack) > 1:
            scene = GameScene.scene_stack.pop()
            scene.cleanup()

        GameScene.scene_stack = [new_scene]

    @staticmethod
    def update_current(event_list, elapsed):
        GameScene.scene_stack[-1].update(event_list, elapsed)

    @staticmethod
    def draw_current(screen):
        GameScene.scene_stack[-1].draw(screen)

    def cleanup(self):
        raise Exception('This should have been overridden')

    def update(self, event_list, elapsed):
        raise Exception('This should have been overridden')

    def draw(self, screen):
        raise Exception('This should have been overridden')