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
    sum_x = 0
    sum_y = 0
    sum_z = 0

    for point in polygon.points:
        sum_x += point[0]
        sum_y += point[1]
        sum_z += point[2]
    n = len(polygon.points)
    avg = [sum_x/n, sum_y/n, sum_z/n]
    return avg

def distFromPointToPoint(p1, p2):
    d = sqrt( (p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2 )
    return d

def sortPoltgons(polygons, camera): 
    # sorting the polygons by the disdantes from the camera (Painter's algorithm)
    all_polygons = []
    sorted_polygons = []
    for polygon in polygons:
        centrum = avgPointInPolygon(polygon)
        dist = distFromPointToPoint(camera, centrum)
        all_polygons.append([dist, polygon])
    all_polygons.sort(key=lambda x: x[0])  # Sort by distance
    for polygon in all_polygons:
        sorted_polygons.append(polygon[1])
    sorted_polygons.reverse() 
    return sorted_polygons

def getPointOnPlan(polygons, plan, pov):  #creates a list of points on a plane
    final = []
    for polygon in polygons:
        polygon_2D = []  
        for point in polygon.points:
            r = []
            for j in range(len(point)):
                a = float(point[j]) - pov[j] 
                r.append(a)
            
            x = [float(pov[0]), r[0]]
            y = [float(pov[1]), r[1]]
            z = [float(pov[2]), r[2]]

            ligning_num = plan[0]*x[0] + plan[1]*y[0] + plan[2]*z[0] + plan[3]
            ligning_t = plan[0]*x[1] + plan[1]*y[1] + plan[2]*z[1]

            t = (-(ligning_num))/ligning_t

            decimals = 2
            point_2D = [
                round(y[0] + t * y[1], decimals),  # y coords
                round(z[0] + t * z[1], decimals)   # z coords
            ]
            polygon_2D.append(point_2D) 
        final.append(Polygon(polygon.color, polygon_2D)) 
    return final

def centerObject(polygons, screenWidth = 800, screenHeight = 600):
    all_points = []
    for polygon in all_polygons_2D:
        all_points.append(polygon.points)
    centerY = screenWidth / 2
    centerZ = screenHeight / 2
    for polygon in polygons:
        for point in polygon.points:  # Iterate over each point in the polygon
            point[0] += centerY
            point[1] += centerZ
    return polygons

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
    skale_cube = [skale, skale, skale] # skale for cube
    transformed_cube = transformMatrix(skale_cube, [roll, pitch, yaw], cube_matrix)

    all_polygons = polygonsFromCubeMatrix(transformed_cube, colors)

    all_polygons_sorted = sortPoltgons(all_polygons, camera)
    all_polygons_2D = getPointOnPlan(all_polygons_sorted, plan, camera)
    
    centerObject(all_polygons_2D, screenWidth, screenHeight) 

    print("Camera:", camera)

    # Draw to the screen
    screen.fill(black)
    
    drawPolygons(all_polygons_2D, screen) 

    # Flip the display
    pg.display.flip()

# Clean up
pg.quit()
sys.exit()
