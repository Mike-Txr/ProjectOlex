import arcade

import functions.settings as settings
import functions.player as player
import functions.player_movement as playmov
import functions.pause_screen as pause_screen
import functions.key_handler as key_handler
import functions.obstacles as obstacles
import functions.screen_logic as screen_logic

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)

        #arcade.set_background_color(arcade.color.AMAZON)

        self.paused = False # Variable to hold paused state. Set to True to pause the game, False to unpause.

        self.scene = None

        self.window_width, self.window_height = self.get_size()
        #x_scale und y_scale sind bei 16:9 Monitoren identisch
        self.x_scale = self.window_width / settings.INGAME_WIDTH
        self.y_scale = self.window_height / settings.INGAME_HEIGHT
        self.either_scale = min(self.x_scale, self.y_scale)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here


        #Load the tilemap (created with Tiled)
        self.tile_map = arcade.load_tilemap("assets/TestMap.tmx", scaling=self.either_scale)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.edge_list = self.tile_map.object_lists["Trigger"] #invisible elements to change map

        #Create a player object based on the player class from the player file
        self.player = player.Player(
            settings.INGAME_WIDTH*0.5*self.x_scale,
            settings.INGAME_HEIGHT*0.5*self.y_scale,
            self.either_scale)
        self.scene.add_sprite("Player", self.player)

        #load the pause screen (so it will load faster when needed)
        self.paused = True
        pause_screen.on_draw(self)
        self.paused = False

        #loads the simple physics engine 
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene["Obstacles"])


        pass

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        self.scene.draw(pixelated=True)

        pause_screen.on_draw(self) # call the on_draw function from pause_screen.py

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.paused:
            return
        

        directions = playmov.calc_movement(self.player)
        directions["x"] *= self.x_scale
        directions["y"] *= self.y_scale
        playmov.move_player(self.player, directions)

        collision = screen_logic.check_collisions(self.player, self.edge_list)
        if collision:
            self.tile_map = arcade.load_tilemap("assets/"+collision.properties["next_map"],
                                                scaling=self.either_scale)
            self.scene = arcade.Scene.from_tilemap(self.tile_map)
            self.scene.add_sprite("Player", self.player)
            self.edge_list = self.tile_map.object_lists["Trigger"]
            self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.scene["Obstacles"])
            self.player = screen_logic.correct_player_pos(self.player, collision, self.either_scale)

        self.physics_engine.update()
        self.scene.update(delta_time)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """

        key_handler.key_press(key)

        # Check if the user hit the Esc key and toggle paused state
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused

        

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
        
        #---buttons for the pause menu---
        if self.paused:
            #continue button
            if (
                self.window_width/2 - 100 < x < self.window_width/2 + 100
                and self.position_continue - 20 < y < self.position_continue + 20
            ):
                self.paused = False
            
            #restart button (not finished)######################################################################################
            if (
                self.window_width/2 - 100 < x < self.window_width/2 + 100
                and self.position_restart - 20 < y < self.position_restart + 20
            ):
                self.paused = False #needs to be changed when the restart function is implemented

            #quit button
            if (
                self.window_width/2 - 100 < x < self.window_width/2 + 100
                and self.position_quit - 20 < y < self.position_quit + 20
            ):
                arcade.exit()

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