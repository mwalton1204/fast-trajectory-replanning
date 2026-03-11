import numpy as np
import random
import pickle
import os

class Grid:
    def __init__(self, rows = 51, cols = 51):
        self.rows = rows
        self.cols = cols
        self.blocked = np.zeros((rows, cols), dtype=bool)
        
    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols
    
    def get_neighbors(self, r, c):
        # Up, Down, Left, Right offsets
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        neighbors = []
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                neighbors.append((nr,nc))
                
        return neighbors

def generate_maze(grid):
    visited = np.zeros((grid.rows, grid.cols), dtype=bool)
    
    start_r = random.randint(0, grid.rows - 1)
    start_c = random.randint(0, grid.cols - 1)
    
    visited[start_r, start_c] = 1
    grid.blocked[start_r, start_c] = 0
    
    stack = []
    stack.append((start_r, start_c))
    
    while True:
    
        while stack:
            r, c = stack[-1] # Check current position
            unvisited_neighbors = []
            
            for nr, nc in grid.get_neighbors(r, c):
                    if not visited[nr, nc]:
                        unvisited_neighbors.append((nr, nc))
                
            # If all current neighbors visited, move to next position in stack     
            if not unvisited_neighbors:
                stack.pop()
            else:
                # Pick random unvisited neighbor
                nr, nc = random.choice(unvisited_neighbors)
                
                visited[nr, nc] = 1
                
                # 30% chance: mark blocked
                if random.random() < 0.3:
                    grid.blocked[nr, nc] = 1
                # 70% chance: mark not blocked, push to stack and visit later
                else:
                    grid.blocked[nr, nc] = 0
                    stack.append((nr, nc))
        
        ## Check for unvisited cells after stack is emptied            
        unvisited = [(r, c) for r in range(grid.rows) for c in range(grid.cols) if not visited[r, c]]
        
        if not unvisited:
            break # Every cell has been visited
        
        # Pick rendom unvisited cell
        r, c = random.choice(unvisited)
        visited[r, c] = 1
        
        if random.random() < 0.3:
            grid.blocked[r, c] = 1
        else:
            grid.blocked[r, c] = 0
            stack.append((r, c))

def save_grids(n = 30, folder = "grids"):
    os.makedirs(folder, exist_ok = True)
    
    # Generate n grids with unique start and goal locations
    for i in range(n):
        grid = Grid()
        generate_maze(grid)
        
        unblocked = [(r,c) for r in range(grid.rows) for c in range(grid.cols) if not grid.blocked[r, c]]
        start, goal = random.sample(unblocked, 2)
        
        # Create a dictionary with grid data and save to grids folder
        data = {"grid": grid, "start": start, "goal": goal}
        with open(f"{folder}/grid_{i}.pkl", "wb") as f:
            pickle.dump(data, f)
            
        print(f"Saved grid {i+1}/30")
        
def load_grid(index, folder = "grids"):
    # Load and return specified grid data
    with open(f"{folder}/grid_{index}.pkl", "rb") as f:
        data = pickle.load(f)
    return data["grid"], data["start"], data["goal"]