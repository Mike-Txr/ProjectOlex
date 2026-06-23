#basic player class, for variables and functions
import arcade

from PIL import Image
import io

import functions.settings as settings
import functions.entity as entity

class Player(entity.Entity):
    def __init__(self, x, y, scale, game=None):

        self.debug_variable = False#just for debug/presentation for the teacher

        self.facing = "south"

        super().__init__(x, y, scale, "player/"+self.facing+".png")

        
        self.dia_icon = "assets/player_dia.png"

        #our player texture is handled like this:
        #there are 8 gif files, looking in each direction
        #every one of them is animated with the players walk animation
        #here we are loading every single one of these gif-files as frames
        self.animation_frames = {
            "north": self.extract_frames_from_gif("assets/player/north.gif"),
            "south": self.extract_frames_from_gif("assets/player/south.gif"),
            "east": self.extract_frames_from_gif("assets/player/east.gif"),
            "west": self.extract_frames_from_gif("assets/player/west.gif"),
            "north-east": self.extract_frames_from_gif("assets/player/north-east.gif"),
            "north-west": self.extract_frames_from_gif("assets/player/north-west.gif"),
            "south-east": self.extract_frames_from_gif("assets/player/south-east.gif"),
            "south-west": self.extract_frames_from_gif("assets/player/south-west.gif"),
        }

        #converting the frames to textures
        self.textures = {}
        for direction, pil_frames in self.animation_frames.items():
            self.textures[direction] = [
                arcade.Texture(image=frame) for frame in pil_frames
            ] 

        #these textures are loaded from png files
        #there are also 8 of them, looking in each direction
        #but they are not animated.
        #instead, this is just how the player is supposed to look when not moving
        self.idle_textures = {
            direction: arcade.load_texture(f"assets/player/{direction}.png")
            for direction in self.animation_frames
        }

        self.animation_enabled = False
        self.current_frame = 0 #index for going through the frames
        self.frame_counter = 0 #timer for how long we've been at the current frame
        self.frame_speed = 0.1 #time for how long we're supposed to be at each frame
        self.last_facing = self.facing  #store previous direction to detect direction changes


        self.game = game
        
        #Main Game Variables
        self.max_health = 10#max_health variable, could be changed throughout the game
        self.health = self.max_health#current health variable, starts with max health

        self.max_power = 50#max_power variable, could be changed throughout the game
        self.power = self.max_power#current power variable, starts with max power

        self.attack = 2#variable for the attack stat, could be changed throughout the game

        self.level = 1#variable for the current level, starts at 1
        self.levelup = 100#variable, level up will be reached at 100
        self.current_xp = 0#current experience points variable

        if self.debug_variable == True:
            self.current_xp = 80

        self.coins = 10#variable for coins, could be changed throughout the game

        #"inventory" --> the current number
        self.sausages = 0#variable for sausages, fills up hearts
        self.pills = 0#variable for pills, fills up power
        self.sausage_heal_amount = 5#how much a sausage heals
        self.pill_power_amount = 10#how much a pill restores power

    #function to set the health of the player, which also updates the health label
    def set_health(self, value: int):
        self.health = max(0, min(self.max_health, value))#health is set to the value, but it can't be lower than 0 or higher than max health
        if self.game is not None:
            self.game.health_label.text = f"{self.health} / {self.max_health}"#update the health label in the game, which shows the current health and max health of the player

    #function to set the power of the player, which also updates the power label
    def set_power(self, value: int):
        self.power = max(0, min(self.max_power, value))#power is set to the value, but it can't be lower than 0 or higher than max power
        if self.game is not None:
            self.game.power_label.text = f"{self.power} / {self.max_power}"#update the power label in the game, which shows the current power and max power of the player

    #function to set the XP of the player, which also updates the level progress bar and level label
    def set_xp(self, value: int):
        self.current_xp = max(0, value)#current XP is set to the value, but it can't be lower than 0, there is no upper limit for XP, because when the player reaches the level up XP, the current XP will be reduced by the level up

        while self.current_xp >= self.levelup:#if the current XP is higher than or equal to the level up XP, the player levels up
            self.current_xp -= self.levelup
            self.level += 1#plus 1, because it must not be 0, because of division by 0. 1 isn't very visible in the progress
            print("Level up! Aktuelles Level:", self.level)

        if self.game is not None:#update the level label and progress bar
            if self.level > 0:
                progress = self.current_xp / self.levelup#progress is calculated by current XP divided by level up XP, which is then used to fill the level progress bar
            else:
                progress = 0

            progress = max(0, min(1, progress))#progress is set to the value, but it can't be lower than 0 or higher than 1, because it's used to fill the level progress bar, which is between 0 and 1
            self.game.level_label.text = f"{self.level}"#update the level label in the game, which shows the current level
            bar_width = max(1, self.game.level_panel_width - 100)#calculate the width of the level progress bar, which is the width of the level panel minus 100 pixels for padding, but it can't be lower than 1 pixel, because then the progress bar would be invisible
            self.game.level_bar_fill.width = max(1, int(bar_width * progress))#calculate the width of the filled part of the level progress bar, which is the width of the level progress bar multiplied by the progress

    #function to set the coins of the player, which also updates the coin label
    def set_coins(self, value: int):
        self.coins = max(0, value)#does not have an upper limit
        if self.game is not None:
            self.game.coins_label.text = f"{self.coins}"#update the coin label in the game, which shows the current coins of the player

    #function to add sausages, which updates the sausage count
    def add_sausage(self, amount: int = 1):
        self.sausages = max(0, self.sausages + amount)
        print(f"Added {amount} sausage(s). Total sausages: {self.sausages}")

    #function to add pills, which updates the pill count
    def add_pill(self, amount: int = 1):
        self.pills = max(0, self.pills + amount)
        print(f"Added {amount} pill(s). Total pills: {self.pills}")

    #function to use a sausage to increase current health
    def use_sausage(self):
        if self.sausages <= 0:#if ther are no, cant be used
            return False
        if self.health >= self.max_health:#if the health is already full, cant be used
            return False

        self.sausages -= 1
        self.set_health(self.health + self.sausage_heal_amount)#value, can be easily modified
        return True

    #function to use a pill to increase current power, same as sausages but with power
    def use_pill(self):
        if self.pills <= 0:
            return False
        if self.power >= self.max_power:
            return False

        self.pills -= 1
        self.set_power(self.power + self.pill_power_amount)
        return True
    

    def extract_frames_from_gif(self, filepath): #use the PIL library to extract our frames
        frames = []

        gif = Image.open(filepath)
        for frame_index in range(gif.n_frames):
            gif.seek(frame_index)
            frames.append(gif.copy().convert("RGBA"))

        return frames

    def update_animation(self, delta_time): #called each frame
        
        if self.animation_enabled: #only executed if the player is currently walking

            #delta_time is calculated by the arcade library - it's the time the last frame took to run
            self.frame_counter += delta_time
            
            if self.frame_counter >= self.frame_speed: #if we've been at the current frame for long enough
                #go to the next one
                self.frame_counter = 0
                self.current_frame += 1
                
                #if we're at the last frame, reset to the first one
                max_frames = len(self.textures[self.facing])
                if self.current_frame >= max_frames:
                    self.current_frame = 0
                
                #update texture
                self.texture = self.textures[self.facing][self.current_frame]
        
        else: #if the player is not currently walking, reset to the standard image (png)
            self.texture = self.idle_textures[self.facing]
    
    def update_texture(self): #update the player texture based on the direction the player is facing
        if self.facing != self.last_facing:
            self.last_facing = self.facing
            self.current_frame = 0
            self.frame_counter = 0
            self.texture = self.idle_textures[self.facing]