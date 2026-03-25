

current_pressed = []


def key_press(key):
    current_pressed.append(key)

def key_release(key):
    try:
        current_pressed.remove(key)
    except:
        pass