import pygame as pg
import sys
import numpy as np # For matrix operations
from math import sin, cos
import random
# Initialize Pygame
pg.init()

# Screen dimensions
screenWidth = 800
screenHeight = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


# Variables for the cube
plan = [1, 0, 0, 0] # lignigen for plan [a, b, c, k] ax+by+cz+k=0
camera = [100, 0, 0] # koordinater for kamera [x, y, z]
roll = 0 # rotation for x-axis
pitch = 0 # rotation for y-axis
yaw = 0 # rotation for z-axis






cube_matrix = np.array([
    [-0.5, -0.5, -0.5],  # 0: Bottom-back-left
    [ 0.5, -0.5, -0.5],  # 1: Bottom-back-right
    [ 0.5,  0.5, -0.5],  # 2: Top-back-right
    [-0.5,  0.5, -0.5],  # 3: Top-back-left
    [-0.5, -0.5,  0.5],  # 4: Bottom-front-left
    [ 0.5, -0.5,  0.5],  # 5: Bottom-front-right
    [ 0.5,  0.5,  0.5],  # 6: Top-front-right
    [-0.5,  0.5,  0.5],  # 7: Top-front-left
])
cube_matrix = np.array([
    [ 0.5, -0.5, -0.5],  # 0: Bottom-back-left
    [ 1.5, -0.5, -0.5],  # 1: Bottom-back-right
    [ 1.5,  0.5, -0.5],  # 2: Top-back-right
    [ 0.5,  0.5, -0.5],  # 3: Top-back-left
    [ 0.5, -0.5,  0.5],  # 4: Bottom-front-left
    [ 1.5, -0.5,  0.5],  # 5: Bottom-front-right
    [ 1.5,  0.5,  0.5],  # 6: Top-front-right
    [ 0.5,  0.5,  0.5],  # 7: Top-front-left
])

def transformMatrix(skale, rotation, matrix): # skale = [x, y, z] rotation = [roll, pitch, yaw] 
    # Skale matrix
    scale_matrix = np.array([
        [skale[0], 0, 0],
        [0, skale[1], 0],
        [0, 0, skale[2]]
    ])

    # Rotation matrix (X-axis rotation) roll
    rotation_matrix_x = np.array([
        [1, 0, 0],
        [0, cos(rotation[0]), -sin(rotation[0])],
        [0, sin(rotation[0]), cos(rotation[0])]
    ])

    # Rotation matrix (Y-axis rotation) pitch
    rotation_matrix_y = np.array([
        [cos(rotation[1]), 0, sin(rotation[1])],
        [0, 1, 0],
        [-sin(rotation[1]), 0, cos(rotation[1])]
    ])

    # Rotation matrix (Z-axis rotation) yaw
    rotation_matrix_z = np.array([
        [cos(rotation[2]), -sin(rotation[2]), 0],
        [sin(rotation[2]), cos(rotation[2]), 0],
        [0, 0, 1]
    ])

    # Translation matrix
    translation_matrix = scale_matrix.dot((rotation_matrix_z.dot(rotation_matrix_y.dot(rotation_matrix_x))))

    # Translation matrix on the matrix given
    matrix = np.array(matrix)
    transformed_matrix = matrix.dot(translation_matrix)

    return transformed_matrix


skale = 2
skale_cube = [skale, skale, skale] # skale for cube
transformed_cube = transformMatrix(skale_cube, [roll, pitch, yaw], cube_matrix)
print(cube_matrix)
print(transformed_cube)


def getPointOnPlan(fig,plan,pov): # lave liste af punkter på planen givet
    final = []
    for i in range(len(fig)):
        r = []
        for j in range(len(fig[i])):
            a = fig[i][j]-pov[j]
            r.append(a)
        
        x = [pov[0],r[0]]
        y = [pov[1],r[1]]
        z = [pov[2],r[2]]

        ligning_num = plan[0]*x[0] + plan[1]*y[0] + plan[2]*z[0] + plan[3]
        ligning_t = plan[0]*x[1] + plan[1]*y[1] + plan[2]*z[1]

        t = (-(ligning_num))/ligning_t

        decimals = 2
        final.append([round(x[0]+t*x[1],decimals) , round(y[0]+t*y[1],decimals) , round(z[0]+t*z[1],decimals)])

        for f in final:  # makes list of points 2D
            if len(f) > 2:
                f.pop(0)
    return final


a = getPointOnPlan(transformed_cube,plan,camera)
print(a)

def centerObject(points, screenWidth = 800, screenHeight = 600):
    centerY = screenWidth / 2
    centerZ = screenHeight / 2
    for p in points:
        p[0] += centerY
        p[1] += centerZ
    return points

a = centerObject(a)
print(a)

def drawPoints(points, screen):
    for p in points:
        pg.draw.circle(screen, RED, (p[0], p[1]), 1)

# Set up the display
screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Pygame")

# Clock to control the frame rate
clock = pg.time.Clock()
FPS = 60

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_UP:
                skale += 1
            if event.key == pg.K_DOWN:
                skale -= 1
    keys = pg.key.get_pressed()
    if keys[pg.K_d]:
        yaw += 0.1
    if keys[pg.K_a]:
        yaw -= 0.1 
    if keys[pg.K_w]:
        pitch += 0.1
    if keys[pg.K_s]:
        pitch -= 0.1 


    # Update game state
    
    skale_cube = [skale, skale, skale] # skale for cube
    transformed_cube = transformMatrix(skale_cube, [roll, pitch, yaw], cube_matrix)
    a = getPointOnPlan(transformed_cube,plan,camera)
    a = centerObject(a)

    # Draw to the screen
    screen.fill(BLACK)

    drawPoints(a, screen)
    pg.draw.polygon(screen, BLUE, a)
    a = random.shuffle(a)
    # Flip the display
    pg.display.flip()

# Clean up
pg.quit()
sys.exit()
