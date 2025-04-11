from pygame import *
import sys,pygame,os
FONT='space_invaders.ttf'
color=[(250,20,20),(20,250,20),(20,20,250),(250,250,20),(250,20,250)
,(10,10,10),(100,100,100)]
class SpriteSheet:
	def __init__(self):
		self.sheet=pygame.image.load('r1.png').convert()
	def image_at(self,x,y,w,h):	
		rect=pygame.Rect(x,y,w,h)		
		image=pygame.Surface(rect.size).convert()
		image.blit(self.sheet,(0,0),rect)
		image.set_colorkey((255,0,255), pygame.RLEACCEL)				
		return image
def Color(image,color):
	image=image.copy()
	image.fill((100,100,100),None,BLEND_RGBA_MULT)
	image.fill(color[0:3]+(0,),None,BLEND_RGBA_ADD)
	return image
def Frame(cicle,total,start,rate):
	if start[0]==rate:
		if cicle:
			if start[1]>=total:
				start[1]=0
			else:
				start[1]+=1
		else:
			if start[1]<total:
				start[1]+=1
		start[0]=0
	start[0]+=1
	return start	

class Rhe(sprite.Sprite):
	def __init__(self,pos,py,group):
		sprite.Sprite.__init__(self)
		self.image,self.group=Surface((13,16)),group
		self.rect,self.enter=self.image.get_rect(topleft=(pos)),0
		self.y,self.x,self.max,self.maj,self.jump=0,0,4,-5,0
		self.may,self.walljump,self.der,self.izq,self.pyr=7,0,1,1,py
		self.t=[0,0,0]
		self.st=0
		self.at=0
		self.d=0
	def dspy(self,sup):
		sup.blit(self.image,self.rect)
	def move(self,scroll):
		self.rect.y+=round(self.y)-round(scroll[1])
		self.rect.x+=round(self.x)-round(scroll[0])	
	def update(self,keys):
		if self.at!=self.st:
			self.t=[0,0,0]
		if not self.st:
			self.t=Frame(1,7,self.t,6)
		if self.st==1:
			self.t=Frame(1,7,self.t,5)
		if self.st==2:
			self.t=Frame(0,4,self.t,3)
		if self.st==3:
			self.t=Frame(0,7,self.t,5)
		if self.st==4:
			self.t=Frame(1,7,self.t,4)
		self.at=self.st
		self.image=SpriteSheet().image_at(((13*self.t[1])),15*self.st,13,15)
		self.image=transform.flip(self.image,self.d,0)
		if self.jump:
			if keys[2]:
				self.d=0
				if self.der:
					self.st=1
				else:
					self.st=4
			elif keys[3]:
				self.d=1
				if self.izq:
					self.st=1
				else:
					self.st=4
			else:
				self.st=0
		else:
			if self.y<0:
				self.st=2
			else:
				self.st=3
		if keys[2]and self.der:
			if self.x>=self.max:
				self.x=self.max
			else:
				if self.jump:
					self.x+=.4
				else:
					self.x+=.25
		if keys[3] and self.izq:
			if self.x<=-self.max:
				self.x=-self.max
			else:
				if self.jump:
					self.x-=.4
				else:
					self.x-=.25
		if not(keys[3]or keys[2])and self.x and self.jump:
			self.x*=.7 
		if keys[0]:
			if self.jump:
				self.y=(self.maj-abs(self.x/6))
			if self.walljump:
				if keys[2]and not self.izq:
					Walljump(0,self.rect.topleft,self.group)
					self.y,self.x=-5,3
					self.d=0
				if keys[3]and not self.der:
					Walljump(1,self.rect.topleft,self.group)
					self.y,self.x=-5,-3
					self.d=1
		if self.y>=self.may:
			self.y=self.may
		else:
			if keys[1]:
				self.y+=.4
			else:
				self.y+=.2	
		if keys[8]and not self.enter:
				self.enter=1
class Walljump(sprite.Sprite):
	def __init__(self,d,pos,*groups):
		super(Walljump, self).__init__(*groups)
		self.t,self.d,self.image=0,d,image.load("wj1.png")
		self.image=transform.flip(self.image,d,0)
		self.rect=self.image.get_rect(topleft=(pos[0]-10*d,pos[1]))
	def dspy(self,sup):
		sup.blit(self.image,self.rect)
	def move(self,scroll,*args):
		self.t+=1
		self.image=image.load("wj"+str(self.t)+".png")
		self.image=transform.flip(self.image,self.d,0)
		self.rect.x-=round(scroll[0])
		self.rect.y-=round(scroll[1])
		if self.t>7:
			self.kill()					
