from tkinter import W
import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont("Arial", 30)

class Direction(Enum):
    UP = 3
    DOWN = 4
    LEFT = 2
    RIGHT = 1

Point = namedtuple('Point', 'x, y')

BLOCK_SIZE = 20
SPEED = 5
class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(w // 2, h // 2)
        self.snake = [self.head, 
                        Point(self.head.x-BLOCK_SIZE, self.head.y), 
                        Point(self.head.x-2*BLOCK_SIZE, self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
    
    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
            

    def play_step(self):
        # 1. collect events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = Direction.UP
            
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
            
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
        # 2. move
        self._move(self.direction) # move snake head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move snake
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        game_over = False
        return game_over, self.score

    def _is_collision(self):
        # check if snake hits border
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True

        # check if snake hits itself
        if self.head in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill((0, 0, 0))

        for point in self.snake:
            pygame.draw.rect(self.display, (0, 0, 255), (point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, (0, 100, 255), (point.x+4, point.y+4, 12, 12))

        pygame.draw.rect(self.display, (255, 0, 0), (self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render('Score:' + str(self.score), True, (255, 255, 255))
        self.display.blit(text, (0, 0))
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.RIGHT:
            x += BLOCK_SIZE

        self.head = Point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()