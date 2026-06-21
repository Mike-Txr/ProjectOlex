import arcade
import functions.settings as settings
import functions.dialogue_interface as dia_int
import json

class Entity(arcade.Sprite):

    def __init__(self, x, y, scale, file): #this init-function is not currently used, but might be useful later
        super().__init__("assets/"+file, scale = scale)
        self.center_x = x
        self.center_y = y


    @classmethod #this declares the following method to be a "class method", meaning it's called on the class itself instead of an instance of it
    def from_sprite(cls, sprite): #Used to convert an arcade.Sprite object to an Entity object
        obj = cls.__new__(cls) #create a new instance of our class (saved in cls)

        arcade.Sprite.__init__( #initialize the new object as a sprite, giving us all the basic features of a sprite (as the Entity class is a subclass of arcade.Sprite)
            obj,
            sprite.texture,
            scale=sprite.scale
        )

        #these are the new properties, unique to Entity and it's subclasses
        obj.center_x = sprite.center_x
        obj.center_y = sprite.center_y

        #look at the properties of the original sprite and save them to our object. the sprite itself gets these properties from it's tmx-file (can be viewed in Tiled)
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

        #when the player collides with an NPC, its dialogue file should determine what happens next
        obj.on_collision = "dialogue"

        return obj
    

    def collision(self, game): #called in main.py when the player collides with an NPC
        if self.on_collision == "dialogue":
            game.dialogue_box = dia_int.speech_box(self, game.either_scale, game) #let dialogue_interface.py handle everything dialogue-related
            self.on_collision = "nothing" #after interacting with the NPC once, it can not be interacted with again

    