class Tile(sprite.Sprite):
	def __init__(self,x,y,tipe):
		sprite.Sprite.__init__(self)
		self.image=image.load("tile"+str(tipe)+".png")
		self.rect=self.image.get_rect(topleft=(x,y))
	def dspy(self,sup):
		sup.blit(self.image,self.rect)
	def move(self,scroll,*args):
		self.rect.x-=round(scroll[0])
		self.rect.y-=round(scroll[1])
class Meta(sprite.Sprite):
	def __init__(self,x,y,l,a,tipe):
		sprite.Sprite.__init__(self)
		self.image=Surface((l,a))
		self.rect=self.image.get_rect(topleft=(x,y))
	def dspy(self,sup):
		0
		#sup.blit(self.image,self.rect)
	def move(self,scroll,*args):
		self.rect.x-=round(scroll[0])
		self.rect.y-=round(scroll[1])
class Text(object):
	def __init__(self,xpos,ypos,size,col):
		self.font=font.Font(FONT,size)
		self.image,self.c=Surface((30,30)),color[col]
		self.rect=self.image.get_rect(center=(xpos,ypos))
	def update(self,sup,text):
		self.surface=self.font.render(str(text),True,self.c)
		self.imarect=self.surface.get_rect(center=(self.rect.center))
		sup.blit(self.surface,self.imarect) 
class Scr(sprite.Sprite):
	def __init__(self,pyr,lis,grp,tip):
		super(Scr,self).__init__(grp)
		self.image=image.load('sele'+str(pyr)+'.png').convert_alpha()
		self.pos,self.r,self.selec,self.c,self.tp=[0,0],0,0,0,tip
		self.m=lis
		self.rect,self.p=self.image.get_rect(),(0,0,0)
	def update(self,sup,keys,active):
		if (not self.tp and active)or(self.tp and not self.selec):
			if self.r!=keys:
				if keys[0]:
					self.pos[1]-=1-len(self.m[self.pos
					[0]])*(not self.pos[1]+1)
				if keys[1]:
					self.pos[1]+=1-len(self.m[self.pos[0]])*(not
					self.pos[1]-(len(self.m[self.pos[0]])-1))
				if keys[2]:
					self.pos[0]+=1-len(self.m)*(not
					self.pos[0]-(len(self.m)-1))
				if keys[3]:
					self.pos[0]-=1-len(self.m)*(not self.pos[0]+1)
			try:
				self.p=self.m[self.pos[0]][self.pos[1]]
			except:
				self.pos=[0,0]
			self.c+=8-132*int(self.c/160)
			self.imag2=Color(self.image,(self.c,self.c,self.c))
		else:
			self.imag2=self.image
		if self.r!=keys:
			if keys[4]and self.tp==1:
				self.selec=not self.selec
		self.r,self.rect.topleft=keys,self.p[:2]
		sup.blit(self.imag2,self.rect)
class EnterMenu(sprite.Sprite):
	def __init__(self,pyr,li):
		sprite.Sprite.__init__(self)
		self.imag1,self.tx=pygame.transform.scale_by(image.load('paused.png'), 0.5),Text(320,190,16,5)
		self.imrect=self.imag1.get_rect(topleft=(220,70))
		self.imag2,self.key=pygame.transform.scale_by(image.load('botton.png'), 0.5),0
		self.rec2=self.imag1.get_rect(topleft=(220,122))
		self.l,self.pos,self.r,self.selec=li,[0,0],0,False
		self.g,self.a=sprite.Group(),sprite.Group()
		self.sel1,self.sel2=Scr(4,sl3,self.a,0),Scr(3,sl2,self.g,0)
		self.p,self.rec,self.start,self.ind,self.t=pyr,0,1,0,4
		self.s,self.h=0,0
	def dspy(self,sup):
		sup.blit(self.imag1,self.imrect)
		self.a.update(sup,self.h,not(self.key))
		if self.key:
			sup.blit(self.imag2,self.rec2)
			if not self.t:
				self.g.update(sup,self.h,not(self.rec)),self.tx.update(
				sup,(self.sel2.p[3],self.l[self.sel2.p[2]]))
	def update(self,keys):
		s,g=keys,inp(keys,self.l)
		self.s,self.h=s,g
		if self.r!=s and not self.t:
			if self.key and self.rec:
				for keyr in keys:
					if keyr:
						self.l[self.ind]=keys.index(keyr)
						Rewrite(self.l,self.p-1),Control()
						self.rec,self.t=0,8
			if keys[self.l[8]]and not self.rec:
				if not self.key:
					if not self.sel1.pos[0] and self.start:
						self.start=False
						self.kill()
					if self.sel1.pos[0]==1:
						self.key=1
				else:
					if not self.sel2.pos[0]:
						self.key=0
					else:
						self.rec,self.ind=1,(self.sel2.p[2])
		self.r=s
		self.t-=1*bool(self.t)
