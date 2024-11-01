import signal
import msvcrt
import time
import base64
import pygame
import math
from typing import Union
import pygame.gfxdraw

pygame.init()
pygame.display.init()

screen = pygame.display.set_mode([1200, 700])

pygame.display.set_caption("AD cheap yes graphics knockoff")

Roboto_Black = "Roboto/Roboto-Black.ttf"

class Text:
    def __init__(self, text, font, color, pos, font_size):
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, font_size)
        self.color = color
        self.pos = pos

    def draw_centeredx(self, posy, screen):
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect(center=(screen.get_width() // 2, posy))
        screen.blit(self.text_surface, self.text_rect)
    
    def draw(self, screen):
        self.text_surface = self.font.render(self.text, False, self.color)
        screen.blit(self.text_surface, self.pos)


class Button:
    def __init__(self, position, size, clr, cngclr, func, text, font, font_size, font_clr,outline_clr, corner_radius, outline_width):
        self.x, self.y = position
        self.width, self.height = size
        self.clr    = clr
        self.size   = size
        self.func   = func
        self.outlineSize = outline_width
        self.surf = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)
        self.outlineColor = outline_clr
        self.cornerRad = corner_radius

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])


        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.outline_rect = pygame.Rect(self.x - self.outlineSize, self.y - self.outlineSize, self.width + 2 * self.outlineSize, self.height + 2 * self.outlineSize)
        self.collisionbox = self.outline_rect

    def draw(self,surface):
        self.mouseover()

        # Draw the outline first (larger rectangle)
        outline_rect = pygame.Rect(self.x - self.outlineSize, self.y - self.outlineSize, self.width + 2 * self.outlineSize, self.height + 2 * self.outlineSize)
        pygame.draw.rect(surface, self.outlineColor, outline_rect, border_radius=self.cornerRad + self.outlineSize)

        # Draw the inner filled rectangle (smaller rectangle)
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.curclr, button_rect, border_radius=self.cornerRad)
    
        text_surface = self.font.render(self.txt, True, self.font_clr)  # Render text 
        text_rect = text_surface.get_rect(center=button_rect.center)  # Center the text on the button
        surface.blit(text_surface, text_rect)

        self.collisionbox = outline_rect

    def draw_centeredx(self,surface):
        self.mouseover()

        self.rectOuter   = self.surf.get_rect(center=((screen.get_width() // 2, self.y)))
        # Draw the outline first (larger rectangle)
        x,y,width,height = self.rectOuter
        outline_rect = pygame.Rect(x - self.outlineSize, y - self.outlineSize, width + 2 * self.outlineSize, height + 2 * self.outlineSize)
        pygame.draw.rect(surface, self.outlineColor, outline_rect, border_radius=self.cornerRad + self.outlineSize)

        # Draw the inner filled rectangle (smaller rectangle)
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, self.curclr, button_rect, border_radius=self.cornerRad)

        text_surface = self.font.render(self.txt, True, self.font_clr)  # Render text in white
        text_rect = text_surface.get_rect(center=button_rect.center)  # Center the text on the button
        surface.blit(text_surface, text_rect)

        self.collisionbox = outline_rect

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.collisionbox.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            return self.func(*args)
        
    def event(self, event, *args):
        isReleased = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                isReleased = False
        elif not(isReleased) or event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.collisionbox.collidepoint(pos):
                isReleased= True
                return self.call_back(*args)
                            

class Dimention:
    def __init__(self, name, baseCost, costMult, powerMult, amount):
        self.name = name
        self.baseCost = baseCost
        self.costMult = costMult
        self.powerMult = powerMult
        self.amount = amount

        self.cost = baseCost
        self.preduce = 0

    def func(self, antimatterAmount=0): #buying a dimension
        if self.cost <= antimatterAmount:
            print(self.name)
            self.amount += 1
            antimatterAmount -= self.cost
            if self.amount%10 == 0:
                self.cost *= self.costMult
                self.powerMult *= 2
            self.preduce += 1
            return antimatterAmount
    
    def funcx10(self, antimatterAmount=0): # buying up to 10 dimension
        toTen = (10 - int(str(self.amount)[-1]))
        if toTen * self.cost <= antimatterAmount: #finds amount to 10 and checks if you have enough to buy
            print(self.name)
            self.amount += toTen
            antimatterAmount -= toTen*self.cost
            self.cost *= self.costMult
            self.powerMult *= 2
            self.preduce += toTen
            return antimatterAmount

        

class Antimatter:
    def __init__(self,fps):
        self.clock = pygame.time.Clock()
        self.tickspeed = 1
        self.tickspeedMult = 1.125
        self.tickspeedCost = pow(10,3)
        self.fps = fps
        self.dt = self.clock.tick(self.fps)/1000
        self.AntimatterAmount = 10
        self.Dimentions = 0
        self.BAB = None
        self.allDimentions = [Dimention("AD_1", pow(10, 1), pow(10, 3), 1, 0), Dimention("AD_2", pow(10, 2), pow(10, 4), 1, 0), 
                              Dimention("AD_3", pow(10, 4), pow(10, 5), 1, 0), Dimention("AD_4", pow(10, 6), pow(10, 6), 1, 0),
                              Dimention("AD_5", pow(10, 9), pow(10, 8), 1, 0), Dimention("AD_6", pow(10, 13), pow(10, 10), 1, 0),
                              Dimention("AD_7", pow(10, 18), pow(10, 12), 1, 0), Dimention("AD_8", pow(10, 24), pow(10, 15), 1, 0)]
        self.dButtons = []
        self.dTxtAmount = []
        self.dTxtPreduce = []
        self.dButtonsx10 = []

        self.DimentionsUI()
    
    def ADsProduction(self):
        self.dt = self.clock.tick(self.fps)/1000
        count = len(self.allDimentions)-1
        while count > 0:
            #print(self.allDimentions[count].name)
            self.allDimentions[count-1].preduce += self.allDimentions[count].powerMult*self.allDimentions[count].preduce*self.tickspeed*self.dt
            count-=1
        self.AntimatterAmount += self.allDimentions[0].preduce*self.allDimentions[0].powerMult*self.tickspeed*self.dt
        return self.AntimatterAmount
    
    def buyAll(self):
        for d in self.allDimentions[::-1]:
            while d.cost <= self.AntimatterAmount:
                self.AntimatterAmount = d.func(self.AntimatterAmount)

    def DimentionsUI(self):
        count = 0
        for dimention in self.allDimentions:
            self.dButtons.append(Button((25, 150+60*count), (350,50), (200,200,200), (255, 0, 0), self.allDimentions[count].func, f"button {count+1}, cost: {numToExpones(dimention.cost)}", Roboto_Black, 30,  (0,0,0), "black", 10, 1))
            self.dButtonsx10.append(Button((825, 150+60*count), (350,50), (200,200,200), (255, 0, 0), self.allDimentions[count].funcx10, f"buy 10 of tier {count+1}, cost: {numToExpones((10 - int(str(self.allDimentions[count].amount)[-1]))*dimention.cost)}", Roboto_Black, 30,  (0,0,0), "black", 10, 1))
            self.dTxtAmount.append(Text(f"({dimention.amount%10})", Roboto_Black, "Black", (750, 150+60*count), 30))
            self.dTxtPreduce.append(Text(f"{dimention.preduce}", Roboto_Black, "Black", (450, 150+60*count), 30))
            count += 1
        self.BAB = Button((500, 100), (100, 50), (200,200,200), (255, 0, 0), self.buyAll, f"Buy All", Roboto_Black, 30, (0,0,0), "black", 10, 1)

    def draw(self, screen):
        count1 = 0
        for b in self.dButtons:
            b.txt = f"button {count1+1}, cost: {numToExpones(self.allDimentions[count1].cost)}"
            b.draw(screen)
            count1+=1
        countx10 = 0
        for b in self.dButtonsx10:
            b.txt = f"buy 10 of tier {countx10+1}, cost: {numToExpones((10 - int(str(self.allDimentions[countx10].amount)[-1]))*self.allDimentions[countx10].cost)}"
            b.draw(screen)
            countx10+=1
        count2 = 0
        for tA in self.dTxtAmount:
            tA.text = f"({self.allDimentions[count2].amount%10})"
            tA.draw(screen)
            count2+=1
        count3 = 0
        for tP in self.dTxtPreduce:
            tP.text = f"{numToExpones(self.allDimentions[count3].preduce)}"
            tP.draw(screen)
            count3+=1
        if self.BAB:
            self.BAB.draw_centeredx(screen)
    def event(self, event):
        for b in self.dButtons:
            t = b.event(event, self.AntimatterAmount)
            if t is not None:
                print(t)
                self.AntimatterAmount = t
        for bx10 in self.dButtonsx10:
            t = bx10.event(event, self.AntimatterAmount)
            if t is not None:
                print(t)
                self.AntimatterAmount = t
        self.BAB.event(event)

    def update(self, screen):
        self.draw(screen)
        return(self.ADsProduction())



def numToExpones(num):
    if num > 0:
        if num < 1.18e308:
            base = len(str(num).split(".")[0])-1 #splits the number into the int part and the decimal part and then  removes one from the length of the int part
            if base < 3:
                return (f"{num:.2f}")
            else:
                return str((f"{(num/(pow(10, base))):.2f}"))+"e"+str(base)
    else:
        return str(f"{num}")

def test():
    print("test")

def main(isRunning):
    score = 0
    fps = 20

    scoreText = Text("", Roboto_Black, "black", (400, 40), 30)
    ADs = Antimatter(fps)
    while isRunning:

        screen.fill("white")

        scoreText.draw_centeredx(40,screen)
        #button.draw(screen)

        score += ADs.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

            ADs.event(event)

        pygame.display.flip()
        scoreText.text = "Antimatter Amount " + str(numToExpones(ADs.AntimatterAmount))
            
    pygame.quit()


if __name__ == '__main__':
    main(True)
