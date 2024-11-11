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

display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h -50
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.FULLSCREEN)


pygame.display.set_caption("AD cheap yes graphics knockoff")

Roboto_Black = "Roboto/Roboto-Black.ttf"

getcontext().prec = 1000 #Decimal will now store up to 1000 digits of info



Savesfolder = os.path.join(os.getenv("APPDATA"), "Antimatter Dimensions") # Makes the path to the directory to the save
os.makedirs(Savesfolder, exist_ok=True)  # Ensure the directory exists or create it
Savefile = os.path.join(Savesfolder, "save_game.json") # Makes the path to the save file 

class Text:
    def __init__(self, text, font, color, pos, font_size):
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.SysFont(font, font_size)
        self.color = color
        self.pos = pos
        self.text_surface = self.font.render(self.text, False, self.color)
        self.text_width = self.text_surface.get_width()
        self.text_height = self.text_surface.get_height()

    def relocate(self,pos):
        self.pos = pos

    def draw_centeredx(self, posy, screen):
        self.text_surface = self.font.render(self.text, False, self.color)
        self.text_width = self.text_surface.get_width()
        self.text_height = self.text_surface.get_height()
        self.text_rect = self.text_surface.get_rect(center=(screen.get_width() // 2, posy))
        screen.blit(self.text_surface, self.text_rect)
    
    def draw(self, screen):
        self.text_surface = self.font.render(self.text, False, self.color)
        self.text_width = self.text_surface.get_width()
        self.text_height = self.text_surface.get_height()
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
        self.locked = locked #Is the button locked?
        self.lockedtxt =  lockedText #Text to display if button locked
        self.locked_color = (66, 57, 66) #color of button when locked

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

    def relocate(self,position): #relocate the button by redefining all the position based methods
        self.x, self.y = position
        self.rect   = self.surf.get_rect(center=position)
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

        self.collisionbox = outline_rect #Button collision box to click on is the outline rectangle (the inner rectangle is in it)

    def mouseover(self):
        self.curclr = self.clr
        self.outline_curclr = self.outlineColor
        pos = pygame.mouse.get_pos()
        if self.collisionbox.collidepoint(pos):
            self.curclr = self.cngclr
            self.outline_curclr = self.outcngclr
        if self.locked: #If the button is locked display it
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
            if keys[pygame.K_b]: #The Buy all button has the hotkey b
                if self.name == "BAB":
                    return self.call_back(*args)
            elif keys[pygame.K_d]:#The Dimension boost button has the hotkey d
                if self.name == "DIMBOOST":
                    return self.call_back(*args)
            elif keys[pygame.K_g]:#...
                if self.name == "GALAXY":
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
        self.DEFAULTGAMESTATE = { #Defining the default game values, incase the save file is missing
            "AntimatterAmount": 10,
            "fps": fps,
            "tickspeed": 1,
            "tickspeedCost": pow(10,3),
            "tickspeedMult": 1.125,
            "DimBoosts": 0,
            "DimBoostCost": [20,4],
            "Galaxies": 0,
            "Dimensions": [
                {"name":"AD_1","amount":0,"baseCost":pow(10, 1),"costMult":pow(10, 3),"powerMult": 1}, {"name":"AD_2","amount":0,"baseCost":pow(10, 2),"costMult":pow(10, 4),"powerMult": 1}, 
                {"name":"AD_3","amount":0,"baseCost":pow(10, 4),"costMult":pow(10, 5),"powerMult": 1}, {"name":"AD_4","amount":0,"baseCost":pow(10, 6),"costMult":pow(10, 6),"powerMult": 1},
                {"name":"AD_5","amount":0,"baseCost":pow(10, 9),"costMult":pow(10, 8),"powerMult": 1}, {"name":"AD_6","amount":0,"baseCost":pow(10, 13),"costMult":pow(10, 10),"powerMult": 1},
                {"name":"AD_7","amount":0,"baseCost":pow(10, 18),"costMult":pow(10, 12),"powerMult": 1}, {"name":"AD_8","amount":0,"baseCost":pow(10, 24),"costMult":pow(10, 15),"powerMult": 1}
            ]
        }
        self.clock = pygame.time.Clock()
        self.AntimatterAmount = self.DEFAULTGAMESTATE["AntimatterAmount"] #getting the value for Antimatter amount by default
        self.DimBoosts =  self.DEFAULTGAMESTATE["DimBoosts"] # for Dimension boosts
        self.DimBoostCost = self.DEFAULTGAMESTATE["DimBoostCost"]# ...
        self.Galaxies = self.DEFAULTGAMESTATE["Galaxies"]
        self.fps = fps
        self.tickspeed = self.DEFAULTGAMESTATE["tickspeed"]
        self.tickspeedMult = self.DEFAULTGAMESTATE["tickspeedMult"]
        self.tickspeedCost = self.DEFAULTGAMESTATE["tickspeedCost"]

        self.dt = self.clock.tick(self.fps)/1000
        self.wipeSaveClicks = 5
        self.Dimentions = 0
        
        self.GalaxyButton = None
        self.DimBoostbutton = None
        self.BAB = None
        self.tickspeedbutton = None
        self.wipesavebutton = None
        
        self.allDimentions = [Dimention(**d) for d in self.DEFAULTGAMESTATE["Dimensions"]]
        self.dButtons = []
        self.dTxtAmount = []
        self.dTxtPreduce = []
        self.dButtonsx10 = []
        self.newstickers = ['The cookie is a lie.', 'Antimatter cookies have been confirmed to not exist, whoever claims that, stop.', "Antimatter ghosts do not exist. Just like matter ghosts. They don't have any matter, for that matter.", 'Nuclear power plants have been abandoned in favor of antimatter power.', 'Antimatter prices have drastically dropped due to newfound abundance.', 'In the news today, humans make an antimatter animal sacrifice to the antimatter god.', 'You made one antimatter! Whatever that means.', 'Scientists confirm that the colour of antimatter is Blurple', 'How does it matter if its antimatter?', 'None of this matters', "IN THE END, IT DOESN'T ANTIMATTER -hevipelle", 'How does NASA organise a party? They planet.', "Electrons are now seeing the happy things in life. We're calling these happy electrons 'Positrons.' Wait, that's taken?", "This completely useless sentence will get you nowhere and you know it. What a horrible obnoxious man would come up with it, he will probably go to hell, and why would the developer even implement it? Even if you kept reading it you wouldn't be able to finish it (the first time).", 'GHOST SAYS HELLO -Boo-chan', 'Can someone tell hevi to calm down? -Mee6', 'Due to Antimatter messing with physics, a creature that was once a moose is now a human', '!hi', 'Alright -Alright', 'The English greeting is not present in Antimatter speak.', 'To buy max or not to buy max, that is the question', 'This antimatter triggers me', "No, mom, I can't pause this game.", 'Scientific notation has entered the battlefield.', 'Make the Universe Great Again! -Tronald Dump', '#dank-maymays', "A new religion has been created, and it's spreading like wildfire. The believers of this religion worship the Heavenly Pelle, the goddess of antimatter. They also believe that 10^308 is infinite.", 'Someone has just touched a blob, and blown up. Was the blob antimatter, or was the guy made of Explodium?', 'If you are not playing on Kongregate or ivark.github.io, the site is bootleg.', 'Rate 5 on Kongregate so more people can experience this 5 star Rating', 'BOO!', 'You ate for too long. -hevipelle', 'I hate myself. -Boo-chan', 'Gee golly -Xandawesome', 'Above us, there is nothing above, But the stars, above.', 'If black lives matter, do white lives antimatter?', "Somebody wasn't nice, he got an antimatter-storm.", 'You are living, you occupy space, you have a mass, you matter... unless you antimatter.', 'I clicked too fast... my PC is now dematerialised.', 'If an alien lands on your front lawn and extends an appendage as a gesture of greeting, before you get friendly, toss it an eightball. If the appendage explodes, then the alien was probably made of antimatter. If not, then you can proceed to take it to your leader. -Neil deGrasse Tyson', 'There always must be equal matter than there is antimatter, I guess your mom balances that a bit', 'Nothing is created, nothing is destroyed.', "We dug a big hole to store this antimatter... Adele's rolling in it.", 'If everything is antimatter, how can you see yourself?', 'The stock markets have crashed due to antimatter beings somehow knowing what they will be tomorrow.', "My dog ate too much antimatter, now he is doing 'meow!'", 'If you put infinity into your calculator it will result in 42!', "You have found the rarest antimatter pepe, it's ultra rare!", 'Can we get 1e169 likes on this video??? Smash that like button!!', 'The smell of antimatter has been revealed. It smells like kittens', 'Just another antimatter in the wall', 'GET SNIPED, WEAKLING', 'Thanks a lot -dankesehr', 'This world situation is a SOS situation to the world!! MAYDAY, MAYDAY!!', 'As for sure as the sun rises in the west, of all the singers and poets on earth, I am the bestest. - hevipelle', "I'm good at using github -hevipelle", 'A new chat server has been created for Antimatter people to spy on Matter people, and the world has fallen into chaos and discord', 'A new study has come out linking the consumption of potatoes with increased risk of Antimatter implosion.  Scientists suggest eating more.', 'I thought that I fixed that bug but apparently some update broke it again -hevipelle', "Maybe I'm gay then -Bootato", 'Breaking news! Hevipelle has just announced that the buy max button is in fact going to be removed!', 'I dedicate this game to my girlfriend', "Antimatter guns don't kill antimatter people, antimatter people kill antimatter people but does that mean that antimatter toaster doesn't toast antimatter toasts, antimatter toast toasts antimatter toasts?", "But to an antimatter person, wouldn't they be matter and us antimatter?", 'And nothing Antimatters', 'School starting up strikes fear in students universe-wide, as schools are no longer segregated between Matter and antimatter. Annihilation is prominent.', 'Why does no one talk about the 0th dimension?', 'The fatter catter satter on the antimatter.', 'Who let the DOgs out?', "If you can't read this you disabled the news.", "Doesn't leave, just mutes the server so he doesn't receive notifications", 'Most quotes found online are falsely atributed -Abraham Lincoln', "It should work now, but it doesn't -hevipelle", "This game doesn't have any errors... they're alternative successes.", "A third type of matter has been discovered: null matter. It doesn't do anything and is basically useless. The scientists who discovered it were fired.", 'Your Mother-in-Law keeps nagging you about all these antimatter colliders.', 'If matter exists, then does antimatter not exist?', 'Antimatter=Life. Not cobblestone, not dirt, nothing like that. Antimatter.', 'Breaking News: Error Error Error', 'How much antiwood could an antiwoodchuck chuck if an antiwoodchuck could chuck antiwood?', 'Chaos isnt a pit, chaos is a matter', "That's because I'm a good game developer and pushed some code that totally works -hevipelle", "What's the matter with anti matter?", "Doesn't it annoy you when people don't finish their", "Don't anti-quote me on this", 'Antimatter is honest, matter makes up everything', 'According to no known laws of aviation, there are multiple ways a bee should be able to be swallowed up by antimatter', 'You either die as matter or live long enough to be consumed by the antimatter, and then die again', 'If you gaze long enough into the antimatter, the antimatter gazes back into you', 'Always gonna give you up. Always gonna let you down. - anti-Rick Astley', 'Antimatter Dimensions: the next update is always 5 hours away. Always.', '#DimensionLivesAntimatter', 'Do antimatter people with suicidal thoughts get depressants?', 'To matter or to antimatter, that is the question.', 'Why is everything so Hevi?', 'It has been scientifically proven ages ago, that cats made of matter are assholes. We have good news, because cats made of antimatter are still assholes', 'Nobody once told me the anti-world wasn’t gonna roll me', "Antimatter is like internet. If you're reading this, you can't have enough of it.", "Antimatter has made time travel possible and I'm here to make the past great again. - 2nd President of the World", 'Please insert Disc -1 to continue playing  Antimatter Dimensions ™.', 'Lore - coming soon ™', 'I was a part of antimatter like you once. But then I got matter in my knee.', "Antimatter... antimatter never changes... until you get to quantum physics of antimatter, but we don't have enough tachyon particles for that.", 'There is no war in Antimatter Dimensions. Here we are safe. Here we are free.', 'Antimatter has solved global warming.  In unrelated news, the Earth no longer exists.', 'Anti-water, anti-Earth, anti-fire, anti-air. Long ago, the four anti-nations lived together in harmony. Then, everything changed when the anti-Fire Nation attacked. Only the anti-Avatar, the master of all 4 anti-elements could bring balance to the anti-world, but when the world needed him most, he accidentally touched some regular matter and exploded.', 'If you open an anti-lootbox, are you selling random possessions for in-game currency?', "People are beginning to question Hevipelle's existence.", "Antimatter Dimensions is proud to be sponsored by Lehmä! Now offering - grass eating lessons! Learn what grass is safe to eat and what grass isn't.", "It is the year 2422. The update still isn't out. Hevi is working on balancing unfunity dimension dimensions and challenges for the 38th layer of prestige. There are over 100 rows of achievements. They're getting ready to start using breaking_breaking_breaking_infinity.js", 'Import Christmas for a secret theme', 'What the f*ck did you just f*cking say about me, you little b*tch? I’ll have you know I graduated top of my class in the Antimatter Seals, and I’ve been involved in numerous secret raids on the 9th Dimension, and I have over 300 NNnNeMI-NNnNe confirmed kills. I am trained in potato warfare and I’m the top sniper in the entire Antimatter Galactic armed forces. You are nothing to me but just another infinity. I will wipe you the f*ck out with Max All mashing the likes of which has never been seen before in this dimension, mark my f*cking words. You think you can get away with saying that shit to me over the Interdimensional network? Think again, f*cker. As we speak I am contacting my secret network of autobuyers across the galaxy and your IP is being traced right now so you better prepare for the Big Crunch, maggot. The Big Crunch that wipes out the pathetic little thing you call your life. You’re f*cking dead, kid. I can be anywhere, anytime, and I can kill you in over seven 😠💩 different ways, and that’s just with my mouse. Not only am I extensively trained in dimension shift combat, but I have access to the entire arsenal of the Antimatter Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the universe, you little shit. If only you could have known what unhevi retribution your little “clever” comment was about to bring down upon you, maybe you would have held your f*cking tongue. But you couldn’t, you didn’t, and now you’re buying until 10, you goddamn idiot. I will shit antimatter shit all over you and you will drown in it. You’re f*cking dead, kiddo.', "So I've pondered this question for a long time. Antimatter Dimensions... what does it mean? I mean it's game, that's clear. You buy the first dimension, and it gives you antimatter, and the second dimension provides more first dimensions and so on... But what does it mean? It can't just be a game, it seems too plain for that. The developer must have made it as a metaphor. I was doing my weekly ritual of using the fingernail clipper to cut my pubic hair, when finally the realization came to me. The dimensions are just thinly veiled misspellings of the word 'depression'. Regular matter are the cruel and negative thoughts that add to and fuel depression, while antimatter is the positive thoughts and good friends that dispel it You start off with something simple, and it fights almost imperceptibly against the depression, but as you keep going the fight builds. But it never seems to fix everything. The depression seems like it could go on to infinity. So you keep going. But eventually, you figure out, depression isn't infinite. It's just very very large. But your 'dimensions' eventually, with enough work, make enough 'antimatter' to usurp that seeming infinity of depression. Then the possibilities are endless. You are actually happy for once, and your happiness grows exponentially as you go beyond and seemingly 'break' the 'infinity' of depression. And you go on until that 'infinity' seems tiny in comparison to the happiness you've managed to achieve in your life, where if you reset you get over that infinity in less than the blink of an eye. If you want to know what the multiple layers of prestige are...'Dimensional Shifts' are getting new things and methods to give you happiness. 'Dimensional Boosts' are upgrading the things and methods. Examples would be getting a new car being a 'Dimensional Shift' and trading that car in for a new one would be a 'Dimensional Boost'. 'Eternities' are major tragedies such as a loved one dying. That lapse brings you straight back to the beginning, with seemingly no hope of return. But with time, you grow back stronger and happier than ever before. 'Dimensional Sacrifice' is moving away. You have to give up a lot of the things you had that made you happy, but there is new opportunity in where you move to. And that new opportunity gives you more happiness than you ever had. 'Tickspeed' is how easy it is to make you happy, and 'Time Dimensions' make it even easier to be happy. Antimatter Dimensions is a metaphor for a depressed man's successful battle against his illness.", "(Make me sleep) Put me to sleep inside. (I can't sleep) Put me to sleep inside. (Leave me) Whisper my name and give me to the dark. (Make me sleep) Bid my milk to stay. (I can't fall asleep) Before I become done. (Leave me) Leave me to the nothing I've become.", 'A preview of the next update - loot boxes! Feel a sense of pride and progression as you open cosmic, galactic, and universal lootboxes for chances at rare skins, unique challenges with uniquer rewards, time skips and even new dimensions!', 'The intent of dimensions is to give a sense of pride and accomplishment', 'Refreshing cures cancer', "I have a 9th, i have a dimension... UHH... IT DOESN'T EXIST!", "Since when did we start reporting stuff like this? Half of it isn't even proper news, it's just jokes and meta-references, it doesn't even make sens-HAHAHA DISREGARD THAT I SUCK CO-", "The year is 1944, Hevipelle can't release updates for AD because he doesn't exist", '"THAT DIMENSION DOESN\'T EXIST" -GhostBot', 'Most things you know as nuts are actually Drupe seeds or Legumes. Hevipelle on the other hand is quite crazy and can thus be considered a dry uncompartmented fruit.', 'Only today you can call 1-800-ANTIMATTER and get a FREE Infinity Dimension! The package also comes with a COMPLETELY FREE SHIPPING and a FREE HIGH DEFINITION ANTI-V!!! Only today for the low price of 42! Estimated delivery time - 5 hours.', '1e420 blaze it.', "This game doesn't have any bugs, you're just doing it wrong.", 'Antimatter_Dimensions.mp1.79e308', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'Click this to unlock a secret achievement.', "Warning - We have just been informed that there is a chance of infection with a mind-virus of the Basilisk type, similar to the infamous winking parrot. This particular example is known as 'Fractal Cancer Type III'. This is believed to cause a 'crashing' of the mind, similar to a computer crash, due to the mathematical complexity of the image causing mathematical ideas that the mind can't comprehend, a Gondelian shock input eventually leading to crashing through Gondelian spoilers. All who have researched it have eventually died the same way, so it is impossible to tell exactly, but this is the common belief. Regardless, with the introduction of 'cancer' mode, as well as reports of it's spontaneous appearance, sufficient repetition of this mode's appearance may lead to  an image forming in the mind similar to 'Fractal Cancer Type III'. With this in mind, we have some suggestions if you find yourself plagued with it. First, refresh immediately and see if that fixes the issue. If not, navigate to options, and change the theme from cancer to literally anything else. And above all else, Godspeed. We can't afford to lose anymore viewers.", "If I have bad English, I'll study English until I have good English.", "Someone once told me that antimatter is gonna roll me. I ain't the sharpest atom in the shed. WELL, the tubes start coming and they don't stop coming...", 'Because of this game I can now use the word "infinity" as a verb.', 'Ahhh i love the smell of particle annihilation in the morning', "The person who said ghosts don't exist obviously doesn't have a discord", 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAntimatter Dimensions was made by some dude from Finland', 'The Holy trinity of Hevipelle, Antimatter, Infinity Points, and Eternity Points. These 3 resources let us access Hevi’s gift, Time Theorems. And with these Time Theorems, we reach out to Hevi, and call, “Hevi, bless us on this fine day!” And Hevi does. He give us the blessing of Time Studies. These Time Studies were blessings so powerful, Hevi restricted their power. He said, “ I will give you a choice of three paths” and then humanity chose. The short, cheap route of Normal Dimensions, giving instant gratification, the powerful choice of Infinity Dimensions, which were a fast, middle ground path, or Time Dimension, the long wait, and struggle, of humanity. Then, as humanity chose, a crack broke the earth. A serpent snaked out and sneered to humanity, “I will offer the powerful choice of a ninth dimension! I am Slabdrill, lord of all Unhevi. Humanity rose and said “ Begone Slabdrill! We want none of your foul Heresy!” And Hevi rose as well, and smote Slabdrill with his godlike power. As Slabdrill’s corpse fell into the earth, he cried “ this will not be the last of me! Hevi will betr-“ and he fell in the Abyss of matter. Hevi gifted humanity with Eternity upgrades, which boosted infinity dimensions and time dimensions. And Hevi gave humanity his greatest gift . EP multipliers. He said, these will multiply all EP gained by 5, but their cost will increase 25 times. Use them wisely. And Humanity journeyed off with their new power, as Slabdrill’s words echoed in their heads.', 'We have updated our Antimatter Privacy Policy.', 'Is this a jojo reference?', 'You just made your 1,000,000,000,000,000 antimatter. This one tastes like chicken', 'Nerf the galaxies please.', "What do you mean, more than two dimensions??? We're on a screen, clearly there are only 2 dimensions.", 'How much is Infinity? -literally everyone at least once', 'Eh, the Fourth Dimension is alright...', 'Antimatter people seem to be even more afraid of 13 then we are. They destroyed entire galaxies just to remove 13 from their percents.', 'To understand dimensional sacrifice, you do actually need a PhD in theoretical physics. Sorry!', "A new group for the standardisation of numbers have come forward with a novel new format involving emoji's.", 'Antimatter ice cream stand has recently opened- they have octillions of flavors!', 'The Heavenly Pelle has generated too much antimatter and needed to create another galaxy. This one can be seen in the southwestern sky.', 'What does the CTRL button do again?', '9th Dimension is a lie.', "The square root of 9 is 3, therefore the 9th dimension can't exist.", 'You got assimilated by the 9th dimension? Just call your doctor for mental illness!', 'Why is there no 9th dimension? Because 7 8 9.', 'The 9th dimension cannot exist because the Nein-speaking nazis died in WW2.', "If you break the fourth wall... well, there's still the fifth, sixth, seventh, and eighth to get through before you encounter bad things, so you should be fine", 'Conditions must be met for Hevipelle to sleep. First, it needs to be a blue moon. Second, a specific town in the arctic must have not seen light for a month. Third, he needs to release an AD update. And finally, no one on the discord can be on dimension 9. Only then can he rest, for up to 6 hours, before waking up forcefully to avoid getting the offline achievement.']
        self.DimentionsUI(screen)

    def ADsProduction(self):
        self.dt = self.clock.tick(self.fps)/1000 #updating delta time
        count = len(self.allDimentions)-1 
        while count > 0:
            #print(self.allDimentions[count].name)
            self.allDimentions[count-1].preduce += self.allDimentions[count].powerMult*self.allDimentions[count].preduce*self.tickspeed*self.dt
            count-=1
        self.AntimatterAmount += self.allDimentions[0].preduce*self.allDimentions[0].powerMult*self.tickspeed*self.dt
        return self.AntimatterAmount
    
    def buyAll(self):
        for d in self.allDimentions[::-1]:
            while d.cost <= self.AntimatterAmount and self.allDimentions.index(d)< self.DimBoosts + 4: #buys only the dimensions unlocked and making sure you have the antimatter for them
                self.AntimatterAmount = d.func(self.AntimatterAmount,self.DimBoosts)
        while self.tickspeedCost <= self.AntimatterAmount:
            self.tickspeedup()

    def tickspeedup(self):
        if self.tickspeedCost <= self.AntimatterAmount:
            self.tickspeed *= self.tickspeedMult
            self.tickspeedCost *= 10


    def DimBoostReset(self):
        """default values for tickspeed, antimatter and dimensions."""
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
        if self.DimBoostCost[0] <= self.allDimentions[self.DimBoostCost[1]-1].preduce: #checks if you have enough of the dimension needed to buy the dimension boost
            self.DimBoostReset()
            self.DimBoosts += 1 #adds a dimension boost
            if self.DimBoostCost[1] < 8: #if the dimension boost needs dimension under 8 make the dimension needed one tier higher (eg 20 tier 4 --> 20 tier 5)
                self.DimBoostCost[1] += 1
            else: #else add 15 to the 
                self.DimBoostCost[0] += 15
            for i in range(min(self.DimBoosts,8)): #powers the dimensions based on dimboosts
                self.allDimentions[i].powerMult = pow(2,self.DimBoosts-i)

    def GalaxyReset(self):
        """default values for tickspeed, dimension boosts , antimatter and dimensions."""
        self.AntimatterAmount = self.DEFAULTGAMESTATE["AntimatterAmount"]
        self.fps = self.DEFAULTGAMESTATE["fps"]
        self.tickspeed = self.DEFAULTGAMESTATE["tickspeed"]
        self.tickspeedCost = self.DEFAULTGAMESTATE["tickspeedCost"]
        self.tickspeedMult = self.DEFAULTGAMESTATE["tickspeedMult"]
        self.DimBoosts = self.DEFAULTGAMESTATE["DimBoosts"]
        self.DimBoostCost = self.DEFAULTGAMESTATE["DimBoostCost"]

        # Reset all dimensions to their original state
        for i, dimension in enumerate(self.allDimentions):
            original_dim = self.DEFAULTGAMESTATE["Dimensions"][i]
            dimension.amount = original_dim["amount"]
            dimension.baseCost = original_dim["baseCost"]
            dimension.cost = original_dim["baseCost"]
            dimension.costMult = original_dim["costMult"]
            dimension.powerMult = original_dim["powerMult"]
            dimension.preduce = 0

        print("Galaxy reset complete.")

    def GalaxyUpgrade(self):
        if self.Galaxies*60 + 80 <= self.allDimentions[7].preduce: #checks if you have enough of the eighth dimension for the galaxy boost
            self.GalaxyReset()
            self.Galaxies += 1 #adds a galaxy
            self.tickspeedMult += 0.02 #adds the galaxy boost to tickspeed
            

    def DimentionsUI(self,screen):
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        count = 0
        for dimention in self.allDimentions:
            if self.DimBoosts + 3 >= count: 
                self.dButtons.append(Button((25, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].func, f"Dimension {count+1}, cost: {numToExpones(dimention.cost)}", Roboto_Black, 30,  (0,0,0) , (0,0,0) , (250,0,0), 10, 1))
                self.dButtonsx10.append(Button((WIDTH - 375, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].funcx10, f"buy 10 of tier {count+1}, cost: {numToExpones((10 - int(str(self.allDimentions[count].amount)[-1]))*dimention.cost)}", Roboto_Black, 30,  (0,0,0), (0,0,0) , (255,0,0), 10, 1))
            else:
                self.dButtons.append(Button((25, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].func, f"Dimension {count+1}, cost: {numToExpones(dimention.cost)}", Roboto_Black, 30,  (0,0,0) , (0,0,0) , (250,0,0), 10, 1,locked=True))
                self.dButtonsx10.append(Button((WIDTH - 375, 220+60*count), (350,50), (200,200,200), (0, 255, 0), self.allDimentions[count].funcx10, f"buy 10 of tier {count+1}, cost: {numToExpones((10 - int(str(self.allDimentions[count].amount)[-1]))*dimention.cost)}", Roboto_Black, 30,  (0,0,0), (0,0,0) , (255,0,0), 10, 1,locked=True))
            self.dTxtAmount.append(Text(f"({dimention.amount%10})", Roboto_Black, "Black", (WIDTH - 425, 240+60*count), 30))
            self.dTxtPreduce.append(Text(f"{dimention.preduce} x {numToExpones(dimention.powerMult)}", Roboto_Black, "Black", (425, 240+60*count), 30))
            count += 1
        self.BAB = Button((500, 110), (100, 50), (200,200,200), (0, 255, 0), self.buyAll, f"Buy All", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1,"BAB")
        self.tickspeedbutton = Button((500, 180), (500, 50), (200,200,200), (0, 255, 0), self.tickspeedup, f"Tickspeed: {numToExpones(self.tickspeed)}, Upgrade x{self.tickspeedMult}: {numToExpones(self.tickspeedCost)}", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1)
        self.wipesavebutton = Button((25, 35), (150, 50), (200,200,200), (0, 255, 0), self.wipeSave, f"Wipe save ({self.wipeSaveClicks})", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1)
        self.DimBoostbutton = Button((25, 760), (400, 50), (200,200,200), (0, 255, 0), self.dimensionboost, f"Dimension boost ({self.DimBoosts}): {self.DimBoostCost[0]} {self.DimBoostCost[1]}th dimensions", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1, name= "DIMBOOST")
        self.newsticker = Text(rnd.choice(self.newstickers), Roboto_Black, "Black",(WIDTH-1, 10),30)
        self.GalaxyButton = Button((WIDTH-375, 760), (400, 50), (200,200,200), (0, 255, 0), self.GalaxyUpgrade, f"Galaxies ({self.Galaxies}) Costs {self.Galaxies*60 + 80} 8th dimensions", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1, name= "GALAXY")


    def draw(self, screen):
        WIDTH = screen.get_width()
        HEIGHT = screen.get_height()
        count1 = 0
        for b in self.dButtons:
            if self.DimBoosts + 3  >= count1:
                b.locked = False
            else:
                b.locked = True
            #b.relocate((25, 220+60*count1)) #Relocates the dimension buttons, currently not used
            b.txt = f"Dimension {count1+1}, cost: {numToExpones(self.allDimentions[count1].cost)}"
            b.draw(screen)
            count1+=1
        countx10 = 0
        for b in self.dButtonsx10:
            if self.DimBoosts + 3  >= countx10:
                b.locked = False
            else:
                b.locked = True
            b.relocate((WIDTH - 375, 220+60*countx10)) #Relocates the dimension x10 buttons based on the screen width
            b.txt = f"buy 10 of tier {countx10+1}, cost: {numToExpones((10 - int(str(self.allDimentions[countx10].amount)[-1]))*self.allDimentions[countx10].cost)}"
            b.draw(screen)
            countx10+=1
        count2 = 0
        for tA in self.dTxtAmount:
            tA.relocate((WIDTH - 425, 240+60*count2))# moves text based on the width of the screen
            tA.text = f"({self.allDimentions[count2].amount%10})"
            tA.draw(screen)
            count2+=1
        count3 = 0
        for tP in self.dTxtPreduce:
            #tP.relocate(425, 240+60*count3) #currently not in use, can move the text
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
            #self.BAB.relocate((500, 110)) #Currently not in use, can be modified to move the buy all button
            self.BAB.draw_centeredx(screen)

        if self.tickspeedbutton:
            #self.tickspeedbutton.relocate((500, 180))# currently not in use, can be modified to move the tickspeed button
            self.tickspeedbutton.txt = f"Tickspeed: {numToExpones(self.tickspeed)}, Upgrade x{self.tickspeedMult}: {numToExpones(self.tickspeedCost)}"
            self.tickspeedbutton.draw_centeredx(screen)

        if self.wipesavebutton:
            #self.wipesavebutton.relocate((25,35))# currently out of use, can be modified to move the button
            self.wipesavebutton.txt = f"Wipe save ({self.wipeSaveClicks})"
            self.wipesavebutton.draw(screen)

        if self.DimBoostbutton:
            #self.DimBoostbutton.relocate((25, 760))# currently not in use, can be modified to move the button
            self.DimBoostbutton.txt = f"Dimension boost ({self.DimBoosts}): {self.DimBoostCost[0]} {self.DimBoostCost[1]}th dimensions"
            self.DimBoostbutton.draw(screen)

        if self.GalaxyButton:
            self.GalaxyButton.relocate((WIDTH-425, 760))# Used to fit the Galaxy button location based on the screen size
            self.GalaxyButton.txt = f"Galaxies ({self.Galaxies}): Costs {self.Galaxies*60 + 80} 8th dimensions"
            self.GalaxyButton.draw(screen)


        if self.newsticker: #update newsticker
            if not self.newsticker.pos[0] < -self.newsticker.text_width: #if the newsticker is still on screen
                self.newsticker.pos = [self.newsticker.pos[0]-(60*self.dt),self.newsticker.pos[1]] #increment 60 pixels left per second
            else:
                self.newsticker.text = rnd.choice(self.newstickers) #choose a new meassage
                self.newsticker.pos = [screen.get_width()-1,self.newsticker.pos[1]] #reset newsticker location
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
        self.GalaxyButton.event(event)

    def update(self, screen):
        self.draw(screen)
        return(self.ADsProduction())

    # Method no longer used
    """""""""
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
        self.tickspeedbutton = Button((500, 180), (500, 50), (200, 200, 200), (0, 255, 0), self.tickspeedup,f"Tickspeed: {numToExpones(self.tickspeed)}, Upgrade x{self.tickspeedMult}: {numToExpones(self.tickspeedCost)}",Roboto_Black, 30, (0, 0, 0), (0, 0, 0), (255, 0, 0), 10, 1)
        self.wipesavebutton = Button((25, 35), (150, 50), (200,200,200), (0, 255, 0), self.wipeSave, f"Wipe save ({self.wipeSaveClicks})", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1)
        self.DimBoostbutton = Button((25, 760), (350, 50), (200,200,200), (0, 255, 0), self.dimensionboost, f"Dimension boost ({self.DimBoosts}): {self.DimBoostCost[0]} {self.DimBoostCost[1]}th dimensions", Roboto_Black, 25, (0,0,0), (0,0,0), (255,0,0), 10, 1, name= "DIMBOOST")
        self.newsticker = Text(rnd.choice(self.newstickers), Roboto_Black, "Black",(WIDTH-1,10),30)
        self.GalaxyButton = Button((WIDTH-375, 760), (350, 50), (200,200,200), (0, 255, 0), self.GalaxyUpgrade, f"Galaxies ({self.Galaxies}): Costs {self.Galaxies*60 + 80} of dimensions 8", Roboto_Black, 30, (0,0,0), (0,0,0), (255,0,0), 10, 1, name= "GALAXY")
    """""""""""

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
            "Galaxies": self.Galaxies,
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
            self.Galaxies = data.get("Galaxies",self.Galaxies)

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
        self.Galaxies = 0
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
    display_info = pygame.display.Info()
    WIDTH, HEIGHT = display_info.current_w, display_info.current_h
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
                #ADs.resize(screen) # Method no longer used
            ADs.event(event)

        #ADs.tickspeed = 1000 # cheat code :-)

        pygame.display.flip()
        scoreText.text = "Antimatter Amount " + numToExpones(ADs.AntimatterAmount)
            
    pygame.quit()

if __name__ == '__main__':
    main(True)