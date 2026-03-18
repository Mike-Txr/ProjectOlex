import arcade

def on_draw(self):
    self.clear()

    self.all_sprites.draw(pixelated=True)

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
            self.window_height / 2,
            arcade.color.WHITE,
            font_size = 50,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ESC to continue",
            self.window_width / 2,
            self.window_height / 2 - 60,
            arcade.color.WHITE,
            font_size = 20,
            anchor_x="center"
        )