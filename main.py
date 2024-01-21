import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import tan

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
camera_pos = [0.0, 0.0, -5.0]

perspective_projection(45, (width / height), 0.1, 50.0)


class Model:
    def __init__(self, position=[0, 0, 0], rotation=[0, 0, 0, 0], vertices=[], edges=[]):
        self.vertices = vertices
        self.edges = edges
        self.position = position
        self.rotation = rotation


    def draw(self):
        glTranslatef(*self.position)
        glRotatef(*self.rotation)

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glTranslatef(self.position[0] * -1, self.position[1] * -1, self.position[2] * -1)
        glRotatef(self.rotation[0] * -1, self.rotation[1] * -1, self.rotation[2] * -1, self.rotation[3] * -1, )




cube1 = Model([-3, 0, 0])
cube2 = Model([3, 0, 0])

cube1.vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
)

cube1.edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
)

cube2.vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
)

cube2.edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
)

glTranslatef(*camera_pos)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glRotatef(1, 0, 0, 1)
    #glTranslatef(camera_pos[0], camera_pos[1], -0.01)

    cube1.draw()
    cube2.draw()

    pygame.display.flip()
    pygame.time.wait(10)
