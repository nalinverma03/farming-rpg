import pygame
from game import Game

game = Game()

running = True
while running:
  running = game.update()
    
pygame.quit()