import pygame

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Moving Text Right to Left")

# Define font
font = pygame.font.SysFont("Arial", 36)

# Text settings
text = "Hello, World!"
text_surface = font.render(text, True, (255, 255, 255))  # White text
text_width = text_surface.get_width()
text_height = text_surface.get_height()

# Variables to control text position
x_pos = screen_width  # Start from the right side of the screen
y_pos = (screen_height - text_height) // 2  # Center vertically
speed = 3  # Speed of movement

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen (black background)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the text from right to left
    x_pos -= speed
    
    # If text goes off the left side of the screen, reset to the start position
    if x_pos < -text_width:
        x_pos = screen_width

    # Draw the text
    screen.blit(text_surface, (x_pos, y_pos))

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)  # 60 frames per second

# Quit Pygame
pygame.quit()
