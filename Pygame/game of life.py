import pygame, sys
from pygame.locals import *

pygame.init()

#game settings
FPS = 10
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 550
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

TEXT_COLOR = BLACK

FPSCLOCK = pygame.time.Clock()

DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")


status = 'stopped'
grid = []
for i in range(GRID_ROWS):
    grid.append([])
    for j in range(GRID_COLS):
        grid[i].append(0)

def main():
    buttons = []
    start_button = Button(50, GRID_HEIGHT + 25, 100, 100, "Start", start)
    buttons.append(start_button)
    stop_button = Button(250, GRID_HEIGHT + 25, 100, 100, "Stop", stop)
    buttons.append(stop_button)
    clear_button = Button(450, GRID_HEIGHT + 25, 100, 100, "Clear", clear)
    buttons.append(clear_button)
    
    spawnRPentomino(25, 25)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                cell = determineCellClick(pos[0], pos[1])
                if cell:
                    cellToggle(cell[0], cell[1])
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
            
        drawGrid()
        if status == 'running':
            updateGrid()
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def drawTile(x, y):
    if grid[y][x]:
        top_left = [x * BLOCK_WIDTH, y  * BLOCK_HEIGHT]
        rect = (top_left[0], top_left[1], BLOCK_WIDTH, BLOCK_HEIGHT)
        color = BLACK
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
            change = updateTileStatus(x + 1, y + 1)
            new_grid[change[1]][change[0]] = change[2]
            
    grid = new_grid

    
def updateTileStatus(x, y):
    global grid
    
    live_neighbors = 0
    adjacentCells = getAdjacentCells(x, y)
    for cell in adjacentCells:
        if cell == 1:
            live_neighbors += 1

    if live_neighbors == 3 or (live_neighbors == 2 and grid[y][x] == 1):
        return (x, y, 1)
    else:
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

def start():
    global status
    status = 'running'

def stop():
    global status
    status = 'stopped'

def clear():
    #stops game and resets all cells to empty
    global status, grid
    status = 'stopped'
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = 0

def determineCellClick(mouseX, mouseY):
    #check if mouse on grid and return cell coords if so
    if (0 <= mouseX and mouseX <= GRID_WIDTH) and (0 <= mouseY and mouseY <= GRID_HEIGHT):
        return [int(mouseX / BLOCK_WIDTH), int(mouseY / BLOCK_HEIGHT)]
    else:
        return False

def cellToggle(x, y):
    #player clicked on cell, toggle on/off
    global grid
    if grid[y][x]:
        grid[y][x] = 0
    else:
        grid[y][x] = 1

def spawnRPentomino(x, y):
    global grid
    
    grid[y][x - 1] = 1
    grid[y - 1][x] = 1
    grid[y][x] = 1
    grid[y + 1][x] = 1
    grid[y - 1][x + 1] = 1

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


if __name__ == '__main__':
    main()
    
