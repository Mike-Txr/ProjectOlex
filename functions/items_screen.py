#manages the items screen (just for overworld)
import arcade
import arcade.gui

class ItemsScreen:#class for the buttons
    def __init__(self, game):
        self.game = game#is used to access the main game class

        self.show_items = False#variable to show the items screen, which is handled in the main game loop in the on_draw function
        self.selected_index = 0#index, used to keep track of which button is selected, starts with the first button

        #load manager and UIBox
        self.manager = arcade.gui.UIManager()#contains all the UI elements, which are drawn in the draw function, can be enabled and disabled
        self.v_box = arcade.gui.UIBoxLayout()#v_box is used to arrange the buttons vertically, which is added to the manager in the draw function

        #Dimensions of the center (for easier use in the draw function)
        center_x = self.game.window_width / 2
        center_y = self.game.window_height / 2

        #load item textures
        self.sausage_texture = arcade.load_texture("assets/sausages.png")
        self.pill_texture = arcade.load_texture("assets/pills.png")

        #Arrow (realised with a sprite, which is rotated to point to the selected button)
        self.ui_sprites = arcade.SpriteList()
        self.arrow = arcade.Sprite("assets/arrow.png", scale=0.1)
        self.ui_sprites.append(self.arrow)

        #initial position of the arrow, will be updated in the draw function
        self.arrow.center_x = 0
        self.arrow.center_y = 0

        #preview image for the selected item
        self.preview_sprites = arcade.SpriteList()
        self.item_preview = arcade.Sprite()
        self.item_preview.texture = self.sausage_texture
        self.item_preview.scale = 0.6
        self.item_preview.center_x = self.game.window_width * 0.75
        self.item_preview.center_y = self.game.window_height * 0.52
        self.preview_sprites.append(self.item_preview)

        #create all the buttons
        self.sausage_button = arcade.gui.UIFlatButton(text="Use Sausage", width=240)
        self.pill_button = arcade.gui.UIFlatButton(text="Use Pill", width=240)
        self.back_button = arcade.gui.UIFlatButton(text="Back", width=240)

        self.buttons = [self.sausage_button, self.pill_button, self.back_button]#list for the arrow to know which button is selected

        #events for the buttons (mouse click), which calls the activate_selected function
        @self.sausage_button.event("on_click")
        def _(event):
            self.selected_index = 0
            self.activate_selected()

        @self.pill_button.event("on_click")
        def _(event):
            self.selected_index = 1
            self.activate_selected()

        @self.back_button.event("on_click")
        def _(event):
            self.selected_index = 2
            self.activate_selected()

        #create layout of the buttons
        self.v_box.add(self.sausage_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.pill_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.back_button)

        #anchors, used to position the buttons in the center of the screen, which is added to the manager
        self.anchor = arcade.gui.UIAnchorLayout()
        self.anchor.add(self.v_box, anchor_x="center_x", anchor_y="center_y")

        self.manager.add(self.anchor)

        #insert "ITEMS" text
        self.text_items = arcade.Text(
            "ITEMS",
            center_x,
            center_y + 200,
            arcade.color.WHITE,
            60,
            anchor_x="center"
        )

        #info text under the title
        self.text_info = arcade.Text(
            "",
            center_x,
            center_y + 145,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        #feedback text for usage messages
        self.feedback_text = ""
        self.feedback_timer = 0.0
        self.feedback_duration = 1.0

        #refresh preview and info once at start
        self.update_preview()
        self.update_info_text()


    #updates the item preview image based on the selected button
    def update_preview(self):
        if self.selected_index == 0:
            self.item_preview.texture = self.sausage_texture
        elif self.selected_index == 1:
            self.item_preview.texture = self.pill_texture
        else:
            self.item_preview.texture = self.sausage_texture


    #updates the info text with current item counts
    def update_info_text(self):
        self.text_info.text = f"Sausages: {self.game.player.sausages}   Pills: {self.game.player.pills}"


    #Keyboard events to navigate through the buttons, which also calls the activate_selected function when the enter key is pressed
    def on_key_press(self, symbol, modifiers):
        #the corresponding keys for navigating through the buttons
        if symbol in (arcade.key.W, arcade.key.UP) and self.show_items:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
            self.update_preview()

        elif symbol in (arcade.key.S, arcade.key.DOWN) and self.show_items:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
            self.update_preview()

        elif symbol in (arcade.key.ENTER, arcade.key.RETURN) and self.show_items:
            self.activate_selected()

        elif symbol == arcade.key.ESCAPE and self.show_items:
            self.close_items()

        elif symbol == arcade.key.I:
            self.close_items()
            return


    #function to activate the selected button and either use an item or close the screen
    def activate_selected(self):
        if self.selected_index == 0:
            used = self.game.player.use_sausage()
            if used:
                self.feedback_text = f"Used Sausage! +{self.game.player.sausage_heal_amount} HP"
                self.feedback_timer = self.feedback_duration
            else:
                self.feedback_text = "NO SAUSAGE / NO EFFECT!"
                self.feedback_timer = self.feedback_duration

        elif self.selected_index == 1:
            used = self.game.player.use_pill()
            if used:
                self.feedback_text = f"Used Pill! +{self.game.player.pill_power_amount} Power"
                self.feedback_timer = self.feedback_duration
            else:
                self.feedback_text = "NO PILL / NO EFFECT!"
                self.feedback_timer = self.feedback_duration

        elif self.selected_index == 2:
            self.close_items()

        self.update_info_text()


    #opens the items screen
    def open_items(self):
        self.show_items = True
        self.selected_index = 0
        self.update_preview()
        self.update_info_text()
        self.manager.enable()


    #closes the items screen
    def close_items(self):
        self.show_items = False
        self.manager.disable()


    #updates the feedback timer
    def update(self, delta_time):
        if self.feedback_timer > 0:
            self.feedback_timer -= delta_time
            if self.feedback_timer <= 0:
                self.feedback_text = ""


    #funciton to draw the items screen, which is called in the main game loop when the items screen is active
    def draw(self):
        if not self.show_items:
            return

        #draw rectangle over the whole screen (transparent)
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.game.window_width,
            0,
            self.game.window_height,
            arcade.color.LIGHT_BLUE[:3] + (200,)
        )

        #draw the arrow next to the selected button, the position is updated based on the selected_index
        for i, button in enumerate(self.buttons):
            if i == self.selected_index:
                self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
                self.arrow.center_y = button.center_y

        #draw everything
        self.ui_sprites.draw()
        self.preview_sprites.draw()
        self.text_items.draw()
        self.text_info.draw()
        self.manager.draw()

        if self.feedback_text != "":
            feedback = arcade.Text(
                self.feedback_text,
                self.game.window_width // 2,
                self.game.window_height * 0.28,
                arcade.color.WHITE,
                28,
                anchor_x="center"
            )
            feedback.draw()