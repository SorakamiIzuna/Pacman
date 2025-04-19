import time
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
blueTime=[]
redTime=[]
orangeTime=[]
pinkTime=[]
rounds = 100
def measureTimeEachGhost(ghost, target_x, target_y):
    start_time = time.time()
    ghost.find_path_to_pacman(target_x, target_y)
    end_time = time.time()
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
def timeMeasure(rounds):
    for i in range(rounds):
        pacman=Pacman()

        blueGhost = BlueGhost(pacman_pos=(pacman.x,pacman.y))
        pinkGhost = PinkGhost(pacman_pos=(pacman.x,pacman.y))
        orangeGhost = OrangeGhost(pacman_pos=(pacman.x,pacman.y))
        redGhost = RedGhost(pacman_pos=(pacman.x,pacman.y))

        measureTimeEachGhost(blueGhost, pacman.x, pacman.y)
        measureTimeEachGhost(pinkGhost, pacman.x, pacman.y)
        measureTimeEachGhost(orangeGhost, pacman.x, pacman.y)
        measureTimeEachGhost(redGhost, pacman.x, pacman.y)
timeMeasure(rounds)
rounds = list(range(1, len(orangeTime) + 1))

plt.plot(rounds, orangeTime, label='UCS', color='orange')
plt.plot(rounds, blueTime, label='BFS', color='blue')
plt.plot(rounds, redTime, label='A*', color='red')
plt.plot(rounds, pinkTime, label='DFS', color='purple')

# Labels, title, legend
plt.xlabel('Rounds')
plt.ylabel('Time (s)')
plt.title('Time per Round')
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()


#Thời gian chạy trung bình
means = [
    np.mean(orangeTime),
    np.mean(blueTime),
    np.mean(redTime),
    np.mean(pinkTime)
]

# Labels
labels = ['UCS', 'BFS', 'A*', 'DFS']

# Plot as bar chart
plt.bar(labels, means, color=['orange', 'blue', 'red', 'pink'], alpha=0.7)

# Add value labels above bars
for i, mean in enumerate(means):
    plt.text(i, mean + 0.00000001, f'{mean:.8f}', ha='center')

# Labels and title
plt.ylabel('Mean Time (s)')
plt.title('Average Execution Time per Search')
plt.tight_layout()
plt.show()