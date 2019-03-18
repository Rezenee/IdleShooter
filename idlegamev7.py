
import pygame
import pygame.freetype
import time
import random
import math
import os
from pygame.locals import *
pygame.init()

xres = 1024
yres = 768
gameDisplay = pygame.display.set_mode((xres, yres))
pygame.display.set_caption('Idle Shooter')
pause = False
gameExit = False

gray = (200, 200, 200)
black = (0, 0, 0)
white = (255, 255, 255)
peach = (254, 154, 101)
red = (200, 0, 0)
green = (0, 200, 0)
orange = (200,100,50)
trans = (1,1,1)

dark_gray = (100,100,100)
dark_peach = (204, 104, 51)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

baseSelectIdle = 1
baseSelectPrac = 1

upgrademultiplier = 1.2
upgradecost = 10
scoreNum = 99
scoreAdd = 1
hitNum = 0
hitAdd = 1
fontsmall = pygame.freetype.Font(None, 24)
fontlarge = pygame.freetype.Font(None, 100)
game_font = pygame.freetype.Font(None, 24)

upgradelabel = 'UPGRADE ($' + str(upgradecost) + ')'
scoreLab = fontsmall.render_to(gameDisplay, (80, 70), "Score :", black)

forwardsarrow = pygame.image.load(os.path.join("images", "forwardsarrow.png"))
backarrow = pygame.image.load(os.path.join('images', 'backwardsarrow.png'))
targetimg = pygame.image.load(os.path.join('images', 'shooting_target.png'))
hitmarker = pygame.image.load(os.path.join('images', 'hitmarker.png'))
musicnote = pygame.image.load(os.path.join('images', 'musicnote.png'))
gear = pygame.image.load(os.path.join('images', 'gear.png'))
weaponFlash = pygame.image.load(os.path.join('images', 'weaponflash.png'))
weaponFlash = pygame.transform.scale(weaponFlash,[25,25])
clock = pygame.time.Clock()
gameDisplay.fill(gray)
pygame.mixer.music.load(os.path.join('images', 'background.wav'))
font = pygame.font.SysFont("Verdana", 12)
hitmarkers = []


pauseKey = 108
reloadKey = 112
keybindList = [pauseKey,reloadKey]

def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass



def changeKeyBind(keyIndex):
    global keybindList
    inkey = get_key()
    while 1:
        if inkey <= 500:
            keybindList[keyIndex] = inkey
            break

def clear_decals_key():
    changeKeyBind(1)

def pause_hotkey():
    changeKeyBind(0)
class gun(object):
    def __init__(self, cost, gunSelectIdle, gunSelectPrac, gunBought):
        self.cost = cost
        self.gunSelectIdle = gunSelectIdle
        self.gunSelectPrac = gunSelectPrac
        self.gunBought = gunBought


class Slider():
    def __init__(self, name, val, maxi, mini, xpos,ypos):
        self.val = val  # start value
        self.maxi = maxi  # maximum at slider position right
        self.mini = mini  # minimum at slider position left
        self.xpos = xpos  # x-location on screen
        self.ypos = ypos
        self.surf = pygame.surface.Surface((100, 50))
        self.hit = False  # the hit attribute indicates slider movement due to mouse interaction
        self.txt_surf = font.render(name, 1, black)
        self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

        # Static graphics - slider background #
        if name == '':
            self.surf.fill((dark_gray))
            pygame.draw.rect(self.surf, gray, [0, 0, 100, 50], 3)
            pygame.draw.rect(self.surf, white, [10, 19, 80, 5], 0)
        else:
            self.surf.fill((dark_gray))
            pygame.draw.rect(self.surf, gray, [0, 0, 100, 50], 3)
            pygame.draw.rect(self.surf, orange, [10, 10, 80, 10], 0)
            pygame.draw.rect(self.surf, white, [10, 30, 80, 5], 0)
        self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes

        # dynamic graphics - button surface #
        self.button_surf = pygame.surface.Surface((20, 20))
        self.button_surf.fill(trans)
        self.button_surf.set_colorkey(trans)
        pygame.draw.circle(self.button_surf, black, (10, 10), 6, 0)
        pygame.draw.circle(self.button_surf, orange, (10, 10), 4, 0)

    def draw(self,name):
        """ Combination of static and dynamic graphics in a copy of
    the basic slide surface
    """
        # static
        surf = self.surf.copy()
        # dynamic
        if name == '':
            pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 21)
        else:
            pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)

        self.button_rect = self.button_surf.get_rect(center=pos)
        surf.blit(self.button_surf, self.button_rect)
        self.button_rect.move_ip(self.xpos, self.ypos)  # move of button box to correct screen position

        # screen
        gameDisplay.blit(surf, (self.xpos, self.ypos))

    def move(self):
        """
    The dynamic part; reacts to movement of the slider button.
    """
        self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini
        if self.val < self.mini:
            self.val = self.mini
        if self.val > self.maxi:
            self.val = self.maxi


    check = 1

