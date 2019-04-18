
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
peach = (224, 134, 81)
red = (200, 0, 0)
green = (0, 200, 0)
orange = (200,100,50)
trans = (1,1,1)
brown = (139,69,19)


dark_gray = (100,100,100)
darkish_peach = (210,110,61)
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
miss_num = 0
hit_percent = 0
hit_percent_label = 0
y_practice_value = 0
fontsmall = pygame.freetype.Font(None, 24)
fontlarge = pygame.freetype.Font(None, 100)
game_font = pygame.freetype.Font(None, 24)

upgradelabel = 'UPGRADE ($' + str(upgradecost) + ')'
scoreLab = fontsmall.render_to(gameDisplay, (80, 70), "Score :", black)

forwardsarrow = pygame.image.load(os.path.join("images", "forwardsarrow.png"))
backarrow = pygame.image.load(os.path.join('images', 'backwardsarrow.png'))
rainbow_target = pygame.image.load(os.path.join('images', 'target_colors.png'))
stick_img = pygame.image.load(os.path.join('images', 'homescreen.jpg'))

targetimg = pygame.image.load(os.path.join('images', 'shooting_target.png'))
rangeimg = pygame.image.load(os.path.join('images', 'range.jpg'))
rangeimg = pygame.transform.scale(rangeimg, [934,440])
homescreen = pygame.image.load(os.path.join('images', 'homescreen.jpg'))
homescreen = pygame.transform.scale(homescreen, [1024,768])
deathscreen = pygame.image.load(os.path.join('images', 'deathscreen.jpg'))
deathscreen = pygame.transform.scale(deathscreen, [1024, 768])
brick_wall = pygame.image.load(os.path.join('images', 'brick_wall.jpg'))
brick_wall = pygame.transform.scale(brick_wall, [1024,768])

minecraft_button = pygame.image.load(os.path.join('images', 'minecraft_button.jpg'))
minecraft_button = pygame.transform.scale(minecraft_button, [160, 50])
minecraft_buttonLarge = pygame.image.load(os.path.join('images', 'minecraft_button.jpg'))
minecraft_buttonLarge = pygame.transform.scale(minecraft_buttonLarge, [166, 54])
#csgo_t_model = pygame.image.load(os.path.join('images', 'csgo_T_model.png'))
# button('', 30, 30, 964, 470, brown, brown, None, black)

hitmarker = pygame.image.load(os.path.join('images', 'hitmarker.png'))
musicnote = pygame.image.load(os.path.join('images', 'musicnote.png'))
gear = pygame.image.load(os.path.join('images', 'gear.png'))
weaponFlash = pygame.image.load(os.path.join('images', 'flashfinal1.png'))
weaponFlash = pygame.transform.scale(weaponFlash,[25,25])
clock = pygame.time.Clock()
gameDisplay.fill(gray)
pygame.mixer.music.load(os.path.join('images', 'background.wav'))
pygame.mixer.music.load(os.path.join('images', 'background2.mp3'))

font = pygame.font.SysFont("Verdana", 12)
hitmarkers = []
games = ["rust", "csgo"]
# This makes a variable that is called to check what game it is.
game = 0


pauseKey = 108
reloadKey = 112
resetStats = 121

start_tick = 600
current_tick = start_tick
end_tick = 200
ticks_per_decrease = 1
lives = 3
valList = [start_tick, current_tick, end_tick, ticks_per_decrease, lives]

open_target_change = 0
hitmarker_img_change = 0
flash_img_change = 0
sprite_change_list = [open_target_change, hitmarker_img_change, flash_img_change]


pygame.mixer.music.play(-1)
global_time = 0

def get_key():
      while 1:
          event = pygame.event.poll()
          if event.type == KEYDOWN:
              return event.key
          else:
              pass



class gun(object):
    def __init__(self, cost, gunSelectIdle, gunSelectPrac, gunBought):
        self.cost = cost
        self.gunSelectIdle = gunSelectIdle
        self.gunSelectPrac = gunSelectPrac
        self.gunBought = gunBought

# First variable = cost, second = selectIdle, third = selectprac, fourth = gunbought all the states of them, 0 at the start


ak = gun(100, 0, 0, 0)
mp5 = gun(100, 0, 0, 0)


akcs = gun(100, 0, 0, 0)
m4cs = gun(100,0,0,0)
m1cs = gun(100,0,0,0)
famascs = gun(100,0,0,0)
augcs = gun(100,0,0,0)
augscopedcs = gun(100,0,0,0)
galilcs = gun(100,0,0,0)
kreigcs = gun(100,0,0,0)
umpcs = gun(100,0,0,0)
mp7cs = gun(100,0,0,0)
p90cs = gun(100,0,0,0)
mac10cs = gun(100,0,0,0)
bizoncs = gun(100,0,0,0)

weaponSelectedIdle = [baseSelectIdle, ak.gunSelectIdle, mp5.gunSelectIdle, akcs.gunSelectIdle, m4cs.gunSelectIdle, m1cs.gunSelectIdle, famascs.gunSelectIdle
                      , augcs.gunSelectIdle, galilcs.gunSelectIdle, augscopedcs.gunSelectIdle, kreigcs.gunSelectIdle, umpcs.gunSelectIdle
                      , mp7cs.gunSelectIdle, p90cs.gunSelectIdle, mac10cs.gunSelectIdle, bizoncs.gunSelectIdle]
