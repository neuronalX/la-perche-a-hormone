import pygame
import sprites

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
			if s.visible:
				if s.img is not None:
					self.blit(s.img,(s.X,s.Y))

	def activate(self):
		pass

	def deactivate(self):
		pass


class HomeScreen(Screen):
	def __init__(self,game):
		Screen.__init__(self,game=game,background='images/home.png')
		s = sprites.Button(screen=self,img='images/blih.png',action={'action':'enter_level','timer':30},img_pushed='images/blah.png')
		s.activate()
		s.show()
		self.sprites['start_button'] = s

	def loop(self):
		Screen.loop(self)

	def draw(self):
		Screen.draw(self)


class LevelScreen(Screen):
	def __init__(self,game):
		Screen.__init__(self,game=game,background='images/level.jpg')
		s = sprites.Button(screen=self,img='images/blih.png',action={'action':'return_home','timer':30},img_pushed='images/blah.png',X=50,Y=100)
		s.activate()
		s.show()
		self.sprites['home_button'] = s
		self.polluants = [0,0,0]
		self.depolluants = [0,0,0]

	def loop(self):
		Screen.loop(self)

	def draw(self):
		Screen.draw(self)

	def activate(self):
		self.polluants = [random.choice(range(4)),random.choice(range(4)),random.choice(range(4))]