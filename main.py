import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import tan
import json




def perspective_projection(fovy, aspect, zNear, zFar):
    f = 1.0 / tan(fovy / 2.0)
    matrix = [
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (zFar + zNear) / (zNear - zFar), -1,
        0, 0, (2.0 * zFar * zNear) / (zNear - zFar), 0
    ]
    glMultMatrixf(matrix)




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

        print(rotation)

        glRotatef(rotation[0] * -1, rotation[1], rotation[2], rotation[3])
        glTranslatef(position[0] * -1, position[1] * -1, position[2] * -1)
    

    def load_model(self, filename):
        with open(filename) as input_file:
            self.vertices, self.edges = json.load(input_file)



class Body:
    def __init__(self, mass, model, position=[0,0,0], rotation=[0,0,0,0], speed=[0,0,0], rot_vec=[0,0,0,0]):
        self.mass = mass
        self.model = model
        self.position = position
        self.rotation = rotation
        self.speed = speed
        self.rot_vec = rot_vec
    
    def move(self):
        for i in range(3):
            self.position[i] += self.speed[i]
        for i in range(4):
            self.rotation[i] += self.rot_vec[i]
        
    
    def draw(self):
        self.model.draw(self.position, self.rotation)



class Scene:
    def __init__(self, bodies, position=[0,0,0], rotation=[0,0,0,0], speed=[0,0,0], rot_vec=[0,0,0,0]):
        self.bodies = bodies
        self.position = position
        self.rotation = rotation
        self.speed = speed
        self.rot_vec = rot_vec

        glTranslatef(*self.position)


    def show(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for body in self.bodies:
            body.move()
            body.draw()
        

    def move(self):
        glRotatef(*self.rotation)
        glTranslatef(*self.speed)

        


main_scene = Scene([
    Body(100, Model(load="models/cube.json"), [-3, 0, 0], [87, 2, 0, 1], rot_vec=[1, 0, 0, 0]),
    Body(10, Model(load="models/cube.json"), [3, 0, 0], [37, 3, 1, 3], )],
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