import signal
import os
import msvcrt
import time
import base64
import pygame
import math
import json
import random as rnd
from typing import Union
import pygame.gfxdraw
from decimal import Decimal,getcontext

pygame.init()
pygame.display.init()

WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


pygame.display.set_caption("AD cheap yes graphics knockoff")

Roboto_Black = "Roboto/Roboto-Black.ttf"

getcontext().prec = 1000 #Decimal will now store up to 1000 digits of info



Savesfolder = os.path.join(os.getenv("APPDATA"), "Antimatter Dimensions")
os.makedirs(Savesfolder, exist_ok=True)  # Ensure the directory exists or create it
Savefile = os.path.join(Savesfolder, "save_game.json")

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
    def __init__(self, position, size, clr, cngclr, func, text, font, font_size, font_clr,outline_clr,outline_cngclr, corner_radius, outline_width, name = None, locked = False, lockedText = "Locked"):
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
        self.name = name
        self.locked = locked
        self.lockedtxt =  lockedText
        self.locked_color = (66, 57, 66)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr
        
        if outline_cngclr:
            self.outcngclr = outline_cngclr
        else:
            self.outcngclr = outline_clr
        if len(clr) == 4:
            self.surf.set_alpha(clr[3])
        
        if self.locked:
            self.curclr = self.locked_color
            self.txt = self.lockedtxt


        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.outline_rect = pygame.Rect(self.x - self.outlineSize, self.y - self.outlineSize, self.width + 2 * self.outlineSize, self.height + 2 * self.outlineSize)
        self.collisionbox = self.outline_rect

    def draw(self,surface):
        self.mouseover()

        # Draw the outline first (larger rectangle)
        outline_rect = pygame.Rect(self.x - self.outlineSize, self.y - self.outlineSize, self.width + 2 * self.outlineSize, self.height + 2 * self.outlineSize)
        pygame.draw.rect(surface, self.outline_curclr, outline_rect, border_radius=self.cornerRad + self.outlineSize)

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
        pygame.draw.rect(surface, self.outline_curclr, outline_rect, border_radius=self.cornerRad + self.outlineSize)

        # Draw the inner filled rectangle (smaller rectangle)
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, self.curclr, button_rect, border_radius=self.cornerRad)

        text_surface = self.font.render(self.txt, True, self.font_clr)  # Render text in white
        text_rect = text_surface.get_rect(center=button_rect.center)  # Center the text on the button
        surface.blit(text_surface, text_rect)

        self.collisionbox = outline_rect

    def mouseover(self):
        self.curclr = self.clr
        self.outline_curclr = self.outlineColor
        pos = pygame.mouse.get_pos()
        if self.collisionbox.collidepoint(pos):
            self.curclr = self.cngclr
            self.outline_curclr = self.outcngclr
        if self.locked:
            self.curclr = self.locked_color
            self.txt = self.lockedtxt

    def call_back(self, *args):
        if self.func:
            return self.func(*args)
        
    def event(self, event, *args):
        if not self.locked:
            isReleased = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    isReleased = False
            elif not(isReleased) or event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self.collisionbox.collidepoint(pos):
                    isReleased= True
                    return self.call_back(*args)
        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_b]:
                if self.name == "BAB":
                    return self.call_back(*args)
            elif keys[pygame.K_d]:
                if self.name == "DIMBOOST":
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

    def func(self, antimatterAmount=0, dims = 0): #buying a dimension
        if self.cost <= antimatterAmount and int(self.name[-1]) <= dims + 4:
            print(self.name)
            self.amount += 1
            antimatterAmount -= self.cost
            if self.amount%10 == 0:
                self.cost *= self.costMult
                self.powerMult *= 2
            self.preduce += 1
            return antimatterAmount
        return antimatterAmount
    
    def funcx10(self, antimatterAmount=0, dims = 0): # buying up to 10 dimension
        toTen = (10 - int(str(self.amount)[-1]))
        if toTen * self.cost <= antimatterAmount and int(self.name[-1]) <= dims + 4: #finds amount to 10 and checks if you have enough to buy
            print(self.name)
            self.amount += toTen
            antimatterAmount -= toTen*self.cost
            self.cost *= self.costMult
            self.powerMult *= 2
            self.preduce += toTen
            return antimatterAmount
        return antimatterAmount

        

