import functions.settings as settings
import functions.dialogue_interface as dia_int
import arcade

current_pressed = []


def key_press(key, key_modifiers, game): #function to handle all key press events

    current_pressed.append(key) #add the pressed key to the list of currently pressed keys (used for player movement)


    #if the menu, paused or game over screen is active, pass the key press event to the corresponding .py file

    if game.menu:
        game.menu_screen.on_key_press(key, key_modifiers)
        return
    
    if game.paused:
        game.pause_screen.on_key_press(key, key_modifiers)
        return
    
    if game.game_over:
        game.game_over_screen.on_key_press(key, key_modifiers)
        return
    
    if game.items_screen.show_items:
        game.items_screen.on_key_press(key, key_modifiers)
        return
    
    if game.current_dialogue:
        if key == arcade.key.DOWN:
            game.dialogue_box.next_line(game)
    
    if game.battle:
        if key == arcade.key.ESCAPE:
            if game.battleview.submenu_open():
                game.battleview.on_key_press(key, key_modifiers)
                return
            else:
                game.paused = True
                return

        game.battleview.on_key_press(key, key_modifiers)
        return

    if key == arcade.key.ESCAPE and not game.game_over:#only allow pausing if the game is not over (not game.game_over)
            game.paused = True
            return

    if key == arcade.key.I:
        if game.menu or game.game_over or game.paused or game.battle or game.current_dialogue:
            return

        if game.items_screen.show_items:
            game.items_screen.close_items()
        else:
            game.items_screen.open_items()

        return 
    
    if key == arcade.key.G:###############################only for debugging, will be removed later, triggers the game over screen when G is pressed
        game.game_over = not game.game_over
        
    if key == arcade.key.B:#################################only for debugging, will be removed later, triggers the battle view when B is pressed
        #enemy data will be part of a class later
        if not game.battle:
            enemy_data = {"max_hp": 50, "attack": 5, "red_time": 1.0, "xp_reward": 10, "coin_reward": 10, "image": "assets/NPC.png"}#########
            game.battle = True
            game.battleview.start_battle(enemy_data)
            
        else:
            game.battle = False
            game.battleview.disable()
            
        return

    #pass key to the battleview file if there is currently an active battle    
    if game.battle:
        game.battleview.on_key_press(key, key_modifiers)
        return
        

def key_release(key): #function to handle key release events
    try:
        current_pressed.remove(key) #remove the released key from currently pressed keys list
    except:
        pass