weaponSelectedPractice = [baseSelectPrac, ak.gunSelectPrac, mp5.gunSelectPrac, akcs.gunSelectPrac, m4cs.gunSelectPrac, m1cs.gunSelectPrac, famascs.gunSelectPrac
                          , augcs.gunSelectPrac, galilcs.gunSelectPrac, augscopedcs.gunSelectPrac, kreigcs.gunSelectPrac, umpcs.gunSelectPrac
                          , mp7cs.gunSelectPrac, p90cs.gunSelectPrac, mac10cs.gunSelectPrac]
weaponbought = [ak.gunBought, mp5.gunBought, akcs.gunBought,m4cs.gunBought, m1cs.gunBought, famascs.gunBought, augcs.gunBought, galilcs.gunBought,
                augscopedcs.gunBought, kreigcs.gunBought, umpcs.gunBought, mp7cs.gunBought, p90cs.gunBought, mac10cs.gunBought
                , bizoncs.gunBought]


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


musicsound = Slider("", .5, 1, 0, 300, 180)
recoilamp = Slider("", .5, 1, 0, 15, 350)
sensitivity = Slider("sens", .5, 1, 0, 300, 250)
slides = [musicsound,sensitivity, recoilamp]



def gunbuy(cost, weaponBoughtNum, idleNum, pracNum):
    global scoreNum
    if gamemode == "game_loop_idle":
        if int(scoreNum) >= cost and weaponbought[weaponBoughtNum] == 0:
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


def mp5gunbuy(): gunbuy(mp5.cost, 0, 2, 2)
def akgunbuy(): gunbuy(ak.cost, 0, 1, 1)
def akcsgunbuy(): gunbuy(akcs.cost, 0, 3, 3)
def m4csgunbuy(): gunbuy(m4cs.cost,0,4,4)
def m1csgunbuy(): gunbuy(m1cs.cost,0,5,5)
def famasgunbuy(): gunbuy(famascs.cost,0,6,6)
def auggunbuy(): gunbuy(augcs.cost,0,7,7)
def augscopedgunbuy(): gunbuy(augscopedcs.cost,0,9,9)
def galilgunbuy(): gunbuy(galilcs.cost,0,8,8)
def kreiggunbuy(): gunbuy(kreigcs.cost,0,10,10)
def umpgunbuy(): gunbuy(umpcs.cost,0,11,11)
def mp7gunbuy(): gunbuy(mp7cs.cost,0,12,12)
def p90gunbuy(): gunbuy(p90cs.cost,0,13,13)
def mac10gunbuy(): gunbuy(mac10cs.cost,0,14,14)
def bizongunbuy(): gunbuy(bizoncs.cost,0,15,15)


def target(xx, yy): gameDisplay.blit(targetimg, (xx, yy))


def quitgame(): pygame.quit, quit()


def text_objects(text, font):
    textSurface = font.render(str(text), True, black)
    return textSurface, textSurface.get_rect()


