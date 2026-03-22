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
    CELL_SIZE = 15  # pixels per cell — change this to zoom in/out!
    WIDTH = grid.cols * CELL_SIZE
    HEIGHT = grid.rows * CELL_SIZE
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze")
    font = pygame.font.SysFont("monospace", 14)
    
    current_step = 0
    stepping = False
    show_maze = False
    
    play_speed = 5
    tick_counter = 0
    clock = pygame.time.Clock()
    
    while True:
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: # Right arrow step forward
                    current_step = min(current_step + 1, len(steps) - 1)
                if event.key == pygame.K_LEFT: # Left arrow step back
                    current_step = max(current_step - 1, 0)
                if event.key == pygame.K_SPACE: # Space start/stop stepping
                    stepping = not stepping
                if event.key == pygame.K_t: # T show full maze
                    show_maze = not show_maze
        
        if stepping:
            tick_counter += 1
            if tick_counter >= 60 // play_speed:
                tick_counter = 0
                current_step = min(current_step + 1, len(steps) - 1)
                if current_step == len(steps) - 1:
                    stepping = False
                
        step = steps[current_step]
        
        screen.fill((128, 128, 128))  # clear screen with grey background each frame
        
        # Draw each cell
        for r in range(grid.rows):
            for c in range(grid.cols):
                if show_maze:
                    color = (0, 0, 0) if grid.blocked[r, c] else (255, 255, 255)
                elif step["known_blocked"][r, c]:
                    color = (0, 0, 0)
                elif not step["observed"][r, c]: # Fog of war
                    color = (200, 200, 200)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(screen, color, (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
            # Draw current path
            for (r, c) in step["visited"]:
                if (r, c) != start and (r, c) != goal:
                    pygame.draw.rect(screen, (0, 0, 255), (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    
            # Draw projected path
            for (r, c) in step["projected_path"]:
                if (r, c) != start and (r, c) != goal and (r, c) != step["agent"]:
                    pygame.draw.rect(screen, (255, 165, 0), (c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    
            # Draw start and goal
            if start:
                pygame.draw.rect(screen, (0, 200, 0), (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if goal:
                pygame.draw.rect(screen, (200, 0, 0), (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        
            # Draw agent
            agent = step["agent"]
            pygame.draw.rect(screen, (255, 255, 0), (agent[1]*CELL_SIZE, agent[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
            # Draw info panel background
            panel = pygame.Surface((220, 120))
            panel.set_alpha(120)
            panel.fill((0, 0, 0))
            screen.blit(panel, (5, 5))
            
            # Draw info text
            info_lines = [
                f"Move: {step['moves']}",
                f"Start: {start}",
                f"Goal: {goal}",
                f"Agent: {step['agent']}",
                f"Replans: {step['replans']}",
                f"Expansions: {step['expansions']}",
            ]
            for i, line in enumerate(info_lines):
                text = font.render(line, True, (255, 255, 255))
                screen.blit(text, (10, 10 + i * 18))
        
        pygame.display.flip()
        clock.tick(60)