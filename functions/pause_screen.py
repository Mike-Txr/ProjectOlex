#manages the pause screen
import arcade
import arcade.gui

class PauseScreen:#class for the Buttons
    def __init__(self, game):
        self.game = game#is used to access the main game class

        #load manager and UIBox
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        #Dimensions of the center
        center_x = self.game.window_width / 2
        center_y = self.game.window_height / 2

        #Arrow (realised with a sprite, which is rotated to point to the selected button)
        self.ui_sprites = arcade.SpriteList()
        self.arrow = arcade.Sprite("assets/arrow.png", scale=0.1)
        self.ui_sprites.append(self.arrow)

        #initial position of the arrow, will be updated in the draw function
        self.arrow.center_x = 0
        self.arrow.center_y = 0
        
        #create buttons
        self.continue_button = arcade.gui.UIFlatButton(text="Continue", width=200)
        self.restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        self.buttons = [self.continue_button, self.restart_button, self.quit_button]#list for the arrow to know which button is selected
        self.selected_index = 0#index, used to keep track of which button is selected, starts with the first button (Continue)

        #events for the buttons (mouse click), which calls the activate_selected function
        @self.continue_button.event("on_click")
        def _(event):
            self.selected_index = 0
            self.activate_selected()

        @self.restart_button.event("on_click")
        def _(event):
            self.selected_index = 1
            self.activate_selected()

        @self.quit_button.event("on_click")
        def _(event):
            self.selected_index = 2
            self.activate_selected()

        #create layout of the buttons
        self.v_box.add(self.continue_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.restart_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.quit_button)

        #anchor layout to position the buttons in the center of the screen
        self.anchor = arcade.gui.UIAnchorLayout()
        self.anchor.add(anchor_x="center_x", anchor_y="center_y", child=self.v_box)
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


    #Keyboard events to navigate through the buttons, which also calls the activate_selected function when the enter key is pressed
    def on_key_press(self, symbol, modifiers):
        #the corresponding keys for navigating through the buttons, W and UP for up, S and DOWN for down, ENTER and RETURN to activate the selected button
        if symbol in (arcade.key.W, arcade.key.UP):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)

        elif symbol in (arcade.key.S, arcade.key.DOWN):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)

        elif symbol in (arcade.key.ENTER, arcade.key.RETURN):
            self.activate_selected()

        elif symbol == arcade.key.ESCAPE and not self.game.game_over:#only allow pausing if the game is not over (not self.game_over)
            self.game.paused = not self.game.paused
    
    #function to activate the selected button and either continue, restart or quit
    def activate_selected(self):
        if self.selected_index == 0:
            self.game.paused = False#close the paused screen

        elif self.selected_index == 1:
            self.game.paused = False
            self.game.setup()#call setup = always equals restart

        elif self.selected_index == 2:
            arcade.exit()#close game

    #funciton to draw the paused screen, which is called in the main game loop when the paused screen is active
    def draw(self):
        #draw rectangle over the whole screen
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.game.window_width,
            0,
            self.game.window_height,
            arcade.color.ORANGE[:3] + (200,)
        )

        #draw the arrow next to the selected button, the position is updated based on the selected_index
        for i, button in enumerate(self.buttons):
            if i == self.selected_index:
                self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
                self.arrow.center_y = button.center_y

        #draw everything
        self.ui_sprites.draw()
        self.text_paused.draw()
        self.manager.draw()

    #functions to enable and disable the manager, which is used to handle the events for the buttons
    def enable(self):
        self.manager.enable()

    def disable(self):
        self.manager.disable()