def button2(x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1 and action != None:
            action()


def buttonstate2(gunselect, selectmsg, unselectmsg, x, y, w, h, icselected, acselected, icunselected, acunselected,
              action=None,bordercolor = None):
    if gunselect == 1:
        button(selectmsg, x, y, w, h, icselected, acselected, action,bordercolor)
    elif gunselect == 0:
        button(unselectmsg, x, y, w, h, icunselected, acunselected, action,bordercolor)


def buttonstate(gunselect, gunbought, selectedmsg, boughtmsg, buyingmsg, brokemsg, guncost, x, y, w, h, icselected,
             acselected, icbought, acbought, icbroke, acbroke, icbuying, acbuying, action=None,bordercolor = None):
    if gunbought == 1 and gunselect == 1:
        button(selectedmsg, x, y, w, h, icselected, acselected, action, bordercolor)
    elif gunbought == 1 and gunselect == 0:
        button(boughtmsg, x, y, w, h, icbought, acbought, action,bordercolor)
    elif gunbought == 0 and int(scoreNum) < guncost:
        button(brokemsg, x, y, w, h, icbroke, acbroke, action,bordercolor)
    elif gunbought == 0 and int(scoreNum) >= guncost:
        button(buyingmsg, x, y, w, h, icbuying, acbuying, action,bordercolor)

for i in range(len(weaponSelectedPractice)):
    weaponSelectedPractice[i] = 0
weaponSelectedPractice[2] = 1

def buttonMc(msg, x, y,action=None, minecraft = None ):
    # this gets the mouse's position
    mouse = pygame.mouse.get_pos()
    # This gets when the mouse clicks, it makes a list like this: [1,1,1]
    # left, middle, right, 1 is active, 0 is inactive
    click = pygame.mouse.get_pressed()
    # If mouse[0] or left click is between the box then draw the active color
    if x + 160 > mouse[0] > x and y + 50 > mouse[1] > y:
        #gameDisplay.blit(deathscreen,(x,y))
        gameDisplay.blit(minecraft_buttonLarge, (x-3,y-2))
        # If the click is left then do the action that is called
        if click[0] == 1 and action != None:
            action()
    # If not draw the box with  the inactive color.
    else:
        gameDisplay.blit(minecraft_button, (x,y))

   # This calls a small text. It goes the font then font size
    if minecraft == 1:
        smallText = pygame.font.Font("Minecraft.ttf", 20)
    else:
        smallText = pygame.font.Font("freesansbold.ttf", 20)

    # no clue just do it
    textSurf, textRect = text_objects(msg, smallText)
    # This makes the text in the center of the button
    textRect.center = ((x + (160 / 2)), (y + (50 / 2)))
    # Draws something on screen
    gameDisplay.blit(textSurf, textRect)


def button(msg, x, y, w, h, ic, ac, action=None, bordercolor = None):
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
    if bordercolor != None:
        pygame.draw.rect(gameDisplay,bordercolor,(x,y,w,h),2)

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
# goes left again for 5 bulletsn
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

AKPOSCS = (
 (6, -10),
 (-5, -26),
 (4, -39),
 (1, -42),
 (-18, -44),
 (-10, -38),
 (-19, -28),
 (22, -19),
 (60, 4),
 (29, -3),
 (-19, -14),
 (22, -8),
 (40, 5),
 (-3, 6),
 (-52, -6),
 (-26, -12),
 (-18, -13),
 (-38, 1),
 (-44, 13),
 (25, 3),
 (-5, -5),
 (8, -12),
 (10, -4),
 (-26, 2),
 (-9, -6),
 (30, 1),
 (43, 4),
 (64, 28),
 (20, 0),
 (0, 0),
)

M4POSCS = (
 (-3, -15),
 (1, -17),
 (9, -32),
 (-11, -42),
 (14, -48),
 (10, -53),
 (-31, -28),
 (-20, -25),
 (-45, -12),
 (10, -21),
 (32, -12),
 (62, 9),
 (48, -1),
 (53, 12),
 (0, -9),
 (-18, -8),
 (20, -1),
 (30, 5),
 (-5, -3),
 (-69, -1),
 (-18, -13),
 (-55, -6),
 (-18, -3),
 (-22, -2),
 (22, 2),
 (-10, -10),
 (-9, -9),
 (-8, -2),
 (-8, 2),
 (0, 0),
)

M1POSCS = (
 (-2, -10),
 (2, -10),
 (7, -28),
 (-10, -36),
 (11, -43),
 (9, -47),
 (-27, -28),
 (-15, -24),
 (-37, -10),
 (8, -19),
 (30, -10),
 (48, 6),
 (40, -2),
 (42, 7),
 (-2, -5),
 (-15, -8),
 (20, -2),
 (17, 2),
 (6, 3),
 (0, 0),
)

FAMASPOSCS = (
 (9, -8),
 (-2, -8),
 (13, -20),
 (3, -35),
 (-2, -40),
 (-28, -37),
 (-33, -23),
 (13, -23),
 (39, -16),
 (35, -11),
 (25, -4),
 (-11, -11),
 (-45, -8),
 (-24, -11),
 (-39, 7),
 (-10, -3),
 (-30, -1),
 (-6, -8),
 (10, -4),
 (48, 2),
 (7, -7),
 (-22, 1),
 (-30, 13),
 (-30, 23),
 (0, 0),
)

AUGPOSCS = (
 (-8, -12),
 (0, -25),
 (8, -45),
 (14, -52),
 (-11, -58),
 (-17, -61),
 (-27, -39),
 (-13, -32),
 (-27, -25),
 (33, -22),
 (10, -12),
 (-29, -1),
 (-2, -14),
 (47, -7),
 (74, 23),
 (64, 26),
 (4, -12),
 (12, -12),
 (16, 1),
 (-48, -3),
 (-65, -6),
 (-18, -14),
 (-11, 4),
 (-23, 3),
 (-58, 20),
 (-38, 1),
 (33, -10),
 (42, -10),
 (-10, 3),
 (0, 0),
)

AUGSCOPEDPOSCS = (
 (-6, -8),
 (3, -8),
 (4, -11),
 (5, -24),
 (-5, -34),
 (-9, -39),
 (-15, -27),
 (-7, -20),
 (-15, -15),
 (21, -15),
 (4, -8),
 (-18, -0),
 (0, -10),
 (29, -4),
 (44, 15),
 (34, 16),
 (0, -9),
 (6, -8),
 (9, 1),
 (-31, -2),
 (-38, -3),
 (-26, -4),
 (11, -2),
 (8, -2),
 (-55, 20),
 (-21, -1),
 (23, -7),
 (20, -3),
 (3, -2),
 (0, 0),
)

GALILPOSCS = (
 (-8, -9),
 (5, -9),
 (-13, -21),
 (-24, -28),
 (2, -42),
 (-3, -49),
 (-13, -34),
 (-22, -18),
 (9, -27),
 (44, -18),
 (60, 8),
 (59, 22),
 (18, -13),
 (24, -6),
 (13, -2),
 (-1, 2),
 (-7, -17),
 (-51, -14),
 (-27, -7),
 (-50, 7),
 (-62, 16),
 (-11, -5),
 (23, -7),
 (-25, 4),
 (-21, 3),
 (-31, 6),
 (17, -9),
 (64, 11),
 (50, 5),
 (27, -11),
 (-12, -16),
 (29, 7),
 (47, 28),
 (28, 3),
 (0, 0),
)
KREIGPOSCS = (
    (6, -12),
    (21, -26),
    (13, -39),
    (11, -46),
    (13, -52),
    (10, -56),
    (32, -23),
    (-22, -27),
    (13, -20),
    (26, -12),
    (8, -8),
    (-9, -7),
    (12, -11),
    (-3, -17),
    (22, 7),
    (32, 29),
    (28, 13),
    (13, 5),
    (-65, -6),
    (-91, 9),
    (-68, 1),
    (-28, -15),
    (-24, -15),
    (-9, -10),
    (-35, 5),
    (-44, 5),
    (10, -12),
    (22, -8),
    (62, 8),
    (0, 0),
)

UMPPOSCS = (
 (2, -13),
 (7, -16),
 (3, -34),
 (9, -44),
 (19, -45),
 (5, -52),
 (-22, -34),
 (8, -24),
 (-17, -26),
 (-37, -17),
 (-28, -9),
 (1, -7),
 (-9, -12),
 (0, -11),
 (-18, 6),
 (-11, 5),
 (25, -11),
 (38, -4),
 (-1, 4),
 (-27, 12),
 (-33, 4),
 (8, -4),
 (43, 2),
 (7, 3),
 (0, 0),
)

MP7POSCS = (
    (0, -8),
    (2, -7),
    (6, -6),
    (11, -19),
    (18, -28),
    (-1, -34),
    (19, -25),
    (6, -26),
    (21, -7),
    (12, -7),
    (-17, -17),
    (-38, -8),
    (-36, -3),
    (-29, -1),
    (-2, -10),
    (12, -11),
    (8, -1),
    (7, -5),
    (-7, -5),
    (4, -8),
    (30, 6),
    (40, 19),
    (8, 0),
    (18, 4),
    (-5, 5),
    (3, 5),
    (3, -5),
    (7, -1),
    (1, -6),
    (0, 0),
)

P90POSCS = (
   (6, -7),
   (-1, -8),
   (-4, -10),
   (6, -23),
   (22, -30),
   (24, -24),
   (20, -34),
   (-17, -28),
   (-20, -26),
   (-4, -23),
   (-6, -24),
   (6, -14),
   (25, -1),
   (11, -6),
   (14, -5),
   (20, 0),
   (-24, -3),
   (-32, -2),
   (-21, -3),
   (-20, -2),
   (-28, 2),
   (-20, 7),
   (-9, -1),
   (0, 0),
   (23, -1),
   (29, 0),
   (41, 4),
   (5, -3),
   (-11, -7),
   (8, -3),
   (6, -6),
   (-9, -2),
   (-29, 1),
   (-18, 2),
   (8, -2),
   (4, -1),
   (24, 2),
   (24, 4),
   (-4, -4),
   (-25, 0),
   (-38, 9),
   (-18, 3),
   (-24, 1),
   (-31, 6),
   (-17, -2),
   (-22, 8),
   (8, -6),
   (24, -6),
   (-9, 3),
   (0, 0),
)

MAC10POSCS = (
    (9, -6),
    (3, -7),
    (-6, -12),
    (-8, -27),
    (-20, -33),
    (-23, -48),
    (-17, -41),
    (11, -34),
    (-17, -20),
    (-8,  -22),
    (-9, -22),
    (5, -15),
    (4, -8),
    (19, -6),
    (41, -1),
    (58, 13),
    (3, 1),
    (23, 7),
    (-13, 0),
    (12, 5),
    (24, 1),
    (21, -4),
    (-32, -2),
    (-26, -4),
    (-31, -1),
    (-43, 3),
    (-5, -8),
    (42, 10),
    (-5, 2),
    (0, 0),
)

BIZONPOSCS = (
    (2, -9), #2
    (5, -6), #3
    (7, -15), #4
    (15, -24), #5
    (25, -29), #6
    (-6, -39), #7
    (-18, -38), #8
    (-1, -33), #9
    (-37, -11), #10
    (-28, -10), #11
    (-11, -17),
    (-28, -4),
    (13, -15),
    (51, 2),
    (0, -6),#16
    (-25, 0),
    (-12, 0),
    (8, -6),
    (-13, -11),
    (-19, -4), #21
    (500, 1),
    (500, -15),
    (500, -15),
    (500, -10),
    (500, 5), #26
    (500, 5),
    (500, -12),
    (500, -8),
    (500, 8),
    (500, 0), #31
    (500, -8),
    (500, -7),
    (500, -6),
    (500, -46),
    (500, -52), #36
    (500, -56),
    (500, -23),
    (500, -27),
    (500, -20),
    (500, -12), #41
    (500, -8),
    (500, -7),
    (500, -11),
    (500, -17),
    (500, 7),
    (500, 29), #47
    (500, 13),
    (500, 5),
    (500, -6),
    (500, 9),
    (500, 1), #52
    (500, -15),
    (500, -15),
    (500, -10),
    (500, 5),
    (500, 5), #57
    (500, -12), #58
    (500, -8), #59
    (500, 8), #60
    (500, 0), #61
    (500, -8), #62
    (500, 8), #63
    (500, 0), #64
    (500, -8),

)

dummypos = (
    (500, -8),
    (500, -7),
    (500, -6),
    (500, -46),
    (500, -52),
    (500, -56),
    (500, -23),
    (500, -27),
    (500, -20),
    (500, -12),
    (500, -8),
    (500, -7),
    (500, -11),
    (500, -17),
    (500, 7),
    (500, 29),
    (500, 13),
    (500, 5),
    (500, -6),
    (500, 9),
    (500, 1),
    (500, -15),
    (500, -15),
    (500, -10),
    (500, 5),
    (500, 5),
    (500, -12),
    (500, -8),
    (500, 8),
    (500, 0),
)
def makeGunStart(GUNPOS,sleepTime):
    global scoreNum, hitNum, hitmarkers, miss_num, hit_percent, hit_percent_label
    click = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    if 0 <= x - 250 <= 300 and 0 <= y - 150 <= 300 and click[0] == 1:
        #0 <= x - 250 <= 300 and 0 <= y - 150 <= 300 put this back when you want it tarrget only
        for dx, dy in GUNPOS:
            recoilchange = recoilamp.val * 2
            dx *= recoilchange
            dy *= recoilchange
            x,y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                x,y = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if event.key == keybindList[0]:
                        pause = True
                        paused()
                    if event.key == keybindList[1]:
                        hitmarkers = []
                    if event.key == keybindList[2]:
                        clear_stats()
            # make teh 250 300 when done with guns
            if x - 250 > 330:
                break
            button("", 0, 0, 580, 768, gray, gray)
            blit_labels_prac()
            click = pygame.mouse.get_pressed()
            if click[0] != 1:
                break
            pygame.mouse.set_pos(x + dx, y + dy)
            hitmarkers.append((x - 5, y - 5))
            for z in range(len(hitmarkers)):
                gameDisplay.blit(hitmarker, (hitmarkers[z][0], hitmarkers[z][1]))
            gameDisplay.blit(weaponFlash, (x - 12, y - 12))
            if 0 <= x - 250 <= 300 and 0 <= y - 150 <= 300:
                if gamemode == "game_loop_idle":
                    scoreNum += scoreAdd
                    hit_percent = hitNum / (scoreNum + miss_num)
                    hit_percent_label = round(hit_percent,2)
                    if int(scoreNum) >= upgradecost:
                        button(upgradelabel, 600, 90, 180, 50, green, bright_green)
                        button('UPGRADE (MAX)', 800, 90, 180, 50, green, bright_green)
                    if int(scoreNum) < upgradecost:
                        button('UPGRADE (MAX)', 800, 90, 180, 50, red, bright_red)
                elif gamemode == "game_loop_practice":
                    hitNum += hitAdd
                    hit_percent = hitNum / (hitNum + miss_num)
                    hit_percent_label = round(hit_percent,2)
            else:
                if gamemode == "game_loop_idle":
                    miss_num += 1
                    hit_percent = miss_num / (scoreNum + miss_num)
                    hit_percent_label = round(hit_percent,2)
                    if int(scoreNum) >= upgradecost:
                        button(upgradelabel, 600, 90, 180, 50, green, bright_green)
                        button('UPGRADE (MAX)', 800, 90, 180, 50, green, bright_green)
                    if int(scoreNum) < upgradecost:
                        button('UPGRADE (MAX)', 800, 90, 180, 50, red, bright_red)
                elif gamemode == "game_loop_practice":
                    miss_num += 1
                    hit_percent = hitNum / (hitNum + miss_num)
                    hit_percent_label = round(hit_percent,2)

            pygame.display.update()
            time.sleep(sleepTime)

def clear_stats():
    global miss_num, hit_percent, hitNum, scoreNum, hit_percent_label
    miss_num = 0
    hitNum = 0
    scoreNum = 0
    hit_percent = 0
    hit_percent_label = 0


def akrust(): makeGunStart(AKPOS,.125)
def mp5rust(): makeGunStart(mp5pos,.1)
def akcscall(): makeGunStart(AKPOSCS, .091)
def m4cscall(): makeGunStart(M4POSCS, .091)
def m1cscall(): makeGunStart(M1POSCS, .1)
def famascscall(): makeGunStart(FAMASPOSCS, .091)
def augcscall(): makeGunStart(AUGPOSCS, .091)
def augscopedcscall(): makeGunStart(AUGSCOPEDPOSCS, .091)
def galilcscall(): makeGunStart(GALILPOSCS, .091)
def kreigcscall(): makeGunStart(KREIGPOSCS, .091)
def umpcscall(): makeGunStart(UMPPOSCS, .091)
def mp7cscall(): makeGunStart(MP7POSCS, .08)
def p90cscall(): makeGunStart(P90POSCS, .07)
def mac10cscall(): makeGunStart(MAC10POSCS, .075)


csguncalldict = {'0': akcscall, '1': m4cscall, '2': m1cscall, '3': famascscall, '4': augcscall,
             '5': galilcscall, '6': augscopedcscall, '7': kreigcscall, '8': umpcscall,
             '9': mp7cscall, '10': p90cscall, '11': mac10cscall}



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

# valList = [start_tick, current_tick, end_tick, ticks_per_decrease, lives]

def deathScreen():
    global valList, play
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.blit(deathscreen,(0,0))
        valList[4] = 3
        valList[1] = valList[0]
        play = 0
        button2(243,415,565,55, game_loop_flickPractice)
        button2(243,488,565,55, game_intro)
        pygame.display.update()


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
        # gameDisplay.fill(gray)
        gameDisplay.blit(homescreen,(0,0))



        # The two buttons on this page, remember not to put the () in the function being called
        button("Play Game", 80, 530, 140, 50, green, bright_green, game_loop_idle)
        button("Play Practice", 80, 590, 140, 50, green, bright_green, game_loop_practice)
        button('Flick Practice', 80, 650, 140, 50, green, bright_green, game_loop_flickPractice)
        # button("Quit", 620, 450, 100, 50, red, bright_red, quitgame)
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


keybindList = [pauseKey, reloadKey, resetStats]
dictKeys = {0: K_0, 1: K_1, 2: K_2, 3: K_3, 4: K_4, 5: K_5, 6: K_6, 7: K_7, 8: K_8, 9: K_9}

def changeVal(keyIndex):
    global valList
    tempstr = str(valList[keyIndex])
    while True:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            tempstr = tempstr[:-1]

        elif inkey == K_RETURN:
            game_loop_flickPractice()
        elif inkey > 47 and inkey < 58:
            tempstr += chr(inkey)
        try:
            valList[keyIndex] = int(tempstr)
        except ValueError:
            valList[keyIndex]= 0
        blit_labels_flick()


def change_start_tick(): changeVal(0)
def change_end_tick(): changeVal(2)
def change_tick_interval(): changeVal(3)
def change_live_count(): changeVal(4)
def changeKeyBind(keyIndex):
    global keybindList
    inkey = get_key()
    while 1:
        if inkey <= 500:
            keybindList[keyIndex] = inkey
            break


def reset_stats_hotkey(): changeKeyBind(2)
def clear_decals_key(): changeKeyBind(1)
def pause_hotkey(): changeKeyBind(0)

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
        fontsmall.render_to(gameDisplay, (80, 70), "Keybinds", black)
        button("Back", 100, 650, 100, 50, green, bright_green)
        button(("Clear Decals: " + chr(keybindList[1])), 50,140, 160,50, green,bright_green, clear_decals_key)
        button(("Pause: " + chr(keybindList[0])), 50,200, 160,50, green,bright_green, pause_hotkey)
        button(("Clear Stats: " + chr(keybindList[2])), 50, 260, 160,50, green, bright_green, reset_stats_hotkey)

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
                if musicsound.button_rect.collidepoint(pos):
                    musicsound.hit = True
                if sensitivity.button_rect.collidepoint(pos):
                    sensitivity.hit = True
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


def change_flash():
    global sprite_change_list, check_in_dropdown
    check_in_dropdown = 1
    if sprite_change_list[2] == 0:
        for i in range(3):
            sprite_change_list[i] = 0
        sprite_change_list[2] = 1
    else:
        sprite_change_list[2] = 0

def change_hitmarker():
    global sprite_change_list, check_in_dropdown
    check_in_dropdown = 1
    if sprite_change_list[1] == 0:
        for i in range(3):
            sprite_change_list[i] = 0
        sprite_change_list[1] = 1
    else:
        sprite_change_list[1] = 0

check_in_dropdown = 0
def change_target():
    global open_target_change
    global check_in_dropdown
    check_in_dropdown = 1
    if sprite_change_list[0] == 0:
        # makes the other dropdowns disabled
        for i in range(3):
            sprite_change_list[i] = 0
        sprite_change_list[0] = 1
    else:
        sprite_change_list[0] = 0
def make_flash_flash():
    global weaponFlash, sprite_change_list, check_in_dropdown
    weaponFlash = pygame.image.load(os.path.join('images', 'flashfinal1.png'))
    weaponFlash = pygame.transform.scale(weaponFlash, [25, 25])
    sprite_change_list[2] = 0
    check_in_dropdown = 0
def make_flash_nothing():
    global weaponFlash, sprite_change_list, check_in_dropdown
    weaponFlash = pygame.image.load(os.path.join('images', 'nothing.png'))

    sprite_change_list[2] = 0
    check_in_dropdown = 0
def make_hitmarker_cod():
    global hitmarker, sprite_change_list, check_in_dropdown
    hitmarker = pygame.image.load(os.path.join('images', 'hitmarker.png'))

    sprite_change_list[1] = 0
    check_in_dropdown = 0
def make_hitmarker_hole():
    global hitmarker, sprite_change_list, check_in_dropdown
    hitmarker = pygame.image.load(os.path.join('images', 'bullethole.png'))
    hitmarker = pygame.transform.scale(hitmarker, [15, 15])
    sprite_change_list[1] = 0
    check_in_dropdown = 0
def make_target_target():
    global targetimg, sprite_change_list, check_in_dropdown
    targetimg = pygame.image.load(os.path.join('images', 'shooting_target.png'))

    sprite_change_list[0] = 0
    check_in_dropdown = 0
def make_target_CS():
    global targetimg, sprite_change_list, check_in_dropdown
    targetimg = pygame.image.load(os.path.join('images', 'mp5.png'))
    sprite_change_list[0] = 0
    check_in_dropdown = 0


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
                if event.key == keybindList[0]:
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
                    180, 50, peach, peach, dark_peach, peach, red, bright_red, green, bright_green, akgunbuy, black)

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


