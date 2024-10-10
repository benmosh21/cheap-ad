import signal
import msvcrt
import time
import base64
import pygame
import math

pygame.init()
pygame.display.init()

screen = pygame.display.set_mode([1200, 700])

pygame.display.set_caption("AD cheap yes graphics knockoff")


class Text:
    def __init__(self, text, font, color, pos, font_size):
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, font_size)
        self.color = color
        self.pos = pos


    def draw(self, screen):
        self.text_surface = self.font.render(self.text, False, self.color)
        screen.blit(self.text_surface, self.pos)


class Button:
    def __init__(self, text, color, pos, size):
        self.pos = pos
        self.size = size
        self.color = color
        self.text = text

    def draw(self, screen):
        self.button_surface = pygame.Surface(self.size)
        self.text.pos = self.text.text_surface.get_rect(center=(self.button_surface.get_width()/2, self.button_surface.get_height()/2))
    
    def isClick(self):
        pass

class Dimention:
    def __init__(self, name, baseCost, costMult, powerMult, amount):
        self.name = name
        self.baseCost = baseCost
        self.costMult = costMult
        self.powerMult = powerMult
        self.amount = amount
        

class Antimatter:

    def __init__(self) -> None:
        self.AntimatterAmount = 10
        self.Dimentions = 0
        self.allDimentions = [Dimention("AD_1", pow(10, 1), pow(10, 3), 1.16, 4), Dimention("AD_2", pow(10, 2), pow(10, 4), 1.16, 0), 
                              Dimention("AD_3", pow(10, 4), pow(10, 5), 1.16, 0), Dimention("AD_4", pow(10, 6), pow(10, 6), 1.16, 0),
                              Dimention("AD_5", pow(10, 9), pow(10, 8), 1.16, 0), Dimention("AD_6", pow(10, 13), pow(10, 10), 1.23, 0),
                              Dimention("AD_7", pow(10, 18), pow(10, 12), 1.16, 0), Dimention("AD_8", pow(10, 24), pow(10, 15), 1.16, 0)]
        
    def addAntimatter(self):
        for dimention in self.allDimentions:
            self.AntimatterAmount += dimention.amount*dimention.powerMult
        return self.AntimatterAmount

def numToExpones(num):
    num1 = num
    base = int(math.log(num, 10))
    if base < 3:
        return (f"{num:.2f}")
    else:
        return str((f"{(num/(pow(10, base))):.2f}"))+"e"+str(base)


def main(isRunning):
    score = 0
    clock = pygame.time.Clock()

    scoreText = Text("", "Roboto/Roboto-Black.ttf", "black", (400, 40), 30)
    ADs = Antimatter()
    while isRunning:

        screen.fill("white")

        scoreText.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

        pygame.display.flip()
        scoreText.text = "Antimatter Amount " + str(numToExpones(ADs.AntimatterAmount))
        score+=ADs.addAntimatter()
        #print(ADs.addAntimatter())
        clock.tick(50)
            
    pygame.quit()


if __name__ == '__main__':
    main(True)