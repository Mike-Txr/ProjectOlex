import arcade

def on_draw(self):
    self.clear()

    self.scene.draw(pixelated=True)
    
    self.position_continue = self.window_height / 2
    self.position_restart = self.window_height / 2 - 50
    self.position_quit = self.window_height / 2 - 100

    if self.paused:
        # dunkles Overlay
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=320*self.width,
            bottom=0,
            top=180*self.height,
            color=arcade.color.ORANGE[:3] + (200,))

        arcade.draw_text(
            "PAUSED",
            self.window_width / 2,
            self.window_height / 2 + 150,
            arcade.color.WHITE,
            font_size = 60,
            anchor_x="center"
        )

        arcade.draw_text(
            "Continue",
            self.window_width / 2,
            self.position_continue,
            arcade.color.WHITE,
            font_size = 30,
            anchor_x="center"
        )

        arcade.draw_text(
            "Restart",
            self.window_width / 2,
            self.position_restart,
            arcade.color.WHITE,
            font_size = 30,
            anchor_x="center"
        )

        arcade.draw_text(
            "Quit",
            self.window_width / 2,
            self.position_quit,
            arcade.color.WHITE,
            font_size = 30,
            anchor_x="center"
        )