import numpy as np
import matplotlib.pyplot as plt
import math

# Configuration parameters
GRID_HEIGHT = 1000
GRID_WIDTH = 1000
ITERATIONS = 200
D_VAL = 0.5

def generate_grid():
    """Generate a grid with random initial values"""
    return np.random.uniform(low=-0.1, high=0.1, size=(GRID_HEIGHT, GRID_WIDTH))

def calculate_all(grid):
    """Calculate the next state for all cells in the grid at once"""
    # Create shifted arrays for each direction (with proper wrapping)
    up = np.roll(grid, -1, axis=0)
    down = np.roll(grid, 1, axis=0)
    left = np.roll(grid, -1, axis=1)
    right = np.roll(grid, 1, axis=1)
    
    # Diagonal neighbors
    ne = np.roll(np.roll(grid, -1, axis=0), 1, axis=1)  # North-East
    se = np.roll(np.roll(grid, 1, axis=0), 1, axis=1)   # South-East
    sw = np.roll(np.roll(grid, 1, axis=0), -1, axis=1)  # South-West
    nw = np.roll(np.roll(grid, -1, axis=0), -1, axis=1) # North-West
    
    # Calculate the tanh of current values
    tan = np.tanh(grid)
    
    # Sum of neighbors with proper weighting
    close_sum = (up + down + left + right)
    diag_sum = (ne + se + sw + nw)
    
    # Full calculation
    return 1.3 * tan + D_VAL * ((close_sum / 6) + (diag_sum / 12) - grid)


def calculate_vote(grid):

    up = np.roll(grid, -1, axis=0)
    down = np.roll(grid, 1, axis=0)
    left = np.roll(grid, -1, axis=1)
    right = np.roll(grid, 1, axis=1)
    
    # Diagonal neighbors
    ne = np.roll(np.roll(grid, -1, axis=0), 1, axis=1)  # North-East
    se = np.roll(np.roll(grid, 1, axis=0), 1, axis=1)   # South-East
    sw = np.roll(np.roll(grid, 1, axis=0), -1, axis=1)  # South-West
    nw = np.roll(np.roll(grid, -1, axis=0), -1, axis=1) # North-West

    total = up + down + left + right + ne + se + sw + nw + grid

    val = 1 if total == 4 or total > 5 else 0

    return val

def vote_ca(grid):

    new_grid = (grid >= 0).astype(int)
    


def main():
    # Initialize grid and plot
    grid = generate_grid()
    grid2 = np.where(grid >= 0, 1, 0)
    
    # Create a figure with two subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 5))
    
    # First subplot: Initial state
    img1 = ax1.imshow(grid, cmap='seismic', interpolation='nearest', vmin=-1, vmax=1)
    plt.colorbar(img1, ax=ax1, label='Value')
    ax1.set_title('Initial Random Values')
    
    # Second subplot: Evolving state
    img2 = ax2.imshow(grid, cmap='seismic', interpolation='nearest', vmin=-1, vmax=1)
    plt.colorbar(img2, ax=ax2, label='Value')
    iteration_title = ax2.set_title('Iteration: 0')
    
    img3 = ax3.imshow(grid, cmap='seismic', interpolation='nearest', vmin=0, vmax=1)
    plt.colorbar(img2, ax=ax2, label='Value')
    iteration_title = ax2.set_title('Iteration: 0')

    # Run simulation
    for iter in range(ITERATIONS):
        # Update the grid using vectorized calculation
        grid = calculate_all(grid)
        grid2 = calculate_vote(grid2)
        
        # Update the visualization
        img2.set_data(grid)
        img3.set_data(grid2)
        iteration_title.set_text(f'Iteration: {iter+1}')
        # plt.pause(0.05)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()