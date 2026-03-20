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
    
    steps_fwd, exp_fwd = astar.forward_large_g(grid, start, goal)
    steps_adp, exp_adp = astar.adaptive_large_g(grid, start, goal)

    print(f"\nExpansion comparison:")
    print(f"Forward:  {exp_fwd}")
    print(f"Adaptive: {exp_adp}")
    
    visualizer.visualize_steps(grid, start=start, goal=goal, steps=steps_fwd)
    visualizer.visualize_steps(grid, start=start, goal=goal, steps=steps_adp)