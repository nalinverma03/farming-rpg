import pygame
from player import Player

pygame.init()

# Game consts
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

DOWN = 0
UP = 1
LEFT = 2
RIGHT = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
player = Player()

running = True
while running:
  # Run game at 60 FPS
  clock.tick(60)
  
  screen.fill((255,255,255))

  key = pygame.key.get_pressed()
  if key[pygame.K_DOWN] == True:
    player.move(DOWN)
  if key[pygame.K_UP] == True:
    player.move(UP)
  if key[pygame.K_LEFT] == True:
    player.move(LEFT)
  if key[pygame.K_RIGHT] == True:
    player.move(RIGHT)

  if (key[pygame.K_DOWN] == False and key[pygame.K_DOWN] == False and 
      key[pygame.K_DOWN] == False and key[pygame.K_DOWN] == False ):
    player.stop_move()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  player.draw(screen)

  pygame.display.flip()
    
pygame.quit()