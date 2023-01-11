import sys
import pygame
import random
import time

#Default screen size
SCREENX = 600
SCREENY = 600

rowX = 4 #Number of rows
rowY = 4 #Number of columns

#Default colors of cubes (for visual display)
cubeColors = {
    2:      (239, 225, 212),
    4:      (239, 222, 194),
    8:      (246, 168, 102),
    16:     (239, 143, 93),
    32:     (253, 113, 80),
    64:     (252, 80, 40),
    128:    (242, 204, 97),
    256:    (241, 197, 85),
    512:    (238, 195, 56),
    1024:   (242, 191, 38),
    2048:   (239, 189, 4),
    4096:   (55, 51, 42),
    }

class Cube:
    """Cube object, holds the coordinates and size of tile on board"""
    def __init__(self, size, x, y):
        self.size = size
        self.x = x
        self.y = y
        self.merged = False

    def get_rect(self, SCREENX, SCREENY):
        """Get pygame rectangle of coordinate"""
        return pygame.Rect(SCREENX * self.x /float(rowX), SCREENY * self.y / float(rowY), SCREENX / float(rowX), SCREENY / float(rowY))

    def __str__(self):
        """Returns string value of self"""
        return "Cube of value " + str(self.size) + " at (" + str(self.x) + "," + str(self.y) + ")"

    def __del__(self):
        """Returns deletion of code"""
        return "Deleted cube of value " + str(self.size) + " at (" + str(self.x) + "," + str(self.y) + ")"

    #Move Cube------------

    def moveDown(self, cubes):
        """Moves the cube down one unit, relative to board size and other cubes, merging if neccessary."""
        global score
        if self.y == rowY - 1: #at bottom
            return False
        else:
            below = findCube(self.x, self.y + 1, cubes)
            if (below):
                if (below.size == self.size and not below.merged and not self.merged): #Merge
                    below.size *= 2
                    score += below.size
                    cubes.remove(self)
                    below.merged = True
                    return True
            else:
                self.y = self.y + 1 #Move down
                return True

    def moveUp(self, cubes):
        """Moves the cube up one unit, relative to board size and other cubes, merging if neccessary."""
        global score
        if self.y == 0:
            return False #at top
        else:
            above = findCube(self.x, self.y - 1, cubes)
            if (above):
                if (above.size == self.size and not above.merged and not self.merged): #Merge
                    above.size *= 2
                    score += above.size
                    cubes.remove(self)
                    above.merged = True
                    return True
            else:
                self.y = self.y - 1 #Move up
                return True

    def moveLeft(self, cubes):
        """Moves the cube left one unit, relative to board size and other cubes, merging if neccessary."""
        global score
        if self.x == 0:
            return False #at left
        else:
            adj = findCube(self.x - 1, self.y, cubes)
            if (adj):
                if (adj.size == self.size and not adj.merged and not self.merged): #Merge
                    adj.size *= 2
                    score += adj.size
                    cubes.remove(self)
                    adj.merged = True
                    return True
            else:
                self.x = self.x - 1 #Move left
                return True

    def moveRight(self, cubes):
        """Moves the cube right one unit, relative to board size and other cubes, merging if neccessary."""
        global score
        if self.x == rowX - 1:
            return False #at right
        else:
            adj = findCube(self.x + 1, self.y, cubes)
            if (adj):
                if (adj.size == self.size and not adj.merged and not self.merged): #Merge
                    adj.size *= 2
                    score += adj.size
                    cubes.remove(self)
                    adj.merged = True
                    return True
            else:
                self.x = self.x + 1 #Move left
                return True

def findCube(x, y, cubes):
    """Returns cube with coordinates X and Y on list of cubes"""
    for cube in cubes:
        if (cube.x == x and cube.y == y):
            return cube
    return False

def getCubeArray(cubes):
    """Returns 2D array of tile based on whether or not a cube exists there"""
    a = [[False]*rowX for i in range(rowY)]
    for cube in cubes:
        if cube.x >= rowX or cube.y >= rowY:
            pass
        else:
           a[cube.y][cube.x] = True
    return a
        
def checkFull(cubeArray):
    """Returns boolean value of whether or not a cubeArray is full or not"""
    for i in cubeArray:
        for i2 in i:
            if not i2:
                return False
    return True

def checkPossible(cubes):
    """Checks if a further move is possible"""
    if not checkFull(getCubeArray(cubes)):
        return True
    for cube in cubes:
        if (cube.x != 0): #Check X-1
            if findCube(cube.x - 1, cube.y, cubes).size == cube.size:
                return True
        if (cube.x != rowX - 1): #Check X+1
            if findCube(cube.x + 1, cube.y, cubes).size == cube.size:
                return True
        if (cube.y != 0): #Check Y-1
            if findCube(cube.x, cube.y - 1, cubes).size == cube.size:
                return True
        if (cube.y != rowY - 1): #Check Y+1
            if findCube(cube.x, cube.y + 1, cubes).size == cube.size:
                return True
    return False
            

def sendAllDown(cubes):
    """Sends all cubes one row down"""
    result = False
    for y in range(rowY-1,-1,-1):
        for x in range(rowX):
            cube = findCube(x, y, cubes)
            if (cube):
                if cube.moveDown(cubes):
                    result = True
    return result

def sendAllUp(cubes):
    """Sends all cubes one row up"""
    result = False
    for y in range(0,rowY):
        for x in range(rowX):
            cube = findCube(x, y, cubes)
            if (cube):
                if cube.moveUp(cubes):
                    result = True
    return result

