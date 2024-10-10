import pygame
import pygame.gfxdraw
import time
from typing import Union
# Initialize Pygame
pygame.init()


# Set up the game window
WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Make window resizable
pygame.display.set_caption("Score Game")

# Center text around a coordinate
def render_centered_text(text, font, screen, width, height, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width , height))
    screen.blit(text_surface, text_rect)



# Numbers above 1000
def eform(x):
    if x > 999:
        zeros = 0
        for i in str(x):
            if i == ".":
                return(eform(int(x)))
            else:
                zeros +=1
        return(f"{str(x/10**(zeros-1))[:3:]}e{zeros}")
    return(int(x))        


def intabove(x,minim,exitmenumessage,exitprompt):
   if x == exitprompt:
       return(exitprompt)
   n = x
   while not type(n) == int:
        try:
            int(n)
        except ValueError:
            if x == exitprompt:
                return(exitprompt)
            print(f"Error, {n} is not a whole number:")
            n = Input(f"Please enter a whole number above or equal to {minim}. {exitmenumessage}\n",input_time,exitprompt)
        else:
            if n == exitprompt:
                return(exitprompt)
            if int(n) >= minim:
                x = int(n)
                return(x)
            else:
                return(intabove(Input(f"Error, {n} is not a whole:\nPlease enter a whole number above or equal to {minim}. {exitmenumessage}\n",input_time,exitprompt),minim))


# Set up fonts
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (204,247,255)
BUTTON_COLOR = WHITE 
OUTLINE_COLOR = RED
# Score
score = 0.0  # Use float to allow fractional scores

# Dimensions
gens = [[1,10,1,1],[0,100,0,1],[0,10**4,0,1],[0,10**6,0,1],[0,10**9,0,1],[0,10**13,0,1],[0,10**18,0,1],[0,10**24,0,1]]
class dimension:
    def __init__ (self,amount:Union[float,int,None],price:Union[float,int],bought:Union[int,None],mult:[float,int,None]):
        self.amount = 0
        if amount:
            self.amount = amount
        self.price = price
        self.bought = 0
        if bought:
            self.bought = bought
        self.mult =  1
        if mult:
            self.mult = mult
        
dim1 = dimension(1,10,0,1)
# Timer
timer = time.time()

# Fullscreen flag
is_fullscreen = False
# Buttons
class button:
    def __init__(self,outline_color: Union[tuple, None],fill_color: Union[tuple, None], coords : list,size : list ,corner_radius: Union[int, None], outline_width: Union[int, None]):
        self.surface = screen
        self.outline_color = RED
        if outline_color:
            self.outline_color = outline_color
        self.fill_color = WHITE
        if fill_color:
            self.fill_color = fill_color
        self.coords = coords
        self.size = size
        self.rect = self.coords + self.size
        self.corner_radius = 10
        if corner_radius:
            self.corner_radius = corner_radius
        self.outline_width = 1
        if outline_width:
            self.outliine_width = outline_width

button1 = button(None,None,[100,100],[100,100],None,None)




def draw_rounded_rect_with_outline(surface, outline_color, fill_color, rect, corner_radius, outline_width):
    x, y, width, height = rect

    # Draw the outline first (larger rectangle)
    outline_rect = pygame.Rect(x - outline_width, y - outline_width, width + 2 * outline_width, height + 2 * outline_width)
    pygame.draw.rect(surface, outline_color, outline_rect, border_radius=corner_radius + outline_width)

    # Draw the inner filled rectangle (smaller rectangle)
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, fill_color, button_rect, border_radius=corner_radius)
    
    # Return the inner button rect for collision detection
    return button_rect
# Create a clock object
clock = pygame.time.Clock()
FPS = 60  # Set your desired frames per second

def toggle_fullscreen():
    global screen, is_fullscreen, WIDTH, HEIGHT
    if is_fullscreen:
        # Exit fullscreen
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    else:
        # Enter fullscreen
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # Update WIDTH and HEIGHT to fullscreen size
        WIDTH, HEIGHT = screen.get_size()
    is_fullscreen = not is_fullscreen
# Game loop
graytime = 0
running = True
while running:
    screen.fill(BLACK)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                toggle_fullscreen()  # Press 'F' to toggle fullscreen
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resize
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if button_rect.collidepoint(mouse_pos):
                BUTTON_COLOR = GRAY  # Change the color when clicked
                graytime = time.time()
                OUTLINE_COLOR = GREEN
    # Draw a rounded rectangle and get button areas
    button_rect = draw_rounded_rect_with_outline(screen, OUTLINE_COLOR, BUTTON_COLOR, [WIDTH-300, 200, 250, 40], 10, 1)

    # Turn the button black again

    if time.time() - graytime > 0.1:
        BUTTON_COLOR = WHITE
        OUTLINE_COLOR = RED

    # Automatically increase score by 1/60 each frame
    for i in range(7):
        gens[i][0] += gens[i+1][0]/FPS
    score += gens[0][0] / FPS  # Increment score by 1/60 each frame


    # Display the score
    render_centered_text(f"You currently have {eform(score)} antimatter.", font, screen, (screen.get_width() // 2), 20 , WHITE)
    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(FPS)  # Limit to the desired FPS

# Quit Pygame
pygame.quit()
