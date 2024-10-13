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
    def __init__(self, position, size, clr, cngclr, func, text, font, font_size, font_clr):
        self.clr    = clr
        self.size   = size
        self.func   = func
        self.surf   = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])


        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()

        self.surf.fill(self.curclr)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            return self.func(*args)
        
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.rect.collidepoint(pos):
                        self.call_back()


class Dimention:
    def __init__(self, name, baseCost, costMult, powerMult, amount):
        self.name = name
        self.baseCost = baseCost
        self.costMult = costMult
        self.powerMult = powerMult
        self.amount = amount

    def func(self):
        print(self.name)
        

class Antimatter:

    def __init__(self) -> None:
        self.AntimatterAmount = 10
        self.Dimentions = 0
        self.allDimentions = [Dimention("AD_1", pow(10, 1), pow(10, 3), 1.16, 4), Dimention("AD_2", pow(10, 2), pow(10, 4), 1.16, 0), 
                              Dimention("AD_3", pow(10, 4), pow(10, 5), 1.16, 0), Dimention("AD_4", pow(10, 6), pow(10, 6), 1.16, 0),
                              Dimention("AD_5", pow(10, 9), pow(10, 8), 1.16, 0), Dimention("AD_6", pow(10, 13), pow(10, 10), 1.23, 0),
                              Dimention("AD_7", pow(10, 18), pow(10, 12), 1.16, 0), Dimention("AD_8", pow(10, 24), pow(10, 15), 1.16, 0)]
        self.dButtons = []

        self.DimentionsButton()


    def addAntimatter(self):
        for dimention in self.allDimentions:
            self.AntimatterAmount += dimention.amount*dimention.powerMult
        return self.AntimatterAmount
    
    def DimentionsButton(self):
        count = 0
        for dimention in self.allDimentions:
            self.dButtons.append(Button((80, 150+60*count), (100,50), (200,200,200), (255, 0, 0), self.allDimentions[count].func, f"button {count+1}", "Roboto/Roboto=Black.ttf", 30,  (0,0,0)))
            count += 1

    def draw(self, screen):
        for b in self.dButtons:
            b.draw(screen)

    def event(self, event):
        for b in self.dButtons:
            b.event(event)


def numToExpones(num):
    num1 = num
    base = int(math.log(num, 10))
    if base < 3:
        return (f"{num:.2f}")
    else:
        return str((f"{(num/(pow(10, base))):.2f}"))+"e"+str(base)

def test():
    print("test")

def main(isRunning):
    score = 0
    clock = pygame.time.Clock()

    scoreText = Text("", "Roboto/Roboto-Black.ttf", "black", (400, 40), 30)
    ADs = Antimatter()
    while isRunning:

        screen.fill("white")

        scoreText.draw(screen)
        #button.draw(screen)

        ADs.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

            ADs.event(event)

        pygame.display.flip()
        scoreText.text = "Antimatter Amount " + str(numToExpones(ADs.AntimatterAmount))
        score+=ADs.addAntimatter()


        clock.tick(50)
            
    pygame.quit()


if __name__ == '__main__':
    main(True)