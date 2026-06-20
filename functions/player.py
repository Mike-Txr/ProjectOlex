import arcade
import functions.settings as settings
import functions.entity as entity

class Player(entity.Entity):
    def __init__(self, x, y, scale, game=None):
        super().__init__(x, y, scale, "player.png")
        self.center_x = x
        self.center_y = y
        self.dia_icon = "assets/player_dia.png"

        self.game = game
        
        #Main Game Variables
        self.max_health = 10#max_health variable, could be changed throughout the game
        self.health = self.max_health#current health variable, starts with max health

        self.max_power = 50#max_power variable, could be changed throughout the game
        self.power = self.max_power#current power variable, starts with max power

        self.attack = 5#variable for the attack stat, could be changed throughout the game

        self.level = 1#variable for the current level, starts at 1
        self.levelup = 100#variable, level up will be reached at 100
        self.current_xp = 90#current experience points variable, starts with 50

        self.coins = 10#variable for coins, could be changed throughout the game

    #function to set the health of the player, which also updates the health label
    def set_health(self, value: int):
        self.health = max(0, min(self.max_health, value))
        if self.game is not None:
            self.game.health_label.text = f"{self.health} / {self.max_health}"

    def set_power(self, value: int):
        self.power = max(0, min(self.max_power, value))
        if self.game is not None:
            self.game.power_label.text = f"{self.power} / {self.max_power}"

    def set_xp(self, value: int):
        self.current_xp = max(0, value)

        while self.current_xp >= self.levelup:
            self.current_xp -= self.levelup
            self.level += 1
            print("Level up! Aktuelles Level:", self.level)

        if self.game is not None:
            if self.level > 0:
                progress = self.current_xp / self.levelup
            else:
                progress = 0

            progress = max(0, min(1, progress))
            self.game.level_label.text = f"{self.level}"
            bar_width = max(1, self.game.level_panel_width - 100)
            self.game.level_bar_fill.width = max(1, int(bar_width * progress))

    def set_coins(self, value: int):
        self.coins = max(0, value)
        if self.game is not None:
            self.game.coins_label.text = f"{self.coins}"