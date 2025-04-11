import os, pygame

from Util.Text_messages import *
in1=[0,0,0,0,0,0,0]
color = [(250, 20, 20), (20, 250, 20), (20, 20, 250), (250, 250, 20),
         (250, 20, 250), (10, 10, 10), (100, 100, 100), (255, 255, 255)]

tiles = [pygame.transform.scale_by(pygame.image.load("Assets/images/tiles/tile"+str(tipe)+".png"), 2)
         if os.path.exists("Assets/images/tiles/tile"+str(tipe)+".png") else 0 for tipe in range(12)]


def Color(image, color):
    image = image.copy()
    image.fill((100, 100, 100), None, pygame.BLEND_RGBA_MULT)
    image.fill(color[0:3]+(0,), None, pygame.BLEND_RGBA_ADD)
    return image


def Frame(cicle, total, start, rate):
    if start[0] == rate:
        if cicle:
            if start[1] >= total:
                start[1] = 0
            else:
                start[1] += 1
        else:
            if start[1] < total:
                start[1] += 1
        start[0] = 0
    start[0] += 1
    return start


class rigel(pygame.sprite.Sprite):
    def __init__(self, pos, py, group):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.group = pygame.Surface((26, 32)), group
        self.rect, self.enter = self.image.get_rect(topleft=(pos)), 0
        self.y_speed, self.x_speed, self.max_ground_speed, self.max_air_speed, self.grounded = 0, 0, 9, -12, 0
        self.jump_speed, self.walljump, self.right_wall, self.left_wall, self.pyr = 10, 0, 1, 1, py
        self.frame = [0, 0, 0]
        self.state = 0
        self.at = 0
        self.facing = 0

        self.sheet = pygame.image.load('Assets/images/rigel/r1.png').convert()

    def image_at(self, x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey((255, 0, 255), pygame.RLEACCEL)
        return image

    def display(self, screen, scroll):
        screen.blit(self.image, (self.rect[0]+scroll[0], self.rect[1]+scroll[1]))
       
    def update(self, keys):
        if self.at != self.state:
            self.frame = [0, 0, 0]
        if not self.state:
            self.frame = Frame(1, 7, self.frame, 6)
        if self.state == 1:
            self.frame = Frame(1, 7, self.frame, 5)
        if self.state == 2:
            self.frame = Frame(0, 4, self.frame, 3)
        if self.state == 3:
            self.frame = Frame(0, 7, self.frame, 5)
        if self.state == 4:
            self.frame = Frame(1, 7, self.frame, 4)
        self.at = self.state
        self.image = self.image_at(
            ((13*self.frame[1])), 15*self.state, 13, 15)
        self.image = pygame.transform.flip(
            pygame.transform.scale_by(self.image, 2), self.facing, 0)
        if self.grounded:
            if keys[2]:
                self.facing = 0
                if self.right_wall:
                    self.state = 1
                else:
                    self.state = 4
            elif keys[3]:
                self.facing = 1
                if self.left_wall:
                    self.state = 1
                else:
                    self.state = 4
            else:
                self.state = 0
        else:
            if self.y_speed < 0:
                self.state = 2
            else:
                self.state = 3
        if keys[2] and self.right_wall:
            if self.x_speed >= self.max_ground_speed:
                self.x_speed = self.max_ground_speed
            else:
                if self.grounded:
                    self.x_speed += .8
                else:
                    self.x_speed += .6
        if keys[3] and self.left_wall:
            if self.x_speed <= -self.max_ground_speed:
                self.x_speed = -self.max_ground_speed
            else:
                if self.grounded:
                    self.x_speed -= .8
                else:
                    self.x_speed -= .6
        if not (keys[3] or keys[2]) and self.x_speed and self.grounded:
            self.x_speed *= .8
        if keys[0]:
            if self.grounded:
                self.y_speed = (self.max_air_speed-abs(self.x_speed/6))
            if self.walljump:
                if keys[2] and not self.left_wall:
                    Walljump(0, self.rect.topleft, self.group)
                    self.y_speed, self.x_speed = -11, 6
                    self.facing = 0
                if keys[3] and not self.right_wall:
                    Walljump(1, self.rect.topleft, self.group)
                    self.y_speed, self.x_speed = -11, -6
                    self.facing = 1
        if self.y_speed >= self.jump_speed:
            self.y_speed = self.jump_speed
        else:
            if keys[1]:
                self.y_speed += .9
            else:
                self.y_speed += .5
        if keys[8] and not self.enter:
            self.enter = 1

        self.rect.y += round(self.y_speed)
        self.rect.x += round(self.x_speed)


class Walljump(pygame.sprite.Sprite):
    def __init__(self, d, pos, *groups):
        super(Walljump, self).__init__(*groups)
        self.frame, self.facing, self.image = 0, d, pygame.image.load("Assets/images/effects/wj1.png")
        self.image = pygame.transform.flip(self.image, d, 0)
        self.rect = self.image.get_rect(topleft=(pos[0]-10*d, pos[1]))

    def display(self, screen, scroll):
        screen.blit(self.image, (self.rect[0]+scroll[0], self.rect[1]+scroll[1]))

    def update(self, *args):
        self.frame += 1
        self.image = pygame.image.load("Assets/images/effects/wj"+str(self.frame)+".png")
        self.image = pygame.transform.flip(self.image, self.facing, 0)
        if self.frame > 7:
            self.kill()


class Meta(pygame.sprite.Sprite):
    def __init__(self, x, y, l, a, tipe):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((l, a))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.tipe = tipe

    def display(self, screen, scroll):
        0
        # screen.blit(self.image,self.rect)

    def update(self, *args):
        pass





class Scr(pygame.sprite.Sprite):
    def __init__(self, pyr, lis, grp, tip):
        super(Scr, self).__init__(grp)
        self.image = pygame.image.load('Assets/images/ui/sele'+str(pyr)+'.png').convert_alpha()
        self.pos, self.r, self.selec, self.c, self.tp = [0, 0], 0, 0, 0, tip
        self.image, self.m = pygame.transform.scale2x(self.image), lis
        self.rect, self.p = self.image.get_rect(), (0, 0, 0)

    def update(self, screen, keys, active):
        if (not self.tp and active) or (self.tp and not self.selec):
            if self.r != keys:
                if keys[0]:
                    self.pos[1] -= 1-len(self.m[self.pos
                                                [0]])*(not self.pos[1]+1)
                if keys[1]:
                    self.pos[1] += 1-len(self.m[self.pos[0]])*(not
                                                               self.pos[1]-(len(self.m[self.pos[0]])-1))
                if keys[2]:
                    self.pos[0] += 1-len(self.m)*(not
                                                  self.pos[0]-(len(self.m)-1))
                if keys[3]:
                    self.pos[0] -= 1-len(self.m)*(not self.pos[0]+1)
            try:
                self.p = self.m[self.pos[0]][self.pos[1]]
            except:
                self.pos = [0, 0]
            self.c += 8-132*int(self.c/160)
            self.imag2 = Color(self.image, (self.c, self.c, self.c))
        else:
            self.imag2 = self.image
        if self.r != keys:
            if keys[4] and self.tp == 1:
                self.selec = not self.selec
        self.r, self.rect.topleft = keys, self.p[:2]
        screen.blit(self.imag2, self.rect)


class EnterMenu(pygame.sprite.Sprite):
    def __init__(self, pyr, li):
        pygame.sprite.Sprite.__init__(self)
        self.imag1, self.tx = pygame.image.load('Assets/images/ui/paused.png'), Text(384, 384, 30, 4)
        self.imrect = self.imag1.get_rect(topleft=(192, 70))
        self.imag2, self.key = pygame.image.load('Assets/images/ui/botton.png'), 0
        self.rec2 = self.imag1.get_rect(topleft=(192, 170))
        self.l, self.pos, self.r, self.selec = li, [0, 0], 0, False
        self.g, self.a = pygame.sprite.Group(), pygame.sprite.Group()
        self.sel1, self.sel2 = Scr(4, sl3, self.a, 0), Scr(3, sl2, self.g, 0)
        self.p, self.rec, self.start, self.ind, self.frame = pyr, 0, 1, 0, 4

    def update(self, screen, keys):
        s, g = keys, inp(keys, self.l)
        if self.r != s and not self.frame:
            if self.key and self.rec:
                for keyr in keys:
                    if keyr:
                        self.l[self.ind] = keys.index(keyr)
                        Rewrite(self.l, self.p-1), Control()
                        self.rec, self.frame = 0, 8
            if keys[self.l[12]] and not self.rec:
                if not self.key:
                    if not self.sel1.pos[0] and self.start:
                        self.start = False
                        self.kill()
                    if self.sel1.pos[0] == 1:
                        self.key = 1
                else:
                    if not self.sel2.pos[0]:
                        self.key = 0
                    else:
                        self.rec, self.ind = 1, (self.sel2.p[2])
        screen.blit(self.imag1, self.imrect)
        self.a.update(screen, g, not (self.key))
        if self.key:
            screen.blit(self.imag2, self.rec2)
            if not self.frame:
                self.g.update(screen, g, not (self.rec)), self.tx.update(
                    screen, (self.sel2.p[3], self.l[self.sel2.p[2]]))
        self.r = s
        self.frame -= 1*bool(self.frame)


class FMenu(pygame.sprite.Sprite):
    def __init__(self, li):
        pygame.sprite.Sprite.__init__(self)
        self.t1, self.t2 = Text(640, 300, 24, 0), Text(640, 340, 24, 1)
        self.t3, self.t4 = Text(640, 380, 24, 2), Text(640, 420, 24, 3)
        self.key, self.g = 0, pygame.sprite.Group()
        self.sel, self.l, self.pos, self.r = Scr(
            5, sl4, self.g, 1), li, [0, 0], 0
        self.rec, self.start, self.ind, self.frame = 0, 0, 0, 4

    def update(self, screen, keys):
        g = inp(keys, self.l)
        self.g.update(screen, g, 1)
        if not self.sel.pos[0] and self.sel.selec:
            self.start = 1
            self.kill()
        self.t1.update(screen, "START"), self.t2.update(screen, "NEW GAME")
        self.t3.update(screen, "KEYS"), self.t4.update(screen, "LEVEL EDIT")


def Rewrite(new, num):
    with open("Util/control.txt", 'r') as f:
        lines = f.readlines()
    with open("Util/control.txt", 'w') as f:
        for i, line in enumerate(lines, 0):
            if i == num:
                for v in new:
                    f.writelines(str(v)+' ')
                f.writelines("\n")
            else:
                f.writelines(line)
    f.close()


def Control():
    with open('Util/control.txt', 'r') as file:
        data = file.readlines()
    file.close()
    for row in data:
        n, row, lis = data.index(row)+1, row.split(' '), []
        for num in row:
            try:
                lis.append(int(num))
            except:
                0
        p, globals()[p] = "in"+str(n), lis


Control()
sl1 = [[(336, 34), (312, 84), (288, 134), (262, 184), (240, 234), (216, 284)],
       [(416, 16), (394, 66), (370, 116), (346, 166), (322, 216), (298, 266)],
       [(476, 48), (452, 99), (428, 148), (404, 199), (380, 248), (356, 298)]]
sl2, sl3 = [[(216, 162, -1, 'BACK')], [(208, 231, 3, 'LEFT')], [(232, 206, 0, 'UP'),
                                                                (233, 257, 1, 'DOWN'), (233, 331, 12, 'START')], [(256, 231, 2, 'RIGHT')], [(367,
                                                                                                                                             183, 4, 'JAB'), (367, 232, 5, 'STRONG'), (367, 281, 6, 'FIERCE'), (367, 330, 11,
                                                                                                                                                                                                                'EX PUNCH')], [(471, 183, 7, 'CLOSE'), (471, 232, 8, 'FAR'), (471, 281, 9,
                                                                                                                                                                                                                                                                              'ROUNDHOUSE'), (471, 330, 10, 'EX KICK')]], [[(213, 130)], [(332, 130)],
                                                                                                                                                                                                                                                                                                                           [(451, 130)]]
sl4 = [[(550, 284), (530, 324), (560, 364), (515, 404)]]


def inp(keys, liskey):
    lis = []
    for inp in liskey:
        lis.append(keys[liskey[liskey.index(inp)]])
    return lis


def Num(num):
    try:
        return num/abs(num)
    except:
        return 0


class BaseGroup(pygame.sprite.Group):
    def __init__(self):
       pygame.sprite.Group.__init__(self)

    def update(self):
        for obj in self:
            obj.update()

    def display(self, screen, scroll):
        for obj in self:
            obj.display(screen, scroll)


class Game(object):
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 4096)
        pygame.init()

        self.screen = pygame.display.set_mode(
            (1280, 720), pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
        
        self.play, self.frame = 1, pygame.time.Clock()
        self.keys, self.startgame, self.start = tuple(pygame.key.get_pressed()), 1, 0
        self.level, self.leveltime, self.currentTime = 1, 0, 100

    def newlevel(self, l):
        self.startscroll, self.scroll, self.fm = 1, [0, 600], FMenu(in1)
        self.mapt(l)
        self.time, self.effec = Text(640, 40, 24, 5), BaseGroup()
        self.rigel = rigel(self.spawn, 1, self.effec)
        self.primGroup, self.allGroup = pygame.sprite.Group(), BaseGroup()
        self.primGroup.add(self.rigel)
        self.allGroup.add(self.baseGroup, self.metaGroup, self.primGroup)

    def bitmap(self, n):
        f = open("Assets/objects/mapa"+str(n)+".txt", 'r')
        data = f.read()
        f.close()
        data, gamemap = data.split('\n'), []
        for row in data:
            line = str(row)
            line = line.split(' ')
            gamemap.append(list(line))
        return gamemap

    def mapt(self, n):
        lis, y = self.bitmap(n), 100
        lGroup, DGroup = pygame.sprite.Group(), pygame.sprite.Group()
        KGroup = pygame.sprite.Group()
        for i in range(len(lis)):
            y += 30
            for n in (lis[i]):
                bit = list(map(str, str(n)))
                if not i:
                    self.back = (int(bit[0]+bit[1], 16), int(bit[2]
                                                             + bit[3], 16), int(bit[4]+bit[5], 16))
                elif i == 1:
                    self.spawn = (int(bit[0]+bit[1]+bit[2], 16)
                                  * 30, int(bit[3]+bit[4]+bit[5], 16)*30)
                else:
                    if len(bit) > 2:
                        x = (int(bit[0]+bit[1], 16))*30
                        try:
                            ex = (int(bit[3]+bit[4], 16))*30
                        except:
                            ex = 30
                        try:
                            ey = (int(bit[5]+bit[6], 16))*30
                        except:
                            try:
                                ey = (int(bit[5], 16))*30
                            except:
                                ey = 30
                        meta = Meta(x, y, ex, ey, (int(bit[2], 16)))
                        if int(bit[2], 16) == 11:
                            DGroup.add(meta)
                        elif int(bit[2], 16) == 12:
                            KGroup.add(meta)
                        else:
                            lGroup.add(meta)

        self.baseGroup, self.metaGroup = lGroup, DGroup

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.play = False
            

    def collisions(self):
        if pygame.sprite.groupcollide(self.baseGroup, self.primGroup, 0, 0):
            for tile in pygame.sprite.groupcollide(self.baseGroup,
                                            self.primGroup, 0, 0):
                if (self.rigel.rect.centerx < tile.rect.right and
                        self.rigel.rect.centerx > tile.rect.left):
                    self.rigel.walljump, self.rigel.left_wall, self.rigel.right_wall = 0, 1, 1
                    if self.rigel.rect.top < tile.rect.top:
                        self.rigel.grounded, self.rigel.y_speed = 1, 0
                        self.rigel.rect.top = tile.rect.top-30
                    elif (self.rigel.rect.top <= tile.rect.bottom
                          and self.rigel.y_speed < 0):
                        self.rigel.y_speed = 0
                if (self.rigel.rect.centery > tile.rect.top and
                        self.rigel.rect.centery < tile.rect.bottom):
                    self.rigel.walljump, self.rigel.grounded = 1, 0
                    if (self.rigel.rect.left <= tile.rect.left
                            and self.rigel.x_speed > 0):
                        self.rigel.rect.left = tile.rect.left-19
                        self.rigel.right_wall, self.rigel.x_speed = 0, 0
                    elif (self.rigel.rect.right >= tile.rect.right
                          and self.rigel.x_speed < 0):
                        self.rigel.rect.right = tile.rect.right+19
                        self.rigel.left_wall, self.rigel.x_speed = 0, 0
        else:
            self.rigel.grounded, self.rigel.walljump = 0, 0
            self.rigel.left_wall, self.rigel.right_wall = 1, 1
        if pygame.sprite.groupcollide(self.metaGroup, self.primGroup, 0, 0):
            self.leveltime = self.currentTime
            self.level += 1
            self.newlevel(self.level)

        if self.rigel.rect.y > 2000:
            self.rigel.rect.topleft = self.spawn
            self.scroll= (-self.rigel.rect.x)+640 , (-self.rigel.rect.y)+360

    def Act(self):
            self.newlevel(self.level)
            while self.play:

                self.keys = tuple(pygame.key.get_pressed())

                if self.startgame:
                    self.screen.fill(self.back)
                    self.fm.update(self.screen, self.keys)
                    if self.fm.start and self.startgame:
                        self.startgame = 0
                        self.scroll= (-self.rigel.rect.x)+640 , (-self.rigel.rect.y)+360

                    self.scroll = self.scroll[0]-1, 0
                    
                else:
                    self.screen.fill(self.back)
                    if not self.start:
                        self.primGroup.update(inp(self.keys, in1))
                        self.effec.update()
                        if self.startscroll:
                            des= (-self.rigel.rect.x)+640 , (-self.rigel.rect.y)+360
                            self.accel = (self.scroll[0] - des[0])/8, (self.scroll[1] - des[1])/8
                            self.scroll = self.scroll[0] - self.accel[0], self.scroll[1] - self.accel[1]
                        
                        self.currentTime -= 1/60
                       
                        self.collisions()
                        for each in self.primGroup:
                            if each.enter and not self.start:
                                self.start, self.ents = 1, EnterMenu(
                                    each.pyr, eval('in'+str(each.pyr)))
                    else:
                        self.ents.update(self.screen, self.keys)
                        if not self.ents.start:
                            self.start = 0
                            for each in self.primGroup:
                                each.enter = 0

                for block in self.baseGroup:
                    for x in range(int(block.rect[2]/30)):
                        for y in range(int(block.rect[3]/30)):
                            self.screen.blit(
                                    tiles[block.tipe], (block.rect[0]+self.scroll[0]+x*30, block.rect[1]+self.scroll[1]+y*30))
                
                for block in self.metaGroup:
                    for x in range(int(block.rect[2]/30)):
                        for y in range(int(block.rect[3]/30)):
                            #if abs((block.rect[0]+x*30)+self.scroll[0]) > 10 and abs((block.rect[1]+y*30)+self.scroll[1]) > 10:
                            self.screen.blit(
                                    tiles[block.tipe], (block.rect[0]+self.scroll[0]+x*30, block.rect[1]+self.scroll[1]+y*30))


                self.allGroup.display(self.screen, self.scroll)
                self.effec.display(self.screen, self.scroll)

                self.time.update(self.screen, int(self.currentTime))
                pygame.display.flip()
                self.frame.tick(60)
                self.input()
                if self.currentTime < 0:
                    self.play = False
        
        

    
Gameplay=Game()
try:
    Gameplay.Act()
except:
    pass
Game.play = False     
#err_message(Gameplay) # ⚠️ Warning: Do not uncomment this line
pygame.quit()