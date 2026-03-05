import arcade
import settings
import misc_func

class Player(arcade.Sprite):
    def __init__(self, x, y, scale = settings.SCALE):
        super().__init__("assets/player.png", scale = scale)
        self.center_x = x
        self.center_y = y