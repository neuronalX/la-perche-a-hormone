import pygame
import time
from pygame import locals as pg_locals

import games

pygame.init()
pygame.mixer.init()

X = 1366
Y = 768

window = pygame.display.set_mode((X,Y))


game = games.Game(window=window)

while game.looping:
	pygame.time.Clock().tick(30)
	pygame.display.flip()
	game.events = pygame.event.get()
	game.loop()
	game.draw()

	for event in game.events:
		if event.type == pg_locals.QUIT or (event.type == pg_locals.KEYDOWN and event.key == pg_locals.K_ESCAPE):
			game.looping = False		

