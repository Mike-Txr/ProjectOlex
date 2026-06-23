import unittest

from functions import player_movement, screen_logic, key_handler


#small helper class with the minimal player attributes for screen logic testing
class DummyPlayer:
    def __init__(self, center_x=0, center_y=0, width=10, height=10):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height


#small helper class to simulate a trigger collision object
class DummyCollision:
    def __init__(self, side):
        self.properties = {"side": side}


class PlayerMovementTests(unittest.TestCase):
    
    def tearDown(self): #reset pressed keys after each test so state does not leak
        key_handler.current_pressed.clear()

    def test_calc_movement_no_keys(self):
        #no key pressed
        result = player_movement.calc_movement()

        #should return no movement
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 0)

    def test_calc_movement_w(self):
        #W pressed
        key_handler.current_pressed.append(player_movement.arcade.key.W)
        result = player_movement.calc_movement()

        #should return moving up at a speed of one pixel per second
        self.assertEqual(result["x"], 0)
        self.assertEqual(result["y"], 1)

    def test_calc_movement_w_and_d(self):
        #W and D pressed
        key_handler.current_pressed.append(player_movement.arcade.key.W)
        key_handler.current_pressed.append(player_movement.arcade.key.D)
        result = player_movement.calc_movement()

        #should return moving up-right at a speed of one pixel per second (~0.71 each)
        self.assertEqual(result["x"], 0.71)
        self.assertEqual(result["y"], 0.71)



class ScreenLogicTests(unittest.TestCase):
    #tests for the screen transition correction logic

    def test_correct_player_pos_top(self):
        #the player collides with a "top" collision object
        #these are at the top of the map, meaning, the player is supposed to be pushed down to the bottom of the map
        player = DummyPlayer(center_x=50, center_y=50, width=10, height=10) #player entity dummy
        collision = DummyCollision("top") #collision object dummy
        screen_logic.correct_player_pos(player, collision, scale=2)

        #should return the new y being the one defined in screen_logic (that being 0.3 * player.height away from the ground which is at y=0)
        #and x should stay the way it was
        self.assertEqual(player.center_y, 0 + 0.3 * player.height)
        self.assertEqual(player.center_x, 50)

    def test_counter_correct_player_pos_right(self):

        #in this scenario, the player collided with a trigger object on the right side of the screen
        #this triggered a scene change, teleporting the player to the left
        #after this scene change though, it was detected that the player was inside an obstacle
        #this means, the player isn't actually allowed to change scenes, and needs to be moved back to the right side of the screen
        #altough, so the player doesn't immediately trigger the scene change again, he is moved back by one in-game pixel (1 * scale)
        player = DummyPlayer(center_x=20, center_y=20, width=10, height=10)
        collision = DummyCollision("right")
        screen_logic.counter_correct_player_pos(player, collision, scale=2, orig_coords=[20, 20])

        #this should return the player being back where he was before, at 20 20, except 1 ingame-pixel to the left (so 18 20)
        self.assertEqual(player.center_x, 20 - 1 * 2)  # original x 20 minus scale 2
        self.assertEqual(player.center_y, 20)


if __name__ == "__main__":
    unittest.main()


