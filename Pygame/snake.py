import random, pygame, sys
from pygame.locals import *
pygame.init()

FPS = 20
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
BLOCKSIZE = 20
MAX_X = WINDOWWIDTH / BLOCKSIZE
MAX_Y = WINDOWHEIGHT / BLOCKSIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)

SNAKECOLOR = GREEN
MOUSECOLOR = GREY

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Snake Test")
    
    snake = [(7,2), (6,2), (5,2)]
    mouse = newRandomMouse(MAX_X, MAX_Y)
    velX = 1
    velY = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP and velY != 1:
                    velX = 0
                    velY = -1
                elif event.key == K_DOWN and velY != -1:
                    velX = 0
                    velY = 1
                elif event.key == K_RIGHT and velX != -1:
                    velX = 1
                    velY = 0
                elif event.key == K_LEFT and velX != 1:
                    velX = -1
                    velY = 0

        if snakeTouchingPoint(snake, mouse):
            growSnake(snake)
            mouse = newRandomMouse(MAX_X, MAX_Y)
            
        if hasLost(snake, MAX_X, MAX_Y):
            loseAnimation(len(snake))
            pygame.time.wait(2000)
            snake, mouse, velX, velY = resetGame(snake, mouse, velX, velY, MAX_X, MAX_Y)
            
        if snakeTouchingSnake(snake):
            loseAnimation(len(snake))
            pygame.time.wait(2000)
            snake, mouse, velX, velY = resetGame(snake, mouse, velX, velY, MAX_X, MAX_Y)


        DISPLAYSURF.fill(WHITE)
        displaySnake(DISPLAYSURF, snake, BLOCKSIZE, SNAKECOLOR)
        updateSnake(snake, velX, velY)
        displayMouse(DISPLAYSURF, mouse, BLOCKSIZE, MOUSECOLOR)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    
def updateSnake(snake, velX, velY):
    copy = list(snake)
    for i in range(len(snake)):
        snake[i] = copy[i - 1]
    snake[0] = (copy[0][0] + velX, copy[0][1] + velY)
    return snake

def growSnake(snake):
    xDiff = snake[-2][0] - snake[-1][0]
    yDiff = snake[-2][1] - snake[-1][1]
    newX = snake[-1][0] - xDiff
    newY = snake[-1][1] - yDiff

    snake.append((newX, newY))

def newRandomMouse(MAX_X, MAX_Y):
    x = random.randint(1, MAX_X - 1)
    y = random.randint(1, MAX_Y - 1)
    return (x, y)

def displaySnake(surface, snake, blockSize, color):
    for block in snake:
        x = block[0] * blockSize
        y = block[1] * blockSize
        pygame.draw.rect(surface, color, (x, y, blockSize, blockSize))

def displayMouse(surface, mouse, blockSize, color):
    rad = int(blockSize / 2)
    x = mouse[0] * blockSize + rad
    y = mouse[1] * blockSize + rad
    pygame.draw.circle(surface, color, (x, y), rad)

def snakeTouchingPoint(snake, point):
    head = snake[0]
    if head[0] == point[0] and head[1] == point[1]:
        return True
    return False

def snakeTouchingSnake(snake):
    snakeMinusHead = snake[1:]
    for point in snakeMinusHead:
        if snakeTouchingPoint(snake, point):
            return True
    return False

def hasLost(snake, MAX_X, MAX_Y):
    x, y = snake[0]
    if x < 0 or x > MAX_X:
        return True
    if y < 0 or y > MAX_Y:
        return True
    return False

def loseAnimation(length):
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj = fontObj.render('You Lost', True, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (200, 150)
    
    fontObj2 = pygame.font.Font('freesansbold.ttf', 32)
    textSurfaceObj2 = fontObj.render('Your Score: ' + str(length), True, BLACK)
    textRectObj2 = textSurfaceObj.get_rect()
    textRectObj2.center = (200, 250)
    
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
    pygame.display.update()

def resetGame(snake, mouse, velX, velY, MAX_X, MAX_Y):
    snake = [(7,2), (6,2), (5,2)]
    mouse = newRandomMouse(MAX_X, MAX_Y)
    velX = 1
    velY = 0

    return snake, mouse, velX, velY

main()
