import arcade
import functions.entity as ent

def load_scene(game, new_map):
    game.tile_map = arcade.load_tilemap("assets/"+new_map, scaling=game.either_scale)
    game.scene = arcade.Scene.from_tilemap(game.tile_map)
    game.scene.add_sprite("Player", game.player)
    game.edge_list = game.tile_map.object_lists["Trigger"]
    game.entity_sprite_list = game.tile_map.sprite_lists["Entities"]

    game.entity_list = []

    for entity in game.entity_sprite_list:
        if entity.properties["type"] == "npc":
            npc_object = ent.NPC.from_sprite(entity)
            game.entity_list.append(npc_object)