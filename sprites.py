import copy
import pygame
from pygame import locals as pg_locals
import math

class Sprite(object):
	def __init__(self,screen,img,X=0,Y=0,action={},img_deact=None,scale=1.):
		self.X = X
		self.Y = Y
		self.scale = scale
		self.active = False
		self.visible = True
		self.screen = screen
		if img is not None:
			self.img = pygame.image.load(img).convert()
		else:
			self.img = None
		self.img_orig = self.img
		if img_deact is not None:
			self.img_deact = pygame.image.load(img_deact).convert()
		else:
			self.img_deact = self.img
		self.do_action = False
		self.action = copy.deepcopy(action)

	def step(self):
		pass

	def hide(self):
		self.visible = False
		
	def show(self):
		self.visible = True

	def activate(self):
		self.active = True
		self.img = self.img_orig
	
	def deactivate(self):
		self.active = False
		self.img = self.img_deact
		if hasattr(self,sound) and self.sound is not None:
			self.sound.stop()

	def blit(self):
		if self.visible and self.img is not None:
			dX = self.img.get_width()
			dY = self.img.get_height()
			dx = math.floor(dX*self.scale)
			dy = math.floor(dY*self.scale)
			x = self.X+(dX-dx)/2
			y = self.Y+(dY-dy)/2
			img_resized = pygame.transform.scale(self.img, (dx, dy))
			self.screen.blit(img_resized,(x,y))  

class Popup(Sprite):
	def  __init__(self,screen,img,X=0,Y=0,action={},sound=None,img_deact=None,scale=1.):
		Sprite.__init__(self,screen=screen,img=img,X=X,Y=Y,action=copy.deepcopy(action),img_deact=img_deact,scale=scale)
		if sound is None:
			self.sound = None
		else:
			self.sound = pygame.mixer.Sound(sound)
		self.sound_played = False

	def step(self):
		if self.sound is not None and not self.sound_played:
			self.sound.play()
		self.sound_played = True


class Button(Sprite):
	def __init__(self,screen,img,X=0,Y=0,action={},img_pushed=None,sound=None,img_deact=None,scale=1.):
		Sprite.__init__(self,screen=screen,img=img,X=X,Y=Y,action=copy.deepcopy(action),img_deact=img_deact,scale=scale)
		self.pushed = False
		if img_pushed is None:
			self.img_pushed = self.img
		else:
			self.img_pushed = pygame.image.load(img_pushed).convert()
		if sound is None:
			self.sound = None
		else:
			self.sound = pygame.mixer.Sound(sound)




	def push(self):
		if not self.pushed: 
			self.pushed = True
			self.push_action()

	def release(self):
		self.pushed = False
		self.release_action()

	def push_action(self):
		tempimg = self.img
		self.img = self.img_pushed
		if self.sound is not None:
			self.sound.play()

	def release_action(self):
		self.img = self.img_orig
		self.do_action = True

	def step(self):
		if self.visible and self.active:
			for event in self.screen.game.events:
				if event.type == pg_locals.MOUSEBUTTONDOWN and event.button == 1:
					pos = pygame.mouse.get_pos()
					xx = pos[0]
					yy = pos[1]
					if self.X <= xx <= self.X + self.img.get_size()[0] and self.Y <= yy <= self.Y + self.img.get_size()[1]:
						self.push()
				if event.type == pg_locals.MOUSEBUTTONUP and event.button == 1 and self.pushed:
					self.release()

class TextZone(Sprite):

	def __init__(self,screen,img,X=0,Y=0,action={},img_deact=None,scale=1.):
		Sprite.__init__(self,screen=screen,img=None,X=X,Y=Y,action=copy.deepcopy(action),img_deact=img_deact,scale=scale)
		self.font = pygame.font.SysFont("monospace", 15)
		self.img = self.font.render(img, 1, (255,255,0))



class TextVar(TextZone):
	
	def __init__(self,screen,img,X=0,Y=0,action={},img_deact=None,scale=1.):
		Sprite.__init__(self,screen=screen,img=None,X=X,Y=Y,action=copy.deepcopy(action),img_deact=img_deact,scale=scale)
		self.font = pygame.font.SysFont("monospace", 15)
		self.var = img
		self.img = self.font.render(getattr(self.screen.game,self.var), 1, (255,255,0))

	def step(self):
		self.img = self.font.render(getattr(self.screen.game,self.var), 1, (255,255,0))

class MovingElt(Sprite):	
	def __init__(self,screen,img,X=0,Y=0,action={},transition=10,loop_img=True,img_deact=None,sound=None,sound_transition=60,scale=1.):
		Sprite.__init__(self,screen=screen,img=None,X=X,Y=Y,action=copy.deepcopy(action),img_deact=img_deact,scale=scale)
		self.transition = transition
		self.loop_img = loop_img
		if sound is None:
			self.sound = None
		else:
			self.sound = pygame.mixer.Sound(sound)
		self.sound_transition = sound_transition
		if isinstance(img,list):
			self.img_seq = [pygame.image.load(im).convert() for im in img]
		else:
			self.img_seq = [pygame.image.load(img).convert()]
		self.img_index = 0
		self.img = self.img_seq[self.img_index]
		self.counter_transition = 0
		self.counter_sound = 0

	def step(self):
		if self.counter_transition == self.transition:
			self.img_index += 1
			self.img_index = min(self.img_index,len(self.img_seq)-1)
			self.img = self.img_seq[self.img_index]
			self.counter_transition = 0
		else:
			self.counter_transition += 1
		if self.counter_sound == self.sound_transition:
			if self.sound is not None:
				self.sound.play()
		else:
			self.counter_sound += 1
		self.move()

	def move(self):
		pass

class Fish(MovingElt):
	def __init__(self,k=0,loop_img=False,gender='female',end_status='female',*args,**kwargs):
		self.Xmin = 100
		self.dy = 50
		self.Tmax = 150
		Y = 100 + k*dy
		transition = random.choice(range(self.Tmax))
		self.start_img = 'images/poissons/'+gender+'.png'
		self.end_img = 'images/poissons/'+end_status+'.png'
		self.Xmax = 1000
		if k == 0:
			sound = 'sounds/fish.mp3'
			sound_transition = 40
		MovingElt.__init__(self,loop_img=loop_img,img=[self.start_img,self.end_img],transition=transition,X=self.Xmin,Y=Y,*args,**kwargs)

	def move(self):
		if self.end_img != 'images/poissons/dead.png' or self.img != self.img_seq[-1]:
			dx = (self.Xmax-self.Xmin)/self.Tmax
			self.X += dx
			dy = random.choice(range(5))-2
			self.Y += dy


