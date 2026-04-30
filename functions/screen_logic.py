import arcade
import functions.settings as settings

def check_collisions(player, edge_list): #function to check collision with trigger objects
    for object in edge_list:
        #calculate the object's edges
        points = object.shape

        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        left = min(xs)
        right = max(xs)
        bottom = min(ys)
        top = max(ys)

        if ( #if the player is far enough into the edge of the screen (40% of the player is outside)
            player.right-0.4*player.width > left and
            player.left+0.4*player.width < right and
            player.top-0.4*player.height > bottom and
            player.bottom+0.4*player.height < top
        ):
            return object
    return False

def correct_player_pos(player, collision, scale):
    #move the player to the other side of the screen (with 70% of the player being inside the screen)

    if collision.properties["side"] == "top":
        player.center_y = 0 + 0.2*player.height
    elif collision.properties["side"] == "bottom":
        player.center_y = 216*scale - 0.2*player.height
    elif collision.properties["side"] == "right":
        player.center_x = 0 + 0.2*player.width
    elif collision.properties["side"] == "left":
        player.center_x = 384*scale - 0.2*player.width
    return player

def counter_correct_player_pos(player, collision, scale, orig_coords):
    player.center_x = orig_coords[0]
    player.center_y = orig_coords[1]
    if collision.properties["side"] == "top":
        player.center_y -= scale
    elif collision.properties["side"] == "bottom":
        player.center_y += scale
    elif collision.properties["side"] == "right":
        player.center_x -= scale
    elif collision.properties["side"] == "left":
        player.center_x += scale
    return player