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

polyDown1 = [cube_matrix[0], cube_matrix[1], cube_matrix[4]]
polyDown2 = [cube_matrix[4], cube_matrix[1], cube_matrix[4]]
polyTop1 = [cube_matrix[3], cube_matrix[2], cube_matrix[7]]
polyTop2 = [cube_matrix[6], cube_matrix[2], cube_matrix[7]]
polyLeft1 = [cube_matrix[0], cube_matrix[3], cube_matrix[4]]
polyLeft2 = [cube_matrix[7], cube_matrix[3], cube_matrix[4]]
polyRight1 = [cube_matrix[1], cube_matrix[2], cube_matrix[5]]
polyRight2 = [cube_matrix[6], cube_matrix[2], cube_matrix[5]]
polyFront1 = [cube_matrix[4], cube_matrix[5], cube_matrix[6]]
polyFront2 = [cube_matrix[7], cube_matrix[5], cube_matrix[6]]
polyBack1 = [cube_matrix[0], cube_matrix[1], cube_matrix[2]]
polyBack1 = [cube_matrix[3], cube_matrix[1], cube_matrix[2]]

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
polyBack1
]

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
    all_polygons.sort()
    for polygon in all_polygons:
        sorted_polygons.append(polygon[1])
    return sorted_polygons




