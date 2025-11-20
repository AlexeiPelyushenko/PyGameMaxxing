import pygame
import math
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ----------------------
# 3D ENGINE COMPONENTS
# ----------------------

# Cube vertices
points = [
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
]

# Cube edges between vertices
edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

def rotateX(point, angle):
    x, y, z = point
    y2 = y*math.cos(angle) - z*math.sin(angle)
    z2 = y*math.sin(angle) + z*math.cos(angle)
    return [x, y2, z2]

def rotateY(point, angle):
    x, y, z = point
    z2 = z*math.cos(angle) - x*math.sin(angle)
    x2 = z*math.sin(angle) + x*math.cos(angle)
    return [x2, y, z2]

def rotateZ(point, angle):
    x, y, z = point
    x2 = x*math.cos(angle) - y*math.sin(angle)
    y2 = x*math.sin(angle) + y*math.cos(angle)
    return [x2, y2, z]

def project(point):
    """Simple perspective projection"""
    x, y, z = point
    z += 5  # push cube away from camera
    f = 200 / z
    px = x * f + WIDTH // 2
    py = -y * f + HEIGHT // 2
    return (int(px), int(py))

angle = 0

# ---------------
# MAIN LOOP
# ---------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((10, 10, 10))

    # rotate cube
    rotated = []
    for p in points:
        r = rotateX(p, angle)
        r = rotateY(r, angle * 0.5)
        r = rotateZ(r, angle * 0.2)
        rotated.append(r)

    # project cube points to 2D
    projected = [project(p) for p in rotated]

    # draw cube edges
    for e in edges:
        p1 = projected[e[0]]
        p2 = projected[e[1]]
        pygame.draw.line(screen, (255, 255, 255), p1, p2, 2)

    pygame.display.flip()
    angle += 0.01
    clock.tick(60)
