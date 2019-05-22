# physsim
A simulator made by an AP Physics 1 student for extra credit in Python3. This simulator is currently unfinished but can help students visualize physics concepts in an ideal environment. There are many parameters that can also be tweaked to make the scenario different as well. Its purpose is to show that physics can be applied to all sorts of things, including using Newton's laws and what we learned in class to make a simulator. 

Dependencies: Python3 and pygame 

Note from creator: Sometimes I want camel case, sometimes I don't  :p

## New Classes(subclasses of pygame.sprite.Sprite):
 - World
 - Projectile
 - Static
 
 
### World
The World class creates a surface to put items and takes in params: size, g, fps, log=False, dcPlaceRound=0.
Size is a tuple of (x, y), g is acceleration due to gravity so 10, 0, 9.81, or any arbitrary POSITIVE float or integer will work. If you put a negative, stuff will accelerate away from the ground. dcPlaceRound is what place value the world should round to during its calculations, which is currently slightly broken and should not be supplied and left with its default value to prevent the possibility of errors. The World supports the following methods:
 - addObject: takes in a projectile object to display and to run calculations on
 - reset: resets all projectiles and called simply as World.reset()
 - addStatic: takes in a static object to display and keep track of collisions with
 - update: called every tick, update is where the magic happens.
 - render: called every tick after update, renders surface on pygame display. Takes: tuple pos of (x, y) and screen which is display object that the surface is blitted on. 

### Projectile
The projectile class creates a rectangular projectile sprite and takes params: selfinfo, mass, vx, vy, a, a_dir, ctype. Selfinfo is tuple of (radius, color, x_pos, y_pos) color is tuple of (R, G, B) with R, G, and B being an integer from 0-255. Mass is mass of object in kg. Vx, Vy, A, a_dir, and ctype do not have to be supplied and default to value of 0. Vx is x velocity in m/s, vy is y velocity in m/s, a is an acceleration acting on the object in the direction of a_dir in radians. Projectile supports the following methods:
 - move: takes in x, and y. After moving, the distance travelled is assigned to the velocity. ex: projectile.move(5, 0) then projectile.vx = 5.
 - addForce: takes in xForce, yForce, constx, consty. Constx and y default to zero, but if set to true supply a constant force in that dimension. xForce is in Newtons and so is yForce.
 - reset: called by World when World is reset. Goes back to inital position with init velocity and acceleration.
 - update: called every tick. Updates kinetic energy of the object, and ensures forces are applied if constant
 

### Static
The Static class creates a static rectangle and takes params: pos, mass, size, color, muVal. Pos is tuple of (x,y), mass is mass in kg, size is tuple of (width, height), and color is tuple of (R,G,B) where RGB are integers between 0 and 255. Statics have no methods and are basically walls that the objects collide with. Currently only used as floor, but walls and slopes are possible future updates.
