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

width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("AAAAAAAAA")

# Initial camera position
camera_pos = [0.0, 0.0, -2.0]

perspective_projection(45, (width / height), 0.1, 50.0)


class Model:
    def __init__(self, position=[0,0,0], rotation=[0,0,0,0], speed=[0,0,0], rot_vec=[0,0,0,0], load=""):
        self.vertices = []
        self.edges = []
        self.position = position
        self.rotation = rotation
        self.speed = speed
        self.rot_vec = rot_vec
        if load != "":
            self.load_model(load)


    def move(self):
        for i in range(3):
            self.position[i] += self.speed[i]
        for i in range(4):
            self.rotation[i] += self.rot_vec[i]


    def draw(self):
        glTranslatef(*self.position)
        glRotatef(*self.rotation)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glRotatef(self.rotation[0] * -1, self.rotation[1], self.rotation[2], self.rotation[3])
        glTranslatef(self.position[0] * -1, self.position[1] * -1, self.position[2] * -1)
    

    def load_model(self, filename):
        with open(filename) as input_file:
            self.vertices, self.edges = json.load(input_file)



class Scene:
    def __init__(self, models):
        self.models = models


    def show(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glRotatef(1, 0, 0, 1)
        glTranslatef(camera_pos[0], camera_pos[1], -0.01)

        for model in self.models:
            model.move()
            model.draw()

        


main_scene = Scene([
    Model([-3, 0, 0], [87, 2, 0, 1], rot_vec=[1, 0, 0, 0], load="cube.json"),
    Model([3, 0, 0], [37, 3, 1, 3], load="cube.json")
])
 



glTranslatef(*camera_pos)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


    main_scene.show()
    pygame.display.flip()
    pygame.time.wait(10)