import arcade
import functions.settings as settings
import json

class Entity(arcade.Sprite):

    def __init__(self, x, y, scale, file):
        super().__init__("assets/"+file, scale = scale)
        self.center_x = x
        self.center_y = y
    
    #Used to convert an arcade.Sprite object to an Entity object
    @classmethod
    def from_sprite(cls, sprite):
        obj = cls.__new__(cls)

        arcade.Sprite.__init__(
            obj,
            sprite.texture,
            scale=sprite.scale
        )

        obj.center_x = sprite.center_x
        obj.center_y = sprite.center_y

        obj.properties = getattr(sprite, "properties", {})

        return obj


class NPC(Entity):

    #NPC doesnt have an __init__ function - it only gets created by being converted from arcade.Sprite
    
    #Used to convert an arcade.Sprite object to an NPC object
    @classmethod
    def from_sprite(cls, sprite):
        obj = cls.__new__(cls) #creates new object from the class cls (=NPC in this case)

        #init on a sprite, to get all the basic logic a sprite needs
        arcade.Sprite.__init__(
            obj,
            sprite.texture,
            scale=sprite.scale
        )

        #basically the Entity init
        obj.center_x = sprite.center_x
        obj.center_y = sprite.center_y
        
        #from here on it's NPC specific

        #the dialogue json-files feature the lines an NPC says
        #if, instead of talking, a combat should trigger, the line just says "combat"
        file_location = "dialogue/" + sprite.properties["dialogue"]
        with open(file_location, "r") as file:
            obj.dialogue = json.load(file)
        
        

        #each NPC has a json-file with their stats attached
        #these lines read this json file to give the NPC-instance the stats from the json as properties
        file_location = "stats/" + sprite.properties["stats"]
        with open(file_location, "r") as file:
            stats = json.load(file)
        for stat, value in stats.items():
            setattr(obj, stat, value)

        obj.on_collision = "dialogue"

        return obj
    

    def collision(self):
        if self.on_collision == "dialogue":
            print(self.dialogue)
            self.on_collision = "nothing"

    