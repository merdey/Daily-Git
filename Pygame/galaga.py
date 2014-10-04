import pygame, sys, random, math, time
from pygame.locals import *
pygame.init()

#colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 132, 0)
GREY = (200, 200, 200)

PLAYER_SHIP_COLOR = WHITE
ENEMY_SHIP_COLOR = RED
PLAYER_MISSILE_COLOR = BLUE
ENEMY_MISSILE_COLOR = ORANGE
ASTEROID_COLOR = GREY
BACKGROUND_COLOR = BLACK
TEXT_COLOR = WHITE

#game settings
FPS = 20
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
MISSILE_SPEED = 20

#player
STARTING_X = 575
STARTING_Y = 550
PLAYER_MOVE_SPEED = 40
PLAYER_SIZE = 50
INITIAL_LIVES = 3

#asteroid
ASTEROID_SPEED = 5
ASTEROID_SPAWN_RATE = 100
ASTEROID_SIZE = 60
ASTEROID_MIN_ANGLE = 25
ASTEROID_MAX_ANGLE = 60

#enemy ships
WAVE_MOVE_RATE = 25
ENEMY_SPEED = 25
ENEMY_SIZE = 40
ENEMY_HEALTH = 1
ENEMY_ATTACK_RATE = 150

global FPSCLOCK, DISPLAY_SURF
FPSCLOCK = pygame.time.Clock()
DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Galaga Clone")

playerMissiles = []
asteroids = []
enemyShips = []
enemyMissiles = []

class PlayerShip:
    def __init__(self, x, y):
        self.rect = Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.lives = INITIAL_LIVES

    def moveRight(self):
        self.rect.x += PLAYER_MOVE_SPEED

    def moveLeft(self):
        self.rect.x -= PLAYER_MOVE_SPEED

    def fire(self):
        missile = Missile(self.rect.x + ( (PLAYER_SIZE - 10) / 2 ), self.rect.y, -1, PLAYER_MISSILE_COLOR)
        playerMissiles.append(missile)

    def hitByMissile(self):
        self.lives -= 1
        if self.lives <= 0:
            gameLost()

    def hitByAsteroid(self):
        self.lives -= 1
        if self.lives <= 0:
            gameLost()

    def draw(self):
        pygame.draw.rect(DISPLAY_SURF, PLAYER_SHIP_COLOR, self.rect)

class EnemyWave:
    def __init__(self, pattern, height, width):
        self.pattern = pattern #[columns, rows]
        self.height = height
        self.width = width
        self.horizontalState = 0
        self.direction = random.choice(['right', 'left'])

    def moveAsGroup(self):
        if self.direction == 'right':
            self.moveRight()
            if self.horizontalState >= 2:
                self.direction = 'down'
                
        elif self.direction == 'left':
            self.moveLeft()
            if self.horizontalState <= -2:
                self.direction = 'down'
                
        elif self.direction == 'down':
            self.moveDown()
            if self.horizontalState <= -2:
                self.direction = 'right'
            else:
                self.direction = 'left'
        else:
            assert False, 'something broked'

    def moveRight(self):
        self.horizontalState += 1
        
        dX = ENEMY_SPEED
        dY = 0
        self.moveAllShips(dX, dY)

    def moveLeft(self):
        self.horizontalState -= 1
        
        dX = -(ENEMY_SPEED)
        dY = 0
        self.moveAllShips(dX, dY)

    def moveDown(self):
        dX = 0
        dY = ENEMY_SPEED
        self.moveAllShips(dX, dY)

    def moveAllShips(self, dX, dY):
        for ship in enemyShips:
            ship.move(dX, dY)

    def resetWave(self):
        self.horizontalState = 0
        self.direction = random.choice(['right', 'left'])

    def spawnEnemies(self):
        columns = self.pattern[0]
        rows = self.pattern[1]
        
        widthIncrement = int( (self.width - ENEMY_SIZE) / columns)
        horizontalOffset = int( (WINDOW_WIDTH - self.width) / 2 )
        heightIncrement = int(self.height / rows)
        verticalOffset = int(heightIncrement / 2)
        for i in range( columns ):
            for j in range( rows ):
                newShip = EnemyShip(horizontalOffset + (i * widthIncrement),verticalOffset +(j * heightIncrement) )
                enemyShips.append( newShip )