class FMenu(sprite.Sprite):
	def __init__(self,li):
		sprite.Sprite.__init__(self)
		self.t1,self.t2=Text(320,150,16,0),Text(320,210,16,1)
		self.t3,self.t4=Text(320,180,16,2),Text(320,240,16,3)
		self.key,self.g=0,sprite.Group()
		self.sel,self.l,self.pos,self.r=Scr(5,sl4,self.g,1),li,[0,0],0
		self.rec,self.start,self.ind,self.t=0,0,0,4
	def update(self,sup,keys):
		g=inp(keys,self.l)
		self.g.update(sup,g,1)
		if not self.sel.pos[0]and self.sel.selec:
			self.start=1
			self.kill()
		self.t1.update(sup,"START"),self.t2.update(sup,"NEW GAME")
		self.t3.update(sup,"KEYS"),self.t4.update(sup,"LEVEL EDIT")
def Rewrite(new,num):
	with open("control.txt",'r') as f:
		lines=f.readlines()
	with open("control.txt",'w') as f:
		for i,line in enumerate(lines,0):
			if i==num: 
				for v in new:
					f.writelines(str(v)+' ')
				f.writelines("\n")
			else:
				f.writelines(line)
	f.close()
def Control():
	with open('control.txt','r') as file:
		data = file.readlines()
	file.close()
	for row in data:
		n,row,lis=data.index(row)+1,row.split(' '),[]
		for num in row:
			try:
				lis.append(int(num))
			except:
				0
		p,globals()[p]="in"+str(n),lis
Control()
sl1=[[(336,34),(312,84),(288,134),(262,184),(240,234),(216,284)],
[(416,16),(394,66),(370,116),(346,166),(322,216),(298,266)],
[(476,48),(452,99),(428,148),(404,199),(380,248),(356,298)]]
sl2,sl3=[[(234,118,-1,'BACK')],[(232,146,3,'LEFT')],[(244,133,0
,'UP'),(243,158,1,'DOWN')],[(255,146,2,'RIGHT')],[(308,122,8,
'START')],[(359,145,4,'B')],[(373,160,5,'P'),(373,131,7,'F')],
[(387,146,6,'K')]],[[(231,101)],[(291,101)],[(351,101)]]
sl4=[[(265,141),(270,171),(248,201),(238,230)]]
def inp(keys,liskey):
	lis=[]
	for inp in liskey:
		lis.append(keys[liskey[liskey.index(inp)]])
	return lis
def Num(num):
	try:
		return num/abs(num)
	except:
		return 0
class BaseGroup(sprite.Group):
	def __init__(self):
		sprite.Group.__init__(self)
	def move(self,scroll):
		for obj in self:
			obj.move(scroll)
	def dspy(self,sup):
		for obj in self:
			obj.dspy(sup)
