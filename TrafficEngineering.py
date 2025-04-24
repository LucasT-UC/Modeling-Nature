import numpy as np
import matplotlib.pyplot as plt
from random import randint, randrange, shuffle


grid_WIDTH = 10
grid_HEIGHT = 5

MAP_WIDTH = 20
MAP_HEIGHT = 15


def generate_maze(width, height):
    """
    Generate a maze using recursive backtracking algorithm.
    
    Args:
        width: Width of the maze (should be odd)
        height: Height of the maze (should be odd)
        
    Returns:
        A numpy array representing the maze where:
        - 1: Wall
        - 0: Path
        - 6: Entrance
        - 9: Exit
    """
    # Ensure dimensions are odd
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    
    # Initialize maze with all walls
    maze = np.ones((height, width), dtype=int)
    
    # Mark all potential path cells (odd coordinates)
    for y in range(1, height, 2):
        for x in range(1, width, 2):
            maze[y][x] = 0
    
    # Stack for backtracking
    stack = []
    
    # Start at a random position
    start_y = randrange(1, height, 2)
    start_x = 1  # Start from the left edge
    
    # Mark the starting cell as visited
    visited = np.zeros((height, width), dtype=bool)
    visited[start_y][start_x] = True
    
    # Push the starting cell onto the stack
    stack.append((start_x, start_y))
    
    # Continue until the stack is empty
    while stack:
        x, y = stack[-1]
        
        # Find unvisited neighbors
        neighbors = []
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]  # Up, Right, Down, Left
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width-1 and 0 < ny < height-1 and not visited[ny][nx]:
                neighbors.append((nx, ny, dx, dy))
        
        if neighbors:
            # Choose a random unvisited neighbor
            nx, ny, dx, dy = neighbors[randrange(len(neighbors))]
            
            # Knock down the wall between the current cell and the chosen cell
            maze[y + dy//2][x + dx//2] = 0
            
            # Mark the chosen cell as visited
            visited[ny][nx] = True
            
            # Push the chosen cell onto the stack
            stack.append((nx, ny))
        else:
            # If no unvisited neighbors, backtrack
            stack.pop()
    
    # Create entrance and exit
    # Entrance on left side
    maze[start_y][0] = 2
    
    # Find exit point on right side
    possible_exits = []
    for y in range(1, height, 2):
        if maze[y][width-2] == 0:  # Check if there's a path cell adjacent to right edge
            possible_exits.append(y)
    
    if possible_exits:
        exit_y = possible_exits[randrange(len(possible_exits))]
    else:
        # If no good exit points, use the start row
        exit_y = start_y
        # Create a path to the right edge
        for x in range(width-2, 0, -1):
            if maze[exit_y][x] == 0:
                break
            maze[exit_y][x] = 0
    
    # Set exit
    maze[exit_y][width-1] = 2
    
    return maze



def traffic_engineering():
    grid = generate_maze(MAP_WIDTH, MAP_HEIGHT)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap='binary')  # black & white
    plt.draw()
    plt.pause(2)

    change = True

    while change:
        grid, change = iterate(grid)
        img.set_data(grid)
        plt.draw()
        plt.pause(0.5)

    plt.show()

def iterate(grid):
    new_grid = np.copy(grid)
    change = False
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if grid[y][x] == 0:
                new_grid[y][x] = cul_de_sac_rule(grid, x, y)
                if new_grid[y][x] != grid[y][x]:
                    change = True
    return new_grid, change

def cul_de_sac_rule(grid, x, y):
    u = grid[y - 1][x]
    d = grid[y + 1][x]
    l = grid[y][x - 1]
    r = grid[y][x + 1]
    total_borders = [u, d, l, r].count(1)

    return 1 if total_borders >= 3 else 0
    

if __name__ == '__main__':
    traffic_engineering()