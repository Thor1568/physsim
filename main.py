import pygame as pg
from math import cos
from math import sin
from math import pi as PI
import os

class World(pg.Surface):
    def __init__(self, size, g, fps, log=False, dcPlaceRound=0):
        """Takes in the size as (x, y), acceleration due to gravity as g, and the FPS that the world should update.
        Log is the logfile of the World """
        pg.Surface.__init__(self, size)
        self.fill((255,255,255))
        self.G = g
        self.FPS = fps
        self.SIZE = size
        self.dcpl = dcPlaceRound
        self.projectiles = pg.sprite.Group()
        self.statics = pg.sprite.Group()
        if log:
            self.logF = os.path.normpath(log)

    def addObject(self, *objects):
        "Adds a projectile."
        self.projectiles.add(*objects)

    def reset(self):
        for x in self.projectiles:
            x.reset()

    def addStatic(self, *objects):
        "Adds a static object."
        self.statics.add(*objects)

    def update(self):
        "Updates and allows forces to act upon all objects."
        #Final change is actually V, don't know why but it works...
        tempGroup = pg.sprite.Group()
        for sprite in self.projectiles:
            sprite.update()

            if sprite in pg.sprite.groupcollide(self.projectiles, self.statics, False, False):
                #What to do when sprites are colliding with any static. Will eventually have walls, slopes, and floors.
                #Inelastic collisions
                #If collision with floor, then make vx influenced by force of Friction and vy = 0
                #If collision with wall, then make vy influenced by force of Friction and vx = 0
                #elastic collisions
                sprite.vy = 0
                sprite.vx = 0
                #pg.sprite.groupcollide()

            #temp group made here
            if sprite in pg.sprite.groupcollide(self.projectiles, tempGroup, False, False):
                #What to do when sprites are colliding with any other projectile. Projectiles have properties: elastic or inelastic.
                if sprite.elastic:
                    sprite.pi = sprite.m*(sprite.vx+sprite.vy)
                    sprite.vangle = round(arctan(sprite.vy/sprite.vx), self.dcpl)
                print("hit other projectile")

            if (not (sprite in pg.sprite.groupcollide(self.projectiles, self.statics, False, False)) and (not (sprite in pg.sprite.groupcollide(self.projectiles, tempGroup, False, False)))):
                sprite.addForce(0, sprite.m*self.G)
                t = 1/self.FPS
                aX = round(sprite.a*sin(sprite.a_dir), self.dcpl)
                aY = round(sprite.a*cos(sprite.a_dir), self.dcpl)
                print("aX: ", aX, "\n aY", aY)

                if sprite.a == 0:
                    sprite.vy += self.G*t
                    sprite.vx += (sprite.xF/sprite.m)*t
                    if (sprite.vx != 0) and (sprite.vy == 0):
                        #Vx only
                        sprite.move(sprite.vx, (sprite.yF/sprite.m)*t)

                    elif (sprite.vy != 0) and (sprite.vx == 0):
                        #Vy only
                        sprite.move((sprite.xF/sprite.m)*t, (sprite.yF/sprite.m)*t)

                    elif (sprite.vy != 0) and (sprite.vx != 0):
                        #Vy and vx
                        sprite.move(sprite.vx, (sprite.yF/sprite.m)*t)
                    else:
                        #No a and no v
                        sprite.move((sprite.xF/sprite.m)*t, (sprite.yF/sprite.m)*t)
                        print("No a and v")
                        #General equation
                        #vf = vi+at
                        #sprite.vx = sprite.vx+aX*t
                        #sprite.vy = sprite.vx+(sprite.yF/sprite.m)*t
                        #change due to G: sprite.vy = sprite.vy+self.G*t
                        #sprite.move((sprite.xF/sprite.m)*t, (sprite.yF/sprite.m)*t)

                if (aX != 0) and (aY == 0):
                    sprite.xF = (sprite.m*aX)-sprite.xF
                    if (sprite.vx == 0) and (sprite.vy == 0):
                        #Ax only
                        #sprite.move(sprite.xF, (sprite.m*aX)-sprite.yF) Not sure if this works properly?
                        sprite.move((sprite.xF/sprite.m)*t, (sprite.yF/sprite.m)*t)

                    if (sprite.vx != 0) and (sprite.vy == 0):
                        #Ax and vx
                        sprite.move((sprite.xF/sprite.m)*t, (sprite.yF/sprite.m)*t)

                    elif (sprite.vx != 0) and (sprite.vy != 0):
                        #Ax and vy
                        sprite.move((sprite.xF/sprite.m)*t, (sprite.yF/sprite.m)*t)
                if (aY != 0) and (aX == 0):
                    pass
                else:
                    #aY and aX
                    pass




    def render(self, pos, screen):
        self.fill((255,255,255))
        self.projectiles.draw(self)
        self.statics.draw(self)
        screen.blit(self, pos)