class Game(object):
	def __init__(self):
		mixer.pre_init(44100,-16,1,4096)
		pygame.init()
		self.screen=display.set_mode((640,360))
		self.play,self.frame=1,time.Clock()
		self.keys,self.startgame,self.start=tuple(key.get_pressed()),1,0
		self.level,self.leveltime,self.currentTime=1,0,0
	def newlevel(self,l):
		self.startscroll,self.scroll,self.fm=1,[0,0],FMenu(in1)
		self.mapt(l)
		self.time,self.effec=Text(320,20,16,5),BaseGroup()
		self.rhe=Rhe(self.spawn,1,self.effec)
		self.primGroup,self.allGroup=sprite.Group(),BaseGroup()
		self.primGroup.add(self.rhe)
		self.allGroup.add(self.baseGroup,self.metaGroup
		,self.look,self.primGroup)
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
		lis,y=self.bitmap(n),100	
		lGroup,DGroup=sprite.Group(),sprite.Group()
		KGroup,SGroup=sprite.Group(),sprite.Group()
		for i in range(len(lis)):
			y+=15
			for n in (lis[i]):
				bit=list(map(str,str(n)))
				if not i:
					self.back=(int(bit[0]+bit[1],16),int(bit[2]
					+bit[3],16),int(bit[4]+bit[5],16))
				elif i==1:
					self.spawn=(int(bit[0]+bit[1]+bit[2]
					,16)*15,int(bit[3]+bit[4]+bit[5],16)*15)
				else:
					if len(bit)>2:	
						x=(int(bit[0]+bit[1],16))*15
						try:
							ex=(int(bit[3]+bit[4],16))*15
						except:
							ex=15
						try:
							ey=(int(bit[5]+bit[6],16))*15
						except:
							try:
								ey=(int(bit[5],16))*15
							except:
								ey=15
						meta=Meta(x,y,ex,ey,(int(bit[2],16)))
						if int(bit[2],16)==11:
							DGroup.add(meta)
						elif int(bit[2],16)==12:
							KGroup.add(meta)
						else:
							lGroup.add(meta)
						for s in range(int(ex/15)):
							for f in range(int(ey/15)):	
								dsp=Tile(x+15*s,y+15*f,(int(bit[2],16)))
								SGroup.add(dsp)
		self.baseGroup,self.metaGroup,self.look=lGroup,DGroup,SGroup
		a=[]
		for tile in self.metaGroup:
			a.append(tile.rect.bottom)
		for tile in self.baseGroup:
			a.append(tile.rect.bottom)
		self.bttm=max(a)+60
	def input(self):
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				self.play=False
				pygame.quit()
	def collisions(self):
		if sprite.groupcollide(self.baseGroup,self.primGroup,0,0):
			for tile in sprite.groupcollide(self.baseGroup,
			self.primGroup,0,0):
				if (self.rhe.rect.centerx<tile.rect.right and 
				self.rhe.rect.centerx>tile.rect.left):
					if self.rhe.rect.top<tile.rect.top:
						self.rhe.jump,self.rhe.y=1,0
						self.rhe.rect.top=tile.rect.top-15
					elif (self.rhe.rect.top<=tile.rect.bottom 
					and self.rhe.y<0):
						self.rhe.rect.bottom=tile.rect.bottom+15
						self.rhe.y=0
				else:
					self.rhe.jump,self.rhe.izq,self.rhe.der=0,1,1
				if (self.rhe.rect.centery>tile.rect.top and 
				self.rhe.rect.centery<tile.rect.bottom):
					self.rhe.walljump=1
					if (self.rhe.rect.left<=tile.rect.left 
					and self.rhe.x>=0):
						self.rhe.rect.left=tile.rect.left-12
						self.rhe.der,self.rhe.x=0,0
					elif (self.rhe.rect.right>=tile.rect.right 
					and self.rhe.x<=0):
						self.rhe.rect.right=tile.rect.right+12
						self.rhe.izq,self.rhe.x=0,0
				else:
					self.rhe.walljump=0
		else:
			self.rhe.jump,self.rhe.walljump=0,0
			self.rhe.izq,self.rhe.der=1,1
		if sprite.groupcollide(self.metaGroup,self.primGroup,0,0):
			self.leveltime=self.currentTime
			self.level+=1	
			self.newlevel(self.level)		
	def Act(self):
		self.newlevel(self.level)
		while self.play:
			self.keys=tuple(key.get_pressed())
			self.frame.tick(60)
			if self.startgame:
				self.screen.fill(self.back)
				self.fm.update(self.screen,self.keys)
				if self.fm.start and self.startgame:
					self.startgame=0
				self.scroll[0]=1
				self.allGroup.move(self.scroll)
			else:
				self.screen.fill(self.back)
				if self.start:
					self.ents.update(self.keys)
					if not self.ents.start:
						self.start=0
						for each in self.primGroup:
							each.enter=0
				else:
					self.primGroup.update(inp(self.keys,in1))
					if self.startscroll:
						self.scroll=((self.rhe.rect.x-310)
						/8,(self.rhe.rect.y-180)/8)
					self.bttm-=round(self.scroll[1])
					self.currentTime+=1/60
					self.allGroup.move(self.scroll)
					self.effec.move(self.scroll)
					self.collisions()
					for each in self.primGroup:
						if each.rect.bottom>self.bttm:
							self.newlevel(self.level)
						if each.enter and not self.start:
							self.start,self.ents=1,EnterMenu(
							each.pyr,eval('in'+str(each.pyr)))
							self.allGroup.add(self.ents)
			self.allGroup.dspy(self.screen)
			self.effec.dspy(self.screen)
			self.time.update(self.screen,int(self.currentTime))
			display.update()
			self.input()									
Game().Act()
