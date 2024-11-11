import pygame
import math
import random as rnd

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Filling Circle")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)

# Circle settings
CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 10
progress = 0  # starting progress percentage
cps = 0.1

# Clock to control frame rate
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Calculate the end angle in radians based on progress (0 to 100%)
    end_angle = 2 * math.pi * (progress / 100) 

    # Create a filled "pie slice" by drawing a polygon with the center and points on the circumference
    points = [CENTER]
    num_steps = max(3, int(end_angle * 180 / math.pi / 5))  # Ensure we have at least 3 points
    for step in range(num_steps + 1):  # Go up to the end angle
        angle = step * end_angle / num_steps
        x = CENTER[0] + RADIUS * math.cos(angle)
        y = CENTER[1] + RADIUS * math.sin(angle)
        points.append((x, y))

    # Draw the filled part of the circle if we have enough points
    if len(points) > 2:
        pygame.draw.polygon(screen, BLUE, points)

    # Increase progress until it reaches 100%
    if progress < 100:
        progress += cps*100/60  # Adjust this value for speed (lower is slower)
    else:
        BLUE = rnd.choice(["BLUE","RED","BLACK","GREEN","PINK"])
        progress = 0
        cps *= 1.1
    # Draw the outer circle
    pygame.draw.circle(screen, BLUE, CENTER, RADIUS, 3)

    font = pygame.font.Font(None, 36)
    textsurf = font.render(f"Cycles per second: {cps:.2f}", False, "BLACK")
    screen.blit(textsurf, (75,25))
    
    # Update display and set frame rate
    pygame.display.flip()
    clock.tick(60)  # 60 frames per second

# Quit Pygame
pygame.quit()
