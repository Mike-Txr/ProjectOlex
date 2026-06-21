import unittest

from functions import player_movement, screen_logic, key_handler


# small helper class with the minimal player attributes for screen logic testing
class DummyPlayer:
    def __init__(self, center_x=0, center_y=0, width=10, height=10):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height


# small helper class to simulate a trigger collision object
class DummyCollision:
    def __init__(self, side):
        self.properties = {"side": side}


class PlayerMovementTests(unittest.TestCase):
    # reset pressed keys after each test so state does not leak
    def tearDown(self):
        key_handler.current_pressed.clear()

    def test_calc_movement_no_keys(self):
        # no key pressed should return zero movement
        result = player_movement.calc_movement()
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 0)

    def test_calc_movement_w_and_d(self):
        # W and D pressed should move up-right
        key_handler.current_pressed.append(player_movement.arcade.key.W)
        key_handler.current_pressed.append(player_movement.arcade.key.D)
        result = player_movement.calc_movement()
        self.assertEqual(result["x"], 1)
        self.assertEqual(result["y"], 1)


class ScreenLogicTests(unittest.TestCase):
    # tests for the screen transition correction logic
    def test_correct_player_pos_top(self):
        player = DummyPlayer(center_x=50, center_y=50, width=10, height=10)
        collision = DummyCollision("top")
        screen_logic.correct_player_pos(player, collision, scale=2)
        self.assertEqual(player.center_y, 0 + 0.2 * player.height)

    def test_counter_correct_player_pos_right(self):
        player = DummyPlayer(center_x=20, center_y=20, width=10, height=10)
        collision = DummyCollision("right")
        # if screen change is cancelled, the player should be moved back by the scale amount
        screen_logic.counter_correct_player_pos(player, collision, scale=2, orig_coords=[20, 20])
        self.assertEqual(player.center_x, 18)  # original x 20 minus scale 2
        self.assertEqual(player.center_y, 20)


if __name__ == "__main__":
    unittest.main()


