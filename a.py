import pyautogui as gui

LAPTOPSCREEN = False

input("Move the mouse to the top left of the grid")
topLeft = gui.position()
input("Move the mouse to the bottom right of the grid")
botRight = gui.position()
gridRows = int(input("How many rows are in the grid: "))
gridCols = int(input("How many cols are in the grid: "))
"""
topLeft = (708, 435)
botRight = (1315, 1042)
gridRows, gridCols = 20, 20
topLeft = (777, 435)
botRight = (1255, 913)
gridRows, gridCols = 14
topLeft = (819, 436)
botRight = (1224, 841)
gridRows, gridCols = 10
topLeft = (848, 435)
botRight = (1203, 790)
gridRows, gridCols = 8
topLeft = (900, 435)
botRight = (1142, 678)
gridRows, gridCols = 6
"""

BLACK = (102, 102, 102, 255)
WHITE = (204, 204, 204, 255)
EMPTY = (255, 255, 255, 255)
val = [[0 for j in range(gridCols)] for i in range(gridRows)]
blackInRow = [0 for i in range(gridRows)]
blackInCol = [0 for i in range(gridCols)]
whiteInRow = [0 for i in range(gridRows)]
whiteInCol = [0 for i in range(gridCols)]
im = gui.screenshot()

cellWidth = (botRight[0]-topLeft[0])/gridCols
cellHeight = (botRight[1]-topLeft[1])/gridRows
"""
print(topLeft)
print(botRight)
print(gridRows, gridCols)
print("Cell dimensions = %d %d" % (cellWidth, cellHeight))
exit(0)
"""

def readPixel(x, y):
    if LAPTOPSCREEN:
        x *= 2
        y *= 2
    return im.getpixel((x, y))

def readCellColour(i, j):
    curX = topLeft[0]+cellWidth/2+cellWidth*j
    curY = topLeft[1]+cellHeight/2+cellHeight*i
    '''
    gui.moveTo(curX-int(cellWidth/4), curY-int(cellHeight/4))
    gui.moveTo(curX-int(cellWidth/4), curY-int(cellHeight/4))
    gui.moveTo(curX-int(cellWidth/4), curY-int(cellHeight/4))
    gui.moveTo(curX+int(cellWidth/4), curY+int(cellHeight/4))
    gui.moveTo(curX+int(cellWidth/4), curY+int(cellHeight/4))
    gui.moveTo(curX+int(cellWidth/4), curY+int(cellHeight/4))
    '''
    cols = []
    for k in range(-int(cellWidth/4), int(cellWidth/4)+1):
        for l in range(-int(cellHeight/4), int(cellHeight/4)+1):
            pixel = readPixel(curX+k, curY+l)
            ind = -1
            for x in range(len(cols)):
                if cols[x][1] == pixel:
                    ind = x
                    break
            if ind == -1:
                ind = len(cols)
                cols.append([0, pixel])
            cols[ind][0] += 1
    cols.sort(reverse=True)
    if len(cols) == 1:
        return 0
    if cols[0][1][0] < 128:
        return 1
    return 2

gui.click(topLeft[0], topLeft[1])
for i in range(gridRows):
    for j in range(gridCols):
        val[i][j] = readCellColour(i, j)
        print(val[i][j], end='')
    print()

'''
curX = topLeft[0]+cellWidth/2
curY = topLeft[1]+cellHeight/2
gui.click(curX, curY)
for i in range(gridRows):
    for j in range(gridCols):
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
    curX -= gridCols*cellWidth
'''

for i in range(gridRows):
    for j in range(gridCols):
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
    for i in range(gridRows):
        for j in range(gridCols):
            print(val[i][j], end="")
        print()

def doComplete():
    ret = False
    for i in range(gridRows):
        for j in range(gridCols):
            if val[i][j] == 0:
                if blackInRow[i] == gridCols/2 or blackInCol[j] == gridRows/2:
                    setVal(i, j, 2)
                    ret = True
                elif whiteInRow[i] == gridCols/2 or whiteInCol[j] == gridRows/2:
                    setVal(i, j, 1)
                    ret = True
    return ret

def doThree():
    # vertical up
    ret = False
    for i in range(2, gridRows):
        for j in range(gridCols):
            if val[i][j] == 0 and val[i-1][j] == val[i-2][j]:
                if val[i-1][j] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i-1][j] == 2:
                    setVal(i, j, 1)
                    ret = True
    # vertical down
    for i in range(gridRows-2):
        for j in range(gridCols):
            if val[i][j] == 0 and val[i+1][j] == val[i+2][j]:
                if val[i+1][j] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i+1][j] == 2:
                    setVal(i, j, 1)
                    ret = True
    # vertical middle
    for i in range(1, gridRows-1):
        for j in range(gridCols):
            if val[i][j] == 0 and val[i-1][j] == val[i+1][j]:
                if val[i+1][j] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i+1][j] == 2:
                    setVal(i, j, 1)
                    ret = True
    # horizontal left
    for i in range(gridRows):
        for j in range(2, gridCols):
            if val[i][j] == 0 and val[i][j-1] == val[i][j-2]:
                if val[i][j-1] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i][j-1] == 2:
                    setVal(i, j, 1)
                    ret = True
    # horizontal right
    for i in range(gridRows):
        for j in range(gridCols-2):
            if val[i][j] == 0 and val[i][j+1] == val[i][j+2]:
                if val[i][j+1] == 1:
                    setVal(i, j, 2)
                    ret = True
                elif val[i][j+1] == 2:
                    setVal(i, j, 1)
                    ret = True
    # horizontal middle
    for i in range(gridRows):
        for j in range(1, gridCols-1):
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
    for i in range(gridRows):
        if blackInRow[i] == gridCols/2-1 and whiteInRow[i] < gridCols/2-1:
            for j in range(gridCols-2):
                num = 0
                for k in range(3):
                    if val[i][j+k] == 0 or val[i][j+k] == 2:
                        num += 1
                if num == 3:
                    for k in range(gridCols):
                        if (k < j or k > j+2) and val[i][k] == 0:
                            setVal(i, k, 2)
                            ret = True
        elif blackInRow[i] < gridCols/2-1 and whiteInRow[i] == gridCols/2-1:
            for j in range(gridCols-2):
                num = 0
                for k in range(3):
                    if val[i][j+k] == 0 or val[i][j+k] == 1:
                        num += 1
                if num == 3:
                    for k in range(gridCols):
                        if (k < j or k > j+2) and val[i][k] == 0:
                            setVal(i, k, 1)
                            ret = True
    for j in range(gridCols):
        if blackInCol[j] == gridRows/2-1 and whiteInCol[j] < gridRows/2-1:
            for i in range(gridRows-2):
                num = 0
                for k in range(3):
                    if val[i+k][j] == 0 or val[i+k][j] == 2:
                        num += 1
                if num == 3:
                    for k in range(gridRows):
                        if (k < i or k > i+2) and val[k][j] == 0:
                            setVal(k, j, 2)
                            ret = True
        elif blackInCol[j] < gridRows/2-1 and whiteInCol[j] == gridRows/2-1:
            for i in range(gridRows-2):
                num = 0
                for k in range(3):
                    if val[i+k][j] == 0 or val[i+k][j] == 1:
                        num += 1
                if num == 3:
                    for k in range(gridRows):
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
for i in range(gridRows):
    for j in range(gridCols):
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
