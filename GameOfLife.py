import numpy as np
import matplotlib.pyplot as plt
import time


GRID_SIZE = 100
ITERATIONS = 50

def game_of_life(iters=ITERATIONS):
    grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE))
    
    plt.ion()  # interactive mode on
    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap='binary')  # black & white

    for _ in range(iters):
        grid = iterate(grid)
        img.set_data(grid)
        plt.draw()
        plt.pause(0.5)  # delay in seconds

    plt.ioff()
    plt.show()

def iterate(grid):
    height, width = grid.shape
    new_grid = np.copy(grid)
    for y in range(height):
        for x in range(width):
            new_grid[y][x] = life_and_death_rule(grid, y, x)

    return new_grid

def count_live_neighbors(grid, y, x):
    height, width = grid.shape
    count = 0
    
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if (i == y and j == x):
                continue
            if 0 <= i < height and 0 <= j < width:
                count += grid[i][j]

    return count

def life_and_death_rule(grid, y, x):
    living_neighbors = count_live_neighbors(grid, y, x)
    if grid[y][x] == 1:
        return 1 if living_neighbors in [2, 3] else 0
    else:
        return 1 if living_neighbors == 3 else 0

if __name__ == '__main__':
    game_of_life()