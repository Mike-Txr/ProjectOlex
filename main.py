import arcade
import arcade.gui

import functions.settings as settings
import functions.player as player
import functions.player_movement as playmov
import functions.pause_screen as pause_screen
import functions.game_over as game_over
import functions.menu as menu
import functions.key_handler as key_handler
import functions.obstacles as obstacles

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)

        #arcade.set_background_color(arcade.color.AMAZON)

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

        ##Menu##
        self.menu = True#Variable for menu (True because the game starts with the menu)
        self.menu_screen = menu.Menu(self)#class for the menu, which is defined in functions/menu.py

        ##Pause menu##
        self.paused = False # Variable to hold paused state. Set to True to pause the game, False to unpause.
        self.pause_screen = pause_screen.PauseScreen(self)#class for the pause menu, which is defined in functions/pause_screen.py
        
        ##Game over##
        self.game_over = False # Variable to hold game over state. Set to True to trigger the game over screen, False to disable it.
        self.game_over_screen = game_over.GameOver(self)#class for the game over screen, which is defined in functions/game_over.py
        

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        self.all_sprites = arcade.SpriteList()

        self.tile_map = arcade.load_tilemap("assets/TestMap.tmx", scaling=self.either_scale)
        self.ground_list = self.tile_map.sprite_lists["Grass"]
        self.obstacle_list = self.tile_map.sprite_lists["Obstacles"]
        self.all_sprites.extend(self.ground_list)
        self.all_sprites.extend(self.obstacle_list)

        self.player = player.Player(
            settings.INGAME_WIDTH*0.5*self.x_scale,
            settings.INGAME_HEIGHT*0.5*self.y_scale,
            self.either_scale)
        self.all_sprites.append(self.player)
        

        """
        self.obstacle = obstacles.Obstacle(
            330*self.x_scale,
            180*self.y_scale,
            self.either_scale)
        self.obstacles.append(self.obstacle)
        self.all_sprites.append(self.obstacle)
        """

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.obstacle_list)


        

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

        if self.menu:#if the menu variable is true, draw the menu screen
            self.menu_screen.draw() # call the on_draw function from menu.py

        if self.paused:#if the game is paused, draw the pause screen
            self.pause_screen.draw() # call the on_draw function from pause_screen.py
        
        if self.game_over:#if the game is over, draw the game over screen#############################Game over trigger --> game_over = True
            self.game_over_screen.draw() # call the on_draw function from game_over.py


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        ###menu###
        if self.menu:#if the menu variable is true, enable the menu screen and skip the rest of the update function
            self.menu_screen.enable()
            return # Skip the rest of the update function if the menu is active
        else:
            self.game_over_screen.disable()#Disable the game over screen when the game is not over

        ###game over screen###
        if self.game_over:#if the game is over, enable the game over screen and skip the rest of the update function
            self.game_over_screen.enable()
            return # Skip the rest of the update function if the game is over
        else:
            self.game_over_screen.disable()#Disable the game over screen when the game is not over

        ###pause screen###
        if self.paused:#if the game is paused, enable the pause screen and skip the rest of the update function
            self.pause_screen.enable()
            return # Skip the rest of the update function if the game is paused
        else:
            self.pause_screen.disable()#Disable the pause screen when the game is not paused


        directions = playmov.calc_movement(self.player)
        directions["x"] *= self.x_scale
        directions["y"] *= self.y_scale
        playmov.move_player(self.player, directions)
        self.all_sprites.update()


        self.physics_engine.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """

        key_handler.key_press(key)

        # Check if the user hit the Esc key and toggle paused state
        if key == arcade.key.ESCAPE and not self.game_over: #only allow pausing if the game is not over
            self.paused = not self.paused


        if key == arcade.key.SPACE:###############################only for debugging, will be removed later, triggers the game over screen when space is pressed
            self.game_over = not self.game_over
        

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

        key_handler.key_release(key)


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