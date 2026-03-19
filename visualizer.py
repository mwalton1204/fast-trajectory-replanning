import pygame

def visualize_grid(grid, start=None, goal=None, path=None):
    CELL_SIZE = 17  # pixels per cell — change this to zoom in/out!
    WIDTH = grid.cols * CELL_SIZE
    HEIGHT = grid.rows * CELL_SIZE

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze")

    # Draw each cell
    for r in range(grid.rows):
        for c in range(grid.cols):
            color = (0, 0, 0) if grid.blocked[r, c] else (255, 255, 255)
            pygame.draw.rect(screen, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            # Draw grid border
            pygame.draw.rect(screen, (200, 200, 200), (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Draw start and goal
    if start:
        pygame.draw.rect(screen, (0, 200, 0), (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if goal:
        pygame.draw.rect(screen, (200, 0, 0), (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw path if one exists
    if path:
        for (r, c) in path:
            if (r, c) != start and (r, c) != goal:
                pygame.draw.rect(screen, (0, 0, 255),
                    (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

    # Keep window open until closed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
def visualize_steps(grid, start=None, goal=None, steps=None):
    CELL_SIZE = 17  # pixels per cell — change this to zoom in/out!
    WIDTH = grid.cols * CELL_SIZE
    HEIGHT = grid.rows * CELL_SIZE
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze")
    
    current_step = 0
    stepping = False
    clock = pygame.time.Clock()
    
    while True:
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_step = min(current_step + 1, len(steps) - 1)
                if event.key == pygame.K_LEFT:
                    current_step = max(current_step - 1, 0)
                if event.key == pygame.K_SPACE:
                    stepping = not stepping
        
        if stepping:
            current_step = min(current_step + 1, len(steps) - 1)
            if current_step == len(steps) - 1:
                stepping = False
                
        step = steps[current_step]
        
        # Draw each cell
        for r in range(grid.rows):
            for c in range(grid.cols):
                color = (0, 0, 0) if step["known_blocked"][r, c] else (255, 255, 255)
                pygame.draw.rect(screen, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                # Draw grid border
                pygame.draw.rect(screen, (200, 200, 200), (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                
            # Draw current path
            for (r, c) in step["current_path"]:
                if (r, c) != start and (r, c) != goal:
                    pygame.draw.rect(screen, (0, 0, 255), (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    
            # Draw start and goal
            if start:
                pygame.draw.rect(screen, (0, 200, 0), (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if goal:
                pygame.draw.rect(screen, (200, 0, 0), (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        
            # Draw agent
            agent = step["agent"]
            pygame.draw.rect(screen, (255, 255, 0), (agent[1]*CELL_SIZE, agent[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
            pygame.display.flip()
            clock.tick(100)