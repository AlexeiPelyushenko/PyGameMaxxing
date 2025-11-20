import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define vertices and edges of the cube
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],
    [4, 5], [5, 6], [6, 7], [7, 4],
    [0, 4], [1, 5], [2, 6], [3, 7]
]

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Initialize pygame and OpenGL
pygame.init()
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Rotating Cube")

gluPerspective(45, (800 / 600), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the first cube
    glPushMatrix()
    glTranslatef(-2, 0, 0)  # Translate the first cube to the left
    glRotatef(1, 3, 1, 1)
    draw_cube()
    glPopMatrix()

    # Draw the second cube
    glPushMatrix()
    glTranslatef(2, 0, 0)  # Translate the second cube to the right
    glRotatef(1, 3, 1, 1)
    draw_cube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, 0)  # Translate the second cube to the right
    glRotatef(1, 3, 1, 1)
    draw_cube()
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()