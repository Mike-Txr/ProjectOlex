#main file for the whole fighting system, contains the battle logic

#Battle is basically started by doing this:
#enemy_data = {"max_hp": 50, "attack": 5, "red_time": 1.0, "xp_reward": 10, "coin_reward": 10}#########
#game.battle = True
#game.battleview.start_battle(enemy_data)

#and ends with:
#game.battle = False
#game.battleview.disable()
import arcade
import arcade.gui
from functions.Battlemenu import BattleMenu


class BattleScreen:
    def __init__(self, game):
        self.game = game#variable game, to access the main game class and its attributes like health, window_width, etc.
        self.ui = arcade.gui.UIManager()#set up UIManager
        self.root = arcade.gui.UIAnchorLayout()#set up the root layout to anchor the elements

        self.battle_background_texture = arcade.load_texture("assets/battle_background.png")#load background for battle
        self.background_anchor = arcade.gui.UIAnchorLayout()

        self.background_img = arcade.gui.UIImage(
            texture=self.battle_background_texture,
            width=self.game.window_width,
            height=self.game.window_height
        )

        self.background_anchor.add(self.background_img, anchor_x="center", anchor_y="center")
        self.ui.add(self.background_anchor)

        self.ui.add(self.root)#anchor becomes part of self.ui

        self.turn_indicator_sprite = arcade.Sprite("assets/arrow_turn.png", scale=0.12)
        self.turn_indicator_list = arcade.SpriteList()
        self.turn_indicator_list.append(self.turn_indicator_sprite)

        self.turn_indicator_visible = False

        self.current_enemy_texture = None

        self.enemy_sprite = arcade.Sprite()
        self.enemy_sprite.scale = 8.0

        self.enemy_sprite_list = arcade.SpriteList()
        self.enemy_sprite_list.append(self.enemy_sprite)

        self.current_enemy = None#variable to store the current enemy, which will be set when start_battle is called

        #important variables for the battle logic
        self.state = "inactive" #variable to track the state of the battle screen
        #can be: inactive, player_turn, player_timing_attack, enemy_turn, enemy_timing_block, resolving, power_spam, levelup, finished 
        self.timer = 0.0#create a timer variable to track the time since the last state change
        self.turn_delay = 1.5#delay between turns in seconds

        #variables for the timing mechanic (traffic light for blocking and standard attack)
        self.red_time = 1.2
        self.green_time = 0.35
        self.cue_time = 0.0
        self.green_active = False

        self.block_success = False
        self.current_enemy_health = 0

        self.feedback_text = ""
        self.feedback_timer = 0.0
        self.feedback_duration = 0.8

        self.levelup_pending = False

        #variables for the power spam mechanic
        self.power_spam_active = False
        self.power_attack_index = 0
        self.power_spam_count = 0
        self.power_spam_timer = 0.0
        self.power_spam_duration = 1.4

        #All the power attacks and their data, can be easily modified
        self.power_attack_data = [
            {"name": "Wonster flood", "target": 7,  "min_damage": 8,  "max_damage": 14, "power_cost": 5},
            {"name": "Wonster tsunami", "target": 11, "min_damage": 10, "max_damage": 20, "power_cost": 8},
            {"name": "Wonster hurricane", "target": 15, "min_damage": 12, "max_damage": 28, "power_cost": 12},
        ]

        #call Battlemenu.py, a helper class to set up the basic layout of the battle (Standard-Attack, Power-Attacks, Items)
        self.action_menu = BattleMenu(
            game=self.game,
            button_texts=["Standard-Attack", "Power-Attacks", "Items"],
            callbacks=[self.start_standard_attack, self.open_power_menu, self.open_items_menu],
            allow_space=False,
        )
        self.action_menu.disable()

        #again call Battlemenu.py, but this time for the power attacks submenu
        power_button_texts = [
            f"{data['name']}  ({data['power_cost']} Wonster)"
            for data in self.power_attack_data
        ]
        power_button_texts.append("Back")

        self.power_menu = BattleMenu(
            game=self.game,
            button_texts=power_button_texts,
            callbacks=[
                lambda i=i: self.choose_power_attack(i)
                for i in range(len(self.power_attack_data))
            ] + [self.close_power_menu],
            title_text="POWER ATTACKS",
            subtitle_text="Choose an attack!",
            button_width=400,
            escape_index=len(self.power_attack_data),
        )
        self.power_menu.disable()

        #again call Battlemenu.py, but this time for the levelup submenu
        self.levelup_menu = BattleMenu(
            game=self.game,
            button_texts=["Increase Max HP", "Increase Max Power", "Increase Attack"],
            callbacks=[
                lambda: self.apply_levelup_choice(0),
                lambda: self.apply_levelup_choice(1),
                lambda: self.apply_levelup_choice(2),
            ],
            title_text="LEVEL UP!",
            subtitle_text="Choose a stat to increase:",
            allow_space=False,
        )
        self.levelup_menu.disable()

        self.sausage_texture = arcade.load_texture("assets/sausages.png")
        self.pill_texture = arcade.load_texture("assets/pills.png")

        self.current_item_texture = self.sausage_texture

        self.item_preview = arcade.Sprite()
        self.item_preview.texture = self.current_item_texture
        self.item_preview.scale = 0.6
        self.item_preview.center_x = self.game.window_width * 0.75
        self.item_preview.center_y = self.game.window_height * 0.52

        self.item_preview_list = arcade.SpriteList()
        self.item_preview_list.append(self.item_preview)

        self.item_heal_amount = 5
        self.item_power_amount = 10

        self.items_menu = BattleMenu(
            game=self.game,
            button_texts=["Sausages", "Pills", "Back"],
            callbacks=[
                lambda: self.use_item("sausages"),
                lambda: self.use_item("pills"),
                self.close_items_menu,
            ],
            title_text="ITEMS",
            subtitle_text="",
            escape_index=2,
            allow_space=False,
        )
        self.items_menu.disable()

    #This function is called in the main game to start the battle, with all the enemy data passed as a dictionary
    def start_battle(self, enemy):
        #set the current enemy to the passed enemy data
        self.current_enemy = enemy
        self.current_enemy_health = self.current_enemy["max_hp"]

        self.state = "player_turn"#just indicates that the player is the first to act, will be used for the battle logic
        self.timer = 0.0#set timer for the battle
        self.cue_time = 0.0#set cue time for the battle, will be used for the timing mechanic
        self.green_active = False#set basic variables for the timing
        self.block_success = False

        self.feedback_text = ""#set future feedback_text
        self.feedback_timer = 0.0#and timer

        self.power_spam_active = False#set basic variables for the power spam mechanic
        self.power_attack_index = 0
        self.power_spam_count = 0
        self.power_spam_timer = 0.0

        if "image" in self.current_enemy:
            self.current_enemy_texture = arcade.load_texture(self.current_enemy["image"])
            self.enemy_sprite.texture = self.current_enemy_texture
            self.enemy_sprite.center_x = self.game.window_width * 0.8
            self.enemy_sprite.center_y = self.game.window_height * 0.35
        else:
            self.current_enemy_texture = None

        # reset the battle menus and enable the action menu for the player to choose their action
        self.action_menu.reset()
        self.power_menu.reset()
        self.levelup_menu.reset()
        self.items_menu.reset()

        self.action_menu.enable()
        self.power_menu.disable()
        self.levelup_menu.disable()
        self.items_menu.disable()

        self.levelup_pending = False#levelup_pending is set to false, because the player has not leveled up yet

    def submenu_open(self):
        return self.power_menu.enabled or self.items_menu.enabled or self.levelup_pending

    def start_standard_attack(self):#function to start the standard attack
        if self.state != "player_turn":
            return

        self.action_menu.disable()
        self.player_attack_pressed()

    def open_power_menu(self):#fucntion to open the power attacks and chosse from them
        if self.state != "player_turn":
            return

        self.action_menu.disable()
        self.power_menu.reset()
        self.power_menu.enable()

    def close_power_menu(self):#function to close the power attacks and go back if decision is changed by player
        self.power_menu.disable()
        self.action_menu.enable()

    def choose_power_attack(self, index):#function to choose a power attack, if the player has enough power, the power attack will be started
        if self.state != "player_turn" or not self.power_menu.enabled:
            return

        self.start_power_attack(index)

    def start_power_attack(self, index):#function to start one of the power attaks, the just differ in a few variables (spaming, costs, damage, ...)
        if self.state != "player_turn":
            return

        data = self.power_attack_data[index]
        cost = data["power_cost"]

        if self.game.player.power < cost:
            self.feedback_text = "NOT ENOUGH POWER!"
            self.feedback_timer = self.feedback_duration
            print("Not enough power to use")
            self.power_menu.enable()
            return

        self.game.player.set_power(self.game.player.power - cost)#decrease the player's power by the cost of the power attack

        #set the variables for the power spam mechanic, which will be used in the update function to determine how many times the player pressed space and how much time is left
        self.power_attack_index = index
        self.power_spam_count = 0
        self.power_spam_timer = self.power_spam_duration
        self.power_spam_active = True

        self.action_menu.disable()
        self.power_menu.disable()

        self.state = "power_spam"
        self.feedback_text = ""
        self.feedback_timer = 0.0

        print(f"{data['name']} started, costs {cost} Power")

    def resolve_power_attack(self):#function to resolve the power attack, which will be called when the power spam timer runs out, calculates the damage based on how many times the player pressed space and the target value of the power attack
        if self.state != "power_spam":
            return

        data = self.power_attack_data[self.power_attack_index]#based on the index of the power attack, the data is retrieved from the power_attack_data list
        target = data["target"]

        #calculate the damage based on how many times the player pressed space and the target value of the power attack, the damage is clamped between min_damage and max_damage
        ratio = min(self.power_spam_count / target, 1.0)
        damage = int(round(data["min_damage"] + (data["max_damage"] - data["min_damage"]) * ratio))
        damage = max(data["min_damage"], min(data["max_damage"], damage))

        self.feedback_text = f"{data['name']}! {damage} DMG"
        self.feedback_timer = self.feedback_duration

        self.current_enemy_health -= damage
        print(f"{data['name']} deals {damage} damage ({self.power_spam_count}x SPACE)")

        self.power_spam_active = False

        if self.current_enemy_health <= 0:#end battle, if the enemy's health is 0 or less, the battle is won and the end_battle function is called with win=True
            self.end_battle(win=True)
            return

        self.state = "enemy_turn"
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False

    #when the player levels up, this function is called to apply the chosen stat increase, and then the battle is ended
    def apply_levelup_choice(self, choice_index):
        if not self.levelup_pending:
            return

        if choice_index == 0:#increase max health by 5, and set current health to max health
            self.game.player.max_health += 5
            self.game.player.set_health(self.game.player.max_health)
            print("Max HP increased")

        elif choice_index == 1:#increase max power by 10, and set current power to max power
            self.game.player.max_power += 10
            self.game.player.set_power(self.game.player.max_power)
            print("Max Power increased")

        elif choice_index == 2:#increase attack by 2
            self.game.player.attack += 2
            print("Attack increased")

        #call the functions in player.py to set everything
        self.game.player.set_health(self.game.player.max_health)
        self.game.player.set_power(self.game.player.max_power)
        
        self.levelup_pending = False
        self.state = "inactive"
        self.current_enemy = None
        self.game.battle = False

        self.levelup_menu.disable()
        self.action_menu.disable()
        self.power_menu.disable()
        self.disable()

    def refresh_items_menu(self):
        self.items_menu.subtitle_text = (
            f"Sausages: {self.game.player.sausages}   "
            f"Pills: {self.game.player.pills}"
        )

    def update_item_preview(self, item_name: str):
        if item_name == "sausages":
            self.current_item_texture = self.sausage_texture
        elif item_name == "pills":
            self.current_item_texture = self.pill_texture

        self.item_preview.texture = self.current_item_texture

    def open_items_menu(self):
        if self.state != "player_turn":
            return

        self.action_menu.disable()
        self.power_menu.disable()

        self.refresh_items_menu()
        self.update_item_preview("sausages")
        self.items_menu.reset()
        self.items_menu.enable()

    def close_items_menu(self):
        self.items_menu.disable()
        if self.state == "player_turn":
            self.action_menu.enable()

    def use_item(self, item_name):
        if self.state != "player_turn" or not self.items_menu.enabled:
            return

        used = False

        if item_name == "sausages":
            used = self.game.player.use_sausage(self.item_heal_amount)
            if used:
                self.feedback_text = f"Used Sausage! +{self.item_heal_amount} HP"
                self.feedback_timer = self.feedback_duration

        elif item_name == "pills":
            used = self.game.player.use_pill(self.item_power_amount)
            if used:
                self.feedback_text = f"Used Pill! +{self.item_power_amount} Power"
                self.feedback_timer = self.feedback_duration

        if not used:
            self.feedback_text = "NO ITEM / NO EFFECT!"
            self.feedback_timer = self.feedback_duration
            return

        self.items_menu.disable()
        self.state = "enemy_turn"
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False
        self.action_menu.disable()

    #update function, mainly manages the timing mechanic and the power spam mechanic, as well as the state transitions
    def update(self, delta_time):
        if self.state in ("inactive", "finished"):#if inactive or finished, update nothing, just return
            return

        if self.feedback_timer > 0:#if feedback timer is greater than 0, decrease it by delta_time, and if it reaches 0, clear the feedback text
            self.feedback_timer -= delta_time
            if self.feedback_timer <= 0:
                self.feedback_text = ""

        self.timer = self.timer + delta_time

        if self.state == "player_timing_attack":#if the player is in the timing attack state, increase the cue time by delta_time, and if it reaches the red_time, set green_active to True, and if it reaches red_time + green_time, finish the attack timing with missed=True
            self.cue_time = self.cue_time + delta_time

            if self.cue_time >= self.red_time:
                self.green_active = True

                if self.cue_time >= self.red_time + self.green_time:
                    self.finish_attack_timing(missed=True)

        elif self.state == "enemy_turn":#block timing
            if self.timer >= self.turn_delay:
                self.start_block_timing()

        elif self.state == "enemy_timing_block":#enemy timing block
            self.cue_time += delta_time

            if self.cue_time >= self.current_enemy["red_time"]:
                self.green_active = True

            if self.cue_time >= self.current_enemy["red_time"] + self.green_time:
                self.resolve_enemy_attack(blocked=False)

        elif self.state == "power_spam":#if the player is in the power spam state, decrease the power spam timer by delta_time, and if it reaches 0, resolve the power attack
            self.power_spam_timer -= delta_time

            if self.power_spam_timer <= 0:
                self.resolve_power_attack()

    def player_attack_pressed(self):#function to start the timing mechanic for the standard attack, called when the player presses the standard attack button
        if self.state == "player_turn":
            self.state = "player_timing_attack"
            self.timer = 0.0
            self.cue_time = 0.0
            self.green_active = False

    def start_block_timing(self):#function to start the timing mechanic for the enemy attack, called when the enemy's turn starts
        if self.state == "enemy_turn":
            self.state = "enemy_timing_block"
            self.timer = 0.0
            self.cue_time = 0.0
            self.green_active = False
            self.block_success = False

    def finish_attack_timing(self, missed=False):#function to finish the timing mechanic for the standard attack, called when the player presses space during the timing mechanic or when the timing mechanic times out
        if self.state != "player_timing_attack" or self.current_enemy is None:
            return

        self.state = "resolving"

        if missed:#if missed the damage is way lower, give a message to the player
            damage = 2
            self.feedback_text = f"MISS! {damage} DMG"
        else:
            damage = 10
            self.feedback_text = f"PERFECT! {damage} DMG"

        self.feedback_timer = self.feedback_duration

        self.current_enemy_health -= damage
        print(f"Player deals {damage} damage")

        if self.current_enemy_health <= 0:#end battle if the enemy's health is 0 or less, the battle is won and the end_battle function is called with win=True
            self.end_battle(win=True)
            return

        self.state = "enemy_turn"
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False
        self.action_menu.disable()

    def resolve_enemy_attack(self, blocked=False):#function to resolve the enemy attack, called when the player presses space during the timing mechanic or when the timing mechanic times out
        if self.state != "enemy_timing_block":
            return

        damage = self.current_enemy["attack"]

        if blocked or self.block_success:#damage way lower if blocked, give a message to the player
            damage = max(1, int(damage * 0.3))
            self.feedback_text = f"PERFECT! {damage} DMG TAKEN"
        else:
            self.feedback_text = f"MISS! {damage} DMG TAKEN"

        self.feedback_timer = self.feedback_duration
        self.game.player.set_health(self.game.player.health - damage)
        print("Enemy deals", damage, "damage")

        self.state = "player_turn"
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False
        self.block_success = False

        self.action_menu.reset()
        self.action_menu.enable()

    def end_battle(self, win=False):#function to end the battle, called when the enemy's health is 0 or less or when the player's health is 0 or less, the battle is lost and the end_battle function is called with win=False
        print("Battle closing:", "Win" if win else "Loss")
        old_level = self.game.player.level

        self.game.player.set_coins(self.game.player.coins + self.current_enemy["coin_reward"])
        self.game.player.set_xp(self.game.player.current_xp + self.current_enemy["xp_reward"])

        self.action_menu.disable()
        self.power_menu.disable()

        if self.game.player.level > old_level:
            self.levelup_pending = True
            self.state = "levelup"
            self.levelup_menu.reset()
            self.levelup_menu.enable()
            return

        self.state = "finished"
        self.current_enemy = None
        self.game.battle = False
        self.levelup_menu.disable()
        self.disable()

    def enable(self):#enable the battle screen, so that it can be drawn and interacted with
        self.ui.enable()

    def disable(self):#disable the battle screen, so that it can not be drawn and interacted with
        self.ui.disable()

    def draw_traffic_light(self):#draw the traffic light used for standard attack and blocking
        if self.state not in ("player_timing_attack", "enemy_timing_block"):
            return

        x = self.game.window_width * 0.5
        y = self.game.window_height * 0.18
        radius = 25

        if self.green_active:
            color = arcade.color.GREEN
        else:
            color = arcade.color.RED

        arcade.draw_circle_filled(x, y, radius, color)#easy funciton provided by arcade
        arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK, 3)

    def update_turn_indicator(self):
        if self.state in ("player_turn", "player_timing_attack", "power_spam"):
            self.turn_indicator_visible = True
            self.turn_indicator_sprite.center_x = self.game.window_width * 0.2
            self.turn_indicator_sprite.center_y = self.game.window_height * 0.6

        elif self.state in ("enemy_turn", "enemy_timing_block"):
            self.turn_indicator_visible = True
            self.turn_indicator_sprite.center_x = self.game.window_width * 0.8
            self.turn_indicator_sprite.center_y = self.game.window_height * 0.6

        else:
            self.turn_indicator_visible = False

    #draw function
    def draw(self):
        #draw the traffic light and the UI elements, including the menus and feedback text
        self.update_turn_indicator()
        self.ui.draw()
        self.draw_traffic_light()

        if self.turn_indicator_visible:
            self.turn_indicator_list.draw()

        if self.current_enemy is not None and self.current_enemy_texture is not None and self.state not in ("inactive", "finished"):
            self.enemy_sprite_list.draw()

        #if power_spam is activated, draw an overlay with the power attack name, the number of times space was pressed, and the time left
        if self.state == "power_spam":
            center_x = self.game.window_width // 2
            center_y = self.game.window_height // 2

            power_name = self.power_attack_data[self.power_attack_index]["name"]

            shake_text = arcade.Text(
                "SHAKE!",
                center_x,
                center_y + 80,
                arcade.color.BLACK,
                54,
                anchor_x="center"
            )
            shake_text.draw()

            attack_text = arcade.Text(
                power_name,
                center_x,
                center_y + 25,
                arcade.color.BLACK,
                28,
                anchor_x="center"
            )
            attack_text.draw()

            count_text = arcade.Text(
                f"SPACE: {self.power_spam_count}",
                center_x,
                center_y - 25,
                arcade.color.BLACK,
                28,
                anchor_x="center"
            )
            count_text.draw()

            time_text = arcade.Text(
                f"Time left: {max(0.0, self.power_spam_timer):.1f}",
                center_x,
                center_y - 70,
                arcade.color.BLACK,
                24,
                anchor_x="center"
            )
            time_text.draw()

        #draw the enemy's health bar and the feedback text, if the battle is active and the enemy is not defeated
        if self.current_enemy is not None and self.state not in ("inactive", "finished"):
            hp_text = arcade.Text(
                f"Enemy HP: {max(0, self.current_enemy_health)} / {self.current_enemy['max_hp']}",
                self.game.window_width - 185,
                self.game.window_height - 250,
                arcade.color.BLACK,
                24,
                anchor_x="right",
                anchor_y="center"
            )
            hp_text.draw()

        if self.feedback_text != "":
            feedback = arcade.Text(
                self.feedback_text,
                self.game.window_width // 2,
                self.game.window_height * 0.28,
                arcade.color.BLACK,
                28,
                anchor_x="center"
            )
            feedback.draw()

        if self.items_menu.enabled:
            arcade.draw_lrbt_rectangle_filled(
                0,
                self.game.window_width,
                0,
                self.game.window_height,
                (0, 0, 0, 180)
            )
            self.item_preview_list.draw()
            self.items_menu.draw()

        #draw action menu if the player is in their turn and the power menu is not enabled and there is no levelup pending
        if self.state == "player_turn" and not self.power_menu.enabled and not self.levelup_pending:
            self.action_menu.draw()

        if self.power_menu.enabled:
            arcade.draw_lrbt_rectangle_filled(
                0,
                self.game.window_width,
                0,
                self.game.window_height,
                (0, 0, 0, 180)
            )
            self.power_menu.draw()

        #draw levelup menu if there is a levelup pending
        if self.levelup_pending:
            arcade.draw_lrbt_rectangle_filled(
                0,
                self.game.window_width,
                0,
                self.game.window_height,
                (0, 0, 0, 180)
            )
            self.levelup_menu.draw()

    #get key presses, mainly SPACE for the timing mechanics
    def on_key_press(self, key, key_modifiers):
        if self.state == "power_spam":
            if key == arcade.key.SPACE:
                self.power_spam_count += 1
            return


        if self.levelup_pending:
            self.levelup_menu.on_key_press(key, key_modifiers)
            return

        if self.power_menu.enabled:
            self.power_menu.on_key_press(key, key_modifiers)
            return

        if self.items_menu.enabled:
            self.items_menu.on_key_press(key, key_modifiers)

            if self.items_menu.selected_index == 0:
                self.update_item_preview("sausages")
            elif self.items_menu.selected_index == 1:
                self.update_item_preview("pills")

            return

        if self.state == "player_turn":
            self.action_menu.on_key_press(key, key_modifiers)
            return

        if key == arcade.key.SPACE:
            if self.state == "player_timing_attack":
                if self.green_active:
                    self.finish_attack_timing(missed=False)
                else:
                    print("Too early")
                    self.finish_attack_timing(missed=True)

            elif self.state == "enemy_timing_block":
                if self.green_active:
                    self.block_success = True
                    self.resolve_enemy_attack(blocked=True)
                else:
                    print("Too early")
                    self.resolve_enemy_attack(blocked=False)