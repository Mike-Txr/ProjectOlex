import arcade
import functions.settings as settings
import functions.key_handler as kh
import functions.player as player

directions = {"x":0, "y":0}


def calc_movement(player):
    up = arcade.key.W in kh.current_pressed
    down = arcade.key.S in kh.current_pressed
    directions["y"] = up - down

    left = arcade.key.A in kh.current_pressed
    right = arcade.key.D in kh.current_pressed
    directions["x"] = right - left

    return directions

def move_player(player, directions):
    player.center_x += directions["x"]
    player.center_y += directions["y"]