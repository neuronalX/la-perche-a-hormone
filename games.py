import pygame
import screens

from pygame import locals as pg_locals

class Game(object):
	def __init__(self,window):
		self.looping = True
		self.window = window
		self.home_screen = screens.HomeScreen(game=self)
		self.level_screen = screens.LevelScreen(game=self)
		self.active_screen = self.home_screen
		self.timer = 0
		self.action = None

		self.available_fish = 10
		self.available_depolluants = [10,10,10]

		self.level = 0
		self.level_end = 4

	def loop(self):
		for event in self.events:
			if event.type == pg_locals.KEYDOWN:
				if event.key == pg_locals.K_DOWN:
					print('blah')
			elif event.type == pg_locals.MOUSEBUTTONDOWN:
				print(event)
			elif event.type == pg_locals.MOUSEBUTTONUP:
				print(event)
			else:
				pass 

		self.active_screen.loop()

		self.do_action()
		for s in self.active_screen.sprites.values():
			if self.action is None and s.do_action:
				self.action = s.action
				s.do_action = False
				if 'timer' in s.action.keys():
					self.timer = s.action['timer']

	def draw(self):
		self.active_screen.draw()

	def do_action(self):
		if self.timer == 0 and self.action is not None:
			if self.action['action'] == 'return_home':
				if self.active_screen != self.home_screen:
					self.active_screen.deactivate()
					self.active_screen = self.home_screen
					self.active_screen.activate()
			elif self.action['action'] == 'enter_level':
				if self.active_screen != self.level_screen:
					self.active_screen.deactivate()
					self.active_screen = self.level_screen
					self.active_screen.activate()
			elif self.action['action'] == 'launch_fish':
				self.available_fish -= 1
				if self.active_screen.__class__ == screens.LevelScreen:
					for s in self.active_screen.sprites.values():
						if s.visible:
							s.deactivate()
			elif self.action['action'] == 'add_element':
				if self.active_screen.__class__ == screens.LevelScreen:
					getattr(self,'add_'+self.action['element'])()
			elif self.action['action'] == 'substract_element':
				if self.active_screen.__class__ == screens.LevelScreen:
					getattr(self,'substract_'+self.action['element'])()

			self.action = None
		elif self.timer > 0:
			self.timer -= 1
			print(self.timer)


