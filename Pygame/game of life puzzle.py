import pygame, sys
from pygame.locals import *

#game settings
FPS = 10
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 650
BUTTON_BAR_HEIGHT = 50
GRID_WIDTH = WINDOW_WIDTH
GRID_HEIGHT = WINDOW_HEIGHT - BUTTON_BAR_HEIGHT
GRID_COLS = 50
GRID_ROWS = 50
BLOCK_WIDTH = WINDOW_WIDTH / GRID_COLS
BLOCK_HEIGHT = GRID_HEIGHT / GRID_ROWS
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30

#colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PLAYER_COLOR = RED
TARGET_COLOR = BLUE
TEXT_COLOR = BLACK

FPSCLOCK = pygame.time.Clock()
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
    
#set up grid
grid = []
for i in range(GRID_ROWS):
    grid.append([])
    for j in range(GRID_COLS):
        grid[i].append(0)

status = 'begin'
buttons = []

def main():
    #set up target cells
    spawnRPentomino(10, 10, 2)
    
    start_button = Button(50, GRID_HEIGHT + 25, 100, 100, "Start", start)
    buttons.append(start_button)
    stop_button = Button(200, GRID_HEIGHT + 25, 100, 100, "Stop", stop)
    buttons.append(stop_button)
    reset_button = Button(350, GRID_HEIGHT + 25, 100, 100, "Reset", reset)
    buttons.append(reset_button)
    
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell = determineCellClick(pos[0], pos[1])
                if cell:
                    cell_status = 'player'
                    cellToggle(cell[0], cell[1], cell_status)
                else:
                    for button in buttons:
                        if button.hitbox().collidepoint(pos):
                            button.clicked()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY_SURFACE.fill(WHITE)
        
        pygame.draw.line(DISPLAY_SURFACE, BLACK, (0, GRID_HEIGHT), (WINDOW_WIDTH, GRID_HEIGHT))
        for button in buttons:
            button.draw()

        if status == 'running':
            updateGrid()
        drawGrid()
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        if targetsCleared(grid):
            #game over
            gameOver()
            break

def drawTile(x, y):
    if grid[y][x]:
        if grid[y][x] == 1:
            color = PLAYER_COLOR
        else:
            color = TARGET_COLOR
        top_left = [x * BLOCK_WIDTH, y  * BLOCK_HEIGHT]
        rect = (top_left[0], top_left[1], BLOCK_WIDTH, BLOCK_HEIGHT)
        pygame.draw.rect(DISPLAY_SURFACE, color, rect)

def drawGrid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            drawTile(x, y)
    
def updateGrid():
    #updates cells for next interation
    global grid

    new_grid = []
    for i in range(GRID_ROWS):
        new_grid.append([])
        for j in range(GRID_COLS):
            new_grid[i].append(0)
        
    for y in range(len(grid) - 2):
        for x in range(len(grid[y]) - 2):
            tileUpdate = updateTileStatus(x + 1, y + 1)
            new_grid[tileUpdate[1]][tileUpdate[0]] = tileUpdate[2]
            
    grid = new_grid

    
def updateTileStatus(x, y):
    global grid

    player_cells = 0
    live_neighbors = 0
    adjacentCells = getAdjacentCells(x, y)
    for cell in adjacentCells:
        if cell == 1:
            live_neighbors += 1

    if live_neighbors == 3 or (live_neighbors == 2 and grid[y][x]):
        return (x, y, 1)
    else:
        #maintain target cells
        if grid[y][x] == 2:
            return (x, y, 2)

        return (x, y, 0)

def getAdjacentCells(x, y):
    #can probably do something a little more clever than this but it works for now (ie http://www.tristanhearn.com/gameoflife)
    neighbors = [ grid[y][x + 1],
                  grid[y][x - 1],
                  grid[y + 1][x],
                  grid[y - 1][x],
                  grid[y + 1][x + 1],
                  grid[y + 1][x - 1],
                  grid[y - 1][x + 1],
                  grid[y - 1][x - 1]
                  ]

    return neighbors

def determineCellClick(mouseX, mouseY):
    #check if mouse on grid and return cell coords if so
    if (0 <= mouseX and mouseX <= GRID_WIDTH) and (0 <= mouseY and mouseY <= GRID_HEIGHT):
        return [int(mouseX / BLOCK_WIDTH), int(mouseY / BLOCK_HEIGHT)]
    else:
        return False

def cellToggle(x, y, cell_status):
    #player clicked on cell, toggle on/off
    global grid
    if grid[y][x]:
        grid[y][x] = 0
    else:
        if cell_status == 'player':
            grid[y][x] = 1
        if cell_status == 'target':
            grid[y][x] = 2

def targetsCleared(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 2:
                return False
    return True

def gameOver():
    print('game over2')

def spawnRPentomino(x, y, cell_status=1):
    global grid
    
    grid[y][x - 1] = cell_status
    grid[y - 1][x] = cell_status
    grid[y][x] = cell_status
    grid[y + 1][x] = cell_status
    grid[y - 1][x + 1] = cell_status

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = (x, y, width, height)
        self.text = text
        self.action = action
        
        self.fontObj = pygame.font.Font('freesansbold.ttf', 24)
        self.textSurfaceObj = self.fontObj.render(self.text, True, TEXT_COLOR)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (x, y)

    def hitbox(self):
        return self.textRectObj

    def clicked(self):
        self.action()

    def draw(self):
        DISPLAY_SURFACE.blit(self.textSurfaceObj, self.textRectObj)

#Button Functions
def start():
    global status
    status = 'running'

def stop():
    global status
    status = 'stopped'

def reset():
    #stops game and resets all cells to empty
    global status, grid
    status = 'begin'
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = 0

if __name__ == "__main__":
    pygame.init()
    main()
