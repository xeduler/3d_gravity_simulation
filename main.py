import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from math import tan

def perspective_projection(fovy, aspect, zNear, zFar):
    """
    Set up perspective projection using a custom function.
    """
    f = 1.0 / tan(fovy / 2.0)
    matrix = [
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (zFar + zNear) / (zNear - zFar), -1,
        0, 0, (2.0 * zFar * zNear) / (zNear - zFar), 0
    ]
    glMultMatrixf(matrix)

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Simple 3D Animation")

# Set up the perspective projection
perspective_projection(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Define a cube vertices in counter-clockwise order
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
)

# Define cube edges in counter-clockwise order
edges = (
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

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Rotate the cube
    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw cube
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    pygame.display.flip()
    pygame.time.wait(10)
