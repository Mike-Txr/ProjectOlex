import arcade
from arcade import Rect
import textwrap
import functions.settings as settings

class speech_box():
    def __init__(self, entity, scale):

        wid = settings.INGAME_WIDTH * scale
        hei = settings.INGAME_HEIGHT * scale


        self.entity = entity


        self.line = 0
        self.lines = entity.dialogue
        self.current_text = self.lines[0][1]
        self.visible_characters = 0 #amount of characters that should currently be visible (for a typewriter effect)
        self.current_speaker = self.lines[0][0]

        self.icon_sprite_NPC = arcade.Sprite(entity.texture, scale=scale)
        self.icon_sprite_NPC.center_x = wid * 0.142
        self.icon_sprite_NPC.center_y = hei * 0.275
        self.NPC_icon_list = arcade.SpriteList()
        self.NPC_icon_list.append(self.icon_sprite_NPC)

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



    def next_line(self):
        self.line += 1

        self.current_displayed_text = self.lines[self.line][1]
        self.current_speaker = self.lines[self.line][0]
        

        self.visible_characters = 0
    
    def draw(self):

        arcade.draw_rect_filled(
            self.text_box,
            (255, 255, 255, 150)
        )

        arcade.draw_rect_outline(
            self.text_box,
            (0, 0, 0, 255),
            border_width = 5
        )

        self.text_object.draw()

        if self.current_speaker == "NPC":
            self.NPC_icon_list.draw(pixelated=True)
    