def game_loop_practice():
    global pause, gamemode,hitmarkers, y_practice_value, recoilamp, global_time
    gamemode = "game_loop_practice"
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == keybindList[0]:
                    pause = True
                    paused()
                if event.key == keybindList[1]:
                    hitmarkers = []
                if event.key == keybindList[2]:
                    clear_stats()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button2(250, 650, 50, 50, settings)
                    if check_in_dropdown == 0:
                        button2(600, y_practice_value + 630, 180, 50, change_target)
                        button2(800, y_practice_value + 570, 180, 50, change_hitmarker)
                        button2(600, y_practice_value + 570, 180, 50, change_flash)
                    button2(600, y_practice_value + 80, 80, 50, changeGameDown)
                    button2(900, y_practice_value + 80, 80, 50, changeGameUp)
                    pos = pygame.mouse.get_pos()
                    if recoilamp.button_rect.collidepoint(pos):
                        recoilamp.hit = True
                if event.button == 4: y_practice_value += 10
                if event.button == 5: y_practice_value -= 10
            elif event.type == pygame.MOUSEBUTTONUP:
                for s in slides:
                    s.hit = False
        for s in slides:
            if s.hit:
                s.move()
        gameDisplay.fill(gray)
        button('', 580, 0, 450, 768, (153, 76, 0), (153, 76, 0))
        blit_labels_prac()
        recoilamp.draw('')
        for x in range(len(hitmarkers)):
            gameDisplay.blit(hitmarker, (hitmarkers[x][0], hitmarkers[x][1]))


        if game == 0:
            button("RUST", 700, y_practice_value + 80, 180, 50, red, red, None, black)

            buttonstate2(weaponSelectedPractice[1], "AK Selected", "Select AK", 800, y_practice_value + 150,
                         180, 50, peach, peach, dark_peach, peach, akgunbuy, black)

            buttonstate2(weaponSelectedPractice[2], "MP5 Selected", "Select MP5", 600, y_practice_value + 210, 180, 50,
                         peach, peach, dark_peach, peach, mp5gunbuy, black)

            # Checks if the weapon is selected if it is call the recoil for it.
            if weaponSelectedPractice[1] == 1:
                akrust()
            if weaponSelectedPractice[2] == 1:
                mp5rust()

        if game == 1:
            button("CSGO", 700, y_practice_value+ 80, 180, 50, red, red, None,black)

            buttonstate2(weaponSelectedPractice[3], "AK47 Selected", "Select AK47", 800, y_practice_value + 150,
                         180, 50, peach, peach, dark_peach, peach, akcsgunbuy, black)
            buttonstate2(weaponSelectedPractice[4], "M4A4 Selected", "Select M4A4", 600, y_practice_value + 210,
                         180, 50, peach, peach, dark_peach, peach, m4csgunbuy, black)
            buttonstate2(weaponSelectedPractice[5], "M4A1 Selected", "Select M4A1", 800, y_practice_value + 210,
                         180, 50, peach, peach, dark_peach, peach, m1csgunbuy, black)
            buttonstate2(weaponSelectedPractice[10], "SG553 Selected", "Select SG553", 600, y_practice_value + 330,
                         180, 50, peach, peach, dark_peach, peach, kreiggunbuy, black)
            buttonstate2(weaponSelectedPractice[7], "AUG Selected", "Select AUG", 600, y_practice_value + 270,
                         180, 50, peach, peach, dark_peach, peach, auggunbuy, black)
            buttonstate2(weaponSelectedPractice[9], "AUG Scoped", "AUG Scoped", 800, y_practice_value + 270,
                         180, 50, peach, peach, dark_peach, peach, augscopedgunbuy, black)
            buttonstate2(weaponSelectedPractice[6], "FAMAS Selected", "Select FAMAS", 600, y_practice_value + 390,
                         180, 50, peach, peach, dark_peach, peach, famasgunbuy, black)
            buttonstate2(weaponSelectedPractice[8], "GALIL Selected", "Select GALIL", 800, y_practice_value + 330,
                         180, 50, peach, peach, dark_peach, peach, galilgunbuy, black)
            buttonstate2(weaponSelectedPractice[12], "MP7 Selected", "Select MP7", 600, y_practice_value + 510,
                         180, 50, peach, peach, dark_peach, peach, mp7gunbuy, black)
            buttonstate2(weaponSelectedPractice[13], "P90 Selected", "Select P90", 800, y_practice_value + 390,
                         180, 50, peach, peach, dark_peach, peach, p90gunbuy, black)
            buttonstate2(weaponSelectedPractice[14], "MAC10 Selected", "Select MAC10", 600, y_practice_value + 450,
                         180, 50, peach, peach, dark_peach, peach, mac10gunbuy, black)
            buttonstate2(weaponSelectedPractice[11], "UMP Selected", "Select UMP", 800, y_practice_value + 450,
                         180, 50, peach, peach, dark_peach, peach, umpgunbuy, black)

            for i in range(12):
                if weaponSelectedPractice[i + 3] == 1:
                    csguncalldict[str(i)]()
                else:
                    continue

        pygame.display.update()
        clock.tick(144)

