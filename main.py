import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import tan
import json
from copy import deepcopy



def perspective_projection(fovy, aspect, zNear, zFar):
    f = 1.0 / tan(fovy / 2.0)
    matrix = [
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (zFar + zNear) / (zNear - zFar), -1,
        0, 0, (2.0 * zFar * zNear) / (zNear - zFar), 0
    ]
    glMultMatrixf(matrix)



def dists(pos0, pos1):
    return (pos0[0]-pos1[0])**2 + (pos0[1]-pos1[1])**2 + (pos0[2]-pos1[2])**2


def acceleration_vector(force, pos0, pos1):
    x = pos1[0] - pos0[0]
    y = pos1[1] - pos0[1]
    z = pos1[2] - pos0[2]

    part = force / (abs(x)+abs(y)+abs(z))
    return [x*part, y*part, z*part]



pygame.init()

width, height = 1000, 800
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D D:")


perspective_projection(45, (width / height), 0.1, 50.0)








class Model:
    def __init__(self, load=""):
        self.vertices = []
        self.edges = []
        
        if load != "":
            self.load_model(load)


    def draw(self, position, rotation):
        glTranslatef(*position)
        glRotatef(*rotation)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glRotatef(rotation[0] * -1, rotation[1], rotation[2], rotation[3])
        glTranslatef(position[0] * -1, position[1] * -1, position[2] * -1)
    

    def load_model(self, filename):
        with open(filename) as input_file:
            self.vertices, self.edges = json.load(input_file)






class Body:
    def __init__(self, mass, model, position=None, rotation=None, speed=None, rot_vec=None):
        self.mass = mass
        self.model = model
        if position:
            self.position = position
        else:
            self.position=[0, 0, 0]
        if rotation:
            self.rotation = rotation
        else:
            self.rotation=[0, 0, 0, 0]
        if speed:
            self.speed = speed
        else:
            self.speed = [0, 0, 0]
        if rot_vec:
            self.rot_vec = rot_vec
        else:
            self.rot_vec=[0, 0, 0, 0]


    def move(self):
        for i in range(3):
            self.position[i] += self.speed[i]
        for i in range(4):
            self.rotation[i] += self.rot_vec[i]
        
    
    def draw(self):
        self.model.draw(self.position, self.rotation)






class Scene:
    def __init__(self, bodies, position=None, rotation=None, speed=None, rot_vec=None):
        self.bodies = bodies
        if position:
            self.position = position
        else:
            self.position=[0, 0, 0]
        if rotation:
            self.rotation = rotation
        else:
            self.rotation=[0, 0, 0, 0]
        if speed:
            self.speed = speed
        else:
            self.speed = [0, 0, 0]
        if rot_vec:
            self.rot_vec = rot_vec
        else:
            self.rot_vec=[0, 0, 0, 0]

        glTranslatef(*self.position)


    def show(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for body in self.bodies:
            body.draw()
        

    def move(self):
        glRotatef(*self.rotation)
        glTranslatef(*self.speed)

        for body in self.bodies:
            body.move()



        

class Gravity(Scene):
    def move(self):
        G = 6.67385e-11
        for body in self.bodies:
            for another in self.bodies:
                if body is not another:
                    x, y, z = acceleration_vector((G * another.mass / dists(body.position, another.position)), body.position, another.position)
                    body.speed[0] = body.speed[0] + x
                    body.speed[1] = body.speed[1] + y
                    body.speed[2] = body.speed[2] + z 

                
                
        
        for body in self.bodies:
            body.move()






main_scene = Gravity(
    [
        Body(10000, Model(load="models/cube.json"), [-3, 0, 0], [87, 2, 0, 1], rot_vec=[1, 0, 0, 0]),
        Body(10, Model(load="models/cube.json"), [3, 0, 0], [37, 3, 1, 3])
    ],
    position = [0.0, 0.0, -10.0],
    rotation = [1, 0, 0, 1],
    speed = [0, 0, -0.0]
)





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


    main_scene.move()
    main_scene.show()
    pygame.display.flip()
    pygame.time.wait(10)