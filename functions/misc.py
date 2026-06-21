import arcade
import functions.entity as ent

def load_scene(game, new_map): #loads a scene from a Tiled map
    game.tile_map = arcade.load_tilemap("assets/"+new_map, scaling=game.either_scale) #loads the map
    game.scene = arcade.Scene.from_tilemap(game.tile_map) #creates a scene from the map
    game.scene.add_sprite("Player", game.player) #adds the player to the scene
    game.edge_list = game.tile_map.object_lists["Trigger"] #creates a list of trigger objects, currently only used the switch screens
    game.entity_sprite_list = game.tile_map.sprite_lists["Entities"] #creates a list of all entity sprites

    #create a list of entities. these are the same as in entity_sprite_list, except they are converted to our own custom Entity class
    game.entity_list = []

    for entity in game.entity_sprite_list:
        if entity.properties["type"] == "npc":
            npc_object = ent.NPC.from_sprite(entity)
            game.entity_list.append(npc_object)