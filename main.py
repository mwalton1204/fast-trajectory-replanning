import maze
import visualizer
import astar
import demos
import os

if __name__ == "__main__":
    if not os.path.exists("grids/grid_0.pkl"):
        maze.save_grids()

    while True:
        print("\n=== Fast Trajectory Replanning ===")
        print("0. Generate new mazes")
        print("1. View a maze")
        print("2. Demo an Algorithm")
        print("3. Forward A* large-g vs small-g")
        print("4. Forward vs Backward")
        print("5. Forward vs Adaptive")
        print("6. Run full experiments")
        print("q. Quit")
        
        choice = input("\nChoose: ").strip()
        
        if choice == "q":
            break
        elif choice == "0":
            maze.save_grids()
        elif choice == "1":
            grid, start, goal = demos.get_grid()
            visualizer.visualize_grid(grid, start=start, goal=goal)
        elif choice == "2":
            print("1. Forward A*")
            print("2. Forward A* (large-g)")
            print("3. Forward A* (small-g)")
            print("4. Backward A*")
            print("5. Backward A* (large-g)")
            print("6. Backward A* (small-g)")
            print("7. Adaptive A*")
            print("8. Adaptive A* (large-g)")
            print("9. Adaptive A* (small-g)")
            
            algo_choice = input("\nChoose: ").strip()
            
            if algo_choice == "1":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Forward A*", astar.repeated_forward_astar, grid, start, goal)
            elif algo_choice == "2":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Forward A* (large-g)", astar.forward_large_g, grid, start, goal)
            elif algo_choice == "3":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Forward A* (small-g)", astar.forward_small_g, grid, start, goal)
            elif algo_choice == "4":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Backward A*", astar.repeated_backward_astar, grid, start, goal)
            elif algo_choice == "5":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Backward A* (large-g)", astar.backward_large_g, grid, start, goal)
            elif algo_choice == "6":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Backward A* (small-g)", astar.backward_small_g, grid, start, goal)
            elif algo_choice == "7":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Adaptive A*", astar.adaptive_astar, grid, start, goal)
            elif algo_choice == "8":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Adaptive A* (large-g)", astar.adaptive_large_g, grid, start, goal)
            elif algo_choice == "9":
                grid, start, goal = demos.get_grid()
                demos.run_demo("Adaptive A* (small-g)", astar.adaptive_small_g, grid, start, goal)
        elif choice == "3":
            grid, start, goal = demos.get_grid()
            demos.run_demo("Forward Large-g", astar.forward_large_g, grid, start, goal)
            demos.run_demo("Forward Small-g", astar.forward_small_g, grid, start, goal)
        elif choice == "4":
            grid, start, goal = demos.get_grid()
            demos.run_demo("Forward Large-g", astar.forward_large_g, grid, start, goal)
            demos.run_demo("Backward Large-g", astar.backward_large_g, grid, start, goal)
        elif choice == "5":
            grid, start, goal = demos.get_grid()
            demos.run_demo("Forward Large-g", astar.forward_large_g, grid, start, goal)
            demos.run_demo("Adaptive Large-g", astar.adaptive_large_g, grid, start, goal)
        elif choice == "6":
            results = demos.run_experiments()
            demos.print_summary(results)