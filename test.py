import pygame as pg
import sys
import numpy as np # For matrix operations
from math import sin, cos, sqrt
import random

'''
# Thinking

3D
point = [x,y,z]
polygon = [point, point, point]
all_polygons = [polygon, polygon, ...]
sorts_polygons(all_polygons)
    Calculate the average Z values of each polygon.



2D
pointsOnPlan = getPointOnPlan(sorts_polygons)

draw(filtered_polygons)

how to know what polygons to draw? Painter's algorithm
Calculate the average Z values of each face.

'''



# Initialize Pygame
pg.init()

# Screen dimensions
screenWidth = 800
screenHeight = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
colors = []
for i in range(6):
    color = [255/(i+1), 255/(i+1), 255/(i+1)]
    colors.append(color)
colors.reverse()



# Variables for the cube
plan = [1, 0, 0, 0] # lignigen for plan [a, b, c, k] ax+by+cz+k=0
fov = 500
camera = [fov, 0, 0] # koordinater for kamera [x, y, z]
roll = 0 # rotation for x-axis
pitch = 0 # rotation for y-axis
yaw = 0 # rotation for z-axis
skale = 200

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

def polygonsFromCubeMatrix(cube_matrix):
    polyDown1 = [cube_matrix[0], cube_matrix[1], cube_matrix[4]]
    polyDown2 = [cube_matrix[1], cube_matrix[5], cube_matrix[4]]
    polyTop1 = [cube_matrix[3], cube_matrix[2], cube_matrix[7]]
    polyTop2 = [cube_matrix[6], cube_matrix[2], cube_matrix[7]]
    polyLeft1 = [cube_matrix[0], cube_matrix[3], cube_matrix[4]]
    polyLeft2 = [cube_matrix[7], cube_matrix[3], cube_matrix[4]]
    polyRight1 = [cube_matrix[1], cube_matrix[2], cube_matrix[5]]
    polyRight2 = [cube_matrix[6], cube_matrix[2], cube_matrix[5]]
    polyFront1 = [cube_matrix[4], cube_matrix[5], cube_matrix[6]]
    polyFront2 = [cube_matrix[7], cube_matrix[4], cube_matrix[6]]
    polyBack1 = [cube_matrix[0], cube_matrix[1], cube_matrix[2]]
    polyBack2 = [cube_matrix[3], cube_matrix[0], cube_matrix[2]]

    all_polygons = [
        polyDown1,
        polyDown2,
        polyTop1,
        polyTop2,
        polyLeft1,
        polyLeft2,
        polyRight1,
        polyRight2,
        polyFront1,
        polyFront2,
        polyBack1,
        polyBack2
    ]
    return all_polygons

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

def avgPointInPolygon(polygon):
    sum = 0
    n = 0
    for p in polygon:
        sum += p
        n += 1
    avg = sum/n
    return avg

def distFromPointToPoint(p1, p2):
    d = sqrt( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2 )
    return d

def sortPoltgons(polygons, camera): 
    # sorting the polygons by the disdantes from the camera
    all_polygons = []
    sorted_polygons = []
    for polygon in polygons:
        centrum = avgPointInPolygon(polygon)
        dist = distFromPointToPoint(camera, centrum)
        all_polygons.append([dist, polygon])
    all_polygons.sort(key=lambda x: x[0]) # uses the first element of the list to sort
    for polygon in all_polygons:
        sorted_polygons.append(polygon[1])
    sorted_polygons.reverse() 
    return sorted_polygons

def getPointOnPlan(fig, plan, pov):  # lave liste af punkter på planen givet
    final = []
    for polygon in fig:
        polygon_2D = []  # Store 2D points for the current polygon
        for point in polygon:
            r = []
            for j in range(len(point)):
                a = float(point[j]) - pov[j]  # Ensure elements are scalars
                r.append(a)
            
            x = [float(pov[0]), r[0]]
            y = [float(pov[1]), r[1]]
            z = [float(pov[2]), r[2]]

            # Ensure scalar values are used in calculations
            x0, x1 = x[0], x[1]
            y0, y1 = y[0], y[1]
            z0, z1 = z[0], z[1]

            ligning_num = plan[0] * x0 + plan[1] * y0 + plan[2] * z0 + plan[3]
            ligning_t = plan[0] * x1 + plan[1] * y1 + plan[2] * z1

            t = (-(ligning_num)) / ligning_t

            decimals = 2
            point_2D = [
                round(y0 + t * y1, decimals),  # y-coordinate
                round(z0 + t * z1, decimals)   # z-coordinate
            ]
            polygon_2D.append(point_2D)  # Add the 2D point to the current polygon
        final.append(polygon_2D)  # Add the 2D polygon to the final list
    return final

def centerObject(polygons, screenWidth = 800, screenHeight = 600):
    centerY = screenWidth / 2
    centerZ = screenHeight / 2
    for polygon in polygons:
        for p in polygon:  # Iterate over each point in the polygon
            p[0] += centerY
            p[1] += centerZ
    return polygons

def drawPoints(points, screen):
    for p in points:
        pg.draw.circle(screen, RED, (p[0], p[1]), 1)

def drawPolygons(polygons, screen):
    n = 0
    for polygon in polygons:
        pg.draw.polygon(screen, colors[n//2], polygon)
        n += 1
        for p in polygon:
            pg.draw.circle(screen, RED, (p[0], p[1]), 10)

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
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        yaw += 0.05
    if keys[pg.K_d]:
        yaw -= 0.05
    if keys[pg.K_s]:
        pitch += 0.05
    if keys[pg.K_w]:
        pitch -= 0.05
    if keys[pg.K_UP]:
        skale += 1
    if keys[pg.K_DOWN]:
        skale -= 1
    if keys[pg.K_l]:
        fov += 1
    if keys[pg.K_k]:
        fov -= 1


    # Update game state
    camera = [fov, 0, 0] 
    skale_cube = [skale, skale, skale] # skale for cube
    transformed_cube = transformMatrix(skale_cube, [roll, pitch, yaw], cube_matrix)

    all_polygons_sorted = sortPoltgons(polygonsFromCubeMatrix(transformed_cube), camera) # sort the polygons by distance from the camera
    all_polygons_2D = getPointOnPlan(all_polygons_sorted, plan, camera) # get the points on the plane
    centerObject(all_polygons_2D, screenWidth, screenHeight) # center the object on the screen

    print("Camera:", camera)

    # Draw to the screen
    screen.fill(BLACK)
    
    drawPolygons(all_polygons_2D, screen) 

    # Flip the display
    pg.display.flip()

# Clean up
pg.quit()
sys.exit()