class EnemyShip:
    def __init__(self, x, y):
        self.rect = Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        self.hp = ENEMY_HEALTH
        self.attackTimer = random.randint(0, ENEMY_ATTACK_RATE)

    def move(self, dX, dY):
        self.rect.x += dX
        self.rect.y += dY

    def attack(self):
        self.fire()

    def fire(self):
        missile = Missile(self.rect.x + ( (ENEMY_SIZE - 10) / 2 ), self.rect.y + ENEMY_SIZE, 1, ENEMY_MISSILE_COLOR)
        enemyMissiles.append(missile)

    def hitByMissile(self):
        print(self.hp)
        self.hp -= 1
        if self.isDestroyed():
            enemyShips.remove(self)

    def isDestroyed(self):
        if self.hp <= 0:
            return True
        return False

    def attackReady(self):
        return ( self.attackTimer % ENEMY_ATTACK_RATE == 0 )

    def draw(self):
        pygame.draw.rect(DISPLAY_SURF, ENEMY_SHIP_COLOR, self.rect)

class Asteroid:
    def __init__(self, x, y, angle):
        self.rect = Rect(x, y, ASTEROID_SIZE, ASTEROID_SIZE)
        self.angle = math.radians(angle)

    def updatePosition(self):
        self.rect.x += ASTEROID_SPEED * math.cos(self.angle)
        self.rect.y += ASTEROID_SPEED * math.sin(self.angle)

    def draw(self):
        pygame.draw.rect(DISPLAY_SURF, ASTEROID_COLOR, self.rect)

class Missile:
    def __init__(self, x, y, vel, color):
        self.rect = Rect(x, y, 10, 25)
        self.vel = vel
        self.color = color

    def updatePosition(self):
        self.rect.y += MISSILE_SPEED * self.vel

    def draw(self):
        pygame.draw.rect(DISPLAY_SURF, self.color, self.rect)
        

def main():
    global ENEMY_ATTACK_RATE, WAVE_MOVE_RATE, score, player
    wave = EnemyWave([6,4], WINDOW_HEIGHT / 2, int( WINDOW_WIDTH * (3/4) ))
    player = PlayerShip(STARTING_X, STARTING_Y)
    spawnTimer = 1
    score = -10
    
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.fire()
                if event.key == K_LEFT:
                    player.moveLeft()
                if event.key == K_RIGHT:
                    player.moveRight()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        #spawns asteroids at fixed intervals
        if ASTEROID_SPAWN_RATE != 0 and spawnTimer % ASTEROID_SPAWN_RATE == 0:
            spawnRandomAsteroid()

        #spawn another wave if no enemies remain
        if not enemyShips:
            score += 10
            #increase difficulty
            WAVE_MOVE_RATE = int( 0.9 * WAVE_MOVE_RATE )
            ENEMY_ATTACK_RATE = int( 0.9 * ENEMY_ATTACK_RATE )
            wave.resetWave()
            wave.spawnEnemies()
        else:
            if spawnTimer % WAVE_MOVE_RATE == 0:
                wave.moveAsGroup()
        
        #background
        DISPLAY_SURF.fill(BACKGROUND_COLOR)

        #player missiles
        for missile in playerMissiles:
            #check for collision with enemy ships
            for enemy in enemyShips:
                if pygame.sprite.collide_rect(missile, enemy):
                    enemy.hitByMissile()
                    playerMissiles.remove(missile)
                    score += 1
            #remove once off screen
            if missile.rect.y < -100:
                playerMissiles.remove(missile)
                continue
            missile.updatePosition()
            missile.draw()

        #enemies            
        for enemy in enemyShips:
            enemy.attackTimer += 1
            if enemy.attackReady():
                enemy.attack()
            enemy.draw()

        #enemy_missiles
        for missile in enemyMissiles:
            #check for collision with player
            if pygame.sprite.collide_rect(player, missile):
                player.hitByMissile()
                if missile in enemyMissiles:
                    enemyMissiles.remove(missile)
                break
            #remove once off screen
            if missile.rect.y > WINDOW_HEIGHT + 100:
                enemyMissiles.remove(missile)
                continue
            missile.updatePosition()
            missile.draw()

        #asteroids
        for asteroid in asteroids:
            #check for collision with player
            if pygame.sprite.collide_rect(player, asteroid):
                player.hitByAsteroid()
                if asteroid in asteroids:
                    asteroids.remove(asteroid)
                break
            #remove once off screen, dodging asteroids gives points
            if asteroid.rect.y > WINDOW_HEIGHT + 100:
                asteroids.remove(asteroid)
                score += 3
                continue
            asteroid.updatePosition()
            asteroid.draw()

        #player
        player.draw()

        #TO DO: show lives and score(wave #)
        showLives()
        showScore()

        #update surface
        pygame.display.update()
        
        FPSCLOCK.tick(FPS)
        spawnTimer += 1  

