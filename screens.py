import pygame
import sprites
import random
from pygame import locals as pg_locals

class Screen(object):
	def __init__(self,game,background):
		self.game = game
		self.background = pygame.image.load(background).convert()
		self.sprites = {}

	def loop(self):
		for s in self.sprites.values():
			s.step()

	def blit(self,*args,**kwargs):
		return self.game.window.blit(*args,**kwargs)

	def draw(self):
		self.blit(self.background,(0,0))
		for s in self.sprites.values():
			s.blit()
			#if s.visible:
			#	if s.img is not None:
			#		self.blit(s.img,(s.X,s.Y))

	def activate(self):
		pass

	def deactivate(self):
		pass

class SplashScreen(Screen):
	def loop(self):
		for event in self.game.events:
			if event.type == pg_locals.MOUSEBUTTONUP and event.button == 1:
				self.game.action = {'action':'next'}

class HomeScreen(Screen):
	def __init__(self,game):
		Screen.__init__(self,game=game,background='images/home.png')
		s = sprites.Button(screen=self,img='images/blih.png',action={'action':'enter_level','timer':5},img_pushed='images/blah.png')
		s.activate()
		s.show()
		self.sprites['start_button'] = s

	def loop(self):
		Screen.loop(self)

	def draw(self):
		Screen.draw(self)


class LevelScreen(Screen):
	def __init__(self,game):
		Screen.__init__(self,game=game,background='include/Screens/bassins.png')
		#s = sprites.Button(screen=self,img='images/blih.png',action={'action':'return_home','timer':5},img_pushed='images/blah.png',X=50,Y=100)
		#s.activate()
		#s.show()
		#self.sprites['home_button'] = s
		
		s = sprites.Button(screen=self,img='images/blih.png',sound='include/Audio/BipInterface.wav',action={'action':'launch_fish','timer':5},img_pushed='images/blah.png',X=50,Y=100)
		s.activate()
		s.show()
		self.sprites['run_button'] = s
		
		s = sprites.Button(screen=self,img='images/blih.png',sound='include/Audio/BipInterface.wav',action={'action':'add_dep1','timer':5},img_pushed='images/blah.png',X=50,Y=100)
		s.activate()
		s.show()
		self.sprites['dep1_button'] = s
		
		s = sprites.Button(screen=self,img='images/blih.png',action={'action':'add_dep2','timer':5},img_pushed='images/blah.png',X=50,Y=100)
		s.activate()
		s.show()
		self.sprites['dep2_button'] = s
		
		s = sprites.Button(screen=self,img='images/blih.png',action={'action':'add_dep3','timer':5},img_pushed='images/blah.png',X=50,Y=100)
		s.activate()
		s.show()
		self.sprites['dep3_button'] = s

		self.polluants = [0,0,0]
		self.depolluants = [0,0,0]

	def loop(self):
		Screen.loop(self)

	def draw(self):
		Screen.draw(self)

	def activate(self):
		if self.game.level == 0:
			self.polluants = [0,0,random.choice(range(1,3))]
		elif self.game.level == 1:
			self.polluants = [0,random.choice(range(1,3)),random.choice(range(4))]
		elif self.game.level == 2:
			self.polluants = [random.choice(range(1,3)),0,random.choice(range(4))]
		else:
			self.polluants = [random.choice(range(4)),random.choice(range(4)),random.choice(range(4))]
		self.sprites['run_button'].activate()
		if self.game.available_depolluants[0] > 0 and self.depolluants[0]<3:
			self.sprites['dep1_button'].activate()
		else:
			self.sprites['dep1_button'].deactivate()

		if self.game.available_depolluants[1] > 0 and self.depolluants[1]<3:
			self.sprites['dep2_button'].activate()
		else:
			self.sprites['dep2_button'].deactivate()
		if self.game.available_depolluants[2] > 0 and self.depolluants[2]<3:
			self.sprites['dep3_button'].activate()
		else:
			self.sprites['dep3_button'].deactivate()
