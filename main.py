# Main program for running the snake game. Taken from https://www.youtube.com/playlist?list=PLeo1K3hjS3usVcPj6osMx1tNkARllcRhZ
# by a YouTube channel "codebasics"


import time
import pygame
from pygame.locals import *

SIZE = 40

class Snake:
    def __init__(self, parent_screen, length) -> None:
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.parent_screen = parent_screen
        self.direction = "down"
    
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

        for i in range(self.length-1, 0, -1):
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
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill((110, 110, 5))
        pygame.display.set_caption("Snake")
        self.snake = Snake(self.surface, 6)
        self.snake.draw()

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
            
            self.snake.walk()
            time.sleep(0.3)
                
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
