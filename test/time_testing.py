import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entities.pacman import Pacman
from entities.blueGhost import BlueGhost
from entities.orangeGhost import OrangeGhost 
from entities.pinkGhost import PinkGhost
from entities.redGhost import RedGhost

pacman=Pacman()
blue_ghost = BlueGhost(pacman_pos=(pacman.x,pacman.y))
def test_ghost_pathfinding(ghost, target_x, target_y):
    # ⏱ Time measurement
    start_time = time.time()
    ghost.find_path_to_pacman(target_x, target_y)
    end_time = time.time()
    search_time = end_time - start_time
    print(f"{ghost.__class__.__name__} | Search Time: {search_time:.8f}s")
pacman=Pacman()
blue_ghost = BlueGhost(pacman_pos=(pacman.x,pacman.y))
test_ghost_pathfinding(blue_ghost,pacman.x,pacman.y)
