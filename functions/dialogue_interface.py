import arcade
from arcade import Rect
import textwrap
import functions.settings as settings

class speech_box():
    def __init__(self, entity, scale, game):

        wid = settings.INGAME_WIDTH * scale
        hei = settings.INGAME_HEIGHT * scale

        self.game = game
        self.game.current_dialogue = True

        self.entity = entity


        self.line = 0
        self.lines = entity.dialogue
        self.lines_amount = len(self.lines)

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
            
            

        self.current_text = self.lines[0][1]
        self.visible_characters = 0 #amount of characters that should currently be visible (for a typewriter effect)
        self.current_speaker = self.lines[0][0]

        
        self.icon_sprite_NPC = arcade.Sprite(entity.texture, scale=scale)
        self.icon_sprite_NPC.center_x = wid * 0.142
        self.icon_sprite_NPC.center_y = hei * 0.275
        self.NPC_icon_list = arcade.SpriteList()
        self.NPC_icon_list.append(self.icon_sprite_NPC)
        
        self.icon_sprite_player = arcade.Sprite(game.player.dia_icon, scale=scale)
        self.icon_sprite_player.center_x = wid * 0.142
        self.icon_sprite_player.center_y = hei * 0.275
        self.player_icon_list = arcade.SpriteList()
        self.player_icon_list.append(self.icon_sprite_player)


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



    def next_line(self, game):
        if self.line < self.lines_amount - 1:
            self.line += 1

            if self.lines[self.line] == "combat":
                enemy_data = {"max_hp": self.entity.max_hp,
                              "attack": self.entity.attack,
                              "red_time": self.entity.red_time,
                              "xp_reward": self.entity.xp_reward,
                              "coin_reward": self.entity.coin_reward}
                game.battle = True
                game.battleview.start_battle(enemy_data)
                self.line += 1
            
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

            self.visible_characters = 0
        else:
            self.kill()
    
    def draw(self):

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
        self.game.current_dialogue = False
        self.game.dialogue_box = None
    