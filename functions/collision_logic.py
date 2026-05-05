import arcade
import functions.settings as settings

def coll_check(player, obstacles, adjust_player=False):
    for obstacle in obstacles:
        if(
            #simple overlap logic
            player.right > obstacle.left and
            player.left < obstacle.right and
            player.top > obstacle.bottom and
            player.bottom < obstacle.top
        ):
            if adjust_player: #this moves the player out of the obstacle (exactly onto the nearest edge)
                overlap_list = [ #checks how far you would need to move the player 
                                 #in each direction in order to get him out of the obstacle
                    obstacle.left - player.right,
                    player.left - obstacle.right,
                    obstacle.bottom - player.top,
                    player.bottom - obstacle.top
                ]

                #check which edge is closest
                nearest_edge = max(overlap_list)
                nearest_edge_index = overlap_list.index(nearest_edge)

                #move the player
                if nearest_edge_index == 0:
                    player.right = obstacle.left
                elif nearest_edge_index == 1:
                    player.left = obstacle.right
                elif nearest_edge_index == 2:
                    player.top = obstacle.bottom
                elif nearest_edge_index == 3:
                    player.bottom = obstacle.top
            return True
    return False