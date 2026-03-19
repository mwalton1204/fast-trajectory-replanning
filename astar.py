import numpy as np
import heapq

def compute_path(grid, known_blocked, open_list, g, h, search, parent, counter, start, goal):
    while open_list:
        
        # Compare goal's current g-value to smallest f-value in open_list
        if g[goal] <= open_list[0][0]:
            break
        
        f, (r, c) = heapq.heappop(open_list)
        
        for nr, nc in grid.get_neighbors(r, c):
            if known_blocked[nr, nc]:
                continue
            
            if search[nr, nc] < counter:
                g[nr, nc] = np.inf
                search[nr, nc] = counter
                
            if g[nr, nc] > g[r, c] + 1:
                g[nr, nc] = g[r, c] + 1
                parent[(nr, nc)] = (r, c)
                heapq.heappush(open_list, (g[nr, nc] + h[nr, nc], (nr, nc)))
                
def compute_h(grid, h_array, goal):
    for r in range(grid.rows):
        for c in range(grid.cols):
            # Calculate manhattan distance (|x1 - x2| + |y1 - y2|) and assign as h-value for that cell
            h_array[r, c] = abs(r - goal[0]) + abs(c - goal[1])

def observe_neighbors(grid, known_blocked, current):
    for nr, nc in grid.get_neighbors(current[0], current[1]):
        if grid.blocked[nr, nc]:
            known_blocked[nr, nc] = True
            
def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    
    while current != start:
        path.append(current)
        current = parent[current]
        
    path.append(start)
    path.reverse()
    
    return path

def repeated_forward_astar(grid, start, goal):
    rows = grid.rows
    cols = grid.cols
    
    # Initialize arrays to track necessary values for each cell
    g_array = np.full((rows, cols), np.inf)
    h_array = np.zeros((rows, cols))
    # Search tracks which search last touched each cell, avoids resetting g-values between searches
    search = np.zeros((rows, cols), dtype = int)
    parent = {}
    known_blocked = np.zeros((rows, cols), dtype = bool)
    
    compute_h(grid, h_array, goal)
    counter = 0
    current = start
    solution = [start]
    observe_neighbors(grid, known_blocked, current)
    
    while current != goal:
        counter += 1
        
        print(f"Search #{counter}, current={current}, goal={goal}")
        
        # Initialize start and goal for this search
        g_array[current] = 0
        search[current] = counter
        g_array[goal] = np.inf
        search[goal] = counter
        
        # Initialize and push start to open list
        open_list = []
        heapq.heappush(open_list, (h_array[current], current))
        
        # Run A*
        compute_path(grid, known_blocked, open_list, g_array, h_array, search, parent, counter, current, goal)
        
        print(f"g_array[goal] = {g_array[goal]}")
        
        # If unreachable goal
        if g_array[goal] == np.inf:
            return None
        
        # If goal found, reconstruct path
        path = reconstruct_path(parent, current, goal)
        
        # Make agent traverse path
        for next_cell in path[1:]:
            if known_blocked[next_cell]:
                break
            current = next_cell
            solution.append(current)
            observe_neighbors(grid, known_blocked, current)
            if current == goal:
                return solution