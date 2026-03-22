import maze
import astar
import visualizer
import numpy as np

def get_grid():
    grid_dir = input("Grid directory (Default = '/grids'):")
    grid_no = input("Which grid? (default = 1): ").strip()
    grid_no = int(grid_no)-1 if grid_no and int(grid_no) > 0 else 0
    if not grid_dir:
        grid_dir = "grids"
    return maze.load_grid(grid_no, grid_dir)

def run_demo(name, func, grid, start, goal):
    print(f"\nRunning {name}...")
    steps, expansions = func(grid, start, goal)
    if steps is None:
        print("No path found!")
        return
    print(f"Steps: {len(steps)} | Expansions: {expansions}")
    visualizer.visualize_steps(grid, start=start, goal=goal, steps=steps)

def run_experiments():
    qty_mazes = 30
    
    results = {
        "forward": {"expansions": [], "steps": []},
        "forward_large_g": {"expansions": [], "steps": []},
        "forward_small_g": {"expansions": [], "steps": []},
        
        "backward": {"expansions": [], "steps": []},
        "backward_large_g": {"expansions": [], "steps": []},
        "backward_small_g": {"expansions": [], "steps": []},
        
        "adaptive": {"expansions": [], "steps": []},
        "adaptive_large_g": {"expansions": [], "steps": []},
        "adaptive_small_g": {"expansions": [], "steps": []}
    }
    
    for i in range(qty_mazes):
        grid, start, goal = maze.load_grid(i)
        print(f"\nGrid {i+1}/30 | start = {start}, goal = {goal}")
        
        for name, func in [
            ("forward", astar.repeated_forward_astar),
            ("forward_large_g", astar.forward_large_g),
            ("forward_small_g", astar.forward_small_g),
            
            ("backward", astar.repeated_backward_astar),
            ("backward_large_g", astar.backward_large_g),
            ("backward_small_g", astar.backward_small_g),
            
            ("adaptive", astar.adaptive_astar),
            ("adaptive_large_g", astar.adaptive_large_g),
            ("adaptive_small_g", astar.adaptive_small_g),
        ]:
            steps, expansions = func(grid, start, goal)
            if steps:
                results[name]["expansions"].append(expansions)
                results[name]["steps"].append(len(steps))
            print(f"{name}: steps = {len(steps) if steps else 'FAILED'}, expansions = {expansions}")
            
    return results        
    
def print_summary(results):
    print("\nSUMMARY")
    for name, data in results.items():
        if data["expansions"]:
            mean_exp = np.mean(data["expansions"])
            mean_steps = np.mean(data["steps"])
            solved = len(data["expansions"])
            print(f"{name}: solved = {solved}/30, mean expansions = {mean_exp: .1f}, mean steps = {mean_steps: .1f}")
        else:
            print(f"{name}: solved = 0/30")