def makePlay():
    global play
    play = 1
    game_loop_flickPractice()
def makeStop():
    global play
    play = 0
    game_loop_flickPractice()
play = 0


def game_loop_flickPractice():
    global gamemode, targets, misses, hits, global_time, rainbow_target, rainbow_dynamic, valList, play
    # valList = [start_tick, current_tick, end_tick, ticks_per_decrease, lives]

    gamemode = 'game_loop_flickPractice'
    global_time = 0
    target_time = valList[0]
    target_reset = 0
    tick_sub = valList[3]
    tick_reset = 0
    target_shape_reset = 0
    target_min_size = 1
    target_max_size = 75
    gameDisplay.fill(gray)
    targets = []
    misses = 0
    hits = 0
    lives = valList[4]
    clock.tick(0)
    while not gameExit:
        blit_labels_flick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button2(540, 580, 160, 50, makePlay)
                button2(710, 580, 160, 50, makeStop)

                for i in range(len(targets) - 1):
                    xpos, ypos = pygame.mouse.get_pos()
                    if targets[i][0] + targets[i][2]/2 > xpos > targets[i][0] - targets[i][2]/2 \
                            and targets[i][1] + targets[i][2]/2 > ypos > targets[i][1]-targets[i][2]/2:
                        del targets[i]

                        hits += 1
                        break
                    if i >= len(targets) - 2:
                        misses += 1
        if play == 1:
            if target_reset >= target_time:
                x = random.randint(69, 956)
                y = random.randint(68, 424)
                targets.append([x, y, target_min_size, 0, 0])
                pygame.display.update()
                target_reset = 0
            for i in range(len(targets) - 1):
                if targets[i][4] == 0:
                    targets[i][2] += 1
                    targets[i][3] = pygame.transform.scale(rainbow_target, [targets[i][2], targets[i][2]])
                    if targets[i][2] > target_max_size:
                        targets[i][4] = 1
                else:
                    targets[i][2] -= 1
                    targets[i][3] = pygame.transform.scale(rainbow_target, [targets[i][2], targets[i][2]])
                    if targets[i][2] < target_min_size:
                        del targets[i]
                        lives -= 1
                        if lives <= 0:
                            deathScreen()
            if tick_reset >= tick_sub:
                if target_time > valList[2]:
                    target_time -= .05
                tick_reset = 0

        #if it gets faster than this it will crash
            if target_time <= 20:
                target_time = 20
            dt = clock.tick(60)
            target_reset += dt
            tick_reset += dt
            target_shape_reset += dt
            global_time += dt/1000
            valList[4] = lives
            valList[3] = tick_sub
            valList[1] = target_time