class Antimatter:
    def __init__(self,fps):
        self.DEFAULTGAMESTATE = {
            "AntimatterAmount": 10,
            "fps": fps,
            "tickspeed": 1,
            "tickspeedCost": pow(10,3),
            "tickspeedMult": 1.125,
            "DimBoosts": 0,
            "DimBoostCost": [20,4],
            "Dimensions": [
                {"name":"AD_1","amount":0,"baseCost":pow(10, 1),"costMult":pow(10, 3),"powerMult": 1}, {"name":"AD_2","amount":0,"baseCost":pow(10, 2),"costMult":pow(10, 4),"powerMult": 1}, 
                {"name":"AD_3","amount":0,"baseCost":pow(10, 4),"costMult":pow(10, 5),"powerMult": 1}, {"name":"AD_4","amount":0,"baseCost":pow(10, 6),"costMult":pow(10, 6),"powerMult": 1},
                {"name":"AD_5","amount":0,"baseCost":pow(10, 9),"costMult":pow(10, 8),"powerMult": 1}, {"name":"AD_6","amount":0,"baseCost":pow(10, 13),"costMult":pow(10, 10),"powerMult": 1},
                {"name":"AD_7","amount":0,"baseCost":pow(10, 18),"costMult":pow(10, 12),"powerMult": 1}, {"name":"AD_8","amount":0,"baseCost":pow(10, 24),"costMult":pow(10, 15),"powerMult": 1}
            ]
        }
        self.clock = pygame.time.Clock()
        self.AntimatterAmount = self.DEFAULTGAMESTATE["AntimatterAmount"]
        self.DimBoosts =  self.DEFAULTGAMESTATE["DimBoosts"]
        self.DimBoostCost = self.DEFAULTGAMESTATE["DimBoostCost"]
        self.fps = fps
        self.tickspeed = self.DEFAULTGAMESTATE["tickspeed"]
        self.tickspeedMult = self.DEFAULTGAMESTATE["tickspeedMult"]
        self.tickspeedCost = self.DEFAULTGAMESTATE["tickspeedMult"]
        self.dt = self.clock.tick(self.fps)/1000
        self.wipeSaveClicks = 5
        self.Dimentions = 0
        self.DimBoostbutton = None
        self.BAB = None
        self.tickspeedbutton = None
        self.wipesavebutton = None
        self.allDimentions = [Dimention(**d) for d in self.DEFAULTGAMESTATE["Dimensions"]]
        self.dButtons = []
        self.dTxtAmount = []
        self.dTxtPreduce = []
        self.dButtonsx10 = []
        self.newstickers = ["Test1","Test2"]
        self.DimentionsUI(screen)

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
            while d.cost <= self.AntimatterAmount and self.allDimentions.index(d)< self.DimBoosts + 4:
                self.AntimatterAmount = d.func(self.AntimatterAmount,self.DimBoosts)
        while self.tickspeedCost <= self.AntimatterAmount:
            self.tickspeedup()

    def tickspeedup(self):
        if self.tickspeedCost <= self.AntimatterAmount:
            self.tickspeed *= self.tickspeedMult
            self.tickspeedCost *= 10


    def DimBoostReset(self):
        """Resets all game stats to their original values."""
        self.AntimatterAmount = self.DEFAULTGAMESTATE["AntimatterAmount"]
        self.fps = self.DEFAULTGAMESTATE["fps"]
        self.tickspeed = self.DEFAULTGAMESTATE["tickspeed"]
        self.tickspeedCost = self.DEFAULTGAMESTATE["tickspeedCost"]
        self.tickspeedMult = self.DEFAULTGAMESTATE["tickspeedMult"]

        # Reset all dimensions to their original state
        for i, dimension in enumerate(self.allDimentions):
            original_dim = self.DEFAULTGAMESTATE["Dimensions"][i]
            dimension.amount = original_dim["amount"]
            dimension.baseCost = original_dim["baseCost"]
            dimension.cost = original_dim["baseCost"]
            dimension.costMult = original_dim["costMult"]
            dimension.powerMult = original_dim["powerMult"]
            dimension.preduce = 0

        print("Dimboost reset complete.")

    def dimensionboost(self):
        if self.DimBoostCost[0] <= self.allDimentions[self.DimBoostCost[1]-1].preduce:
            self.DimBoostReset()
            self.DimBoosts += 1
            if self.DimBoostCost[1] < 8:
                self.DimBoostCost[1] += 1
            else:
                self.DimBoostCost[0] += 15
            for i in range(min(self.DimBoosts,8)):
                self.allDimentions[i].powerMult = pow(2,self.DimBoosts-i)
            

    def DimentionsUI(self,screen):
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        count = 0
        for dimention in self.allDimentions:
            if self.DimBoosts + 3 >= count: 
                self.dButtons.append(Button((25, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].func, f"button {count+1}, cost: {numToExpones(dimention.cost)}", Roboto_Black, 30,  (0,0,0) , (0,0,0) , (250,0,0), 10, 1))
                self.dButtonsx10.append(Button((WIDTH - 375, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].funcx10, f"buy 10 of tier {count+1}, cost: {numToExpones((10 - int(str(self.allDimentions[count].amount)[-1]))*dimention.cost)}", Roboto_Black, 30,  (0,0,0), (0,0,0) , (255,0,0), 10, 1))
            else:
                self.dButtons.append(Button((25, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].func, f"button {count+1}, cost: {numToExpones(dimention.cost)}", Roboto_Black, 30,  (0,0,0) , (0,0,0) , (250,0,0), 10, 1,locked=True))
                self.dButtonsx10.append(Button((WIDTH - 375, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].funcx10, f"buy 10 of tier {count+1}, cost: {numToExpones((10 - int(str(self.allDimentions[count].amount)[-1]))*dimention.cost)}", Roboto_Black, 30,  (0,0,0), (0,0,0) , (255,0,0), 10, 1,locked=True))
            self.dTxtAmount.append(Text(f"({dimention.amount%10})", Roboto_Black, "Black", (WIDTH - 425, 240+60*count), 30))
            self.dTxtPreduce.append(Text(f"{dimention.preduce} x {numToExpones(dimention.powerMult)}", Roboto_Black, "Black", (425, 240+60*count), 30))
            count += 1
        self.BAB = Button((500, 110), (100, 50), (200,200,200), (0, 255, 0), self.buyAll, f"Buy All", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1,"BAB")
        self.tickspeedbutton = Button((500, 170), (500, 50), (200,200,200), (0, 255, 0), self.tickspeedup, f"Tickspeed: {numToExpones(self.tickspeed)}, Upgrade x{self.tickspeedMult}: {numToExpones(self.tickspeedCost)}", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1)
        self.wipesavebutton = Button((25, 35), (150, 50), (200,200,200), (0, 255, 0), self.wipeSave, f"Wipe save ({self.wipeSaveClicks})", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1)
        self.DimBoostbutton = Button((25, 760), (200, 50), (200,200,200), (0, 255, 0), self.dimensionboost, f"Dimension boost ({self.DimBoosts}): {self.DimBoostCost[0]} {self.DimBoostCost[1]}th dimensions", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1, name= "DIMBOOST")
        self.newsticker = Text(rnd.choice(self.newstickers), Roboto_Black, "Black",(WIDTH, 10),30)

    def draw(self, screen):
        count1 = 0
        for b in self.dButtons:
            if self.DimBoosts + 3  >= count1:
                b.locked = False
            else:
                b.locked = True
            b.txt = f"button {count1+1}, cost: {numToExpones(self.allDimentions[count1].cost)}"
            b.draw(screen)
            count1+=1
        countx10 = 0
        for b in self.dButtonsx10:
            if self.DimBoosts + 3  >= countx10:
                b.locked = False
            else:
                b.locked = True
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
            if count3 < 7:
                if (self.allDimentions[count3+1].preduce * self.allDimentions[count3+1].powerMult) != 0:
                    tP.text = f"{numToExpones(self.allDimentions[count3].preduce)} x {numToExpones(self.allDimentions[count3].powerMult)} (+{numToExpones(((self.allDimentions[count3+1].preduce * self.allDimentions[count3+1].powerMult)/(self.allDimentions[count3].preduce))*100)}%)"
                else:
                    tP.text = f"{numToExpones(self.allDimentions[count3].preduce)} x {numToExpones(self.allDimentions[count3].powerMult)} (+0.00%)"
            else:
                tP.text = f"{numToExpones(self.allDimentions[count3].preduce)} x {numToExpones(self.allDimentions[count3].powerMult)}"
            tP.draw(screen)
            count3+=1
        if self.BAB:
            self.BAB.draw_centeredx(screen)
        if self.tickspeedbutton:
            self.tickspeedbutton.txt = f"Tickspeed: {numToExpones(self.tickspeed)}, Upgrade x{self.tickspeedMult}: {numToExpones(self.tickspeedCost)}"
            self.tickspeedbutton.draw_centeredx(screen)
        if self.wipesavebutton:
            self.wipesavebutton.txt = f"Wipe save ({self.wipeSaveClicks})"
            self.wipesavebutton.draw(screen)
        if self.DimBoostbutton:
            self.DimBoostbutton.txt = f"Dimension boost ({self.DimBoosts}): {self.DimBoostCost[0]} {self.DimBoostCost[1]}th dimensions"
            self.DimBoostbutton.draw(screen)
        if self.newsticker:
            if self.newsticker.pos[0] > 0:
                self.newsticker.pos = [self.newsticker.pos[0]-(60*self.dt),self.newsticker.pos[1]]
            else:
                self.newsticker.text = rnd.choice(self.newstickers)
                self.newsticker.pos = [screen.get_width(),self.newsticker.pos[1]]
            self.newsticker.draw(screen)

    def event(self, event):
        for b in self.dButtons:
            t = b.event(event, self.AntimatterAmount, self.DimBoosts)
            if t is not None:
                print(t)
                self.AntimatterAmount = t
        for bx10 in self.dButtonsx10:
            t = bx10.event(event, self.AntimatterAmount, self.DimBoosts)
            if t is not None:
                print(t)
                self.AntimatterAmount = t
        self.BAB.event(event)
        self.tickspeedbutton.event(event)
        self.wipesavebutton.event(event)
        self.DimBoostbutton.event(event)

    def update(self, screen):
        self.draw(screen)
        return(self.ADsProduction())

    def resize(self,screen):
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        count = 0
        self.dButtons = []
        self.dButtonsx10 = []
        self.dTxtAmount = []
        self.dTxtPreduce = []
        for dimention in self.allDimentions:
            if self.DimBoosts + 3 >= count : 
                self.dButtons.append(Button((25, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].func, f"button {count+1}, cost: {numToExpones(dimention.cost)}", Roboto_Black, 30,  (0,0,0) , (0,0,0) , (250,0,0), 10, 1))
                self.dButtonsx10.append(Button((WIDTH - 375, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].funcx10, f"buy 10 of tier {count+1}, cost: {numToExpones((10 - int(str(self.allDimentions[count].amount)[-1]))*dimention.cost)}", Roboto_Black, 30,  (0,0,0), (0,0,0) , (255,0,0), 10, 1))
            else:
                self.dButtons.append(Button((25, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].func, f"button {count+1}, cost: {numToExpones(dimention.cost)}", Roboto_Black, 30,  (0,0,0) , (0,0,0) , (250,0,0), 10, 1,locked=True))
                self.dButtonsx10.append(Button((WIDTH - 375, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].funcx10, f"buy 10 of tier {count+1}, cost: {numToExpones((10 - int(str(self.allDimentions[count].amount)[-1]))*dimention.cost)}", Roboto_Black, 30,  (0,0,0), (0,0,0) , (255,0,0), 10, 1,locked=True))
            self.dTxtAmount.append(Text(f"({dimention.amount % 10})", Roboto_Black, "Black", (WIDTH - 425, 240 + 60 * count), 30))
            self.dTxtPreduce.append(Text(f"{dimention.preduce} x {numToExpones(dimention.powerMult)}", Roboto_Black, "Black", (425, 240 + 60 * count), 30))
            count += 1
        self.BAB = Button((500, 110), (100, 50), (200, 200, 200), (0, 255, 0), self.buyAll, f"Buy All", Roboto_Black,30, (0, 0, 0), (0, 0, 0), (255, 0, 0), 10, 1,"BAB")
        self.tickspeedbutton = Button((500, 210), (500, 50), (200, 200, 200), (0, 255, 0), self.tickspeedup,f"Tickspeed: {numToExpones(self.tickspeed)}, Upgrade x{self.tickspeedMult}: {numToExpones(self.tickspeedCost)}",Roboto_Black, 30, (0, 0, 0), (0, 0, 0), (255, 0, 0), 10, 1)
        self.wipesavebutton = Button((25, 35), (150, 50), (200,200,200), (0, 255, 0), self.wipeSave, f"Wipe save ({self.wipeSaveClicks})", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1)
        self.DimBoostbutton = Button((25, 760), (350, 50), (200,200,200), (0, 255, 0), self.dimensionboost, f"Dimension boost ({self.DimBoosts}): {self.DimBoostCost[0]} {self.DimBoostCost[1]}th dimensions", Roboto_Black, 25, (0,0,0), (0,0,0), (255,0,0), 10, 1, name= "DIMBOOST")
        self.newsticker = Text(rnd.choice(self.newstickers), Roboto_Black, "Black",(10,HEIGHT-30),30)

    def getGameState(self):
        # Store all game state data in a dictionary for easy JSON serialization
        self.GAMESTATE = {
            "AntimatterAmount": self.AntimatterAmount,
            "fps": self.fps,
            "tickspeed": self.tickspeed,
            "tickspeedCost": self.tickspeedCost,
            "tickspeedMult": self.tickspeedMult,
            "DimBoosts": self.DimBoosts,
            "DimBoostCost": self.DimBoostCost,
            "Dimensions": [
                {
                    "name": dimension.name,
                    "amount": dimension.amount,
                    "baseCost": dimension.baseCost,
                    "cost": dimension.cost,
                    "costMult": dimension.costMult,
                    "powerMult": dimension.powerMult,
                    "preduce": dimension.preduce
                }
                for dimension in self.allDimentions
            ]
        }

    def saveGame(self, path):
        # Call getGameState to populate the GAMESTATE dictionary
        self.getGameState()
        
        try:
            # Write the GAMESTATE dictionary to a JSON file
            with open(Savefile, "w") as file:
                json.dump(self.GAMESTATE, file, indent=4)
            print("Game saved successfully in AppData.")
        except Exception as e:
            print(f"An error occurred while saving: {e}")

    def loadSave(self, path):
        try:
            # Load data from the JSON file
            with open(path, "r") as file:
                data = json.load(file)

            # Restore basic game attributes
            self.AntimatterAmount = data.get("AntimatterAmount", self.AntimatterAmount)
            #self.fps = data.get("fps", self.fps)
            self.tickspeed = data.get("tickspeed", self.tickspeed)
            self.tickspeedCost = data.get("tickspeedCost", self.tickspeedCost)
            self.tickspeedMult = data.get("tickspeedMult", self.tickspeedMult)
            self.DimBoosts = data.get("DimBoosts",self.DimBoosts)
            self.DimBoostCost = data.get("DimBoostCost", self.DimBoostCost)

            # Restore dimension attributes from JSON data
            dimensions_data = data.get("Dimensions", [])
            for i, dimension_data in enumerate(dimensions_data):
                if i < len(self.allDimentions):  # Ensure index is within bounds
                    dimension = self.allDimentions[i]
                    dimension.amount = dimension_data.get("amount", dimension.amount)
                    dimension.baseCost = dimension_data.get("baseCost", dimension.baseCost)
                    dimension.cost = dimension_data.get("cost", dimension.cost)
                    dimension.costMult = dimension_data.get("costMult", dimension.costMult)
                    dimension.powerMult = dimension_data.get("powerMult", dimension.powerMult)
                    dimension.preduce = dimension_data.get("preduce", dimension.preduce)
            print("Game loaded successfully.")
            
        except FileNotFoundError:
            print("Save file not found, starting with default values.")
        except json.JSONDecodeError:
            print("Error reading save file, it may be corrupted.")

    def wipeSave(self):
    # Confirm wipe save if there are remaining confirmation clicks
        if self.wipeSaveClicks > 0:
            self.wipeSaveClicks -= 1
            return
    
    # Reset Antimatter and game state variables
        self.AntimatterAmount = 10
        self.tickspeed = 1
        self.tickspeedCost = pow(10, 3)
        self.tickspeedMult = 1.125
        self.DimBoosts = 0
        self.DimBoostCost = [20,4]
        self.wipeSaveClicks = 5  # Reset wipe-save confirmation clicks
    
    # Reset all Dimention instances
        for dimension in self.allDimentions:
            dimension.amount = 0
            dimension.cost = dimension.baseCost
            dimension.preduce = 0
            dimension.powerMult = 1  # If this is the intended reset value
    
    # Clear save file content
        with open(Savefile, "w") as file:
            file.write("")
        print("Save wiped and game reset to initial state.")


