import maze

if __name__ == "__main__":
    grid = maze.Grid()
    maze.generate_maze(grid)
    
    total_cells = grid.rows * grid.cols
    blocked_count = grid.blocked.sum()
    unblocked_count = total_cells - blocked_count
    
    print(f"Total cells:    {total_cells}")
    print(f"Blocked cells:  {blocked_count}")
    print(f"Unblocked cells:{unblocked_count}")
    print(f"Block rate:     {blocked_count/total_cells:.1%}")