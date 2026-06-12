import arcade
import arcade.gui

class BattleScreen:
    def __init__(self, game):
        self.game = game#variable game, to access the main game class and its attributes like health, window_width, etc.
        self.ui = arcade.gui.UIManager()
        self.root = arcade.gui.UIAnchorLayout()
        self.ui.add(self.root)
        
        self.current_enemy = None#variable to store the current enemy, which will be set when start_battle is called

        #debug text, not relevant
        self.title_label = arcade.gui.UILabel(text="Battle!", font_size=40, text_color=arcade.color.WHITE)
        self.root.add(self.title_label, anchor_x="center", anchor_y="center")

        #important variables for the battle logic
        self.state = "inactive" #variable to track the state of the battle screen, can be "inactive", "active", or "victory"
        self.timer = 0.0
        self.turn_delay = 1.5 #delay between turns in seconds

        #variables for the timing mechanic
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

        #########level up menu#########
        self.levelup_manager = arcade.gui.UIManager()

        self.levelup_box = arcade.gui.UIBoxLayout()

        self.hp_button = arcade.gui.UIFlatButton(text="Increase Max HP", width=300)
        self.power_button = arcade.gui.UIFlatButton(text="Increase Max Power", width=300)
        self.attack_button = arcade.gui.UIFlatButton(text="Increase Attack", width=300)

        self.levelup_buttons = [
            self.hp_button,
            self.power_button,
            self.attack_button
        ]

        self.levelup_selected = 0
        self.ui_sprites = arcade.SpriteList()
        self.arrow = arcade.Sprite("assets/arrow.png", scale=0.1)
        self.ui_sprites.append(self.arrow)
        self.arrow.center_x = 0
        self.arrow.center_y = 0

        @self.hp_button.event("on_click")
        def _(event):
            self.levelup_selected = 0
            self.activate_levelup_choice()

        @self.power_button.event("on_click")
        def _(event):
            self.levelup_selected = 1
            self.activate_levelup_choice()

        @self.attack_button.event("on_click")
        def _(event):
            self.levelup_selected = 2
            self.activate_levelup_choice()

        self.levelup_box.add(self.hp_button)
        self.levelup_box.add(arcade.gui.UISpace(height=20))

        self.levelup_box.add(self.power_button)
        self.levelup_box.add(arcade.gui.UISpace(height=20))

        self.levelup_box.add(self.attack_button)

        self.levelup_anchor = arcade.gui.UIAnchorLayout()
        self.levelup_anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.levelup_box
        )

        self.levelup_manager.add(self.levelup_anchor)

        self.text_level = arcade.Text("LEVEL UP!", self.game.window_width // 2, self.game.window_height // 2 + 200, arcade.color.WHITE, 50, anchor_x="center")
        self.text_chooser = arcade.Text("Choose a stat to increase:", self.game.window_width // 2, self.game.window_height // 2 + 150, arcade.color.WHITE, 30, anchor_x="center")

        #########battle action menu#########
        # battle action menu
        self.action_manager = arcade.gui.UIManager()
        self.action_box = arcade.gui.UIBoxLayout()

        self.standard_attack_button = arcade.gui.UIFlatButton(text="Standard-Attack", width=300)
        self.power_attack_button = arcade.gui.UIFlatButton(text="Power-Attacks", width=300)
        self.items_button = arcade.gui.UIFlatButton(text="Items", width=300)

        self.action_buttons = [
            self.standard_attack_button,
            self.power_attack_button,
            self.items_button
        ]

        self.action_selected = 0

        @self.standard_attack_button.event("on_click")
        def _(event):
            self.action_selected = 0
            self.start_standard_attack()

        @self.power_attack_button.event("on_click")
        def _(event):
            self.action_selected = 1
            self.open_power_menu()

        @self.items_button.event("on_click")
        def _(event):
            self.action_selected = 2
            self.open_items_menu()

        self.action_box.add(self.standard_attack_button)
        self.action_box.add(arcade.gui.UISpace(height=20))
        self.action_box.add(self.power_attack_button)
        self.action_box.add(arcade.gui.UISpace(height=20))
        self.action_box.add(self.items_button)

        self.action_anchor = arcade.gui.UIAnchorLayout()
        self.action_anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.action_box
        )

        self.action_manager.add(self.action_anchor)

        ########power attack submenu########
        # power attack submenu
        self.power_menu_open = False

        self.power_manager = arcade.gui.UIManager()
        self.power_box = arcade.gui.UIBoxLayout()

        self.power_attack_1_button = arcade.gui.UIFlatButton(text="Power Attack 1", width=300)
        self.power_attack_2_button = arcade.gui.UIFlatButton(text="Power Attack 2", width=300)
        self.power_attack_3_button = arcade.gui.UIFlatButton(text="Power Attack 3", width=300)
        self.power_back_button = arcade.gui.UIFlatButton(text="Back", width=300)

        self.power_buttons = [
            self.power_attack_1_button,
            self.power_attack_2_button,
            self.power_attack_3_button,
            self.power_back_button
        ]

        self.power_selected = 0

        @self.power_attack_1_button.event("on_click")
        def _(event):
            self.power_selected = 0
            self.choose_power_attack(0)

        @self.power_attack_2_button.event("on_click")
        def _(event):
            self.power_selected = 1
            self.choose_power_attack(1)

        @self.power_attack_3_button.event("on_click")
        def _(event):
            self.power_selected = 2
            self.choose_power_attack(2)

        @self.power_back_button.event("on_click")
        def _(event):
            self.power_selected = 3
            self.close_power_menu()

        self.power_box.add(self.power_attack_1_button)
        self.power_box.add(arcade.gui.UISpace(height=20))
        self.power_box.add(self.power_attack_2_button)
        self.power_box.add(arcade.gui.UISpace(height=20))
        self.power_box.add(self.power_attack_3_button)
        self.power_box.add(arcade.gui.UISpace(height=20))
        self.power_box.add(self.power_back_button)

        self.power_anchor = arcade.gui.UIAnchorLayout()
        self.power_anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.power_box
        )

        self.power_manager.add(self.power_anchor)
        self.power_manager.disable()

    def start_battle(self, enemy):
        self.current_enemy = enemy
        self.current_enemy_health = self.current_enemy["max_hp"]
        self.title_label.text = "Battle!"
        self.state = "player_turn"
        self.timer = 0.0
        self.cue_time = 0.0
        self.feedback_text = ""
        self.feedback_timer = 0.0
        self.green_active = False
        self.block_success = False
        self.action_selected = 0
        self.action_manager.enable()
        self.power_menu_open = False
        self.power_manager.disable()
        self.action_manager.enable()
        self.action_selected = 0
        self.power_selected = 0
        # später kannst du hier enemy.hp, enemy.texture usw. übernehmen

    def start_standard_attack(self):
        if self.state != "player_turn":
            return

        self.action_manager.disable()
        self.player_attack_pressed()

    def open_power_menu(self):
        if self.state != "player_turn":
            return

        self.power_menu_open = True
        self.power_selected = 0

        self.action_manager.disable()
        self.power_manager.enable()

    def close_power_menu(self):
        self.power_menu_open = False

        self.power_manager.disable()
        self.action_manager.enable()

    def choose_power_attack(self, index):
        if self.state != "player_turn" or not self.power_menu_open:
            return

        # Platzhalter: noch keine echte Power-Attack-Funktion
        print(f"Power Attack {index + 1} gewählt")

        # fürs Erste einfach wieder ins Hauptmenü zurück
        self.close_power_menu()

    def open_items_menu(self):
        if self.state != "player_turn":
            return

        print("Items submenu kommt als nächstes")

    def update(self, delta_time):
        if self.state in ("inactive", "finished"):
            return
        
        if self.feedback_timer > 0:
            self.feedback_timer -= delta_time
            if self.feedback_timer <= 0:
                self.feedback_text = ""

        self.timer = self.timer + delta_time

        if self.state == "player_timing_attack":
            self.cue_time = self.cue_time + delta_time

            if self.cue_time >= self.red_time:
                self.green_active = True

                if self.cue_time >= self.red_time + self.green_time:
                    self.finish_attack_timing(missed=True)

        elif self.state == "enemy_turn":
            if self.timer >= self.turn_delay:
                self.start_block_timing()

        elif self.state == "enemy_timing_block":
            self.cue_time += delta_time

            if self.cue_time >= self.current_enemy["red_time"]:
                self.green_active = True

            if self.cue_time >= self.current_enemy["red_time"] + self.green_time:
                self.resolve_enemy_attack(blocked=False)

    def player_attack_pressed(self):
        if self.state == "player_turn":
            self.state = "player_timing_attack"
            self.timer = 0.0
            self.cue_time = 0.0
            self.green_active = False

    def start_block_timing(self):
        if self.state == "enemy_turn":
            self.state = "enemy_timing_block"
            self.timer = 0.0
            self.cue_time = 0.0
            self.green_active = False
            self.block_success = False

    def finish_attack_timing(self, missed=False):
        if self.state != "player_timing_attack" or self.current_enemy is None:
            return
        
        self.state = "resolving"

        if missed:
            damage = 2
            self.feedback_text = "MISS!"
        else:
            damage = 10
            self.feedback_text = "PERFECT!"

        self.feedback_timer = self.feedback_duration

        self.current_enemy_health -= damage
        print(f"Spieler macht {damage} Schaden")

        if self.current_enemy_health <= 0:
            self.end_battle(win=True)
            return

        self.state = "enemy_turn"
        self.action_manager.disable()
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False

    def resolve_enemy_attack(self, blocked=False):
        if self.state != "enemy_timing_block":
            return

        damage = self.current_enemy["attack"]

        if blocked or self.block_success:
            damage = max(1, int(damage * 0.3))
            self.feedback_text = "PERFECT!"

        else:
            self.feedback_text = "MISS!"

        self.feedback_timer = self.feedback_duration
        self.game.set_health(self.game.health - damage)
        print("Gegner macht", damage, "Schaden")

        self.state = "player_turn"
        self.action_manager.enable()
        self.timer = 0.0
        self.cue_time = 0.0
        self.green_active = False
        self.block_success = False

    def activate_levelup_choice(self):

        if self.levelup_selected == 0:
            self.game.max_health += 5
            self.game.set_health(self.game.max_health)

            print("Max HP erhöht")

        elif self.levelup_selected == 1:
            self.game.max_power += 10
            self.game.set_power(self.game.max_power)

            print("Max Power erhöht")

        elif self.levelup_selected == 2:
            self.game.attack += 2

            print("Attack erhöht")

        self.levelup_pending = False

        self.state = "inactive"
        self.current_enemy = None
        self.game.battle = False

        self.levelup_manager.disable()
        self.disable()

    def end_battle(self, win=False):
        print("Battle beendet:", "Sieg" if win else "Niederlage")
        old_level = self.game.level

        self.game.set_coins(self.game.coins + self.current_enemy["coin_reward"])
        self.game.set_xp(self.game.current_xp + self.current_enemy["xp_reward"])

        if self.game.level > old_level:
            self.levelup_pending = True
            self.levelup_selected = 0
            self.levelup_manager.enable()
            self.state = "levelup"
            return
        
        self.state = "inactive"
        self.state = "finished"
        self.current_enemy = None
        self.game.battle = False
        self.disable()

    def enable(self):
        self.ui.enable()

    def disable(self):
        self.ui.disable()

    def draw_traffic_light(self):
        if self.state not in ("player_timing_attack", "enemy_timing_block"):
            return

        x = self.game.window_width * 0.5
        y = self.game.window_height * 0.18
        radius = 25

        if self.green_active:
            color = arcade.color.GREEN
        else:
            color = arcade.color.RED

        arcade.draw_circle_filled(x, y, radius, color)
        arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK, 3)


    def draw(self):
        arcade.draw_lrbt_rectangle_filled(
            0,
            self.game.window_width,
            0,
            self.game.window_height,
            arcade.color.WHITE
        )

        self.draw_traffic_light()
        self.ui.draw()

        if self.state == "player_turn" and not self.power_menu_open:
            for i, button in enumerate(self.action_buttons):
                if i == self.action_selected:
                    self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
                    self.arrow.center_y = button.center_y

            self.ui_sprites.draw()
            self.action_manager.draw()

        if self.power_menu_open:
            arcade.draw_lrbt_rectangle_filled(
                0,
                self.game.window_width,
                0,
                self.game.window_height,
                (0, 0, 0, 180)
            )

            self.arrow.visible = True

            for i, button in enumerate(self.power_buttons):
                if i == self.power_selected:
                    self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
                    self.arrow.center_y = button.center_y

            self.ui_sprites.draw()
            self.power_manager.draw()

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

        if self.current_enemy is not None and self.state not in ("inactive", "finished"):
            hp_text = arcade.Text(
                f"Enemy HP: {max(0, self.current_enemy_health)} / {self.current_enemy['max_hp']}",
                self.game.window_width // 2,
                self.game.window_height - 80,
                arcade.color.BLACK,
                24,
                anchor_x="center"
            )
            hp_text.draw()

        if self.levelup_pending:

            arcade.draw_lrbt_rectangle_filled(
                0,
                self.game.window_width,
                0,
                self.game.window_height,
                (0, 0, 0, 180)
            )

            # Pfeil neben dem aktuell ausgewählten Button
            for i, button in enumerate(self.levelup_buttons):
                if i == self.levelup_selected:
                    self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
                    self.arrow.center_y = button.center_y

            self.ui_sprites.draw()
            self.text_level.draw()
            self.text_chooser.draw()
            self.levelup_manager.draw()

    def on_key_press(self, key, key_modifiers):
        if self.levelup_pending:
            if key == arcade.key.W or key == arcade.key.UP:
                self.levelup_selected = (self.levelup_selected - 1) % len(self.levelup_buttons)

            elif key == arcade.key.S or key == arcade.key.DOWN:
                self.levelup_selected = (self.levelup_selected + 1) % len(self.levelup_buttons)

            elif key == arcade.key.ENTER or key == arcade.key.RETURN:
                self.activate_levelup_choice()

            return

        if self.power_menu_open:
            if key == arcade.key.W or key == arcade.key.UP:
                self.power_selected = (self.power_selected - 1) % len(self.power_buttons)

            elif key == arcade.key.S or key == arcade.key.DOWN:
                self.power_selected = (self.power_selected + 1) % len(self.power_buttons)

            elif key == arcade.key.ENTER or key == arcade.key.RETURN or key == arcade.key.SPACE:
                if self.power_selected == 3:
                    self.close_power_menu()
                else:
                    self.choose_power_attack(self.power_selected)

            elif key == arcade.key.ESCAPE:
                self.close_power_menu()

            return

        if self.state == "player_turn":
            if key == arcade.key.W or key == arcade.key.UP:
                self.action_selected = (self.action_selected - 1) % len(self.action_buttons)

            elif key == arcade.key.S or key == arcade.key.DOWN:
                self.action_selected = (self.action_selected + 1) % len(self.action_buttons)

            elif key == arcade.key.ENTER or key == arcade.key.RETURN or key == arcade.key.SPACE:
                if self.action_selected == 0:
                    self.start_standard_attack()
                elif self.action_selected == 1:
                    self.open_power_menu()
                elif self.action_selected == 2:
                    self.open_items_menu()

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