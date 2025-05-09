import pygame as pg
import sys
import numpy as np 
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

pg.init()

screenWidth = 800
screenHeight = 600

black = (0, 0, 0)
white = (255, 255, 255)
white2 = (200, 200, 200)
red = (255, 0, 0)
red2 = (200, 0, 0)
green = (0, 255, 0)
green2 = (0, 200, 0)
blue = (0, 0, 255)
blue2 = (0, 0, 200)
yellow = (255, 255, 0)
yellow2 = (200, 200, 0)
puprle = (255, 0, 255)
puprle2 = (200, 0, 200)
orange = (255, 165, 0)
orange2 = (200, 100, 0)
colors = [red, orange, blue, green, white, yellow]
colors2 = [red2, orange2, blue2, green2, white2, yellow2]

class Polygon:
    def __init__(self, color, points):
        self.color = color
        self.points = points

    def __str__(self):
        return f"{self.color}({self.points})"

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
        Polygon(colors2[0],  [cube_matrix[0], cube_matrix[1], cube_matrix[4]]), # Bottom
        Polygon(colors[0], [cube_matrix[1], cube_matrix[5], cube_matrix[4]]),   # Bottom
        Polygon(colors2[1],  [cube_matrix[3], cube_matrix[2], cube_matrix[7]]), # Top
        Polygon(colors[1], [cube_matrix[6], cube_matrix[2], cube_matrix[7]]),   # Top
        Polygon(colors2[2],  [cube_matrix[0], cube_matrix[3], cube_matrix[4]]), # Left
        Polygon(colors[2], [cube_matrix[7], cube_matrix[3], cube_matrix[4]]),   # Left
        Polygon(colors2[3],  [cube_matrix[1], cube_matrix[2], cube_matrix[5]]), # Right
        Polygon(colors[3], [cube_matrix[6], cube_matrix[2], cube_matrix[5]]),   # Right
        Polygon(colors2[4],  [cube_matrix[4], cube_matrix[5], cube_matrix[6]]), # Front
        Polygon(colors[4], [cube_matrix[7], cube_matrix[4], cube_matrix[6]]),   # Front
        Polygon(colors2[5],  [cube_matrix[0], cube_matrix[1], cube_matrix[2]]), # Back
        Polygon(colors[5], [cube_matrix[3], cube_matrix[0], cube_matrix[2]])    # Back
    ]

def movePointsXYZ(points, x, y, z):
    for point in points:
        point[0] += x
        point[1] += y
        point[2] += z


def transformMatrix(skale, rotation, matrix): # skale = [x, y, z] rotation = [roll, pitch, yaw] 
    # Skale matrix
    scale_matrix = np.array([
        [skale[0], 0, 0],
        [0, skale[1], 0],
        [0, 0, skale[2]]
    ])
    # Rotation x matrix roll
    rotation_matrix_x = np.array([
        [1, 0, 0],
        [0, cos(rotation[0]), -sin(rotation[0])],
        [0, sin(rotation[0]), cos(rotation[0])]
    ])
    # Rotation y matrix pitch
    rotation_matrix_y = np.array([
        [cos(rotation[1]), 0, sin(rotation[1])],
        [0, 1, 0],
        [-sin(rotation[1]), 0, cos(rotation[1])]
    ])
    # Rotation z matrix yaw
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
    d = sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)
    return d

def sortPolygons(polygons, camera): 
    # sorting the polygons by the disdantes from the camera (Painter's algorithm)
    all_polygons = []
    sorted_polygons = []
    for polygon in polygons:
        centrum = avgPointInPolygon(polygon)
        dist = distFromPointToPoint(camera, centrum)
        all_polygons.append([dist, polygon])
    all_polygons.sort(key=lambda x: x[0])  # Sort by distance index 0
    for polygon in all_polygons:
        sorted_polygons.append(polygon[1])
    sorted_polygons.reverse() 
    return sorted_polygons

def avgPointOnLine(point1, point2):
    sum_x = point1[0]+point2[0]
    sum_y = point1[1]+point2[1]
    sum_z = point1[2]+point2[2]

    avg = [sum_x/2, sum_y/2, sum_z/2]
    return avg

def middleOfLongestSide(polygon):
    a = (polygon.points[0], polygon.points[1])
    b = (polygon.points[1], polygon.points[2])
    c = (polygon.points[2], polygon.points[0])

    len_a = distFromPointToPoint(*a)
    len_b = distFromPointToPoint(*b)
    len_c = distFromPointToPoint(*c)

    lens = [len_a, len_b, len_c]
    lens.sort()
    biggest_len = lens[-1]

    if biggest_len == len_a:
        return avgPointOnLine(*a)
    if biggest_len == len_b:
        return avgPointOnLine(*b)
    if biggest_len == len_c:
        return avgPointOnLine(*c)
    else:
        return None

def sortPolygons2(polygons, camera):
    all_polygons = []
    sorted_polygons = []
    for polygon in polygons:
        hyp = middleOfLongestSide(polygon)
        dist = distFromPointToPoint(camera, hyp)
        all_polygons.append([dist, polygon])  
    all_polygons.sort(key=lambda x: x[0])  # Sort by distance index 0
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

            point_2D = [
                y[0] + t * y[1],
                z[0] + t * z[1]
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
        for point in polygon.points: 
            point[0] += centerY
            point[1] += centerZ
    return polygons

def drawPolygons(polygons, screen):
    for polygon in polygons:
        pg.draw.polygon(screen, polygon.color, polygon.points)
        for point in polygon.points:
            pg.draw.circle(screen, black, (int(point[0]), int(point[1])), 10)
            pg.draw.circle(screen, blue, (int(point[0]), int(point[1])), 8) 

screen = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("Pygame")

clock = pg.time.Clock()
FPS = 60

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Events
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
    if keys[pg.K_q]:
        roll += 0.05
    if keys[pg.K_e]:
        roll -= 0.05
    if keys[pg.K_UP]:
        skale += 1
    if keys[pg.K_DOWN]:
        skale -= 1
    if keys[pg.K_l]:
        fov += 10
    if keys[pg.K_k]:
        fov -= 10
    if keys[pg.K_y]:
        movePointsXYZ(cube_matrix, 0, -0.1, 0)
    if keys[pg.K_h]:
        movePointsXYZ(cube_matrix, 0, 0.1, 0)
    
    # Updates
    camera = [fov, 0, 0] 
    skale_cube = [skale, skale, skale] # skale for cube
    transformed_cube = transformMatrix(skale_cube, [roll, pitch, yaw], cube_matrix)
    all_polygons = polygonsFromCubeMatrix(transformed_cube, colors)
    all_polygons_sorted = sortPolygons2(all_polygons, camera)
    all_polygons_2D = getPointOnPlan(all_polygons_sorted, plan, camera)
    centerObject(all_polygons_2D, screenWidth, screenHeight) 

    clock.tick()
    #print("FPS: ", clock.get_fps())    

    # Drawing
    screen.fill(black)
    drawPolygons(all_polygons_2D, screen) 

    # flip display
    pg.display.flip()
pg.quit()
sys.exit()
