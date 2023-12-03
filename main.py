# Main program for running the snake game. Taken from https://www.youtube.com/playlist?list=PLeo1K3hjS3usVcPj6osMx1tNkARllcRhZ
# by a YouTube channel "codebasics"

import random
import time
import pygame
from pygame.locals import *

SIZE = 40
SCREEN_SIZE_X, SCREEN_SIZE_Y = 1000, 800


class Apple:
    def __init__(self, parent_screen) -> None:
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3
    
    def draw(self) -> None:
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    
    # Move the apple to a random position
    def move(self) -> None:
        self.x = random.randint(0, (SCREEN_SIZE_X // SIZE) - 1) * SIZE
        self.y = random.randint(0, (SCREEN_SIZE_Y // SIZE) - 1) * SIZE
        self.draw()

class Snake:
    def __init__(self, parent_screen, length) -> None:
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.parent_screen = parent_screen
        self.direction = "down"
    
    # Increase the length of the snake 
    def increase_length(self) -> None:
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def move_up(self) -> None:
        self.direction = "up"
    
    def move_down(self) -> None:
        self.direction = "down"
    
    def move_left(self) -> None:
        self.direction = "left"
    
    def move_right(self) -> None:
        self.direction = "right"
    
    def draw(self) -> None:
        self.parent_screen.fill((110, 110, 5))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    
    def walk(self) -> None:

        for i in range(self.length-1, 0, -1): # Move every block of the snake
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "down":
            self.y[0] += SIZE
        elif self.direction == "up":
            self.y[0] -= SIZE
        elif self.direction == "left":
            self.x[0] -= SIZE
        elif self.direction == "right":
            self.x[0] += SIZE
        
        self.draw()


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.surface.fill((110, 110, 5))
        pygame.display.set_caption("Snake")
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        
    
    def is_collision(self, x1, y1, x2, y2) -> bool:
        if x1 == x2 and y1 == y2:
            return True
        return False
    
    def play(self) -> None:
        self.snake.walk()
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
        self.apple.draw()
        self.display_score()
    
    def display_score(self) -> None:
        font = pygame.font.SysFont('arial', 30)
        text = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(text, (800, 10))
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Escape key for quitting the game
                    if event.key == K_ESCAPE:
                        running = False
                    
                    # Movement keys for the snake
                    if event.key == K_UP:
                        self.snake.move_up()
                    elif event.key == K_DOWN:
                        self.snake.move_down()
                    elif event.key == K_LEFT:
                        self.snake.move_left()
                    elif event.key == K_RIGHT:
                        self.snake.move_right()
                    
                elif event.type == QUIT:
                    running = False
            
            self.play()

            time.sleep(.2)
                
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
