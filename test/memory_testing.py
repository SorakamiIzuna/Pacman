import tracemalloc
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


blueMemory, pinkMemory, redMemory, orangeMemory = [], [], [], []

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
def memoryMeasure(rounds):
    for _ in range(rounds):
        pacman = Pacman()

        ghosts = [
            BlueGhost(pacman_pos=(pacman.x, pacman.y)),
            PinkGhost(pacman_pos=(pacman.x, pacman.y)),
            OrangeGhost(pacman_pos=(pacman.x, pacman.y)),
            RedGhost(pacman_pos=(pacman.x, pacman.y)),
        ]

        for ghost in ghosts:
            measureMemoryEachGhost(ghost, pacman.x, pacman.y)

# Example usage
memoryMeasure(100)  # Run 10 rounds

rounds = list(range(1, len(orangeMemory) + 1))

plt.plot(rounds, orangeMemory, label='UCS', color='orange')
plt.plot(rounds, blueMemory, label='BFS', color='blue')
plt.plot(rounds, redMemory, label='A*', color='red')
plt.plot(rounds, pinkMemory, label='DFS', color='purple')

# Labels, title, legend
plt.xlabel('Rounds')
plt.ylabel('Memory (KB)')
plt.title('Memory per Round')
plt.legend()

plt.grid(True)
plt.tight_layout()
plt.show()


#Thời gian chạy trung bình
means = [
    np.mean(orangeMemory),
    np.mean(blueMemory),
    np.mean(redMemory),
    np.mean(pinkMemory)
]

# Labels
labels = ['UCS', 'BFS', 'A*', 'DFS']

# Plot as bar chart
plt.bar(labels, means, color=['orange', 'blue', 'red', 'pink'], alpha=0.7)

# Add value labels above bars
for i, mean in enumerate(means):
    plt.text(i, mean + 0.00000001, f'{mean:.8f}', ha='center')

# Labels and title
plt.ylabel('Mean Memory (KB)')
plt.title('Average Execution Memory Required per Search')
plt.tight_layout()
plt.show()