import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Initialize Pygame and set up the display
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
glViewport(0, 0, width, height)
glOrtho(0, width, height, 0, -1, 1)

# Simple vertex shader
vertex_code = """
    void main() {
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
"""

# Simple fragment shader
fragment_code = """
    void main() {
        gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    }
"""

# Compile shaders and create shader program
vertex_shader = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vertex_shader, vertex_code)
glCompileShader(vertex_shader)

fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fragment_shader, fragment_code)
glCompileShader(fragment_shader)

shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)

# Set up VBO (Vertex Buffer Object) for a simple quad
vertices = [
    100.0, 100.0, 0.0,
    100.0, 500.0, 0.0,
    500.0, 500.0, 0.0,
    500.0, 100.0, 0.0,
]

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(vertices) * 4, (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT)

    # Use the shader program
    glUseProgram(shader_program)

    # Set up VAO (Vertex Array Object) and enable attributes
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 0, None)

    # Draw the quad
    glDrawArrays(GL_QUADS, 0, 4)

    # Clean up
    glDisableClientState(GL_VERTEX_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glUseProgram(0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
