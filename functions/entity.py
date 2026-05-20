import arcade
import functions.settings as settings

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

    def __init__(self, x, y, scale, file):
        super().__init__(x, y, scale, file)
    
    #Used to convert an arcade.Sprite object to an NPC object
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

        obj.dialogue = sprite.properties.get("dialogue", "")

        return obj