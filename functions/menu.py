import arcade
import arcade.gui

class Menu:#Klasse für die Buttons
    def __init__(self, game):
        self.game = game#is used to access the main game class

        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()

        #Center
        center_x = self.game.window_width / 2
        center_y = self.game.window_height / 2

        # --- Buttons ---
        self.start_button = arcade.gui.UIFlatButton(text="Start Daddys Adventure", width=200)
        self.github_button = arcade.gui.UIFlatButton(text="View on GitHub", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        @self.start_button.event("on_click")
        def _(event):
            self.game.menu = False#disable menu, start game
            self.game.setup()

        @self.github_button.event("on_click")
        def _(event):
            import webbrowser
            webbrowser.open("https://github.com/Mike-Txr/ProjectOlex")###########################link will probably change
       
        @self.quit_button.event("on_click")
        def _(event):
            arcade.exit()

        #create layout
        self.v_box.add(self.start_button)
        self.v_box.add(arcade.gui.UISpace(height=20))
        self.v_box.add(self.github_button)
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

        #Place holder, will probably be a logo#####################################
        self.text_menu = arcade.Text(
            "Daddys first christmas",
            center_x,
            center_y + 150,
            arcade.color.WHITE,
            60,
            anchor_x="center"
        )

        self.text_by = arcade.Text(
            "A Game by\n    Mike-Txr\n    FinjaAT\n    Matejastinkt",
            center_x - 600,
            center_y - 300,
            arcade.color.WHITE,
            20,
            multiline=True,
            width=300,
            anchor_x="center"
        )

    def draw(self):
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.game.window_width,
            0,
            self.game.window_height,
            arcade.color.GREEN
        )

        self.text_menu.draw()
        self.text_by.draw()
        self.manager.draw()

    def enable(self):
        self.manager.enable()

    def disable(self):
        self.manager.disable()