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
        #x_scale und y_scale sind bei 16:9 Monitoren identisch
        self.x_scale = self.window_width / settings.INGAME_WIDTH
        self.y_scale = self.window_height / settings.INGAME_HEIGHT
        self.either_scale = min(self.x_scale, self.y_scale)
        print(self.either_scale)
        print(self.window_width)
        print(self.window_height)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.all_sprites = arcade.SpriteList()

        self.player = player.Player(
            160*self.x_scale,
            90*self.y_scale,
            self.either_scale)
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
    game = MyGame(1920, 1080, settings.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()