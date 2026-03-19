import maze
import visualizer
import astar
import os

if __name__ == "__main__":
    # Generate 30 grids if non exist
    if not os.path.exists("grids/grid_0.pkl"):
        maze.save_grids()
    
    # Load the first grid
    grid, start, goal = maze.load_grid(0)
    
    steps, expansions = astar.repeated_forward_astar(grid, start, goal)
    
    if steps is None:
        print("No path found!")
    else:
        print(f"Path found! length: {len(steps)-1} steps, {expansions} expansions")
        print(f"Start: {start}")
        print (f"Goal: {goal}")
        
    steps_large, expansions_large = astar.forward_large_g(grid, start, goal)
    steps_small, expansions_small = astar.forward_small_g(grid, start, goal)

    if steps_large:
       print(f"Large-g: {len(steps_large)-1} steps, {expansions_large} expansions")
    if steps_small:
        print(f"Small-g: {len(steps_small)-1} steps, {expansions_small} expansions")
    
    # Visualize the loaded grid
    visualizer.visualize_steps(grid, start = start, goal = goal, steps = steps_large)
    visualizer.visualize_steps(grid, start = start, goal = goal, steps = steps_small)