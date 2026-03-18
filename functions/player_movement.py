import arcade
import functions.settings as settings

current_pressed = []
directions = {"x":0, "y":0}

def key_press(key):
    current_pressed.append(key)

def key_release(key):
    try:
        current_pressed.remove(key)
    except:
        pass

def calc_movement(player):
    up = "W" in current_pressed
    down = "S" in current_pressed
    directions["y"] = up - down

    left = "A" in current_pressed
    right = "D" in current_pressed
    directions["x"] = right - left

    return directions
    