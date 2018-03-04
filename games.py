import pygame
import screens
import mechanisms
import sprites

from pygame import locals as pg_locals

class Game(object):
	def __init__(self,window):
		self.looping = True
		self.window = window
		self.splash_screen = screens.SplashScreen(game=self,background='include/Screens/splash 2.png')
		self.intro_screen = screens.SplashScreen(game=self,background='include/Screens/intro.png')
		self.home_screen = screens.HomeScreen(game=self)
		self.level_screen = screens.LevelScreen(game=self)
		self.active_screen = self.splash_screen
		self.timer = 0
		self.action = None

		self.available_fish = 10
		self.available_depolluants = [10,10,10]

		self.level = 0
		self.level_end = 4

	def loop(self):
		#for event in self.events:
		#	if event.type == pg_locals.KEYDOWN:
		#		if event.key == pg_locals.K_DOWN:
		#			print('blah')
		#	elif event.type == pg_locals.MOUSEBUTTONDOWN:
		#		print(event)
		#	elif event.type == pg_locals.MOUSEBUTTONUP:
		#		print(event)
		#	else:
		#		pass 

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
			if self.action['action'] == 'next':
				if self.active_screen == self.splash_screen:
					self.active_screen = self.intro_screen
				elif self.active_screen == self.intro_screen:
					self.active_screen = self.home_screen
			elif self.action['action'] == 'return_home':
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
					self.create_fish()
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

	def create_fish(self):
		for k in range(10):
			if k < 5:
				gender = 'male'
			else:
				gender = 'femelle'
			end_status = mechanisms.change_sex_or_die(gender=gender,polluants=self.active_screen.polluants,depolluants=self.active_screen.depolluants)
			self.active_screen.sprites['fish'+str(k)] = sprites.Fish(screen=self.active_screen,scale=0.5,k=k,gender=gender,end_status=end_status)