# First variable = cost, second = selectIdle, third = selectprac, fourth = gunbought all the states of them, 0 at the start
ak = gun(100, 0, 0, 0)
mp5 = gun(100, 0, 0, 0)
weaponSelectedIdle = [baseSelectIdle, ak.gunSelectIdle, mp5.gunSelectIdle]
weaponSelectedPractice = [baseSelectPrac, ak.gunSelectPrac, mp5.gunSelectPrac]
weaponbought = [ak.gunBought, mp5.gunBought]
pygame.mixer.music.play(-1)
initialrun = 0


def resetGraphics():
    initialrun = 0

def gunbuy(cost, weaponBoughtNum, idleNum, pracNum):
    global scoreNum
    if gamemode == "game_loop_idle":
        if int(scoreNum) >= 100 and weaponbought[weaponBoughtNum] == 0:
            weaponbought[weaponBoughtNum] = 1
            scoreNum -= ak.cost
        if weaponbought[weaponBoughtNum] == 1:
            for i in range(len(weaponSelectedIdle)):
                weaponSelectedIdle[i] = 0
            weaponSelectedIdle[idleNum] = 1
    if gamemode == "game_loop_practice":
        for i in range(len(weaponSelectedPractice)):
            weaponSelectedPractice[i] = 0
        weaponSelectedPractice[pracNum] = 1


def mp5gunbuy():
    gunbuy(mp5.cost,0,2,2)

def akgunbuy():
   gunbuy(ak.cost, 0,1,1)

def target(xx, yy):
   gameDisplay.blit(targetimg, (xx, yy))


