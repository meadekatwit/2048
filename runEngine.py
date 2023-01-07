import engine
import pygame
from matplotlib import pyplot as plt
import random
import sys

keyReady = True
def userInput(screen, cubes, event): #Has the user play the game
    global keyReady
    if event.type == pygame.KEYUP:
        keyReady = True
    if event.type == pygame.KEYDOWN and keyReady:
        keyReady = False
        if event.key == pygame.K_DOWN:
            engine.downAction(screen, cubes, 0.05)    
        if event.key == pygame.K_UP:
            engine.upAction(screen, cubes, 0.05)
        if event.key == pygame.K_LEFT:
            engine.leftAction(screen, cubes, 0.05)
        if event.key == pygame.K_RIGHT:
            engine.rightAction(screen, cubes, 0.05)

def randomInput(screen, cubes, event): #Plays the game completely randomly
    """Random Input"""
    choice = random.randint(0,3)
    if choice == 0:
        engine.downAction(screen, cubes, 0)
    elif choice == 1:
        engine.upAction(screen, cubes, 0)
    elif choice == 2:
        engine.leftAction(screen, cubes, 0)
    elif choice == 3:
        engine.rightAction(screen, cubes, 0)

def preferUpLeft(screen, cubes, event): #Plays with preference Up, Right, Left, Down
    """Prefers top left corner"""
    if not engine.upAction(screen, cubes, 0):
        if not engine.rightAction(screen, cubes, 0):
            if not engine.downAction(screen, cubes, 0):
                engine.leftAction(screen, cubes, 0)
                
displayProccess = True
engine.display = displayProccess

engine.rowX = 4
engine.rowY = 4

#engines = [randomInput, preferUpLeft] #Engines to be tested
engines = [preferUpLeft, randomInput]

scores = []
highestValues = []

barX = ["Average Score", "Average Highest Value"]

n = 1
z = 0

if "userPlaying" in sys.argv:
    engines.insert(0, userInput)

for eng in engines:
    z += 1
    engine.getInput = eng

    if (eng == userInput):
        engine.display = True
        print("User playing")
        a = engine.main()
        print("Score: " + str(a[0]))
        print("Highest Value: " + str(a[1]))
        plt.bar([len(engines) + z, 2 * len(engines) + z + 1], [a[0], a[1]], label = eng.__name__)
        scores.append(a[0])
        highestValues.append(a[1])
        engine.display = displayProccess
        engine.quit()
    else:
        print("Testing " + eng.__name__ + " engine")

        averageScore = 0
        averageHighestValue = 0
        absoluteHighestValue = 0
        absoluteHighestScore = 0

        for i in range(n):
            a = engine.main()
            averageScore += a[0] / n
            averageHighestValue += a[1] / n
            if absoluteHighestValue < a[1]:
                absoluteHighestValue = a[1]
            if absoluteHighestScore < a[0]:
                absoluteHighestScore = a[0]
        engine.quit()
        
        print("Average Score: " + str(averageScore))
        print("Average Highest Value: " + str(averageHighestValue))
        print("Absolute Highest Score: " + str(absoluteHighestScore))
        print("Absolute Highest Value: " + str(absoluteHighestValue))
        print()

        plt.bar([len(engines) + z, 2 * len(engines) + z + 1], [averageScore, averageHighestValue], label = eng.__name__)

        scores.append(averageScore)
        highestValues.append(averageHighestValue)

plt.gca().set_title("Average Score - Average Highest Value")
plt.gca().set_xlabel("Average Score - Average Highest Value")
plt.gca().set_ylabel("Score")
plt.gca().get_xaxis().set_visible(False)
plt.legend()

plt.show()

#n = int(input("Input number of iterations: "))

#for i in range(n):
#    a = engine.main()
#    scores.append(a[0])
#    highestValues.append(a[1])
#    if (n >= 1000 and i % (n // 100) == 0):
#        print(str(i / (n / 100)) + "%")

#plt.scatter(scores, highestValues)
#plt.show()


