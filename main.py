# Main program for running the snake game. Taken from https://www.youtube.com/playlist?list=PLeo1K3hjS3usVcPj6osMx1tNkARllcRhZ
# by a YouTube channel "codebasics"

import random
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
        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        pygame.display.set_caption("Snake")
        
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

        self.tick_time = 3
        

    def is_collision(self, x1, y1, x2, y2) -> bool:
        if x1 == x2 and y1 == y2:
            return True
        return False
    
    def play_background_music(self) -> None:
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound) -> None:
        pygame.mixer.Sound(f"resources/{sound}.mp3").play()
    
    def render_background(self) -> None:
        bg = pygame.image.load("resources/background.jpg").convert()
        self.surface.blit(bg, (0, 0))
    
    def play(self) -> None:
        self.render_background()
        self.snake.walk()

        # Snake colliding with the apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.tick_time += 1
            self.apple.move()
        self.apple.draw()
        self.display_score()

        # Snake going out of the map
        if self.snake.x[0] < 0 or self.snake.x[0] >= SCREEN_SIZE_X or self.snake.y[0] < 0 or self.snake.y[0] >= SCREEN_SIZE_Y:
            self.play_sound("crash")
            raise "Game Over!"

        # Snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over!"
        

    
    def display_score(self) -> None:
        font = pygame.font.SysFont('arial', 30)
        text = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(text, (800, 10))
        pygame.display.flip()

    def show_game_over_message(self) -> None:
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        text1 = font.render(f"Game Over! Your Score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(text1, (200, 300))
        text2 = font.render(f"To play again, press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(text2, (200, 350))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self) -> None:
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)

    def run(self) -> None:
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # Escape key for quitting the game
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pause = False
                        self.play_background_music()

                    # Movement keys for the snake. Snake can not turn 180 degrees instantly
                    if event.key == K_UP and self.snake.direction != "down":
                        self.snake.move_up()
                    elif event.key == K_DOWN and self.snake.direction!= "up":
                        self.snake.move_down()
                    elif event.key == K_LEFT and self.snake.direction!= "right":
                        self.snake.move_left()
                    elif event.key == K_RIGHT and self.snake.direction!= "left":
                        self.snake.move_right()
                    
                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over_message()
                pause = True
                self.reset()

            pygame.time.Clock().tick(self.tick_time)

                
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
