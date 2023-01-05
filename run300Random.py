import engine
import pygame
from matplotlib import pyplot as plt
import random

def userInput(screen, cubes, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DOWN:
            engine.downAction(screen, cubes, 0)    
        if event.key == pygame.K_UP:
            engine.upAction(screen, cubes, 0)
        if event.key == pygame.K_LEFT:
            engine.leftAction(screen, cubes, 0)
        if event.key == pygame.K_RIGHT:
            engine.rightAction(screen, cubes, 0)

def randomInput(screen, cubes, event):
    choice = random.randint(0,3)

    if choice == 0:
        engine.downAction(screen, cubes, 0.01)
    elif choice == 1:
        engine.upAction(screen, cubes, 0.01)
    elif choice == 2:
        engine.leftAction(screen, cubes, 0.01)
    elif choice == 3:
        engine.rightAction(screen, cubes, 0.01)
        
    #print(choice)


highestValues = []
scores = []

engine.display = False
engine.getInput = randomInput

engine.rowX = 4
engine.rowY = 4

n = int(input("Input number of iterations: "))

for i in range(n):
    a = engine.main()
    scores.append(a[0])
    highestValues.append(a[1])
    if (n >= 10000 and i % (n // 100) == 0):
        print(str(i / (n / 100)) + "%")

plt.scatter(scores, highestValues)
plt.show()
