#function for the whole UI, which is called in the main
import arcade
import arcade.gui

#function for the UI setup
def setup_hud(self):

    self.hud_ui = arcade.gui.UIManager()#create a UI Manager, which is used to handle the events for the buttons and other UI elements
    self.hud_ui.enable()#UI Manager enabled
    self.hud_root = arcade.gui.UIAnchorLayout()#root of all UI elements
    self.hud_ui.add(self.hud_root)#always needs to be added to the UI Manager

    #parameters for the HUD panels
    panel_heights = 50
    transparency = 150

    #colors for:       Health                               Power                           Level                           Coins
    panel_colors = [(241, 130, 136, transparency), (242, 171, 81, transparency), (98, 181, 231, transparency), (81, 198, 94, transparency)]
    panel_weights = [1, 1, 2, 1]#weights for the panels, the level panel is bigger than the others, because it contains more information, can be easily modified
    total_weight = sum(panel_weights)#weight are then used to calculate the width of the panels, so that they are proportional to each other

    current_x = 0#variable to keep track of the current x position for adding the panels
    self.level_panel = None#variable to store the level panel, which is needed to update the level progress bar

    #create panels for health, power, level and coins, the width is calculated based on the weights, so that the level panel is bigger than the others
    #goes through here 4 times, once for each panel 
    for i, (color, weight) in enumerate(zip(panel_colors, panel_weights)): 
        panel_width = self.window_width * (weight / total_weight) 
        panel = arcade.gui.UISpace(width=panel_width, height=panel_heights, color=color) 
        self.hud_root.add(panel, anchor_x="left", anchor_y="top", align_x=current_x, align_y=0)

        if i == 0:#Health-Panel
            self.health_panel_x = current_x
            self.health_panel_width = panel_width

        if i == 1:#Power-Panel
            self.power_panel_x = current_x
            self.power_panel_width = panel_width

        if i == 2:#Level-Panel
            self.level_panel_x = current_x
            self.level_panel_width = panel_width

        if i == 3:#Coins-Panel
            self.coins_panel_x = current_x
            self.coins_panel_width = panel_width

        current_x += panel_width

    #create each panel content (heart and health for health, wonster and power for power, level number and progress bar for level, daddycoin and coin number for coins), which are added to the corresponding panels
    #they get updated in the player class, when the player takes damage, uses power, gains XP or coins

    #create the content of the heart panel
    self.heart_row = arcade.gui.UIBoxLayout(vertical=False)#horizontal box layout 
    self.hud_root.add(self.heart_row, anchor_x="left", anchor_y="top", align_x=self.health_panel_x + self.health_panel_width * 0.08, align_y=-5,)#add the heart row to the health panel, with some padding from the left and top (8% of the panel width and 5 pixels)
    self.heart_row.add(arcade.gui.UIImage(texture=arcade.load_texture("assets/heart_symbol.png"), width=35, height=35))#add a heart image to the heart row, which is loaded from the assets folder and scaled to fit in the panel

    self.health_label = arcade.gui.UILabel(text=f" {self.player.health} / {self.player.max_health}", font_size=25, text_color=arcade.color.WHITE,)#create a label for the health, which shows the current health and max health of the player
    self.heart_row.add(self.health_label)

    #create the content of the power panel (same idea as the health panel)
    self.power_row = arcade.gui.UIBoxLayout(vertical=False)
    self.hud_root.add(self.power_row, anchor_x="left", anchor_y="top", align_x=self.power_panel_x + self.power_panel_width * 0.08, align_y=-5)
    self.power_row.add(arcade.gui.UIImage(texture=arcade.load_texture("assets/wonster.png"), width=25, height=35))

    self.power_label = arcade.gui.UILabel(text=f" {self.player.power} / {self.player.max_power}", font_size=25, text_color=arcade.color.WHITE,)
    self.power_row.add(self.power_label)


    #create the content of the level panel (bit more complicated, because it contains a level progress bar)
    self.level_row = arcade.gui.UIBoxLayout(vertical=False)
    self.hud_root.add(self.level_row, anchor_x="left", anchor_y="top", align_x=self.level_panel_x + 10, align_y=-8)
    self.level_row.add(arcade.gui.UIImage(texture=arcade.load_texture("assets/cugarglaze.png"), width=35, height=35))

    #create the level progress bar, which is a simple rectangle that is filled based on the current XP of the player, the width of the filled part is calculated by current XP / level up XP * width of the progress bar, which is then added to the level panel
    self.level_bar_bg = arcade.gui.UISpace(width=self.level_panel_width - 100, height=20, color=(24, 117, 168, transparency))#bit darker than the level panel
    self.level_bar_fill = arcade.gui.UISpace(width=0, height=20, color=(251, 245, 219, transparency))
    self.hud_root.add(self.level_bar_bg, anchor_x="left", anchor_y="top", align_x=self.level_panel_x + 50, align_y=-15)
    self.hud_root.add(self.level_bar_fill, anchor_x="left", anchor_y="top", align_x=self.level_panel_x + 50, align_y=-15)
    self.level_label = arcade.gui.UILabel(text=f"{self.player.level}", font_size=25, text_color=arcade.color.WHITE,)
    self.hud_root.add(self.level_label, anchor_x="left", anchor_y="top", align_x=self.level_panel_x + self.level_panel_width - 40, align_y=-5)


    #create the content of the coins panel (same idea as the health and power panel)
    self.coin_row = arcade.gui.UIBoxLayout(vertical=False)
    self.hud_root.add(self.coin_row, anchor_x="left", anchor_y="top", align_x=self.coins_panel_x + self.coins_panel_width * 0.08, align_y=-5)
    self.coin_row.add(arcade.gui.UIImage(texture=arcade.load_texture("assets/daddycoin.png"), width=35, height=35))

    self.coins_label = arcade.gui.UILabel(text=f" {self.player.coins}", font_size=25, text_color=arcade.color.WHITE,)
    self.coin_row.add(self.coins_label)