import arcade
from arcade import Rect
import textwrap
import functions.settings as settings

class speech_box():
    def __init__(self, entity, scale, game):

        #temporary variables that allow for the interface to be made in % of the screen (0.5 * wid => horizontal middle of the screen)
        wid = settings.INGAME_WIDTH * scale
        hei = settings.INGAME_HEIGHT * scale

        #save all important objects to our speech_box-object
        self.game = game
        self.game.current_dialogue = True

        self.entity = entity

        #setting up the logic for the lines of dialogue, taken from the json file
        self.line = 0
        self.lines = entity.dialogue
        self.lines_amount = len(self.lines)

        #check if the first line of dialogue is a combat trigger
        combat = False
        if self.lines[0] == "combat":
            enemy_data = {"max_hp": self.entity.max_hp,
                          "attack": self.entity.attack,
                          "red_time": self.entity.red_time,
                          "xp_reward": self.entity.xp_reward,
                          "coin_reward": self.entity.coin_reward}
            game.battle = True
            game.battleview.start_battle(enemy_data)
            combat = True
            
            
        #variables to hold the current text and speaker (= icon)
        self.current_text = self.lines[0][1]
        self.current_speaker = self.lines[0][0]

        #from here on it's just visuals & text-handling

        self.icon_sprite_NPC = arcade.Sprite(entity.texture, scale=scale)
        self.icon_sprite_NPC.center_x = wid * 0.142
        self.icon_sprite_NPC.center_y = hei * 0.275
        self.NPC_icon_list = arcade.SpriteList() #arcade can only draw sprite lists
        self.NPC_icon_list.append(self.icon_sprite_NPC)
        
        self.icon_sprite_player = arcade.Sprite(game.player.dia_icon, scale=scale)
        self.icon_sprite_player.center_x = wid * 0.142
        self.icon_sprite_player.center_y = hei * 0.275
        self.player_icon_list = arcade.SpriteList()
        self.player_icon_list.append(self.icon_sprite_player)

        #using textwrap.wrap, because the arcade multiline feature is based on amount of characters instead of pixels and that isn't always smooth
        wrapped_text = "\n".join(
            textwrap.wrap(
                self.current_text,
                width=97,
                break_long_words=False,
                break_on_hyphens=False
            )
        )

        self.text_object = arcade.Text(
            text = wrapped_text,
            x = wid * 0.2,
            y = hei * 0.3,
            width = wid * 0.8,
            multiline = True,
            color = arcade.color.BLACK,
            font_size = 20
        )

        box_x = wid / 2
        box_y = hei * 0.2
        box_width = wid * 0.8
        box_height = hei * 0.3


        self.text_box = Rect.from_kwargs(
            x = box_x,
            y = box_y,
            width = box_width,
            height = box_height
        )

        

        if combat:
            self.next_line(game)



    def next_line(self, game): #function to go to the next line of dialogue, triggered by arrow down key (from key_handler.py)
        if self.line < self.lines_amount - 1: #check if there are lines left
            self.line += 1

            if self.lines[self.line] == "combat": #check if this line is a combat trigger
                enemy_data = {"max_hp": self.entity.max_hp,
                              "attack": self.entity.attack,
                              "red_time": self.entity.red_time,
                              "xp_reward": self.entity.xp_reward,
                              "coin_reward": self.entity.coin_reward}
                game.battle = True
                game.battleview.start_battle(enemy_data) #trigger combat
                self.line += 1 #skip this line, as it is only a trigger and not actual dialogue
            
            #update text & current_speaker to the new line

            self.current_displayed_text = self.lines[self.line][1]
            self.current_speaker = self.lines[self.line][0]
            
            self.text_object.text = "\n".join(
                textwrap.wrap(
                    self.current_displayed_text,
                    width=97,
                    break_long_words=False,
                    break_on_hyphens=False
                )
            )

        else: #if there are no lines left
            self.kill() #end the dialogue
    
    def draw(self): #draws everything related to the dialogue box, called in the draw-part of the main game loop in main.py

        wid = settings.INGAME_WIDTH * self.game.either_scale
        hei = settings.INGAME_HEIGHT * self.game.either_scale

        arcade.draw_rect_filled(
            self.text_box,
            (255, 255, 255, 150)
        )

        arcade.draw_rect_outline(
            self.text_box,
            (0, 0, 0, 255),
            border_width = 5
        )

        arcade.draw_triangle_filled(
            wid * 0.8625, hei * 0.08,
            wid * 0.8875, hei * 0.08,
            wid * 0.875, hei * 0.065,
            arcade.color.RED
        )

        self.text_object.draw()

        if self.current_speaker == "NPC":
            self.NPC_icon_list.draw(pixelated=True)

        elif self.current_speaker == "Player":
            self.player_icon_list.draw(pixelated=True)

    def kill(self):
        self.game.current_dialogue = False #sets the flag for a currently active dialogue to false, letting the game resume normally
        self.game.dialogue_box = None #removes the reference to the dialogue box object, effectively deleting it
    