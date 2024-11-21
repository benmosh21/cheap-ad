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

Roboto_Black = "Roboto/Roboto-Black.ttf"

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

    def draw(self, screen):
        self.mouseover()
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

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
        
    def event(self, event, *args):
        isReleased = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                isReleased = False
        elif not(isReleased) or event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
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

    def func(self, antimatterAmount=0):
        if self.cost <= antimatterAmount:
            print(self.name)
            self.amount += 1
            antimatterAmount -= self.cost
            if self.amount%10 == 0:
                self.cost *= self.costMult
                self.powerMult *= 2
            self.preduce += 1
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
        self.allDimentions = [Dimention("AD_1", pow(10, 1), pow(10, 3), 1, 0), Dimention("AD_2", pow(10, 2), pow(10, 4), 1, 0), 
                              Dimention("AD_3", pow(10, 4), pow(10, 5), 1, 0), Dimention("AD_4", pow(10, 6), pow(10, 6), 1, 0),
                              Dimention("AD_5", pow(10, 9), pow(10, 8), 1, 0), Dimention("AD_6", pow(10, 13), pow(10, 10), 1, 0),
                              Dimention("AD_7", pow(10, 18), pow(10, 12), 1, 0), Dimention("AD_8", pow(10, 24), pow(10, 15), 1, 0)]
        self.dButtons = []
        self.dTxtAmount = []
        self.dTxtPreduce = []
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
    
    def DimentionsUI(self):
        count = 0
        for dimention in self.allDimentions:
            self.dButtons.append(Button((200, 150+60*count), (350,50), (200,200,200), (255, 0, 0), self.allDimentions[count].func, f"button {count+1}, cost: {numToExpones(dimention.cost)}", Roboto_Black, 30,  (0,0,0)))
            self.dTxtAmount.append(Text(f"({dimention.amount%10})", Roboto_Black, "Black", (800, 150+60*count), 30))
            self.dTxtPreduce.append(Text(f"{dimention.preduce}", Roboto_Black, "Black", (500, 150+60*count), 30))
            count += 1

    def draw(self, screen):
        count1 = 0
        for b in self.dButtons:
            b.txt = f"button {count1+1}, cost: {numToExpones(self.allDimentions[count1].cost)}"
            b.draw(screen)
            count1+=1
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

    def event(self, event):
        for b in self.dButtons:
            t = b.event(event, self.AntimatterAmount)
            if t is not None:
                print(t)
                self.AntimatterAmount = t

    def update(self, screen):
        self.draw(screen)
        return(self.ADsProduction())



def numToExpones(num):
    if num > 0:
        if num < 1.18e+308:
            num1 = num
            base = int(math.log(num, 10))
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

        scoreText.draw(screen)
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