def numToExpones(num):
    if num > 0:
        if num < 1.18e308:
            if num < 9e15:
                base = len(str(num).split(".")[0])-1 #splits the number into the int part and the decimal part and then  removes one from the length of the int part
            else:
                base = len(str(int(num)).split(".")[0])-1 #this part fixes the problem with the numbers not properly converting after e16
            if base < 3:
                return (f"{num:.2f}")
            else:
                return str((f"{(num/(pow(10, base))):.2f}"))+"E+"+str(base)
    else:
        return str(f"{num}")

def test():
    print("test")

def main(isRunning):
    score = 0
    fps = 60
    WIDTH, HEIGHT = 1200, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    scoreText = Text("", Roboto_Black, "black", (400, 40), 30)
    ADs = Antimatter(fps)
    ADs.loadSave(Savefile)

    while isRunning:

        screen.fill("white")

        scoreText.draw_centeredx(50,screen)
        #button.draw(screen)

        score += ADs.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
                ADs.saveGame(Savefile)
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                ADs.resize(screen)
            ADs.event(event)

        #ADs.tickspeed = 1000 # cheat code :-)

        pygame.display.flip()
        scoreText.text = "Antimatter Amount " + numToExpones(ADs.AntimatterAmount)
            
    pygame.quit()

if __name__ == '__main__':
    main(True)