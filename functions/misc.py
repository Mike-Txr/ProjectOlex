import arcade


def load_scene(game, new_map):
    game.tile_map = arcade.load_tilemap("assets/"+new_map, scaling=game.either_scale)
    game.scene = arcade.Scene.from_tilemap(game.tile_map)
    game.scene.add_sprite("Player", game.player)
    game.edge_list = game.tile_map.object_lists["Trigger"]