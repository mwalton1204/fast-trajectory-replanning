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
    steps_bwd, exp_bwd = astar.backward_large_g(grid, start, goal)
    
    if steps_fwd:
        print(f"Forward Large-g: {len(steps_fwd)} steps, {exp_fwd} expansions")
    if steps_bwd:
        print(f"Backward Large-g: {len(steps_bwd)} steps, {exp_bwd} expansions")
    
    visualizer.visualize_steps(grid, start=start, goal=goal, steps=steps_fwd)
    visualizer.visualize_steps(grid, start=start, goal=goal, steps=steps_bwd)