import pyautogui as gui

LAPTOPSCREEN = True

input("Move the mouse to the top left of the grid")
topLeft = gui.position()
input("Move the mouse to the bottom right of the grid")
botRight = gui.position()
gridSize = int(input("How many rows are in the grid: "))
"""
topLeft = (708, 435)
botRight = (1315, 1042)
gridSize = 20
topLeft = (777, 435)
botRight = (1255, 913)
gridSize = 14
topLeft = (819, 436)
botRight = (1224, 841)
gridSize = 10
topLeft = (848, 435)
botRight = (1203, 790)
gridSize = 8
topLeft = (900, 435)
botRight = (1142, 678)
gridSize = 6
"""

BLACK = (102, 102, 102, 255)
WHITE = (204, 204, 204, 255)
EMPTY = (255, 255, 255, 255)
val = [[0 for i in range(gridSize)] for i in range(gridSize)]
blackInRow = [0 for i in range(gridSize)]
blackInCol = [0 for i in range(gridSize)]
whiteInRow = [0 for i in range(gridSize)]
whiteInCol = [0 for i in range(gridSize)]
im = gui.screenshot()

cellWidth = (botRight[0]-topLeft[0])/gridSize
cellHeight = (botRight[1]-topLeft[1])/gridSize
"""
print(topLeft)
print(botRight)
print(gridSize)
print("Cell dimensions = %d %d" % (cellWidth, cellHeight))
exit(0)
"""

def readPixel(x, y):
    if LAPTOPSCREEN:
        x *= 2
        y *= 2
    return im.getpixel((x, y))

curX = topLeft[0]+cellWidth/2
curY = topLeft[1]+cellHeight/2
gui.click(curX, curY)
for i in range(gridSize):
    for j in range(gridSize):
        for k in range(-int(cellWidth/4), int(cellWidth/4)+1):
            for l in range(-int(cellHeight/4), int(cellHeight/4)+1):
                pixel = readPixel(curX+k, curY+l)
                if pixel == BLACK:
                    val[i][j] = 1
                elif pixel == WHITE:
                    val[i][j] = 2
                if val[i][j]:
                    break
            if val[i][j]:
                break
        curX += cellWidth
    curY += cellHeight
    curX -= gridSize*cellWidth

for i in range(gridSize):
    for j in range(gridSize):
        if val[i][j] == 1:
            blackInRow[i] += 1
            blackInCol[j] += 1
        elif val[i][j] == 2:
            whiteInRow[i] += 1
            whiteInCol[j] += 1

def setVal(row, col, c):
    val[row][col] = c
    x = topLeft[0]+cellWidth/2+cellWidth*col
    y = topLeft[1]+cellHeight/2+cellHeight*row
    if c == 1:
        gui.click(x, y)
        blackInRow[row] += 1
        blackInCol[col] += 1
    else:
        gui.rightClick(x, y)
        whiteInRow[row] += 1
        whiteInCol[col] += 1

def printGrid():
    for i in range(gridSize):
        for j in range(gridSize):
            print(val[i][j], end="")
        print()

def doComplete():
    ret = False
    for i in range(gridSize):
        for j in range(gridSize):
            if val[i][j] == 0:
                if blackInRow[i] == gridSize/2 or blackInCol[j] == gridSize/2:
                    setVal(i, j, 2)
                    ret = True
                elif whiteInRow[i] == gridSize/2 or whiteInCol[j] == gridSize/2:
                    setVal(i, j, 1)
                    ret = True
    return ret

def doThree():
    # vertical up
    ret = False
    for i in range(2, gridSize):
        for j in range(gridSize):
            if val[i][j] == 0 and val[i-1][j] == val[i-2][j]:
                if val[i-1][j] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i-1][j] == 2:
                    setVal(i, j, 1)
                    ret = True
    # vertical down
    for i in range(gridSize-2):
        for j in range(gridSize):
            if val[i][j] == 0 and val[i+1][j] == val[i+2][j]:
                if val[i+1][j] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i+1][j] == 2:
                    setVal(i, j, 1)
                    ret = True
    # vertical middle
    for i in range(1, gridSize-1):
        for j in range(gridSize):
            if val[i][j] == 0 and val[i-1][j] == val[i+1][j]:
                if val[i+1][j] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i+1][j] == 2:
                    setVal(i, j, 1)
                    ret = True
    # horizontal left
    for i in range(gridSize):
        for j in range(2, gridSize):
            if val[i][j] == 0 and val[i][j-1] == val[i][j-2]:
                if val[i][j-1] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i][j-1] == 2:
                    setVal(i, j, 1)
                    ret = True
    # horizontal right
    for i in range(gridSize):
        for j in range(gridSize-2):
            if val[i][j] == 0 and val[i][j+1] == val[i][j+2]:
                if val[i][j+1] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i][j+1] == 2:
                    setVal(i, j, 1)
                    ret = True
    # horizontal middle
    for i in range(gridSize):
        for j in range(1, gridSize-1):
            if val[i][j] == 0 and val[i][j-1] == val[i][j+1]:
                if val[i][j+1] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i][j+1] == 2:
                    setVal(i, j, 1)
                    ret = True
    return ret

def doForce():
    ret = False
    for i in range(gridSize):
        if blackInRow[i] == gridSize/2-1 and whiteInRow[i] < gridSize/2-1:
            for j in range(gridSize-2):
                num = 0
                for k in range(3):
                    if val[i][j+k] == 0 or val[i][j+k] == 2:
                        num += 1
                if num == 3:
                    for k in range(gridSize):
                        if (k < j or k > j+2) and val[i][k] == 0:
                            setVal(i, k, 2)
                            ret = True
        elif blackInRow[i] < gridSize/2-1 and whiteInRow[i] == gridSize/2-1:
            for j in range(gridSize-2):
                num = 0
                for k in range(3):
                    if val[i][j+k] == 0 or val[i][j+k] == 1:
                        num += 1
                if num == 3:
                    for k in range(gridSize):
                        if (k < j or k > j+2) and val[i][k] == 0:
                            setVal(i, k, 1)
                            ret = True
    for j in range(gridSize):
        if blackInCol[j] == gridSize/2-1 and whiteInCol[j] < gridSize/2-1:
            for i in range(gridSize-2):
                num = 0
                for k in range(3):
                    if val[i+k][j] == 0 or val[i+k][j] == 2:
                        num += 1
                if num == 3:
                    for k in range(gridSize):
                        if (k < i or k > i+2) and val[k][j] == 0:
                            setVal(k, j, 2)
                            ret = True
        elif blackInCol[j] < gridSize/2-1 and whiteInCol[j] == gridSize/2-1:
            for i in range(gridSize-2):
                num = 0
                for k in range(3):
                    if val[i+k][j] == 0 or val[i+k][j] == 1:
                        num += 1
                if num == 3:
                    for k in range(gridSize):
                        if (k < i or k > i+2) and val[k][j] == 0:
                            setVal(k, j, 1)
                            ret = True
    return ret

while True:
    changed = False
    changed = changed or doComplete()
    changed = changed or doThree()
    changed = changed or doForce()
    if not changed:
        break

finished = True
for i in range(gridSize):
    for j in range(gridSize):
        if val[i][j] == 0:
            finished = False
            break
    if not finished:
        break
if finished:
    gui.press('enter')
    print("FINISHED")
else:
    print("UNFINISHED")