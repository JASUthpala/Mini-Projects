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

        self.food = None

        self.place_food()

    def place_food(self):

        while True:

            x = random.randint(0,(WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
            y = random.randint(0,(HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE

            self.food = [x,y]

            if self.food not in self.snake:
                break

    def play_step(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT

                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT

                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP

                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        x = self.head[0]
        y = self.head[1]

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE

        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE

        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = [x,y]

        self.snake.insert(0,self.head)

        game_over = False

        if self.is_collision():

            game_over = True

            return game_over,self.score

        if self.head == self.food:

            self.score += 1

            self.place_food()

        else:

            self.snake.pop()

        self.update_ui()

        self.clock.tick(SPEED)

        return game_over,self.score

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

    game = SnakeGame()

    while True:

        game_over,score = game.play_step()

        if game_over:

            print("Final Score:",score)

            break

    pygame.quit()