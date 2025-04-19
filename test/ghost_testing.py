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
from time_testing import measureTimeEachGhost
from memory_testing import measureMemoryEachGhost
from expanded_nodes_testing import countNodesOfEachGhost

blueTime, redTime, orangeTime, pinkTime= [], [], [], []
blueMemory, redMemory, orangeMemory, pinkMemory = [], [], [], []
blueNodes, pinkNodes,orangeNodes,redNodes = [], [], [], []
blueLocation, redLocation, orangeLocation, pinkLocation = [], [], [], []
def measureEachGhost(ghost, target_x, target_y):
    measureTimeEachGhost(ghost, target_x, target_y)
    measureMemoryEachGhost(ghost, target_x, target_y)
    countNodesOfEachGhost(ghost, target_x, target_y)
def measure(rounds):
    for _ in range(rounds):
        pacman=Pacman()