def spawnRandomAsteroid():
    x = random.choice([-ASTEROID_SIZE, WINDOW_WIDTH]) #spawns on either left or right just off edge of screen
    y = random.randrange(0, WINDOW_HEIGHT / 3) #along top 1/3 of screen
    if x == -ASTEROID_SIZE: #spawning on left
        angle = random.randrange(ASTEROID_MIN_ANGLE, ASTEROID_MAX_ANGLE)
    else: #spawning on right
        angle = random.randrange(90 + ASTEROID_MIN_ANGLE, 90 + ASTEROID_MAX_ANGLE)

    
    asteroid = Asteroid(x, y, angle)
    asteroids.append(asteroid)

def showLives():
    global player
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    textSurfaceObj = fontObj.render('Lives: ' + str(player.lives), True, TEXT_COLOR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (75, 20)

    DISPLAY_SURF.blit(textSurfaceObj, textRectObj)
    pygame.display.update()

def showScore():
    global score
    fontObj = pygame.font.Font('freesansbold.ttf', 24)
    textSurfaceObj = fontObj.render('Score: ' + str(score), True, TEXT_COLOR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (WINDOW_WIDTH - 75, 20)

    DISPLAY_SURF.blit(textSurfaceObj, textRectObj)
    pygame.display.update()

def gameLost():
    global score

    fontObj = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj = fontObj.render('You Lost', True, TEXT_COLOR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2) - 100)
    
    fontObj2 = pygame.font.Font('freesansbold.ttf', 48)
    textSurfaceObj2 = fontObj.render('Final Score: ' + str(score), True, TEXT_COLOR)
    textRectObj2 = textSurfaceObj.get_rect()
    textRectObj2.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    DISPLAY_SURF.fill(BACKGROUND_COLOR)
    DISPLAY_SURF.blit(textSurfaceObj, textRectObj)
    DISPLAY_SURF.blit(textSurfaceObj2, textRectObj2)
    pygame.display.update()
    
    resetGame()

def resetGame():
    global playerMissiles, asteroids, enemyShips, enemyMissiles, player, spawnTimer, wave, WAVE_MOVE_RATE, ENEMY_ATTACK_RATE, score
    
    playerMissiles = []
    asteroids = []
    enemyShips = []
    enemyMissiles = []

    wave = EnemyWave([6,3], WINDOW_HEIGHT / 2, WINDOW_WIDTH)
    player = PlayerShip(STARTING_X, STARTING_Y)
    spawnTimer = 1
    score = 0

    WAVE_MOVE_RATE = 25
    ENEMY_ATTACK_RATE = 150
    
if __name__ == '__main__':
    main()
