import arcade
import settings

class Player(arcade.Sprite):
    def __init__(self, x, y, scale):
        super().__init__("assets/player.png", scale = scale)
        self.center_x = x
        self.center_y = y