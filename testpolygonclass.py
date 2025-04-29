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
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
puprle = (255, 0, 255)
orange = (255, 165, 0)
colors = [red, green, blue, yellow, puprle, orange]

class Polygon:
    def __init__(self, color, points):
        self.color = color
        self.points = points

    def __str__(self):
        return f"{self.color}({self.points})"


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

def polygonsFromCubeMatrix(cube_matrix, colors):
    return [
        Polygon(colors[0], [cube_matrix[0], cube_matrix[1], cube_matrix[4]]),  # Bottom
        Polygon(colors[0], [cube_matrix[1], cube_matrix[5], cube_matrix[4]]),  # Bottom
        Polygon(colors[1], [cube_matrix[3], cube_matrix[2], cube_matrix[7]]),  # Top
        Polygon(colors[1], [cube_matrix[6], cube_matrix[2], cube_matrix[7]]),  # Top
        Polygon(colors[2], [cube_matrix[0], cube_matrix[3], cube_matrix[4]]),  # Left
        Polygon(colors[2], [cube_matrix[7], cube_matrix[3], cube_matrix[4]]),  # Left
        Polygon(colors[3], [cube_matrix[1], cube_matrix[2], cube_matrix[5]]),  # Right
        Polygon(colors[3], [cube_matrix[6], cube_matrix[2], cube_matrix[5]]),  # Right
        Polygon(colors[4], [cube_matrix[4], cube_matrix[5], cube_matrix[6]]),  # Front
        Polygon(colors[4], [cube_matrix[7], cube_matrix[4], cube_matrix[6]]),  # Front
        Polygon(colors[5], [cube_matrix[0], cube_matrix[1], cube_matrix[2]]),  # Back
        Polygon(colors[5], [cube_matrix[3], cube_matrix[0], cube_matrix[2]])   # Back
    ]

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
    sum_x, sum_y, sum_z = 0, 0, 0
    for point in polygon.points:
        sum_x += point[0]
        sum_y += point[1]
        sum_z += point[2]
    n = len(polygon.points)
    return [sum_x / n, sum_y / n, sum_z / n]

def distFromPointToPoint(p1, p2):
    d = sqrt( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2 )
    return d

def sortPoltgons(polygons, camera): 
    all_polygons = []
    for polygon in polygons:
        centrum = avgPointInPolygon(polygon)
        dist = distFromPointToPoint(camera, centrum)
        all_polygons.append([dist, polygon])
    all_polygons.sort(key=lambda x: x[0])  # Sort by distance
    return [polygon[1] for polygon in reversed(all_polygons)]  # Reverse and return sorted polygons

def getPointOnPlan(polygons, plan, pov):  # Create a list of points on the plane
    final = []
    for polygon in polygons:
        polygon_2D = []  # Store 2D points for the current polygon
        for point in polygon.points:
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
        final.append(Polygon(polygon.color, polygon_2D))  # Add the 2D polygon to the final list
    return final

def centerObject(polygons, screenWidth = 800, screenHeight = 600):
    [polygon.points for polygon in all_polygons_2D]
    centerY = screenWidth/2
    centerZ = screenHeight/2
    for polygon in polygons:
        for point in polygon.points:  # Iterate over each point in the polygon
            point[0] += centerY
            point[1] += centerZ
    return polygons

def drawPoints(points, screen):
    for p in points:
        pg.draw.circle(screen, red, (p[0], p[1]), 1)

def drawPolygons(polygons, screen):
    for polygon in polygons:
        pg.draw.polygon(screen, polygon.color, polygon.points)


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
    skale_cube = [skale, skale, skale]  # Scale for cube
    transformed_cube = transformMatrix(skale_cube, [roll, pitch, yaw], cube_matrix)

    # Generate polygons with colors
    all_polygons = polygonsFromCubeMatrix(transformed_cube, colors)

    # Sort polygons by distance
    all_polygons_sorted = sortPoltgons(all_polygons, camera)

    # Project polygons onto the 2D plane
    all_polygons_2D = getPointOnPlan(all_polygons_sorted, plan, camera)

    # Center the object on the screen
    centerObject([polygon.points for polygon in all_polygons_2D], screenWidth, screenHeight)

    # Draw to the screen
    screen.fill(black)
    drawPolygons(all_polygons_2D, screen)

    # Flip the display
    pg.display.flip()

# Clean up
pg.quit()
sys.exit()
