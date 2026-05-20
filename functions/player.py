import arcade
import functions.settings as settings
import functions.entity as entity

class Player(entity.Entity):
    def __init__(self, x, y, scale):
        super().__init__(x, y, scale, "player.png")
        self.center_x = x
        self.center_y = y