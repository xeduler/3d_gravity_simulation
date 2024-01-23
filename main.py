import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import tan
import json
from itertools import combinations
import numpy as np
from tools import *







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
        glTranslatef(*(position * -1))
    

    def load_model(self, filename):
        with open(filename) as input_file:
            self.vertices, self.edges = json.load(input_file)



class EdgeModel(Model):
    def draw(self, position, rotation):
        glTranslatef(*position)
        glRotatef(*rotation)

        glBegin(GL_LINES)
        for edge in self.edges:
            glVertex3fv(edge[0])
            glVertex3fv(edge[1])
        glEnd()

        glRotatef(rotation[0] * -1, rotation[1], rotation[2], rotation[3])
        glTranslatef(*(position * -1))






class Body:
    def __init__(self, mass, model, position=None, rotation=None, speed=None, rot_vec=None):
        self.mass = mass
        self.model = model
        if position:
            self.position = np.array(position, dtype=np.float64)
        else:
            self.position = np.array([0, 0, 0], dtype=np.float64)
        if rotation:
            self.rotation = np.array(rotation, dtype=np.float64)
        else:
            self.rotation = np.array([0, 0, 0, 0], dtype=np.float64)
        if speed:
            self.speed = np.array(speed, dtype=np.float64)
        else:
            self.speed = np.array([0, 0, 0], dtype=np.float64)
        if rot_vec:
            self.rot_vec = np.array(rot_vec, dtype=np.float64)
        else:
            self.rot_vec = np.array([0, 0, 0, 0], dtype=np.float64)


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
            self.position = np.array(position, dtype=np.float64)
        else:
            self.position = np.array([0, 0, 0], dtype=np.float64)
        if rotation:
            self.rotation = np.array(rotation, dtype=np.float64)
        else:
            self.rotation = np.array([0, 0, 0, 0], dtype=np.float64)
        if speed:
            self.speed = np.array(speed, dtype=np.float64)
        else:
            self.speed = np.array([0, 0, 0], dtype=np.float64)
        if rot_vec:
            self.rot_vec = np.array(rot_vec, dtype=np.float64)
        else:
            self.rot_vec = np.array([0, 0, 0, 0], dtype=np.float64)

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
        
        for pair in combinations(self.bodies, 2):
            body, another = pair
            force = G / dists(body.position, another.position)
            body.speed = body.speed + acceleration_vector(force * another.mass, body.position, another.position)
            another.speed = another.speed + acceleration_vector(force * body.mass, another.position, body.position)

                
                
        
        for body in self.bodies:
            body.move()






main_scene = Gravity(
    [
        Body(100000000, Model(load="models/cube.json"), [0, 0, 0], [87, 2, 0, 1], rot_vec=[0.1, 0, 0, 0]),
        Body(10, Model(load="models/pyramid.json"), [10, 0, 0], [-37, 3, 1, 3], speed=[0, 0.02, 0], rot_vec=[1, 0, 0, 0]),
        Body(10, Model(load="models/cube.json"), [-10, 0, 0], [7, 2, -1, -8], speed=[0, -0.02, 0], rot_vec=[1, 0, 0, 0])
    ],
    position = [0.0, 0.0, -20.0],
    rotation = [1, 0, 0, 1],
    speed = [0, 0, 0.0]
)




if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        main_scene.move()
        main_scene.show()
        pygame.display.flip()
        pygame.time.wait(10)