import arcade
import arcade.gui
from typing import Callable, Optional, Sequence


class BattleMenu:
    def __init__(
        self,
        game,
        button_texts: Sequence[str],
        callbacks: Sequence[Optional[Callable[[], None]]],
        *,
        title_text: str | None = None,
        subtitle_text: str | None = None,
        button_width: int = 300,
        button_spacing: int = 20,
        arrow_path: str = "assets/arrow.png",
        arrow_scale: float = 0.1,
        escape_index: int | None = None,
        allow_space: bool = True,
    ):
        self.game = game
        self.button_width = button_width
        self.button_spacing = button_spacing
        self.title_text = title_text
        self.subtitle_text = subtitle_text
        self.escape_index = escape_index
        self.allow_space = allow_space

        self.enabled = False
        self.selected_index = 0

        # UI
        self.manager = arcade.gui.UIManager()
        self.box = arcade.gui.UIBoxLayout()

        self.buttons: list[arcade.gui.UIFlatButton] = []
        self.callbacks: list[Callable[[], None]] = []

        # Arrow
        self.ui_sprites = arcade.SpriteList()
        self.arrow = arcade.Sprite(arrow_path, scale=arrow_scale)
        self.ui_sprites.append(self.arrow)
        self.arrow.center_x = 0
        self.arrow.center_y = 0

        # Build buttons
        for i, text in enumerate(button_texts):
            button = arcade.gui.UIFlatButton(text=text, width=button_width)
            self.buttons.append(button)

            callback = callbacks[i] if i < len(callbacks) else None
            self.callbacks.append(callback if callback is not None else self._noop)

            @button.event("on_click")
            def _(event, index=i):
                self.selected_index = index
                self.activate_selected()

            self.box.add(button)

            if i < len(button_texts) - 1:
                self.box.add(arcade.gui.UISpace(height=button_spacing))

        self.anchor = arcade.gui.UIAnchorLayout()
        self.anchor.add(anchor_x="center_x", anchor_y="center_y", child=self.box)
        self.manager.add(self.anchor)

        self.title_draw = None
        self.subtitle_draw = None

    def _noop(self):
        pass

    def enable(self):
        self.enabled = True
        self.manager.enable()

    def disable(self):
        self.enabled = False
        self.manager.disable()

    def reset(self):
        self.selected_index = 0

    def set_selected(self, index: int):
        if not self.buttons:
            self.selected_index = 0
            return
        self.selected_index = index % len(self.buttons)

    def activate_selected(self):
        if not self.buttons:
            return
        self.callbacks[self.selected_index]()

    def on_key_press(self, key, modifiers=None):
        if not self.enabled:
            return False

        if key in (arcade.key.W, arcade.key.UP):
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
            return True

        if key in (arcade.key.S, arcade.key.DOWN):
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
            return True

        if key in (arcade.key.ENTER, arcade.key.RETURN):
            self.activate_selected()
            return True

        if self.allow_space and key == arcade.key.SPACE:
            self.activate_selected()
            return True

        if key == arcade.key.ESCAPE and self.escape_index is not None:
            self.set_selected(self.escape_index)
            self.activate_selected()
            return True

        return False

    def _update_arrow_position(self):
        if not self.buttons:
            return

        button = self.buttons[self.selected_index]
        self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
        self.arrow.center_y = button.center_y

    def draw(self):
        if not self.enabled:
            return

        self._update_arrow_position()

        if self.title_text:
            self.title_draw = arcade.Text(
                self.title_text,
                self.game.window_width // 2,
                self.game.window_height // 2 + 200,
                arcade.color.WHITE,
                50,
                anchor_x="center",
            )
            self.title_draw.draw()

        if self.subtitle_text:
            self.subtitle_draw = arcade.Text(
                self.subtitle_text,
                self.game.window_width // 2,
                self.game.window_height // 2 + 150,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
            self.subtitle_draw.draw()

        self.ui_sprites.draw()
        self.manager.draw()