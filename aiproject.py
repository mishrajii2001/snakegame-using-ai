import pygame
import sys
import random
from collections import deque

# Initialize pygame
pygame.init()

# Grid size
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

# Screen setup
SCREEN = pygame.display.set_mode((GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT))
pygame.display.set_caption("Smart Snake Game with BFS AI")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Clock
clock = pygame.time.Clock()
FPS = 10

# Directions
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

# BFS for pathfinding
def bfs(start, goal, snake_body):
    queue = deque([start])
    visited = set()
    parent = {}
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == goal:
            break

        for dir in DIRECTIONS.values():
            neighbor = (current[0] + dir[0], current[1] + dir[1])

            if (0 <= neighbor[0] < GRID_WIDTH and
                0 <= neighbor[1] < GRID_HEIGHT and
                neighbor not in visited and
                neighbor not in snake_body):
                
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    path = []
    if goal in parent:
        current = goal
        while current != start:
            path.append(current)
            current = parent[current]
        path.reverse()
    return path

# Snake Game Class
class SnakeGame:
    def __init__(self):
        self.reset()

    def reset(self):
        self.snake = [(5, 5)]
        self.direction = "RIGHT"
        self.spawn_food()

    def spawn_food(self):
        while True:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.food not in self.snake:
                break

    def move_snake(self, next_pos):
        if next_pos == self.food:
            self.snake.insert(0, next_pos)
            self.spawn_food()
        else:
            self.snake.insert(0, next_pos)
            self.snake.pop()

    def draw(self):
        SCREEN.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(SCREEN, GREEN, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(SCREEN, RED, (self.food[0]*GRID_SIZE, self.food[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.display.update()

    def game_over(self):
        head = self.snake[0]
        return (head in self.snake[1:] or
                head[0] < 0 or head[1] < 0 or
                head[0] >= GRID_WIDTH or head[1] >= GRID_HEIGHT)

    def run(self):
        while True:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            path = bfs(self.snake[0], self.food, set(self.snake))
            if path:
                next_step = path[0]
                self.move_snake(next_step)
            else:
                # No path found; just move in current direction or end
                dx, dy = DIRECTIONS[self.direction]
                next_pos = (self.snake[0][0] + dx, self.snake[0][1] + dy)
                self.move_snake(next_pos)

            if self.game_over():
                print("Game Over! Final Score:", len(self.snake) - 1)
                pygame.time.wait(2000)
                self.reset()

            self.draw()

# Run the game
if __name__ == "__main__":
    SnakeGame().run()
