import arcade
import arcade.gui

class GameOver:#Klasse für die Buttons
    def __init__(self, game):
        self.game = game#is used to access the main game class

        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        #Center
        center_x = self.game.window_width / 2
        center_y = self.game.window_height / 2

        # --- Buttons ---
        self.restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        @self.restart_button.event("on_click")
        def _(event):
            self.game.game_over = False
            self.game.setup()
       
        @self.quit_button.event("on_click")
        def _(event):
            arcade.exit()

        #create layout
        self.v_box.add(self.restart_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.quit_button)

        #anchor
        self.anchor = arcade.gui.UIAnchorLayout()

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.v_box
        )

        self.manager.add(self.anchor)

        # Text
        self.text_gameover = arcade.Text(
            "GAME OVER",
            center_x,
            center_y + 150,
            arcade.color.BLACK,
            60,
            anchor_x="center"
        )

    def draw(self):
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.game.window_width,
            0,
            self.game.window_height,
            arcade.color.RED[:3] + (200,)
        )

        self.text_gameover.draw()
        self.manager.draw()

    def enable(self):
        self.manager.enable()

    def disable(self):
        self.manager.disable()