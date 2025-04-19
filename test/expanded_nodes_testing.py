import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entities.pacman import Pacman
from entities.blueGhost import BlueGhost
from entities.orangeGhost import OrangeGhost 
from entities.pinkGhost import PinkGhost
from entities.redGhost import RedGhost

blueNodes, pinkNodes,orangeNodes,redNodes = [], [], [], []
def countNodesOfEachGhost(ghost, target_x, target_y):
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
def countNodes(rounds):
    for _ in range(rounds):
        pacman=Pacman()

        blueGhost = BlueGhost(pacman_pos=(pacman.x,pacman.y))
        pinkGhost = PinkGhost(pacman_pos=(pacman.x,pacman.y))
        orangeGhost = OrangeGhost(pacman_pos=(pacman.x,pacman.y))
        redGhost = RedGhost(pacman_pos=(pacman.x,pacman.y))

        countNodesOfEachGhost(blueGhost,pacman.x,pacman.y)
        countNodesOfEachGhost(pinkGhost,pacman.x,pacman.y)
        countNodesOfEachGhost(orangeGhost,pacman.x,pacman.y)
        countNodesOfEachGhost(redGhost,pacman.x,pacman.y)
countNodes(10)
rounds = list(range(1, len(orangeNodes) + 1))

plt.plot(rounds, orangeNodes, label='UCS', color='orange')
plt.plot(rounds, blueNodes, label='BFS', color='blue')
plt.plot(rounds, redNodes, label='A*', color='red')
plt.plot(rounds, pinkNodes, label='DFS', color='purple')

# Labels, title, legend
plt.xlabel('Rounds')
plt.ylabel('Nodes')
plt.title('Nodes per Round')
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()


#Thời gian chạy trung bình
means = [
    np.mean(orangeNodes),
    np.mean(blueNodes),
    np.mean(redNodes),
    np.mean(pinkNodes)
]

# Labels
labels = ['UCS', 'BFS', 'A*', 'DFS']

# Plot as bar chart
plt.bar(labels, means, color=['orange', 'blue', 'red', 'pink'], alpha=0.7)

# Add value labels above bars
for i, mean in enumerate(means):
    plt.text(i, mean + 0.00000001, f'{mean:.8f}', ha='center')

# Labels and title
plt.ylabel('Node')
plt.title('Average Nodes Expanded per Search')
plt.tight_layout()
plt.show()

print(blueNodes)