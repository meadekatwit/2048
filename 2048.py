##TODO

#Test dynamic size movement
#Disable generation on non-move
#Endgame state
#Score system


import sys
import pygame
import random

pygame.init()
pygame_window_title = '2048'

pygame.display.set_caption(pygame_window_title)

SCREENX = 600
SCREENY = 600

rowX = 4
rowY = 4

screen = pygame.display.set_mode((SCREENX, SCREENY), pygame.RESIZABLE)

screen.fill((205, 193, 180))

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
    def __init__(self, size, x, y):
        self.size = size
        self.x = x
        self.y = y

    def get_rect(self, SCREENX, SCREENY):
        return pygame.Rect(SCREENX * self.x /float(rowX), SCREENY * self.y / float(rowY), SCREENX / float(rowX), SCREENY / float(rowY))

    def __str__(self):
        return "Cube of value " + str(self.size) + " at (" + str(self.x) + "," + str(self.y) + ")"

    def __del__(self):
        return "Deleted cube of value " + str(self.size) + " at (" + str(self.x) + "," + str(self.y) + ")"

    #Move Cube------------

    def moveDown(self, cubes):
        global score
        if self.y == rowY - 1: #at bottom
            return False
        else:
            below = findCube(self.x, self.y + 1, cubes)
            if (below):
                if (below.size == self.size): #Merge
                    below.size *= 2
                    score += below.size
                    cubes.remove(self)
                    return True
            else:
                self.y = self.y + 1 #Move down
                return True

    def moveUp(self, cubes):
        global score
        if self.y == 0:
            return False #at top
        else:
            above = findCube(self.x, self.y - 1, cubes)
            if (above):
                if (above.size == self.size): #Merge
                    above.size *= 2
                    score += above.size
                    cubes.remove(self)
                    return True
            else:
                self.y = self.y - 1 #Move up
                return True

    def moveLeft(self, cubes):
        global score
        if self.x == 0:
            return False #at left
        else:
            adj = findCube(self.x - 1, self.y, cubes)
            if (adj):
                if (adj.size == self.size): #Merge
                    adj.size *= 2
                    score += adj.size
                    cubes.remove(self)
                    return True
            else:
                self.x = self.x - 1 #Move left
                return True

    def moveRight(self, cubes):
        global score
        if self.x == rowX - 1:
            return False #at right
        else:
            adj = findCube(self.x + 1, self.y, cubes)
            if (adj):
                if (adj.size == self.size): #Merge
                    adj.size *= 2
                    score += adj.size
                    cubes.remove(self)
                    return True
            else:
                self.x = self.x + 1 #Move left
                return True

def findCube(x, y, cubes):
    for cube in cubes:
        if (cube.x == x and cube.y == y):
            return cube
    return False

def getCubeArray(cubes):
    a = [[False]*rowX for i in range(rowY)]
    for cube in cubes:
        if cube.x >= rowX or cube.y >= rowY:
            pass
        else:
           a[cube.y][cube.x] = True
    return a
        
def checkFull(cubeArray):
    for i in cubeArray:
        for i2 in i:
            if not i2:
                return False
    return True

def checkPossible(cubes):
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
    result = False
    for y in range(rowY-1,-1,-1):
        for x in range(rowX):
            cube = findCube(x, y, cubes)
            if (cube):
                if cube.moveDown(cubes):
                    result = True
    return result

def sendAllUp(cubes):
    result = False
    for y in range(0,rowY):
        for x in range(rowX):
            cube = findCube(x, y, cubes)
            if (cube):
                if cube.moveUp(cubes):
                    result = True
    return result

def sendAllLeft(cubes):
    result = False
    for x in range(0,rowX):
        for y in range(rowY):
            cube = findCube(x, y, cubes)
            if (cube):
                if cube.moveLeft(cubes):
                    result = True
    return result

def sendAllRight(cubes):
    result = False
    for x in range(rowX-1,-1,-1):
        for y in range(rowY):
            cube = findCube(x, y, cubes)
            if (cube):
                if cube.moveRight(cubes):
                    result = True
    return result

def genRandom(cubes):
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
    highest = 2
    for cube in cubes:
        if cube.size > highest:
            highest = cube.size
    return highest

score = 0
gameRunning = True

def main():
    global score
    global gameRunning
    gameRunning = True
    score = 0
    cubes = []
    genRandom(cubes)
    genRandom(cubes)

    while gameRunning:
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    
                pygame.quit()
                sys.exit()

##            if event.type == pygame.MOUSEBUTTONDOWN:
##                genRandom(cubes)
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_DOWN:
##                    i = 0
##                    while sendAllDown(cubes):
##                        i += 1
##                    if i != 0:
##                        genRandom(cubes)
##                        
##                if event.key == pygame.K_UP:
##                    i = 0
##                    while sendAllUp(cubes):
##                        i += 1
##                    if i != 0:
##                        genRandom(cubes)
##                    
##                if event.key == pygame.K_LEFT:
##                    i = 0
##                    while sendAllLeft(cubes):
##                        i += 1
##                    if i != 0:
##                        genRandom(cubes)
##                    
##                if event.key == pygame.K_RIGHT:
##                    i = 0
##                    while sendAllRight(cubes):
##                        i += 1
##                    if i != 0:
##                        genRandom(cubes)
##                #print(score)

        n = random.randint(0,4)
        if n == 0:
            i = 0
            while sendAllDown(cubes):
                i += 1
            if i != 0:
                genRandom(cubes)
                
        if n == 1:
            i = 0
            while sendAllUp(cubes):
                i += 1
            if i != 0:
                genRandom(cubes)
            
        if n == 2:
            i = 0
            while sendAllLeft(cubes):
                i += 1
            if i != 0:
                genRandom(cubes)
            
        if n == 3:
            i = 0
            while sendAllRight(cubes):
                i += 1
            if i != 0:
                genRandom(cubes)
        
        SCREENX = screen.get_width()
        SCREENY = screen.get_height()

        screen.fill((205, 193, 180)) #Background

        f = pygame.font.SysFont(name = 'comic_sans_ms', size = SCREENX // 20, bold = False, italic = True)

        for cube in cubes:
            pygame.draw.rect(screen, cubeColors[cube.size], cube.get_rect(SCREENX, SCREENY))
            label = f.render(str(cube.size), True, (0, 0, 0))
            labelRect = label.get_rect()
            labelRect.center = (cube.x * SCREENX / float(rowX) + SCREENX / float(rowX * 2), cube.y * SCREENY / float(rowY) + SCREENY / float(rowY * 2))
            screen.blit(label, labelRect)
        
        for i in range(rowY): #Lines
            pygame.draw.line(screen, (187, 173, 160), (0,SCREENY * i / float(rowY)), (SCREENX, SCREENY * i / float(rowY)), width=min(SCREENX, SCREENY)//60)

        for i in range(rowX):
            pygame.draw.line(screen, (187, 173, 160), (SCREENX * i / float(rowX), 0), (SCREENX * i / float(rowX), SCREENY), width=min(SCREENX, SCREENY)//60)

        
        pygame.display.flip() # refresh the screen.
    return (score, highestTile(cubes))


highest = []
scores = []

for i in range(1, 10):
    a = main()
    highest.append(a[1])
    scores.append(a[0])

import matplotlib    
from matplotlib import pyplot
matplotlib.pyplot.scatter(highest,scores)
matplotlib.pyplot.show()
