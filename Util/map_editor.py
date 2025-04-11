from pygame import *
import sys,pygame,os
FONT='space_invaders.ttf'
color=[(255,177,32),(116,116,116),(132,132,132),(15,149,0),(120,74,50)
,(255,177,32),(129,87,41),(255,177,32),(255,177,32),(255,177,32),
(240,20,20),(255,177,32),(255,177,32),(255,177,32)]
class Base(sprite.Sprite):
	def __init__(self,x,y,tipe):
		sprite.Sprite.__init__(self)
		self.image,self.tile=pygame.Surface((5,5)),color[tipe-1]
		self.x,self.y=(x/5),(y/5)
		self.color,self.rect=False,self.image.get_rect(topleft=(x,y))
	def update(self,sup,zoom):
		self.image=pygame.Surface((zoom,zoom))
		self.rect=self.image.get_rect()
		if self.color:
			self.image.fill((220,40,55))
			self.color=False
		else:
			self.image.fill(self.tile)
		self.rect.left=int(self.x*zoom+500)
		self.rect.top=int(self.y*zoom+300)
		sup.blit(self.image,self.rect)
class BaseGroup(sprite.Group):
	def __init__(self):
		sprite.Group.__init__(self)
		self.l=[]
	def list(self):
		l=[]
		for tile in self:
			l.append(tile.rect.right)
		self.max=max(l)
		a=[]
		for tile in self:
			a.append(tile.rect.top)
		self.may=max(a)
class Punte(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image=pygame.Surface((5,5))
		self.image.fill((250,230,230))
		self.rect=self.image.get_rect(topleft=(500,300))
	def update(self,sup,x,y):
		self.rect.center=(x,y)
		sup.blit(self.image,self.rect)
class Text(object):
    def __init__(self,textFont,size,message,color,xpos,ypos):
        self.font=font.Font(textFont,size)
        self.surface=self.font.render(message,True,color)
        self.rect=self.surface.get_rect(topleft=(xpos,ypos))
    def update(self,sup):
        sup.blit(self.surface,self.rect)   
class Game(object):
	def __init__(self):
		mixer.pre_init(44100,-16,1,4096)
		init()
		self.frame=pygame.time.Clock()
		self.screen=display.set_mode((1000,600))	
		self.startgame,self.keys=1,key.get_pressed()
		self.level,self.scroll=1,[500,300]
		self.zoom,self.punt=5,Punte()
		self.primGroup=sprite.Group(self.punt)
	def newlevel(self,l):
		self.mapt(l)
		self.allGroup=sprite.Group(self.baseGroup)
	def bitmap(self,n):
		f=open("mapa"+str(n)+".txt",'r')
		data=f.read()
		f.close()
		data,gamemap=data.split('\n'),[]
		for row in data:
			line=str(row)
			line=line.split(' ')
			gamemap.append(list(line))
		return gamemap
	def mapt(self,n):
		y,lis,DGroup=100,self.bitmap(n),BaseGroup()
		for i in range(len(lis)):
			y+=5
			for n in (lis[i]):
				bit=list(map(str,str(n)))
				if i>0:
					if len(bit)>2:	
						x=(int(bit[0]+bit[1],16))*5
						try:
							ex=(int(bit[3]+bit[4],16))
						except:
							ex=1
						try:
							ey=(int(bit[5]+bit[6],16))
						except:
							try:
								ey=(int(bit[5],16))
							except:
								ey=1
						for d in range(ex):
							for e in range(ey):
								tile=Base(x+d*5,y+e*5,(int(bit[2],16)))
								DGroup.add(tile)
		self.baseGroup=DGroup
	def input(self):
		self.keys=key.get_pressed()
		for event in pygame.event.get():
			if event.type==KEYUP:
				if self.keys[K_q]:
					self.level-=1
					self.newlevel(self.level)
				elif self.keys[K_e]:
					self.level+=1
					self.newlevel(self.level)
			if event.type==pygame.QUIT:
				self.startgame=False
				pygame.quit()
		if self.keys[K_RIGHT]:
			for tile in self.allGroup:
				tile.x-=1
		elif self.keys[K_LEFT]:
			for tile in self.allGroup:
				tile.x+=1
		elif self.keys[K_UP]:
			for tile in self.allGroup:
				tile.y+=1
		elif self.keys[K_DOWN]:
			for tile in self.allGroup:
				tile.y-=1
		elif self.keys[K_a]:
			if self.zoom<=25:
				self.zoom+=1
		elif self.keys[K_d]:
			if self.zoom>=4:
				self.zoom-=1
	def collisions(self):
		for tile in sprite.groupcollide(self.allGroup,
			self.primGroup,False,False):
				tile.color=True
	def Act(self):
		self.newlevel(self.level)
		self.baseGroup.list()
		self.textlevel=Text(FONT,20,'NIVEL '+str(self.level),(10,20,20),30,8)
		self.textlong=Text(FONT,20,'LONGITUD: '+str(self.baseGroup.max),(10,20,20),400,8)
		self.textalt=Text(FONT,20,'ALTURA: '+str(self.baseGroup.may),(10,20,20),800,8)
		while self.startgame:
			self.frame.tick(60)
			self.collisions()
			self.screen.fill((180,180,250))
			for eve in pygame.event.get():
				if eve.type == quit:
					pygame.quit()
					sys.exit()	
			if self.startgame:
				self.textlevel.update(self.screen)
				self.textlong.update(self.screen)
				self.textalt.update(self.screen)
				x,y=pygame.mouse.get_pos()
				self.punt.update(self.screen,x,y)
			self.allGroup.update(self.screen,self.zoom)
			display.update()
			self.input()								
if __name__=='__main__':
    game=Game()
    game.Act()
