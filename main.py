import arcade
import arcade.gui

import functions.settings as settings
import functions.player as player
import functions.player_movement as playmov
import functions.pause_screen as pause_screen
import functions.game_over as game_over
import functions.items_screen as items_screen
import functions.menu as menu
import functions.key_handler as key_handler
import functions.screen_logic as screen_logic
import functions.UI as UI
import functions.collision_logic as colls
import functions.misc as misc
import functions.Battleview as battleview
import functions.dialogue_interface as dia_int

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
        #all game variables are set up here
        #it is automatically called when the game first starts, but can also be manually called to restart the game

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
        
        #Dialogue Interface
        self.current_dialogue = False
        self.current_screen = "TestMap.tmx"

        #Create a player object based on the player class from the player file
        self.player = player.Player(
            settings.INGAME_WIDTH * 0.5 * self.x_scale,
            settings.INGAME_HEIGHT * 0.5 * self.y_scale,
            self.either_scale,
            self
        )

        #items screen
        self.items_screen = items_screen.ItemsScreen(self)

        misc.load_scene(self, self.current_screen)


        UI.setup_hud(self)#load the function to set up the HUD (health, power, etc.) from UI.py
        self.player.set_xp(self.player.current_xp)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        self.scene.draw(pixelated=True)

        if self.current_dialogue: #Check if there is currently a dialogue_box to be drawn
            self.dialogue_box.draw() #Call the draw method on it (from the speech_box class in dialogue_interface.py)

        if self.menu:#if the menu variable is true, draw the menu screen
            self.menu_screen.draw()#call the on_draw function from menu.py

        if self.battle:
            self.battleview.draw()#call the on_draw function from battle_view.py

        #draw the HUD, but not in the starting menu (not self.menu)
        if not self.menu:
            self.hud_ui.draw()#draw the HUD (health, etc.)
        
        if self.items_screen.show_items:
            self.items_screen.draw()

        if self.paused:#if the game is paused, draw the pause screen 
            self.pause_screen.draw()#call the on_draw function from pause_screen.py

        if self.game_over:#if the game is over, draw the game over screen#############################Game over trigger --> game_over = True
            self.game_over_screen.draw()#call the on_draw function from game_over.py


    def on_update(self, delta_time):
        #function to update everything in the game, called every frame

        #menu
        if self.menu:#if the menu variable is true, enable the menu screen and skip the rest of the update function
            self.menu_screen.enable()
            return 
        else:
            self.menu_screen.disable()#Disable the game over screen when the game is not over

        if self.player.health <= 0:#if the player's health is 0 or less, trigger the game over state
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

        if self.items_screen.show_items:
            self.items_screen.update(delta_time)
            return
        
        if self.current_dialogue: #if there is currently a dialogue_box
            return #skip the rest of on_update() so the game is paused

        directions = playmov.calc_movement()
        directions["x"] *= self.x_scale
        directions["y"] *= self.y_scale
        playmov.move_player(self.player, directions, self.scene["Obstacles"])
        
        collision_entity = colls.coll_check(self.player, self.entity_list, True)
        if collision_entity:
            collision_entity.collision(self)

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

        key_handler.key_press(key, key_modifiers,self)
      

    def on_key_release(self, key, key_modifiers):
        
        key_handler.key_release(key)



def main():
    #function to run the game
    game = MyGame(1920, 1080, settings.SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__": #if this file is executed, run the game
    main()