def quitgame():
    pygame.quit
    quit()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def button2(x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1 and action != None:
            action()


def buttonstate2(gunselect, selectmsg, unselectmsg, x, y, w, h, icselected, acselected, icunselected, acunselected,
              action=None):
    if gunselect == 1:
        button(selectmsg, x, y, w, h, icselected, acselected, action)
    elif gunselect == 0:
        button(unselectmsg, x, y, w, h, icunselected, acunselected, action)


def buttonstate(gunselect, gunbought, selectedmsg, boughtmsg, buyingmsg, brokemsg, guncost, x, y, w, h, icselected,
             acselected, icbought, acbought, icbroke, acbroke, icbuying, acbuying, action=None):
    if gunbought == 1 and gunselect == 1:
        button(selectedmsg, x, y, w, h, icselected, acselected, action)
    elif gunbought == 1 and gunselect == 0:
        button(boughtmsg, x, y, w, h, icbought, acbought, action)
    elif gunbought == 0 and int(scoreNum) < guncost:
        button(brokemsg, x, y, w, h, icbroke, acbroke, action)
    elif gunbought == 0 and int(scoreNum) >= guncost:
        button(buyingmsg, x, y, w, h, icbuying, acbuying, action)

for i in range(len(weaponSelectedPractice)):
    weaponSelectedPractice[i] = 0
weaponSelectedPractice[2] = 1
def button(msg, x, y, w, h, ic, ac, action=None):
    # this gets the mouse's position
    mouse = pygame.mouse.get_pos()
    # This gets when the mouse clicks, it makes a list like this: [1,1,1]
    # left, middle, right, 1 is active, 0 is inactive
    click = pygame.mouse.get_pressed()

    # If mouse[0] or left click is between the box then draw the active color
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

        # If the click is left then do the action that is called
        if click[0] == 1 and action != None:
            action()
    # If not draw the box with  the inactive color.
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

   # This calls a small text. It goes the font then font size
    smallText = pygame.font.Font("freesansbold.ttf", 20)

    # no clue just do it
    textSurf, textRect = text_objects(msg, smallText)
    # This makes the text in the center of the button
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    # Draws something on screen
    gameDisplay.blit(textSurf, textRect)


def baseselect2():
    global weaponSelectedIdle
    global weaponSelectedPractice
    if gamemode == "game_loop_idle":
        for i in range(len(weaponSelectedIdle)):
            weaponSelectedIdle[i] = 0
        weaponSelectedIdle[0] = 1
    if gamemode == "game_loop_practice":
        for i in range(len(weaponSelectedPractice)):
            weaponSelectedPractice[i] = 0
        weaponSelectedPractice[0] = 1


games = ["rust", "csgo"]
# This makes a variable that is called to check what game it is.
game = 0


def changeGameUp():
    global game
    global games
    global weaponSelectedPractice
    global weaponSelectedIdle
    game += 1
    if gamemode == "game_loop_idle":
        for i in range(len(weaponSelectedIdle)):
            weaponSelectedIdle[i] = 0
        weaponSelectedIdle[0] = 1
    if gamemode == "game_loop_practice":
        for i in range(len(weaponSelectedPractice)):
            weaponSelectedPractice[i] = 0
        weaponSelectedPractice[0] = 1
    if game >= len(games):
        game = 0


def changeGameDown():
    global game
    global games
    global weaponSelectedPractice
    global weaponSelectedIdle
    game -= 1
    if gamemode == "game_loop_idle":
        for i in range(len(weaponSelectedIdle)):
            weaponSelectedIdle[i] = 0
        weaponSelectedIdle[0] = 1
    if gamemode == "game_loop_practice":
        for i in range(len(weaponSelectedPractice)):
            weaponSelectedPractice[i] = 0
        weaponSelectedPractice[0] = 1
    if game == -1:
        game = len(games) - 1


def base():
    global scoreNum
    global hitNum
    global hitAdd
    global scoreAdd
    if gamemode == "game_loop_idle":
        scoreNum = int(scoreNum) + scoreAdd
    if gamemode == "game_loop_practice":
        hitNum = int(hitNum) + hitAdd
def clearHitmakers():
    global hitmarkers
    hitmarkers = []

# Stops going left after 7 bullets, goes straight up for 1
# goes right for 3
# goes straight up for 1
# goes left again for 5 bulltes
# satys in about the same position for 3 bullets
# moves right for the rust of the spray


mp5pos = (
 (6, -19),
 (-5, -26),
 (0, -21),
 (-16, -28),
 (-27, -27),
 (-22, -18),
 (2, -8),
 (20, -2),
 (20, -5),
 (20, -7),
 (-1, -5),
 (-14, -11),
 (-14, -17),
 (2, -15),
 (18, 0),
 (9, 0),
 (20, 0),
 (26, 0),
 (28, 0),
 (-1, 0),
 (1, 0),
 (-1, 0),
 (1, 0),
 (-1, 0),
 (1, 0),
 (-1, 0),
 (1, 0),
 (-1, 0),
 (1, 0),
 (0, 0),
)
AKPOS = (
 (25, -32),
 (-5, -28),
 (26, -30),
 (25, -16),
 (7, -27),
 (-21, -12),
 (-3, -7),
 (-29, -20),
 (-30, -14),
 (-20, -0),
 (-26, -8),
 (-14, -11),
 (-14, -17),
 (2, -15),
 (18, -17),
 (9, -25),
 (20, -18),
 (26, -8),
 (28, -25),
 (25, -12),
 (36, -12),
 (14, -1),
 (7, -6),
 (5, -10),
 (3, -30),
 (-33, -15),
 (-15, -20),
 (-35, -14),
 (-17, -25),
 (0, 0),
)
def makeGunStart(GUNPOS,sleepTime):
    global scoreNum
    global hitNum
    global hitmarkers

    click = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    if 0 <= x - 250 <= 300 and 0 <= y - 150 <= 300 and click[0] == 1:
        for dx, dy in GUNPOS:
            x,y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                x,y = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if event.key == pauseKey:
                        pause = True
                        paused()
                    if event.key == keybindList[1]:
                        hitmarkers = []

            if 0 > x - 250 or x -250 > 300 or 0 > y -150 or y-150> 300:
                break
            if gamemode == "game_loop_idle":
                scoreNum += scoreAdd
                button("", 190, 70, 250, 30, gray, gray)
                fontsmall.render_to(gameDisplay, (190, 74), str(int(scoreNum)), black)
                if int(scoreNum) >= upgradecost:
                    button(upgradelabel, 600, 90, 180, 50, green, bright_green, )
                    button('UPGRADE (MAX)', 800, 90, 180, 50, green, bright_green, )
                if int(scoreNum) < upgradecost:
                    button('UPGRADE (MAX)', 800, 90, 180, 50, red, bright_red, )
            elif gamemode == "game_loop_practice":
                hitNum += hitAdd
                button("", 140, 70, 250, 30, gray, gray)
                fontsmall.render_to(gameDisplay, (140, 72), str(int(hitNum)), black)
            click = pygame.mouse.get_pressed()
            if click[0] != 1:
                break
            pygame.mouse.set_pos(x + dx, y + dy)
            button('', 200, 100, 400, 500, gray, gray)
            gameDisplay.blit(targetimg, (250, 150))
            hitmarkers.append((x - 5, y - 5))
            for z in range(len(hitmarkers)):
                gameDisplay.blit(hitmarker, (hitmarkers[z][0], hitmarkers[z][1]))
            gameDisplay.blit(weaponFlash, (x - 12, y - 12))
            pygame.display.update()
            time.sleep(sleepTime)


def akrust():
     makeGunStart(AKPOS,.125)

def mp5rust():
     makeGunStart(mp5pos,.125)



def upgradeall():
    global scoreNum
    global scoreAdd
    global upgradecost
    global upgradelabel
    while int(scoreNum) >= upgradecost:
        scoreAdd += 1
        scoreNum -= upgradecost
        upgradecost = upgradecost * upgrademultiplier
        upgradelabel = 'UPGRADE ($' + str(int(upgradecost)) + ')'


def upgradebase():
    global scoreNum
    global scoreAdd
    global upgradecost
    global upgradelabel
    if int(scoreNum) >= upgradecost:
        scoreAdd += 1
        scoreNum -= upgradecost
        upgradecost = upgradecost * upgrademultiplier
        upgradelabel = 'UPGRADE ($' + str(int(upgradecost)) + ')'

# def previousGamemode():

def game_intro():
    global gamemode
    # This is needed for the while loop
    intro = True
    gamemode = 'game_intro'
    while intro:
        # Always put this so they can exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()

        # This makes the game gray
        gameDisplay.fill(gray)
        fontlarge.render_to(gameDisplay, (220, 300), "Idle Shooter", (black))


        #pygame.mixer.music.play(-1)
        # The two buttons on this page, remember not to put the () in the function being called
        button("Play Game", 320, 450, 140, 50, green, bright_green, game_loop_idle)
        button("Play Practice", 320, 510, 140, 50, green, bright_green, game_loop_practice)
        button("Quit", 620, 450, 100, 50, red, bright_red, quitgame)
        button2(250,650,50,50,settings)
        gameDisplay.blit(gear, (250,650))

        # Needed for the game to run
        pygame.display.update()
        clock.tick(15)

def unpause():
    global pause
    pause = False


def paused():
    while pause:
        # Always put this so they can exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
        # This makes the game gray
        gameDisplay.fill(gray)
        fontlarge.render_to(gameDisplay, (150, 300), "You are Paused", (black))

        # The two buttons on this page, remember not to put the () in the function being called
        button("Continue", 320, 450, 150, 50, green, bright_green, unpause)
        button("Quit", 620, 450, 100, 50, red, bright_red, quitgame)
        # mouse = pygame.mouse.get_pos()

        # Needed for the game to run
        pygame.display.update()
        clock.tick(15)


musicsound = Slider("", .5, 1, 0, 300,180)
sensitivity = Slider("sens", .5,1,0,300,250)
slides = [musicsound,sensitivity]

def keyBindScreen():
    keyBindScreen = True
    while keyBindScreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button2(100,650,100,50, settings)
                button2(100, 650, 100, 50, settings)
        gameDisplay.fill(gray)
        fontsmall.render_to(gameDisplay, (80, 70), "Keybinds", (black))
        button("Back", 100, 650, 100, 50, green, bright_green)
        button(("Reload: " + chr(keybindList[1])), 100,200, 100,50, green,bright_green,clear_decals_key)
        button(("Pause: " + chr(keybindList[0])), 300,200, 100,50, green,bright_green, clear_decals_key)
        pygame.display.update()
        clock.tick(60)


def settings():
    settings = True
    while settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button2(100, 650, 100, 50, gamemodesDict[gamemode])
                button2(250, 650, 100, 50, keyBindScreen)

                pos = pygame.mouse.get_pos()
                for s in slides:
                    if s.button_rect.collidepoint(pos):
                        s.hit = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for s in slides:
                    s.hit = False
        for s in slides:
            if s.hit:
                s.move()
                pygame.mixer.music.set_volume(musicsound.val)
        gameDisplay.fill(gray)
        fontsmall.render_to(gameDisplay, (80, 70), "Settings", (black))
        button("Music Volume", 200,200,0,0,gray,gray)
        button("Back", 100, 650, 100, 50, green, bright_green)
        button("Keybinds", 250, 650, 100,50,green, bright_green)
        sensitivity.draw('sens')
        musicsound.draw('')
        fontsmall.render_to(gameDisplay, (400,180), str(round(musicsound.val* 100)), (black))
        pygame.display.update()
        clock.tick(60)

def game_loop_practice():
    global pause
    global gamemode
    global x
    global y
    global hitmarkers
    gamemode = "game_loop_practice"
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pause:
                    pause = True
                    paused()
                if event.key == keybindList[1]:

                    hitmarkers = []
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button("", 600, 80, 80, 50, green, bright_green, changeGameDown)
                    button("", 900, 80, 80, 50, green, bright_green, changeGameUp)
                    button("Back", 100, 650, 100, 50, green, bright_green, game_intro)
                    button2(250, 650, 50, 50, settings)
        gameDisplay.fill(gray)
        target(250, 150)
        for x in range(len(hitmarkers)):
            gameDisplay.blit(hitmarker, (hitmarkers[x][0], hitmarkers[x][1]))
        click = pygame.mouse.get_pressed()
        fontsmall.render_to(gameDisplay, (140, 72), str(int(hitNum)), black)
        scoreLab = fontsmall.render_to(gameDisplay, (80, 70), "Hits:", black)
        if weaponSelectedPractice[0] != 1:
            button("Select Base", 600, 150, 180, 50, dark_peach, peach, baseselect2)
        elif weaponSelectedPractice[0] == 1:
            button("Base Selected", 600, 150, 180, 50, peach, peach, baseselect2)
        button("Back", 100, 650, 100, 50, green, bright_green)
        button("Clear Hitmarkers",350,650,170,50,green,bright_green,clearHitmakers)
        gameDisplay.blit(backarrow, (600, 80))
        gameDisplay.blit(forwardsarrow, (900, 80))
        x, y = pygame.mouse.get_pos()
        gameDisplay.blit(gear, (250,650))

        if game == 0:
            button("RUST", 700, 80, 180, 50, red, red)

            buttonstate2(weaponSelectedPractice[1], "AK Selected", "Select AK", 800, 150,
                         180, 50, peach, peach, dark_peach, peach, akgunbuy)
            buttonstate2(weaponSelectedPractice[2], "MP5 Selected", "Select MP5", 600, 210, 180, 50, peach, peach,
                         dark_peach, peach, mp5gunbuy)


            if weaponSelectedPractice[1] == 1:
                akrust()
            if weaponSelectedPractice[2] == 1:
                mp5rust()

        if game == 1:
            button("CSGO", 700, 80, 180, 50, red, red)


        pygame.display.update()
        clock.tick(144)


def game_loop_idle():
    global pause
    global gamemode
    gamemode = "game_loop_idle"
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pause:
                    pause = True
                    paused()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if int(scoreNum) < upgradecost:
                        button(upgradelabel, 600, 90, 180, 50, red, bright_red, upgradebase)
                    elif int(scoreNum) >= upgradecost:
                        button(upgradelabel, 600, 90, 180, 50, green, bright_green, upgradebase)
                    if int(scoreNum) < upgradecost:
                        button('UPGRADE (MAX)', 800, 90, 180, 50, red, bright_red, upgradeall)
                    elif int(scoreNum) >= upgradecost:
                        button('UPGRADE (MAX)', 800, 90, 180, 50, green, bright_green, upgradeall)
                    if weaponSelectedIdle[0] == 1:
                        button2(250, 150, 300, 300, base)
                    button2(100, 650, 100, 50, game_intro)
        gameDisplay.fill(gray)
        target(250, 150)
        click = pygame.mouse.get_pressed()
        fontsmall.render_to(gameDisplay, (190, 74), str(int(scoreNum)), black)
        scoreLab = fontsmall.render_to(gameDisplay, (80, 70), "Money : $", black)

        if int(scoreNum) < upgradecost:
            button(upgradelabel, 600, 90, 180, 50, red, bright_red)
        elif int(scoreNum) >= upgradecost:
            button(upgradelabel, 600, 90, 180, 50, green, bright_green)
        if int(scoreNum) < upgradecost:
            button('UPGRADE (MAX)', 800, 90, 180, 50, red, bright_red)
        elif int(scoreNum) >= upgradecost:
            button('UPGRADE (MAX)', 800, 90, 180, 50, green, bright_green)

        buttonstate(weaponSelectedIdle[1], weaponbought[0], "AK Selected", "Select AK", "Buy AK ($100)",
                    "Buy AK ($100)", ak.cost, 800, 150,
                    180, 50, peach, peach, dark_peach, peach, red, bright_red, green, bright_green, akgunbuy)

        if weaponSelectedIdle[0] != 1:
            button("Select Base", 600, 150, 180, 50, dark_peach, peach, baseselect2)
        elif weaponSelectedIdle[0] == 1:
            button("Base Selected", 600, 150, 180, 50, peach, peach, baseselect2)
        button("Back", 100, 650, 100, 50, green, bright_green)

        x, y = pygame.mouse.get_pos()
        if weaponSelectedIdle[1] == 1 and 0 <= x - 250 <= 300 and 0 <= y - 150 <= 300:
            akrust()

        pygame.display.update()
        clock.tick(144)
gamemodesDict = {"game_intro" : game_intro, "game_loop_idle" : game_loop_idle, "game_loop_practice" : game_loop_practice}


game_loop_practice()
