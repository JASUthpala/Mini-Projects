import pygame
import random
from enum import Enum

pygame.init()

# -----------------------------------
# Constants
# -----------------------------------

BLOCK_SIZE = 20
DEFAULT_SPEED = 10

WIDTH = 640
HEIGHT = 480

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
GREEN = (0,255,0)
DARK_GREEN = (0,180,0)
LIGHT_GREEN = (120,255,120)

font = pygame.font.SysFont("arial",25)
font_big = pygame.font.SysFont("arial",40, bold=True)

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
        self.speed = DEFAULT_SPEED
        self.game_over = False

        self.reset()

    def choose_speed(self):

        speed_options = {
            pygame.K_s: 8,
            pygame.K_m: 12,
            pygame.K_h: 18
        }

        while True:
            self.display.fill(BLACK)

            title = font_big.render("Select Snake Speed", True, WHITE)
            self.display.blit(title, (150, 100))

            slow = font.render("S - Slow", True, WHITE)
            medium = font.render("M - Medium", True, WHITE)
            high = font.render("H - High", True, WHITE)

            self.display.blit(slow, (250, 180))
            self.display.blit(medium, (235, 220))
            self.display.blit(high, (245, 260))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key in speed_options:
                        self.speed = speed_options[event.key]
                        return

            self.clock.tick(10)

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
        self.clock.tick(self.speed)

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

    def draw_cartoon_snake(self):

        for index, pt in enumerate(self.snake):
            body_color = LIGHT_GREEN if index == 0 else GREEN
            outline_color = DARK_GREEN if index == 0 else DARK_GREEN

            pygame.draw.rect(
                self.display,
                body_color,
                pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE),
                border_radius=8
            )
            pygame.draw.rect(
                self.display,
                outline_color,
                pygame.Rect(pt[0], pt[1], BLOCK_SIZE, BLOCK_SIZE),
                width=2,
                border_radius=8
            )

        head = self.snake[0]
        head_rect = pygame.Rect(head[0], head[1], BLOCK_SIZE, BLOCK_SIZE)

        pygame.draw.rect(
            self.display,
            LIGHT_GREEN,
            head_rect,
            border_radius=10
        )

        eye_radius = 2

        if self.direction == Direction.RIGHT:
            eye_positions = [(head[0] + 12, head[1] + 6), (head[0] + 12, head[1] + 14)]
        elif self.direction == Direction.LEFT:
            eye_positions = [(head[0] + 2, head[1] + 6), (head[0] + 2, head[1] + 14)]
        elif self.direction == Direction.UP:
            eye_positions = [(head[0] + 6, head[1] + 2), (head[0] + 14, head[1] + 2)]
        else:
            eye_positions = [(head[0] + 6, head[1] + 16), (head[0] + 14, head[1] + 16)]

        for x, y in eye_positions:
            pygame.draw.circle(self.display, BLACK, (x, y), eye_radius)

        mouth_x = head[0] + BLOCK_SIZE // 2
        mouth_y = head[1] + BLOCK_SIZE // 2

        if self.direction == Direction.RIGHT:
            pygame.draw.line(self.display, BLACK, (mouth_x + 5, mouth_y), (mouth_x + 10, mouth_y), 2)
        elif self.direction == Direction.LEFT:
            pygame.draw.line(self.display, BLACK, (mouth_x - 5, mouth_y), (mouth_x - 10, mouth_y), 2)
        elif self.direction == Direction.UP:
            pygame.draw.line(self.display, BLACK, (mouth_x, mouth_y - 5), (mouth_x, mouth_y - 10), 2)
        else:
            pygame.draw.line(self.display, BLACK, (mouth_x, mouth_y + 5), (mouth_x, mouth_y + 10), 2)

    def update_ui(self):

        self.display.fill(BLACK)
        self.draw_cartoon_snake()

        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(
                self.food[0],
                self.food[1],
                BLOCK_SIZE,
                BLOCK_SIZE
            ),
            border_radius=6
        )

        text = font.render("Score: "+str(self.score),True,WHITE)
        self.display.blit(text,[0,0])

        pygame.display.flip()

    def show_game_over(self):

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.display.blit(overlay, (0, 0))

        label = font_big.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        restart_text = font.render("Press any key to exit", True, WHITE)

        self.display.blit(label, (200, 150))
        self.display.blit(score_text, (250, 220))
        self.display.blit(restart_text, (175, 270))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    return

            self.clock.tick(10)

# -----------------------------------
# Main
# -----------------------------------

if __name__ == "__main__":

    from agent import Agent

    game = SnakeGame()
    game.choose_speed()
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
            game.show_game_over()
            agent.n_games += 1
            agent.train_long_memory()
            game.reset()
            game.choose_speed()

    pygame.quit()