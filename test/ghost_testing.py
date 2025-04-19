import matplotlib.pyplot as plt
import numpy as np
import tracemalloc
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entities.pacman import Pacman
from entities.blueGhost import BlueGhost
from entities.orangeGhost import OrangeGhost 
from entities.pinkGhost import PinkGhost
from entities.redGhost import RedGhost
blueTime, redTime, orangeTime, pinkTime= [], [], [], []
blueMemory, redMemory, orangeMemory, pinkMemory = [], [], [], []
blueNodes, pinkNodes,orangeNodes,redNodes = [], [], [], []
blueLocation, redLocation, orangeLocation, pinkLocation = [], [], [], []
def measureTimeEachGhost(ghost, target_x, target_y):
    start_time = time.perf_counter()
    ghost.find_path_to_pacman(target_x, target_y)
    end_time = time.perf_counter()
    search_time = end_time - start_time
    print(f"{ghost.__class__.__name__} | Search Time: {search_time:.20f}s")
    if ghost.__class__.__name__ == "BlueGhost":
        blueTime.append(search_time)
    elif ghost.__class__.__name__ == "PinkGhost":
        pinkTime.append(search_time)
    elif ghost.__class__.__name__ == "RedGhost":
        redTime.append(search_time)
    elif ghost.__class__.__name__ == "OrangeGhost":
        orangeTime.append(search_time)
    return search_time
def countNodesOfEachGhost(ghost, target_x, target_y):
    ghost.nodes = 0
    ghost_name = ghost.__class__.__name__
    ghost.find_path_to_pacman(target_x, target_y)
    count =0
    count+=ghost.getNodes()
    if ghost_name == "BlueGhost":
        blueNodes.append(count)
    elif ghost_name == "PinkGhost":
        pinkNodes.append(count)
    elif ghost_name == "RedGhost":
        redNodes.append(count)
    elif ghost_name == "OrangeGhost":
        orangeNodes.append(count)
    return count
def measureMemoryEachGhost(ghost, target_x, target_y):
    tracemalloc.start()

    ghost.find_path_to_pacman(target_x, target_y)

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    memory_kb = peak / 1024  # Convert to KB
    ghost_name = ghost.__class__.__name__
    print(f"{ghost_name} | Peak Memory: {memory_kb:.2f}KB")

    if ghost_name == "BlueGhost":
        blueMemory.append(memory_kb)
    elif ghost_name == "PinkGhost":
        pinkMemory.append(memory_kb)
    elif ghost_name == "RedGhost":
        redMemory.append(memory_kb)
    elif ghost_name == "OrangeGhost":
        orangeMemory.append(memory_kb)
    return memory_kb
def measureEachGhost(ghost, target_x, target_y):
    time_taken = measureTimeEachGhost(ghost, target_x, target_y)
    memory_used = measureMemoryEachGhost(ghost, target_x, target_y)
    nodes_expanded = countNodesOfEachGhost(ghost, target_x, target_y)
    ghost_name = ghost.__class__.__name__
    if ghost_name == "BlueGhost":
        blueTime.append(time_taken)
        blueMemory.append(memory_used)
        blueNodes.append(nodes_expanded)
        blueLocation.append(ghost.getLocation())
    elif ghost_name == "PinkGhost":
        pinkTime.append(time_taken)
        pinkMemory.append(memory_used)
        pinkNodes.append(nodes_expanded)
        pinkLocation.append(ghost.getLocation())
    elif ghost_name == "RedGhost":
        redTime.append(time_taken)
        redMemory.append(memory_used)
        redNodes.append(nodes_expanded)
        redLocation.append(ghost.getLocation())
    elif ghost_name == "OrangeGhost":
        orangeTime.append(time_taken)
        orangeMemory.append(memory_used)
        orangeNodes.append(nodes_expanded)
        orangeLocation.append(ghost.getLocation())
def measure(rounds):
    for _ in range(rounds):
        pacman=Pacman()
        ghosts = [
            BlueGhost(pacman_pos=(pacman.x, pacman.y)),
            PinkGhost(pacman_pos=(pacman.x, pacman.y)),
            OrangeGhost(pacman_pos=(pacman.x, pacman.y)),
            RedGhost(pacman_pos=(pacman.x, pacman.y)),
        ]
        for ghost in ghosts:
            measureEachGhost(ghost,pacman.x,pacman.y)
measure(10)
def write_ghost_data(file, ghost_name, locations, times, memories, nodes):
    """Write data for a ghost with a section header and formatted rows."""
    file.write(f"{ghost_name}\n")
    for i in range(len(locations)):
        location_str = f"({locations[i][0]}, {locations[i][1]})"  # Convert tuple to string
        line = f"{location_str:<20}{times[i]:>20.8f}{memories[i]:>10.1f}{nodes[i]:>10.0f}\n"
        file.write(line)
with open('output.txt', 'a', encoding='utf-8') as f:
    # Write column header only if file is empty
    if os.path.getsize('output.txt') == 0:
        header = f"{'location':<20}{'time':>20}{'memory':>10}{'number of expanded nodes':>10}\n"
        f.write(header)
    
    # Write data for each ghost
    write_ghost_data(f, "Blue Ghost", blueLocation, blueTime, blueMemory, blueNodes)
    write_ghost_data(f, "Red Ghost", redLocation, redTime, redMemory, redNodes)
    write_ghost_data(f, "Pink Ghost", pinkLocation, pinkTime, pinkMemory, pinkNodes)
    write_ghost_data(f, "Orange Ghost", orangeLocation, orangeTime, orangeMemory, orangeNodes)
