import pyglet

import settings



def realpix(game, ingpix):
    scale_x = game.window_width // settings.INGAME_WIDTH
    scale_y = game.window_height // settings.INGAME_HEIGHT
    scale = min(scale_x, scale_y)
    return ingpix * scale