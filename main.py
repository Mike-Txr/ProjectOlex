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
import functions.UI as UI
import functions.collision_logic as colls
import functions.misc as misc
import functions.Battleview as battleview

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
       
        #Menu, should be shown at the start of the game only
        self.menu = True#Variable for menu (True because the game starts with the menu, False for disabling)
        self.menu_screen = menu.Menu(self)#class for the menu, which is defined in menu.py


    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        #Pause menu
        self.paused = False#Variable to hold paused state. Set to True to pause the game, False to unpause.
        self.pause_screen = pause_screen.PauseScreen(self)#class for the pause menu, which is defined in pause_screen.py
        
        #Game over screen
        self.game_over = False#Variable to hold game over state. Set to True to trigger the game over screen, False to disable it.
        self.game_over_screen = game_over.GameOver(self)#class for the game over screen, which is defined in game_over.py

        #battle view
        self.battle = False#Variable to hold battle state. Set to True to trigger the battle view, False to disable it.
        self.battle_screen = None
        self.current_enemy = None
        self.battleview = battleview.BattleScreen(self)

        #######Main Game Variables#######
        self.max_health = 10#max_health variable, could be changed throughout the game
        self.health = self.max_health#current health variable, starts with max health

        self.max_power = 50#max_power variable, could be changed throughout the game
        self.power = self.max_power#current power variable, starts with max power

        self.attack = 5#variable for the attack stat, could be changed throughout the game

        self.level = 1#variable for the current level, starts at 1
        self.levelup = 100#variable, level up will be reached at 100
        self.current_xp = 90#current experience points variable, starts with 50

        self.coins = 10#variable for coins, could be changed throughout the game


        self.current_screen = "TestMap.tmx"

        #Create a player object based on the player class from the player file
        self.player = player.Player(
            settings.INGAME_WIDTH*0.5*self.x_scale,
            settings.INGAME_HEIGHT*0.5*self.y_scale,
            self.either_scale)

        misc.load_scene(self, self.current_screen)


        UI.setup_hud(self)#load the function to set up the HUD (health, power, etc.) from UI.py
        self.set_xp(self.current_xp)

        pass
    
#############################These functions should maybe be moved to the corresponding .py files, but for now they stay here until more game logic is developed############

    #function to set the health of the player, which also updates the health label
    def set_health(self, value: int):
        self.health = max(0, min(self.max_health, value))
        self.health_label.text = f"{self.health} / {self.max_health}"

    def set_power(self, value: int):
        self.power = max(0, min(self.max_power, value))
        self.power_label.text = f"{self.power} / {self.max_power}"

    def set_xp(self, value: int):
        self.current_xp = max(0, value)

        leveled_up = False

        while self.current_xp >= self.levelup:
            self.current_xp -= self.levelup
            self.level += 1
            leveled_up = True
            print("Level up! Aktuelles Level:", self.level)
        
        if self.level > 0:
            progress = self.current_xp / self.levelup
        else:
            progress = 0

        progress = max(0, min(1, progress))#make sure the progress is between 0 and 1
        self.level_label.text = f"{self.level}"
        bar_width = max(1, self.level_panel_width - 100)#make sure the bar width is at least 1 to avoid errors
        self.level_bar_fill.width = max(1, int(bar_width * progress))

    def set_coins(self, value: int):
        self.coins = max(0, value)
        self.coins_label.text = f"{self.coins}"


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
            self.menu_screen.draw()#call the on_draw function from menu.py

        if self.battle:
            self.battleview.draw()#call the on_draw function from battle_view.py

        #draw the HUD, but not in the starting menu (not self.menu)
        if not self.menu:
            self.hud_ui.draw()#draw the HUD (health, etc.)

        if self.paused:#if the game is paused, draw the pause screen
            self.pause_screen.draw()#call the on_draw function from pause_screen.py
        
        if self.game_over:#if the game is over, draw the game over screen#############################Game over trigger --> game_over = True
            self.game_over_screen.draw()#call the on_draw function from game_over.py


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """

        #menu
        if self.menu:#if the menu variable is true, enable the menu screen and skip the rest of the update function
            self.menu_screen.enable()
            return 
        else:
            self.menu_screen.disable()#Disable the game over screen when the game is not over

        if self.health <= 0:#if the player's health is 0 or less, trigger the game over state
            self.game_over = True

        #game over screen
        if self.game_over:#if the game is over, enable the game over screen and skip the rest of the update function
            self.game_over_screen.enable()
            return 
        else:
            self.game_over_screen.disable()#Disable the game over screen when the game is not over

        #pause screen
        if self.paused:#if the game is paused, enable the pause screen and skip the rest of the update function
            self.pause_screen.enable()
            return 
        else:
            self.pause_screen.disable()#Disable the pause screen when the game is not paused

        if self.battle:#if the battle variable is true, enable the battle view and skip the rest of the update function
            self.battleview.enable()
            self.battleview.update(delta_time)
            return
        else:
            self.battleview.disable()#Disable the battle view when the battle variable is false


        directions = playmov.calc_movement(self.player)
        directions["x"] *= self.x_scale
        directions["y"] *= self.y_scale
        playmov.move_player(self.player, directions, self.scene["Obstacles"])
        
        collision_entity = colls.coll_check(self.player, self.entity_list)
        if collision_entity:
            collision_entity.collision()

        collision = screen_logic.check_collisions(self.player, self.edge_list)
        if collision: #if the player is sufficiently out of the screen to go to the next one

            current_coords = [self.player.center_x, self.player.center_y] #save current coords, in case the player needs to be reset

            #load new scene
            misc.load_scene(self, collision.properties["next_map"])
            screen_logic.correct_player_pos(self.player, collision, self.either_scale)

            if colls.coll_check(self.player, self.scene["Obstacles"]): #if there is an obstacle colliding with the player on the new screen
                
                misc.load_scene(self, self.current_screen) #load old scene again (player isn't allowed to change screens)

                #reset player to old position
                screen_logic.counter_correct_player_pos(self.player, collision, self.either_scale, current_coords)

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

        #if the menu, paused or game over screen is active, pass the key press event to the corresponding .py file
        if self.menu:
            self.menu_screen.on_key_press(key, key_modifiers)
            return
        
        if self.paused:
            self.pause_screen.on_key_press(key, key_modifiers)
            return
        
        if self.game_over:
            self.game_over_screen.on_key_press(key, key_modifiers)
            return
        
        if key == arcade.key.ESCAPE and not self.game_over:#only allow pausing if the game is not over (not self.game_over)
            self.paused = True
            
        if key == arcade.key.G:###############################only for debugging, will be removed later, triggers the game over screen when G is pressed
            self.game_over = not self.game_over
            
        if key == arcade.key.B:#################################only for debugging, will be removed later, triggers the battle view when B is pressed
            #enemy data will be part of a class later
            if not self.battle:
                enemy_data = {"max_hp": 5, "attack": 5, "red_time": 1.0, "xp_reward": 10, "coin_reward": 10}#########
                self.battle = True
                self.battleview.start_battle(enemy_data)
                
            else:
                self.battle = False
                self.battleview.disable()
                
            return
            
        if self.battle:
            self.battleview.on_key_press(key, key_modifiers)
            return
    
        
        
        

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