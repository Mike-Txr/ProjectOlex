import arcade
import functions.settings as settings

class Obstacle(arcade.Sprite):
    def __init__(self, x, y, scale):
        super().__init__("assets/obstacle.png", scale = scale)
        self.center_x = x
        self.center_y = y

def check_collisions(player, obst_list):
    return arcade.check_for_collision_with_list(player, obst_list)