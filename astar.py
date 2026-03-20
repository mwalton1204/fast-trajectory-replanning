import numpy as np
import heapq # Priority Queue
                
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
            known_blocked[nr, nc] = True # If neighbor blocked, put in known_blocked
            
def reconstruct_path(parent, start, goal): # Retrace via parents
    path = []
    current = goal
    
    while current != start:
        path.append(current)
        current = parent[current]
        
    path.append(start)
    path.reverse()
    
    return path

def compute_path(grid, known_blocked, open_list, g, h, search, parent, counter, start, goal, tie_breaker=None):
    num_expansions = 0
    expanded_cells = [] # Tracks which cells are expanded
    
    while open_list:
        
        # Compare cost to get to goal to the cheapest unexplored option
        if g[goal] <= open_list[0][0]:
            break
        
        heap_entry = heapq.heappop(open_list) # Pop the cheapest (f-value) unexplored cell
        r, c = heap_entry[-1]
        num_expansions += 1 # 1 cell popped = 1 expansion
        expanded_cells.append((r, c)) # Add the popped cell to the list of expanded cells
        
        for nr, nc in grid.get_neighbors(r, c):
            if known_blocked[nr, nc]:
                continue
            
            if search[nr, nc] < counter:
                g[nr, nc] = np.inf
                search[nr, nc] = counter
                
            if g[nr, nc] > g[r, c] + 1: # Found a cheaper path to this neighbor through the current cell
                g[nr, nc] = g[r, c] + 1 # Update neighbor's cost to the cheaper path
                parent[(nr, nc)] = (r, c) # Set current cell as neighbor's parent
                f = g[nr, nc] + h[nr, nc] # Calculate neighbor's total estimated cost
                if tie_breaker == "large_g": # Push -g to priority queue so larger g has priority
                    heapq.heappush(open_list, (f, -g[nr, nc], (nr, nc)))
                elif tie_breaker == "small_g": # Push +g to priority queue so smaller g has priority
                    heapq.heappush(open_list, (f, g[nr, nc], (nr, nc)))
                else: # No preference on tie-breaking
                    heapq.heappush(open_list, (f, (nr, nc)))
                    
    return num_expansions, expanded_cells

def repeated_forward_astar(grid, start, goal, tie_breaker=None):
    rows = grid.rows
    cols = grid.cols
    
    # Initializations
    g_array = np.full((rows, cols), np.inf) # Each cell's g-value (cost to get here from start)
    h_array = np.zeros((rows, cols)) # Each cell's h-value (cost to reach goal from here)
    search = np.zeros((rows, cols), dtype = int) # Tracks which search last visited it, avoids resetting g-values between searches
    parent = {} # Tracks expanded cell's parents for path reconstruction
    known_blocked = np.zeros((rows, cols), dtype = bool) # Cells that agent knows are blocked
    observed = np.zeros((rows, cols), dtype = bool) # Cells that agent has seen
    
    # Agent knowledge after each move
    steps = []
    total_expansions = 0
    counter = 0
    current = start
    visited = [start] # Full trajectory of the search
    
    compute_h(grid, h_array, goal) # Calculate inital h-values for each cell
    observe_neighbors(grid, known_blocked, current, observed) # Observe neighbors from start
    
    # Store step data for initial position
    steps.append({"agent": current, "known_blocked": known_blocked.copy(), "visited": visited[:], "observed": observed.copy()})
    
    while current != goal:
        counter += 1
                
        # Initialize start and goal for this search
        g_array[current] = 0 # Costs 0 to go from start to start
        search[current] = counter
        g_array[goal] = np.inf # Cost to go to goal is unknown, set to infinity
        search[goal] = counter
        
        # Initialize and push start to open list
        open_list = [] # Stores a cell's f-value, tie-breaker (if used), and coordinates
        if tie_breaker is not None:
            heapq.heappush(open_list, (h_array[current], 0, current))
        else:
            heapq.heappush(open_list, (h_array[current], current))
        
        # Compute the path from start to goal
        expansions, expanded_cells = compute_path(grid, known_blocked, open_list, g_array, h_array, search, parent, counter, current, goal, tie_breaker)
        total_expansions += expansions
                
        if g_array[goal] == np.inf: # If unreachable goal
            return None, total_expansions
        
        path = reconstruct_path(parent, current, goal) # If goal found, reconstruct path
        
        # Make agent traverse path
        for next_cell in path[1:]:
            if known_blocked[next_cell]:
                break
            current = next_cell
            visited.append(current)
            observe_neighbors(grid, known_blocked, current, observed)
            steps.append({"agent": current, "known_blocked": known_blocked.copy(), "visited": visited[:], "observed": observed.copy()})
            if current == goal:
                return steps, total_expansions
            
