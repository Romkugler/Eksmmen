import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screenWidth = 800
screenHeight = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

cube_matrix = [
    [-0.5, -0.5, -0.5],  # 0: Bottom-back-left
    [ 0.5, -0.5, -0.5],  # 1: Bottom-back-right
    [ 0.5,  0.5, -0.5],  # 2: Top-back-right
    [-0.5,  0.5, -0.5],  # 3: Top-back-left
    [-0.5, -0.5,  0.5],  # 4: Bottom-front-left
    [ 0.5, -0.5,  0.5],  # 5: Bottom-front-right
    [ 0.5,  0.5,  0.5],  # 6: Top-front-right
    [-0.5,  0.5,  0.5],  # 7: Top-front-left
]

transformtion_matrix = [
    
]

plan = [1, 0, 0, 0] # lignigen for plan [a, b, c, k] ax+by+cz+k=0
camera = [5, 0, 0] # koordinater for kamera [x, y, z]


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

a = getPointOnPlan(cube_matrix,plan,camera)
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


# Set up the display
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Pygame")

# Clock to control the frame rate
clock = pygame.time.Clock()
FPS = 60

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Update game state




    # Draw to the screen
    screen.fill(BLACK)

    # Flip the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