def sendAllLeft(cubes):
    """Sends all cubes one row left"""
    result = False
    for x in range(0,rowX):
        for y in range(rowY):
            cube = findCube(x, y, cubes)
            if (cube):
                if cube.moveLeft(cubes):
                    result = True
    return result

def sendAllRight(cubes):
    """Sends all cubes one row right"""
    result = False
    for x in range(rowX-1,-1,-1):
        for y in range(rowY):
            cube = findCube(x, y, cubes)
            if (cube):
                if cube.moveRight(cubes):
                    result = True
    return result

def genRandom(cubes):
    """Generates a new random cube on the board. Returns boolean if succesful or not"""
    cubeArray = getCubeArray(cubes)
    if checkFull(cubeArray):
        return False
    else:
        while True:
            x = random.randint(0, rowX - 1)
            y = random.randint(0, rowY - 1)
            if not cubeArray[y][x]:
                cubes.append(Cube(2**random.randint(1,2), x, y))
                break
        if not checkPossible(cubes):
            global gameRunning
            global score
            gameRunning = False
    return True

def highestTile(cubes):
    """Returns the highest tile on the board"""
    highest = 2
    for cube in cubes:
        if cube.size > highest:
            highest = cube.size
    return highest

def downAction(screen, cubes, n):
    """Action of moving down with delay of n seconds"""
    i = 0
    while sendAllDown(cubes):
        time.sleep(n)
        if(display):
            refreshScreen(screen, cubes)
        i += 1

    for cube in cubes:
        cube.merged = False
        
    if i != 0:
        genRandom(cubes)
        return True
    return False

def upAction(screen, cubes, n):
    """Action of moving up with delay of n seconds"""
    i = 0
    while sendAllUp(cubes):
        time.sleep(n)
        if(display):
            refreshScreen(screen, cubes)
        i += 1

    for cube in cubes:
        cube.merged = False
        
    if i != 0:
        genRandom(cubes)
        return True
    return False

def leftAction(screen, cubes, n):
    """Action of moving left with delay of n seconds"""
    i = 0
    while sendAllLeft(cubes):
        time.sleep(n)
        if(display):
            refreshScreen(screen, cubes)
        i += 1

    for cube in cubes:
        cube.merged = False
    
    if i != 0:
        genRandom(cubes)
        return True
    return False

def rightAction(screen, cubes, n):
    """Action of moving right with delay of n seconds"""
    i = 0
    while sendAllRight(cubes):
        time.sleep(n)
        if(display):
            refreshScreen(screen, cubes)
        i += 1

    for cube in cubes:
        cube.merged = False
        
    if i != 0:
        genRandom(cubes)
        return True
    return False

def refreshScreen(screen, cubes):
    """Updates the pygame display"""
    SCREENX = screen.get_width()
    SCREENY = screen.get_height()

    screen.fill((205, 193, 180)) #Background

    f = pygame.font.SysFont(name = 'comic_sans_ms', size = SCREENX // (max(rowX, rowY) * 4), bold = False, italic = True)

    for cube in cubes:
        try:
            pygame.draw.rect(screen, cubeColors[cube.size], cube.get_rect(SCREENX, SCREENY))
        except:
            pygame.draw.rect(screen, (200, 200, 200), cube.get_rect(SCREENX, SCREENY))
        label = f.render(str(cube.size), True, (0, 0, 0))
        labelRect = label.get_rect()
        labelRect.center = (cube.x * SCREENX / float(rowX) + SCREENX / float(rowX * 2), cube.y * SCREENY / float(rowY) + SCREENY / float(rowY * 2))
        screen.blit(label, labelRect)
    
    for i in range(rowY): #Lines
        pygame.draw.line(screen, (187, 173, 160), (0,SCREENY * i / float(rowY)), (SCREENX, SCREENY * i / float(rowY)), width=min(SCREENX, SCREENY)//60)

    for i in range(rowX):
        pygame.draw.line(screen, (187, 173, 160), (SCREENX * i / float(rowX), 0), (SCREENX * i / float(rowX), SCREENY), width=min(SCREENX, SCREENY)//60)

    
    pygame.display.flip() # refresh the screen.

keyReady = True
def getInput(screen, cubes, event):
    """Default input configuration. Intended to be rewritten for algorithms. User-defined by default."""
    global keyReady
    if event.type == pygame.KEYUP:
        keyReady = True
    if event.type == pygame.KEYDOWN and keyReady:
        keyReady = False
        if event.key == pygame.K_DOWN:
            downAction(screen, cubes, 0.05)    
        if event.key == pygame.K_UP:
            upAction(screen, cubes, 0.05)
        if event.key == pygame.K_LEFT:
            leftAction(screen, cubes, 0.05)
        if event.key == pygame.K_RIGHT:
            rightAction(screen, cubes, 0.05)

def quit():
    pygame.quit()

score = 0
gameRunning = True
display = True

def main():
    """Run game of 2048"""
    pygame.init()
    pygame_window_title = '2048'

    pygame.display.set_caption(pygame_window_title)
    
    screen = pygame.display.set_mode((SCREENX, SCREENY), pygame.RESIZABLE)

    screen.fill((205, 193, 180))
    
    global score
    global gameRunning
    gameRunning = True
    score = 0
    cubes = []

    cubes.append(Cube(16,0,0))
    cubes.append(Cube(8,0,1))
    cubes.append(Cube(4,0,2))
    cubes.append(Cube(4,0,3))
    
    #genRandom(cubes)
    #genRandom(cubes)
    event = "n"

    while gameRunning:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                pygame.quit()
                sys.exit()
        getInput(screen, cubes, event)

        if display:
            refreshScreen(screen, cubes)
        
    return (score, highestTile(cubes))
