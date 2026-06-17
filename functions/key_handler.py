import functions.settings as settings
import functions.dialogue_interface as dia_int
import arcade

current_pressed = []


def key_press(key, game):
    current_pressed.append(key)


    
    #debug: opening the dialogue interface
    if key == arcade.key.Q:
        game.dialogue_box = dia_int.speech_box(game.entity_list[1], game.either_scale)

def key_release(key):
    try:
        current_pressed.remove(key)
    except:
        pass