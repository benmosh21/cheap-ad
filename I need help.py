import pygame
import sys

# Initialize Pygame
pygame.init()

# Get the display's screen size
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h-50

# Create a windowed display with the screen size
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Maximized Windowed Mode")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Press ESC to close the window
                running = False

    # Clear the screen with a color, e.g., black
    screen.fill((0, 0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