def repeated_backward_astar(grid, start, goal, tie_breaker=None):
    rows = grid.rows
    cols = grid.cols
    
    # Initializations
    g_array = np.full((rows, cols), np.inf) # Each cell's g-value (cost to get here from goal)
    h_array = np.zeros((rows, cols)) # Each cell's h-value (cost to reach current from goal)
    search = np.zeros((rows, cols), dtype = int) # Tracks which search last visited it, avoids resetting g-values between searches
    parent = {} # Tracks expanded cell's parents for path reconstruction
    known_blocked = np.zeros((rows, cols), dtype = bool) # Cells that agent knows are blocked
    observed = np.zeros((rows, cols), dtype = bool) # Cells that agent has seen
    
    # Agent knowledge after each move
    steps = []
    total_expansions = 0
    counter = 0
    current = start
    visited = [start] # Full trajectory of the search
    
    compute_h(grid, h_array, goal) # Calculate inital h-values for each cell
    observe_neighbors(grid, known_blocked, current, observed) # Observe neighbors from start
    
    # Store step data for initial position
    steps.append({"agent": current, "known_blocked": known_blocked.copy(), "visited": visited[:], "observed": observed.copy()})

    while current != goal:
        counter += 1
        
        compute_h(grid, h_array, current) # Must recalculate h-value each iteration because the location of current changes
        
        # Initialize start and goal for this search (backwards)
        g_array[goal] = 0 # Costs 0 to go from goal to goal
        search[goal] = counter
        g_array[current] = np.inf # Cost to go to current cell is unknown, set to infinity
        search[current] = counter
        
        open_list = [] # Stores a cell's f-value, tie-breaker (if used), and coordinates
        if tie_breaker is not None:
            heapq.heappush(open_list, (h_array[goal], 0, goal))
        else:
            heapq.heappush(open_list, (h_array[goal], goal))
        
        # Compute the path from goal to current (pass goal for start and current for goal)
        expansions, expanded_cells = compute_path(grid, known_blocked, open_list, g_array, h_array, search, parent, counter, goal, current, tie_breaker)
        total_expansions += expansions
        
        if g_array[current] == np.inf: # If unreachable goal
            return None, total_expansions
        
        path = reconstruct_path(parent, goal, current) # If goal found, reconstruct path
        path.reverse() # Reverse the reconstructed path
        
        # Make agent traverse path
        for next_cell in path[1:]:
            if known_blocked[next_cell]:
                break
            current = next_cell
            visited.append(current)
            observe_neighbors(grid, known_blocked, current, observed)
            steps.append({"agent": current, "known_blocked": known_blocked.copy(), "visited": visited[:], "observed": observed.copy()})
            if current == goal:
                return steps, total_expansions
            
def forward_large_g(grid, start, goal):
    return repeated_forward_astar(grid, start, goal, tie_breaker = "large_g")

def forward_small_g(grid, start, goal):
    return repeated_forward_astar(grid, start, goal, tie_breaker = "small_g")

def backward_large_g(grid, start, goal):
    return repeated_backward_astar(grid, start, goal, tie_breaker = "large_g")

def backward_small_g(grid, start, goal):
    return repeated_backward_astar(grid, start, goal, tie_breaker = "small_g")