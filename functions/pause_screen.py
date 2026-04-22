import arcade
import arcade.gui

class PauseScreen:#Klasse für die Buttons
    def __init__(self, game):
        self.game = game#is used to access the main game class

        self.manager = arcade.gui.UIManager()#Manager for the UI elements
        self.v_box = arcade.gui.UIBoxLayout()#Layout for the buttons

        center_x = self.game.window_width / 2#centers
        center_y = self.game.window_height / 2

        # --- Buttons ---
        #create buttons
        self.continue_button = arcade.gui.UIFlatButton(text="Continue", width=200)
        self.restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        #Events
        @self.continue_button.event("on_click")
        def _(event):
            self.game.paused = False
            self.game_over = True #in case the player clicks continue on the game over screen, it should unpause the game and disable the game over screen

        @self.restart_button.event("on_click")
        def _(event):
            self.game.paused = False
            self.game.setup()

        @self.quit_button.event("on_click")
        def _(event):
            arcade.exit()

        #Build layout
        self.v_box.add(self.continue_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.restart_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.quit_button)

        #anchor for the layout, so that it'll be centered
        self.anchor = arcade.gui.UIAnchorLayout()

        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.v_box
        )

        self.manager.add(self.anchor)

        #Paused text
        self.text_paused = arcade.Text(
            "PAUSED",
            center_x,
            center_y + 150,
            arcade.color.WHITE,
            60,
            anchor_x="center"
        )

    #create orange rectange and draw the buttons and text
    def draw(self):
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.game.window_width,
            0,
            self.game.window_height,
            arcade.color.ORANGE[:3] + (200,)
        )

        self.text_paused.draw()
        self.manager.draw()

    #enable and disable functions for the pause screen, which are called in the main update function
    def enable(self):
        self.manager.enable()

    def disable(self):
        self.manager.disable()


"""
import arcade
import arcade.gui

def on_draw(self):
    self.clear()

    self.scene.draw(pixelated=True)
    
    # Set Position of the buttons for the pause menu (used in the main for the mouse click detection)
    self.position_continue = self.window_height / 2
    self.position_restart = self.window_height / 2 - 50
    self.position_quit = self.window_height / 2 - 100

    self.text_paused = arcade.Text(
        "PAUSED",
        self.window_width / 2,
        self.window_height / 2 + 150,
        arcade.color.WHITE,
        60,
        anchor_x="center"
    )

    self.text_continue = arcade.Text(
        "Continue",
        self.window_width / 2,
        self.window_height / 2,
        arcade.color.WHITE,
        30,
        anchor_x="center"
    )

    self.text_restart = arcade.Text(
        "Restart",
        self.window_width / 2,
        self.window_height / 2 - 50,
        arcade.color.WHITE,
        30,
        anchor_x="center"
    )

    self.text_quit = arcade.Text(
        "Quit",
        self.window_width / 2,
        self.window_height / 2 - 100,
        arcade.color.WHITE,
        30,
        anchor_x="center"
    )

    if self.paused:
        # dark orange overlay
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=320*self.width,
            bottom=0,
            top=180*self.height,
            color=arcade.color.ORANGE[:3] + (200,))

        #set the texts

        self.text_paused.draw()
        self.text_continue.draw()
        self.text_restart.draw()
        self.text_quit.draw()
"""