def blit_labels_flick():
    time_second = int(global_time % 60)
    time_minute = int(global_time//60)
    gameDisplay.blit(brick_wall,(0,0))
    # gameDisplay.fill(gray)
    time_secondstr = str(time_second)
    if time_second < 10:
        time_secondstr = '0' + str(time_second)
    buttonMc("Back", 30, 700, game_intro)
    gameDisplay.blit(rangeimg, (30,30))
    # button('', 30, 30, 964, 470, brown, brown, None, black)
    buttonMc(("Start Tick: " + str(valList[0])), 30, 520, change_start_tick)
    buttonMc(("End Tick: " + str(valList[2])), 200, 520,change_end_tick)
    buttonMc(("Tick Interval: " + str(valList[3])), 30, 580,change_tick_interval)
    buttonMc('Tick: ' + str(int(valList[1])), 200, 580)
    buttonMc('Lives: ' + str(valList[4]), 370, 520,change_live_count)
    buttonMc("Hits: " + str(hits), 540, 520, 160)
    buttonMc("Misses: " + str(misses), 710, 520)
    buttonMc('Time ' + str(time_minute) + ':' + str(time_secondstr), 370, 580)
    buttonMc("Start", 540, 580)
    buttonMc("End", 710, 580)
    for i in range(len(targets)):
        try:
            gameDisplay.blit(targets[i][3], [targets[i][0] - targets[i][2] / 2, targets[i][1] - targets[i][2]/ 2])
        except TypeError:
            pass
    pygame.display.update()


def blit_labels_prac():
    button('', 25, 50, 170, 180, peach, peach, None, brown)
    fontsmall.render_to(gameDisplay, (140,72), str(int(hitNum)), black)
    fontsmall.render_to(gameDisplay, (120,360), str(round(recoilamp.val * 100)), black)
    recoilamp.draw('')
    fontsmall.render_to(gameDisplay, (20, 320), "Recoil Scale", black)
    fontsmall.render_to(gameDisplay, (80, 70), "Hits:", black)
    fontsmall.render_to(gameDisplay, (46, 100), "Misses:", black)
    fontsmall.render_to(gameDisplay, (38, 125), "Percent:", black)
    gameDisplay.blit(gear, (250, 650))
    button("Back", 100, 650, 100, 50, green, bright_green, game_intro)
    button("Clear Hitmarkers", 350, 650, 170, 50, green, bright_green, clearHitmakers)
    gameDisplay.blit(targetimg, (200, 150))
    fontsmall.render_to(gameDisplay, (140, 100), str(int(miss_num)), black)
    fontsmall.render_to(gameDisplay, (140, 125), str(hit_percent_label), black)
    button("Reset", 50, 165, 100, 50, darkish_peach, dark_peach, clear_stats,brown)
    if weaponSelectedPractice[0] != 1:
        button("Select Base", 600, y_practice_value + 150, 180, 50, dark_peach, peach, baseselect2, black)
    elif weaponSelectedPractice[0] == 1:
        button("Base Selected", 600, y_practice_value + 150, 180, 50, peach, peach, baseselect2, black)
    gameDisplay.blit(backarrow, (600, y_practice_value + 80))
    gameDisplay.blit(forwardsarrow, (900, y_practice_value + 80))
    button("Target Type \/", 600, y_practice_value + 630, 180, 50, dark_peach, peach, None, black)
    button("Hitmarker Type \/", 800, y_practice_value + 570, 180, 50, dark_peach, peach, None, black)
    button("Weapon Flash \/", 600, y_practice_value + 570, 180, 50, dark_peach, peach, None, black)
    if sprite_change_list[0] == 1:
        button("Target", 600, y_practice_value + 680, 180, 50, dark_peach, peach,make_target_target, black)
        button("CSGO Model", 600, y_practice_value + 730, 180, 50, dark_peach, peach,make_target_CS, black)
    if sprite_change_list[1] == 1:
        button("COD Hitmarker", 800, y_practice_value + 620, 180, 50, dark_peach, peach, make_hitmarker_cod, black)
        button("Bullet Hole", 800, y_practice_value + 670, 180, 50, dark_peach, peach, make_hitmarker_hole, black)
    if sprite_change_list[2] == 1:
        button("Realistic Flash", 600, y_practice_value + 620, 180, 50, dark_peach, peach, make_flash_flash, black)
        button("Nothing", 600, y_practice_value + 670, 180, 50, dark_peach, peach, make_flash_nothing, black)

gamemodesDict = {"game_intro": game_intro, "game_loop_idle": game_loop_idle, "game_loop_practice": game_loop_practice}
game_intro()
