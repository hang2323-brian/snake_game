import pygame
import sys
import random
from enum import Enum

CELL_WIDTH = 20


class Color(Enum):
    WHITE = (200, 200, 200)
    RED = (255, 0, 0)
    GREEN = (0, 128, 0)
    DARK_GREEN = (18, 65, 22)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0)


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Message():
    """Display game scores"""

    def __init__(self, screen):
        self.screen = screen
        self.screenRect = screen.get_rect()

        self.scoreTextColor = Color.MAGENTA.value
        self.scoreFont = pygame.font.SysFont("Roboto", 25)

        self.messageTextColor = Color.WHITE.value
        self.messageFont = pygame.font.SysFont("Roboto", 80)

    def draw_score(self, text):
        surface = self.scoreFont.render(text, True, self.scoreTextColor)
        self.screen.blit(surface, (30, 30))

    def draw_message(self, msg):
        surface = self.messageFont.render(msg, True, self.messageTextColor)
        textRect = surface.get_rect(center=(int(self.screenRect.width / 2), int(self.screenRect.height / 2)))
        self.screen.blit(surface, textRect)


class Snake():
    def __init__(self, game):
        self.game = game
        self.head = {'x': 0, 'y': 0}
        self.tail = [(11, 10)]
        self.direction = Direction.UP

        """
        If sound
        self.sound = pygame.mixer.Sound("xxx")
        """

        self.head['x'] = random.randint(0, self.game.numCellx - 1)
        self.head['y'] = random.randint(0, self.game.numCelly - 1)

        if self.head['x'] > self.game.numCellx / 2:
            self.direction = Direction.LEFT
        elif self.head['y'] < self.game.numCelly / 2:
            self.direction = Direction.DOWN

    def draw_snake(self):
        """Draw the snake"""

        # draw head
        rect = pygame.Rect(self.head['x'] * CELL_WIDTH, self.head['y'] * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
        pygame.draw.rect(self.game.screen, Color.GREEN.value, rect)

        # draw tail
        for x, y in self.tail:
            rect = pygame.Rect(x * CELL_WIDTH, y * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
            pygame.draw.rect(self.game.screen, Color.DARK_GREEN.value, rect)

    def move_snake(self, bGrowTail):
        # Move the snake
        if not bGrowTail:
            self.tail.pop()  # 1. remove the last element

        # add current head to tail
        self.tail.insert(0, (self.head['x'], self.head['y']))

        if self.direction == Direction.UP:
            self.head['y'] = self.head['y'] - 1
        elif self.direction == Direction.DOWN:
            self.head['y'] = self.head['y'] + 1
        elif self.direction == Direction.LEFT:
            self.head['x'] = self.head['x'] - 1
        elif self.direction == Direction.RIGHT:
            self.head['x'] = self.head['x'] + 1

    def is_head_collide_with_wall(self):
        if self.head['x'] < 0 or self.head['y'] < 0:
            return True
        elif self.head['x'] > self.game.numCellx - 1 or self.head['y'] > self.game.numCelly - 1:
            return True
        return False

    def is_head_collide_with_tail(self):
        for posX, posY in self.tail:
            if posX == self.head['x'] and posY == self.head['y']:
                return True
        return False

    def is_head_collide_with_food(self):
        return self.head['x'] == self.game.food.position['x'] and self.head['y'] == self.game.food.position['y']


class Food():
    def __init__(self, game):
        self.position = {'x': 0, 'y': 0}
        self.game = game

    def draw_food(self):
        rect = pygame.Rect(self.position['x'] * CELL_WIDTH, self.position['y'] * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
        pygame.draw.rect(self.game.screen, Color.RED.value, rect)

    def change_position(self):
        x, y = random.randint(0, self.game.numCellx - 1), random.randint(0, self.game.numCelly - 1)

        # x, y cannot be the head or tail
        while self.game.snake.is_position_find_in_head_or_tail(x, y):
             x, y = random.randint(0, self.game.numCellx-1), random.randint(0, self.game.numCelly-1)

        self.position['x'] = x
        self.position['y'] = y
        print(f'x: {x}, {y}')


class Game():
    def __init__(self, screenWidth, screenHeight):
        # initialize
        pygame.init()
        pygame.display.set_caption("~~Snake Game~~")
        self.score = 0
        self.level = 0
        self.bGameOver = False
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        # self.screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
        self.background = pygame.Surface((screenWidth, screenHeight))
        self.background.fill(Color.BLACK.value)

        self.numCellx = int(screenWidth / CELL_WIDTH)
        self.numCelly = int(screenHeight / CELL_WIDTH)

        # TODO: complete the initialization here
        self.food = Food(self)
        self.snake = Snake(self)
        self.messageBoard = Message(self.screen)

    def restart_game(self):
        self.score = 0
        self.level = 0
        self.bGameOver = False
        self.food.change_position()
        self.snake = Snake(self)

    def run_game(self):

        clock = pygame.time.Clock()

        self.bGameOver = False

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bGameOver:
                        self.restart_game()

                    if not self.bGameOver:
                        # Up
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            if self.snake.direction != Direction.DOWN:
                                self.snake.direction = Direction.UP
                        # Left
                        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            if self.snake.direction != Direction.RIGHT:
                                self.snake.direction = Direction.LEFT
                        # Down
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            if self.snake.direction != Direction.UP:
                                self.snake.direction = Direction.DOWN
                        # Right
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            if self.snake.direction != Direction.LEFT:
                                self.snake.direction = Direction.RIGHT

                    else:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            self.restart_game()

            # Check Game Over
            if self.bGameOver == False and (
                    self.snake.is_head_collide_with_wall() or self.snake.is_head_collide_with_tail()):
                self.bGameOver = True

            # Eat food
            bGrowTail = False
            if self.snake.is_head_collide_with_food():
                bGrowTail = True
                self.score = self.score + 100
                self.level = self.level + 1
                self.food.change_position()
            # Rendering
            self.screen.blit(self.background, (0, 0))
            self.draw_board()
            self.food.draw_food()

            # Game logic
            if not self.bGameOver:
                self.snake.move_snake(bGrowTail)
                self.snake.draw_snake()
            else:
                self.snake.draw_snake()
                self.messageBoard.draw_message("Game Over")

            # show score
            self.messageBoard.draw_score(f"{self.score}")

            clock.tick(10 + self.level)  # FPS difficulty

            pygame.display.flip()
            # pygame.display.update()

    def draw_board(self):
        """Draw the game board"""

        #for x in range(self.numCellx):
        #    for y in range(self.numCelly):
        #        rect = pygame.Rect(x * CELL_WIDTH, y * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
        #        pygame.draw.rect(self.screen, Color.WHITE.value, rect, 1)

        pass


Game(800, 600).run_game()

