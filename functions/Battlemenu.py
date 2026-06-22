#Battlemenu acts as a helper class for Battleview.py, it handles the menus that appear during battles to choose action
import arcade
import arcade.gui
from typing import Callable, Optional, Sequence
#Waht is Sequence? It is a type hint that represents a sequence of items, such as a list or a tuple. In this case, it is used to indicate that button_texts and callbacks should be sequences of strings and callables.


class BattleMenu:
    def __init__(
        self,
        game,#reference to the main game class
        button_texts: Sequence[str],#text displayed on the buttons, should be in the same order as the callbacks
        callbacks: Sequence[Optional[Callable[[], None]]],#functions that are called when the corresponding button is pressed, should be in the same order as the button_texts, if a callback is None, it will be replaced with a no-op function
        *,#seperates required and optional parameters
        title_text: str | None = None,#text displayed above the buttons, can be None if no text should be displayed
        subtitle_text: str | None = None,#text displayed above the buttons, can be None if no text should be displayed
        button_width: int = 300,#width of the buttons in pixels
        button_spacing: int = 20,#space between buttons in pixels
        arrow_path: str = "assets/arrow_black.png",#path to the arrow image that points to the selected button
        arrow_scale: float = 0.1,#scale of the arrow that points to the selected button
        escape_index: int | None = None,#index of the button that should be activated when ESC is pressed, just used for going back in a submenu
        allow_space: bool = True,#when SPACE is allowed to select something (just for power because it is easier to spam after that)
    ):
        #add to self for access
        self.game = game
        self.button_width = button_width
        self.button_spacing = button_spacing
        self.title_text = title_text
        self.subtitle_text = subtitle_text
        self.escape_index = escape_index
        self.allow_space = allow_space
        self.enabled = False
        self.selected_index = 0

        #UI Manager and BoxLayout
        self.manager = arcade.gui.UIManager()
        self.box = arcade.gui.UIBoxLayout()
        self.buttons: list[arcade.gui.UIFlatButton] = []
        self.callbacks: list[Callable[[], None]] = []

        #Arrow to sprite, exactly the same as all the other arrows
        self.ui_sprites = arcade.SpriteList()
        self.arrow = arcade.Sprite(arrow_path, scale=arrow_scale)
        self.ui_sprites.append(self.arrow)
        self.arrow.center_x = 0
        self.arrow.center_y = 0

        #Build all the buttons
        for i, text in enumerate(button_texts):
            button = arcade.gui.UIFlatButton(text=text, width=button_width)
            self.buttons.append(button)

            callback = callbacks[i] if i < len(callbacks) else None#callback is the function that is called when the button is pressed, if there is no callback for this button, it will be None
            self.callbacks.append(callback if callback is not None else self._noop)#set the callback to the no-op function if it is None

            @button.event("on_click")#set the indexes to the buttons, so that when a button is pressed, the corresponding callback is called
            def _(event, index=i):
                self.selected_index = index
                self.activate_selected()

            self.box.add(button)

            if i < len(button_texts) - 1:#add spacing between buttons, but not after the last button
                self.box.add(arcade.gui.UISpace(height=button_spacing))

        self.anchor = arcade.gui.UIAnchorLayout()
        self.anchor.add(anchor_x="center_x", anchor_y="center_y", child=self.box)
        self.manager.add(self.anchor)#add to manager to draw it later

        self.title_draw = None
        self.subtitle_draw = None

    def _noop(self):
        pass

    def enable(self):#enable the menu, so that it can be drawn and interacted with
        self.enabled = True
        self.manager.enable()

    def disable(self):#disable the menu, so that it can not be drawn and interacted with
        self.enabled = False
        self.manager.disable()

    def reset(self):#reset the menu to its initial state
        self.selected_index = 0

    def set_selected(self, index: int):#set the selected button to the given index, if the index is out of bounds, it will be wrapped around to the other side
        if not self.buttons:
            self.selected_index = 0
            return
        self.selected_index = index % len(self.buttons)

    def activate_selected(self):#activate the callback of the selected button
        if not self.buttons:
            return
        self.callbacks[self.selected_index]()

    def on_key_press(self, key, modifiers=None):
        if not self.enabled:
            return False

        #navigate through the buttons
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

    def _update_arrow_position(self):#arrow position is updated to the selected button
        if not self.buttons:
            return

        button = self.buttons[self.selected_index]
        self.arrow.center_x = button.center_x - (button.width / 2) - (self.arrow.width / 2) - 20
        self.arrow.center_y = button.center_y

    #draw everything, including the arrow and the buttons, as well as the title and subtitle if they are set
    def draw(self):
        if not self.enabled:
            return

        self._update_arrow_position()

        if self.title_text:#text is drawn above the buttons, if even needed
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