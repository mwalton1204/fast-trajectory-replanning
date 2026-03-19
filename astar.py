import numpy as np
import heapq # 

def compute_path(grid, known_blocked, open_list, g, h, search, parent, counter, start, goal, tie_breaker=None):
    while open_list:
        
        # Compare goal's current g-value to smallest f-value in open_list
        if g[goal] <= open_list[0][0]:
            break
        
        heap_entry = heapq.heappop(open_list)
        f = heap_entry[0]
        r, c = heap_entry[-1]
        
        for nr, nc in grid.get_neighbors(r, c):
            if known_blocked[nr, nc]:
                continue
            
            if search[nr, nc] < counter:
                g[nr, nc] = np.inf
                search[nr, nc] = counter
                
            if g[nr, nc] > g[r, c] + 1:
                g[nr, nc] = g[r, c] + 1
                parent[(nr, nc)] = (r, c)
                f = g[nr, nc] + h[nr, nc]
                if tie_breaker == "large_g":
                    heapq.heappush(open_list, (f, -g[nr, nc], (nr, nc)))
                elif tie_breaker == "small_g":
                    heapq.heappush(open_list, (f, g[nr, nc], (nr, nc)))
                else:
                    heapq.heappush(open_list, (f, (nr, nc)))
                
def compute_h(grid, h_array, goal):
    for r in range(grid.rows):
        for c in range(grid.cols):
            # Calculate manhattan distance (|x1 - x2| + |y1 - y2|) and assign as h-value for that cell
            h_array[r, c] = abs(r - goal[0]) + abs(c - goal[1])

def observe_neighbors(grid, known_blocked, current, observed):
    observed[current[0], current[1]] = True # Mark current as seen
    
    for nr, nc in grid.get_neighbors(current[0], current[1]):
        observed[nr, nc] = True # Mark neighbors as seen
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

def repeated_forward_astar(grid, start, goal, tie_breaker=None):
    rows = grid.rows
    cols = grid.cols
    
    # Initialize arrays to track necessary values for each cell
    g_array = np.full((rows, cols), np.inf) # Each cell's g-value
    h_array = np.zeros((rows, cols)) # Each cell's h-value
    search = np.zeros((rows, cols), dtype = int) # Number of re-plans
    parent = {}
    known_blocked = np.zeros((rows, cols), dtype = bool) # Cells agent knows are blocked
    observed = np.zeros((rows, cols), dtype = bool) # Cells agent has seen
    
     # Agent knowledge after each move
    steps = []
    
    compute_h(grid, h_array, goal)
    counter = 0
    current = start
    visited = [start] # Full trajectory of the search
    observe_neighbors(grid, known_blocked, current, observed)
    
    steps.append({"agent": current, "known_blocked": known_blocked.copy(), "visited": visited[:], "observed": observed.copy()})
    
    while current != goal:
        counter += 1
                
        # Initialize start and goal for this search
        g_array[current] = 0
        search[current] = counter
        g_array[goal] = np.inf
        search[goal] = counter
        
        # Initialize and push start to open list
        open_list = []
        if tie_breaker != None:
            heapq.heappush(open_list, (h_array[current], 0, current))
        else:
            heapq.heappush(open_list, (h_array[current], current))
        
        # Run A*
        compute_path(grid, known_blocked, open_list, g_array, h_array, search, parent, counter, current, goal, tie_breaker)
                
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
            visited.append(current)
            observe_neighbors(grid, known_blocked, current, observed)
            steps.append({"agent": current, "known_blocked": known_blocked.copy(), "visited": visited[:], "observed": observed.copy()})
            if current == goal:
                steps.append({"agent": current, "known_blocked": known_blocked.copy(), "visited": visited[:], "observed": observed.copy()})
                return steps
            
def forward_large_g(grid, start, goal):
    return repeated_forward_astar(grid, start, goal, tie_breaker = "large_g")

def forward_small_g(grid, start, goal):
    return repeated_forward_astar(grid, start, goal, tie_breaker = "small_g")