class Projectile(pg.sprite.Sprite):
    def __init__(self, selfinfo, mass, vx=0, vy=0, a=0, a_dir=0, ctype="e"):
        """Takes selfInfo, which is (radius, color, x_pos, y_pos)
        Vx is initial velocity in the x, which never changes unless there is air resistance in the world,
        Vy is initial velocoty in the y, which only changes due to G unless there is air resistance,
        a is acceleration and a_dir is the direction of the acceleration with zero being straight down. Ctype is
        type of collision, i for inelastic and e for elastic"""
        pg.sprite.Sprite.__init__(self)
        self.surf = pg.Surface((selfinfo[0], selfinfo[0]))
        self.surf.fill(selfinfo[1])
        #pg.draw.circle(self.surf, selfinfo[1], (0,0), selfinfo[0])
        self.image = self.surf
        self.constx = False; self.consty = False;
        self.rect = self.image.get_rect()
        self.vxi = vx; self.vyi = vy*-1;
        self.rect.x = selfinfo[2]; self.rect.y = selfinfo[3];
        self.xi = self.rect.x; self.yi = self.rect.y;
        self.m = mass
        if ctype== "e":
            self.elastic = True
        else:
            self.elastic = False
        self.K = self.m*(abs(vx)+abs(vy))**2
        self.a_dir = a_dir
        self.vx = vx
        self.vy = vy*-1
        self.a = a
        self.xF = 0
        self.yF = 0

    def move(self, x, y):
        "Moves the sprite in x and y."
        self.rect.x += x
        self.rect.y += y
        self.vx = x
        self.vy = y

    def addForce(self, xForce, yForce, constx=False, consty=False):
        self.xForce = xForce
        self.yForce = yForce
        self.xF += xForce
        self.yF += yForce
        self.constx = constx; self.consty = consty;

    def reset(self):
        self.rect.x = self.xi
        self.rect.y = self.yi
        self.vx = self.vxi
        self.vy = self.vyi
        self.xF = 0
        self.yF = 0

    def update(self):
        v2 = (self.vx+self.vy)**2
        self.K = self.m*v2
        print("Net Velocity Squared:", v2)
        if self.constx:
            self.xF = self.xForce;
        if self.consty:
            self.yF = self.yForce;
        #print("X Force: ", self.xF, "\n Y Force: ", self.K)

class Static(pg.sprite.Sprite):
    def __init__(self, pos, mass, size, color, muVal=0):
        """Creates a static surface that takes (x, y), mass in kg, (xsize, ysize), (R, G, B), muValue.
        Mu helps determine the force of friction that will act on an object in contact."""
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.m = mass
        self.surf = pg.Surface((size[0], size[1]))
        self.image = self.surf; self.image.fill(color)
        #self.rect = (pos[0], pos[1], size[0], size[1])
        self.rect = self.surf.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


def main():
    pg.init()
    pg.mouse.set_cursor(*pg.cursors.broken_x)
    gclock = pg.time.Clock()
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    RED = (255,0,0)
    WORLDRECT = (800, 600)
    WORLDRECT2 = (0, 0, WORLDRECT[0], WORLDRECT[1])
    FPS = 60
    gdisp = pg.display.set_mode(WORLDRECT, 0, 32)
    boxY = 100
    #Force of Gravity
    Fg = 10
    #ForceVector to act on projectile in scenario (xForce, Yforce)
    ForceVector = (100, 0)
    earth = World(WORLDRECT, Fg, FPS, dcPlaceRound=5)
    #selfInfo, which is (radius, color, x_pos, y_pos)
    box = Projectile((20, GREEN, 50, 100), 30, vx=10, vy=20)
    #vx = 10, vy=0,     a_dir=PI/2, a=8)
    box2 = Projectile((20, BLUE, 500, 100), 2)
    #box3 = Projectile((20, RED, 300, boxY), 2, vx=-20, vy=3)
    #box4 = Projectile((20, BLACK, 200, boxY), 2)
    #earth.addObject(box, box2, box3, box4)
    earth.addObject(box, box2)
    floor = Static((0, 550), 20, (800, 50), (0,0,0))
    earth.addStatic(floor)
    play = True

    while play:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                if event.key == pg.K_r:
                    #Reset world
                    earth.reset()
                if event.key == pg.K_f:
                    #Add force to green box
                    box.addForce(ForceVector[0], ForceVector[1], constx=True, consty=True)
                    pass

            if event.type == pg.QUIT:
                pg.quit()
                exit()



        #gdisp.blit(earth, (0,0))
        earth.update()
        earth.render((0,0), gdisp)
        gclock.tick(FPS)
        pg.display.update(WORLDRECT2)
        rawfps = gclock.get_fps()
        pg.display.set_caption(str(round(rawfps)))


if __name__ == '__main__':
    main()
