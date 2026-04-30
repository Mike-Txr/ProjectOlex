import arcade
import arcade.gui

import functions.settings as settings
import functions.player as player
import functions.player_movement as playmov
import functions.pause_screen as pause_screen
import functions.game_over as game_over
import functions.menu as menu
import functions.key_handler as key_handler
import functions.screen_logic as screen_logic
import functions.collision_logic as colls
import functions.misc as misc

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)

        #arcade.set_background_color(arcade.color.AMAZON)


        self.scene = None

        self.window_width, self.window_height = self.get_size()
        #x_scale und y_scale sind bei 16:9 Monitoren identisch
        self.x_scale = self.window_width / settings.INGAME_WIDTH
        self.y_scale = self.window_height / settings.INGAME_HEIGHT
        self.either_scale = min(self.x_scale, self.y_scale)

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


        self.current_screen = "TestMap.tmx"

        #Create a player object based on the player class from the player file
        self.player = player.Player(
            settings.INGAME_WIDTH*0.5*self.x_scale,
            settings.INGAME_HEIGHT*0.5*self.y_scale,
            self.either_scale)

        misc.load_scene(self, self.current_screen)



        

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
        

        collision = screen_logic.check_collisions(self.player, self.edge_list)
        if collision: #if the player is sufficiently out of the screen to go to the next one

            current_coords = [self.player.center_x, self.player.center_y] #save current coords, in case the player needs to be reset

            #load new scene
            misc.load_scene(self, collision.properties["next_map"])
            self.player = screen_logic.correct_player_pos(self.player, collision, self.either_scale)

            if colls.coll_check(self.player, self.scene["Obstacles"]): #if there is an obstacle colliding with the player on the new screen
                
                misc.load_scene(self, self.current_screen) #load old scene again (player isn't allowed to change screens)

                #reset player to old position
                self.player = screen_logic.counter_correct_player_pos(self.player, collision, self.either_scale, current_coords)
                
            else:
                #if the player is allowed to change screens, save the new map to the class variables
                self.current_screen = collision.properties["next_map"]

        colls.coll_check(self.player, self.scene["Obstacles"], True)

        self.scene.update(delta_time)

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