import pygame
import random
from enum import Enum

pygame.init()

# -----------------------------------
# Constants
# -----------------------------------

BLOCK_SIZE = 20
SPEED = 10

WIDTH = 640
HEIGHT = 480

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,255,0)

font = pygame.font.SysFont("arial",25)

# -----------------------------------
# Directions
# -----------------------------------

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

# -----------------------------------
# Game Class
# -----------------------------------

class SnakeGame:

    def __init__(self):

        self.display = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()

        self.reset()

    def reset(self):

        self.direction = Direction.RIGHT

        self.head = [WIDTH//2, HEIGHT//2]

        self.snake = [
            self.head,
            [self.head[0]-BLOCK_SIZE,self.head[1]],
            [self.head[0]-2*BLOCK_SIZE,self.head[1]]
        ]

        self.score = 0
        self.frame_iteration = 0

        self.food = None

        self.place_food()

    def place_food(self):

        while True:

            x = random.randint(0,(WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
            y = random.randint(0,(HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE

            self.food = [x,y]

            if self.food not in self.snake:
                break

    def _turn_left(self, direction):

        if direction == Direction.RIGHT:
            return Direction.UP

        if direction == Direction.LEFT:
            return Direction.DOWN

        if direction == Direction.UP:
            return Direction.LEFT

        if direction == Direction.DOWN:
            return Direction.RIGHT

    def _turn_right(self, direction):

        if direction == Direction.RIGHT:
            return Direction.DOWN

        if direction == Direction.LEFT:
            return Direction.UP

        if direction == Direction.UP:
            return Direction.RIGHT

        if direction == Direction.DOWN:
            return Direction.LEFT

    def _get_next_head(self, direction):

        x = self.head[0]
        y = self.head[1]

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE

        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE

        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        return [x,y]

    def _is_collision_at(self, point):

        if point[0] >= WIDTH or point[0] < 0:
            return True

        if point[1] >= HEIGHT or point[1] < 0:
            return True

        if point in self.snake:
            return True

        return False

    def get_state(self):

        straight = self._get_next_head(self.direction)
        right = self._get_next_head(self._turn_right(self.direction))
        left = self._get_next_head(self._turn_left(self.direction))

        state = [
            int(self._is_collision_at(straight)),
            int(self._is_collision_at(right)),
            int(self._is_collision_at(left)),
            int(self.direction == Direction.LEFT),
            int(self.direction == Direction.RIGHT),
            int(self.direction == Direction.UP),
            int(self.direction == Direction.DOWN),
            int(self.food[0] < self.head[0]),
            int(self.food[0] > self.head[0]),
            int(self.food[1] < self.head[1]),
            int(self.food[1] > self.head[1])
        ]

        return state

    def _move(self, action):

        move_map = {
            (1,0,0): self.direction,
            (0,1,0): self._turn_right(self.direction),
            (0,0,1): self._turn_left(self.direction)
        }

        direction = move_map.get(tuple(action), self.direction)
        self.direction = direction

        self.head = self._get_next_head(self.direction)
        self.snake.insert(0, self.head)

    def play_step(self, action=None):

        self.frame_iteration += 1

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if action is None and event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT

                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT

                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP

                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        if action is not None:
            self._move(action)
        else:
            self.head = self._get_next_head(self.direction)
            self.snake.insert(0, self.head)

        reward = 0
        game_over = False

        if self.is_collision():
            game_over = True
            reward = -10
            return reward, game_over, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.snake.pop()

        if self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10

        self.update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score

    def is_collision(self):

        if self.head[0] > WIDTH-BLOCK_SIZE:
            return True

        if self.head[0] < 0:
            return True

        if self.head[1] > HEIGHT-BLOCK_SIZE:
            return True

        if self.head[1] < 0:
            return True

        if self.head in self.snake[1:]:
            return True

        return False

    def update_ui(self):

        self.display.fill(BLACK)

        for pt in self.snake:

            pygame.draw.rect(
                self.display,
                GREEN,
                pygame.Rect(pt[0],pt[1],BLOCK_SIZE,BLOCK_SIZE)
            )

        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(
                self.food[0],
                self.food[1],
                BLOCK_SIZE,
                BLOCK_SIZE
            )
        )

        text = font.render("Score: "+str(self.score),True,WHITE)

        self.display.blit(text,[0,0])

        pygame.display.flip()

# -----------------------------------
# Main
# -----------------------------------

if __name__ == "__main__":

    from agent import Agent

    game = SnakeGame()
    agent = Agent()

    while True:

        state = game.get_state()
        final_move = agent.get_action(state)
        reward, game_over, score = game.play_step(final_move)

        next_state = game.get_state()
        agent.remember(state, final_move, reward, next_state, game_over)
        agent.train_short_memory(state, final_move, reward, next_state, game_over)

        if game_over:

            print("Final Score:",score)
            agent.n_games += 1
            agent.train_long_memory()
            game.reset()

    pygame.quit()