import arcade
import settings
import player

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)

        arcade.set_background_color(arcade.color.AMAZON)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.all_sprites = None

        self.window_width, self.window_height = self.get_size()

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.all_sprites = arcade.SpriteList()

        self.player = player.Player(self.window_width // 2, self.window_height // 2)
        self.all_sprites.append(self.player)


        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        self.all_sprites.draw(pixelated=True)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main function """
    game = MyGame(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()