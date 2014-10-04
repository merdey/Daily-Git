import random, pygame, sys
from pygame.locals import *

#constants
FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
LANES = 10
LANEHEIGHT = WINDOWHEIGHT / LANES
MISSILESPEED = 40
FIRINGINTEVAL = 5
MISSILERAD = int(LANEHEIGHT / 2)
    

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BGCOLOR = WHITE
SHIPCOLOR = RED
MISSILECOLOR = BLACK
TEXTCOLOR = BLACK

def main():
    pygame.init()

    #globals and set up surface, clock
    global DISPLAYSURF, FPSCLOCK
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Dodging v1")
    FPSCLOCK = pygame.time.Clock()

    shipPos = [0, int(LANES / 2)]
    missiles = []
    i = 0
    score = []
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    shipPos[1] -= 1
                elif event.key == K_DOWN:
                    shipPos[1] += 1

        i += 1
        if i >= FIRINGINTEVAL:
            i -= FIRINGINTEVAL
            fireMissile(missiles, LANES, WINDOWWIDTH)

        DISPLAYSURF.fill(WHITE)
        displayShip(shipPos, SHIPCOLOR, LANEHEIGHT)
        drawMissiles(missiles, MISSILECOLOR, MISSILERAD, LANEHEIGHT)
        updateMissilesAndScore(missiles, MISSILESPEED, score)
        
        pygame.display.update()
        if detectCollisions(shipPos, missiles, LANEHEIGHT):
            loseAnimation(score, TEXTCOLOR)
            pygame.time.wait(2000)

            #reset game
            shipPos = [0, int(LANES / 2)]
            missiles = []
            i = 0
            score = []
            pygame.display.update()
            
        FPSCLOCK.tick(FPS)

def displayShip(shipPos, SHIPCOLOR, LANEHEIGHT):
    pygame.draw.rect(DISPLAYSURF, SHIPCOLOR, (shipPos[0], shipPos[1] * LANEHEIGHT, LANEHEIGHT, LANEHEIGHT))

def fireMissile(missiles, LANES, WINDOWWIDTH):
    x = WINDOWWIDTH
    y = random.randint(0, LANES)
    missiles.append([x, y])

def drawMissiles(missiles, MISSILECOLOR, MISSILERAD, LANEHEIGHT):
    for missile in missiles:
        pygame.draw.circle(DISPLAYSURF, MISSILECOLOR, (missile[0], int((missile[1] * LANEHEIGHT) - (LANEHEIGHT / 2))), MISSILERAD)

def updateMissilesAndScore(missiles, MISSILESPEED, score):
    for missile in missiles:
        missile[0] -= MISSILESPEED
        if missile[0] < 0:
            del missiles[0]
            score.append(0)

def detectCollisions(shipPos, missiles, LANEHEIGHT):
    shipLane = shipPos[1]
    for missile in missiles:
        missileLane = missile[1]
        if missileLane == (shipLane + 1):
            if missile[0] <= LANEHEIGHT:
                return True
    return False

def loseAnimation(score, TEXTCOLOR):
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('You Lost', True, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 150)

    fontObj2 = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj2 = fontObj.render('Your Score: ' + str(len(score)), True, BLACK)
    textRectObj2 = textSurfaceObj.get_rect()
    textRectObj2.center = (200, 250)
    
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
    pygame.display.update()
    
main()
