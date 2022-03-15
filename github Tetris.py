#################################################
# hw6.py
#
# Your name: E.j. Ezuma-Ngwu
# Your andrew id: ufe
# Your partner's name: Brian
# Your partner's andrew id: hlew
#################################################

import copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Tetris
#################################################

def appStarted(app):
    (app.startPieces,app.pieceColors) = genStartPieces()
    app.fallingPiece = []
    app.fallingColor = []
    app.fallingCoord = []
    app.isGameOver = False
    app.timerDelay = 300
    app.score = 0
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.emptyColor = "blue"
    app.board = [([app.emptyColor] * app.cols) for _ in range(app.rows)]

    newFallingPiece(app)
    
#alocate our editable game dimensions
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)
#make a list of all the booleann coordinates on the board
def createEmptyCoord(fallingPiece):
    col = len(fallingPiece[0])
    List = [[(0,0)]*col for row in range(len(fallingPiece))]
    return List

#intitialize tetris
#make a starting piece
#set game over = to false
#clear the board

def initTetris(app):
    newFallingPiece(app)
    app.board = [([app.emptyColor] * app.cols) for _ in range(app.rows)]
    app.isGameOver = False

#allocate our reset button and controls for moving the piece
def keyPressed(app, event):
    if (event.key == "r"):
        initTetris(app)
    elif app.isGameOver != True:
        if (event.key == 'Left'):
            movingFallingPiece(app, 0, -1)
        elif (event.key == 'Right'):
            movingFallingPiece(app, 0, +1)
        elif (event.key == 'Down'):
            movingFallingPiece(app, +1, 0)
        elif (event.key == "Up"):
            rotateFallingPiece(app)
        elif (event.key == "Space"):
            while movingFallingPiece(app, +1, 0) != False:
                None


#we move the falling piece by one cell length if it not 
#interrupted by any border or other color already on the board
def movingFallingPiece(app,drow,dcol):
    cRow = drow * app.cellSize
    cCol = dcol * app.cellSize
    rowLimit = app.height - app.margin
    leftCol = 0
    rightCol = len(app.fallingCoord[0])-1
    tempCoord = copy.deepcopy(app.fallingCoord)
    for row in range(len(app.fallingCoord)):
        for col in range(len(app.fallingCoord[0])):
            app.fallingCoord[row][col][0]
            app.fallingCoord[row][col][0] += drow
            app.fallingCoord[row][col][1] += dcol
    if not fallingPieceIsLegal(app,app.fallingCoord):
        app.fallingCoord = tempCoord
        return False
    return True
        
#we check if the faling piece is out of bounds or 
#in a colored piece of the board
def fallingPieceIsLegal(app, pieceCoord):
    rows, cols = len(pieceCoord), len(pieceCoord[0])
    if pieceCoord[0][0][1] < 0:
        return False
    elif pieceCoord[0][cols-1][1] > (len(app.board[0])-1):
        return False
    for row in range(rows):
        for col in range(cols):
            if app.fallingPiece[row][col] == True:
                (rowCoord, colCoord) = pieceCoord[row][col]
                if (rowCoord not in range(app.rows)) or \
                    (colCoord not in range(app.cols)):
                        return False
                if app.board[rowCoord][colCoord] != app.emptyColor:
                    return False
    return True
#rotate pur piece counter clockwise
def rotateCounterClock(tempPiece):
    rows = len(tempPiece)
    cols = len(tempPiece[0])
    answer = [[(0,0)]*rows for col in range(cols)]
    for row in range(rows):
        for col in range(cols):
            answer[cols-col-1][row] = tempPiece[row][col]
    return answer
#we rotate our piece counterclockwise when it is not interupetd by a 
# border or another colored piece
def rotateFallingPiece(app):
    originalPiece = copy.deepcopy(app.fallingPiece)
    originalCoord = copy.deepcopy(app.fallingCoord)
    topLeftCoord = app.fallingCoord[0][0]
    #rotate the piece by 90degrees counterclockwise
    tempPiece = rotateCounterClock(app.fallingPiece)
    #create a list of empty rotated piece to fit the right coordinates
    tempPieceCoord = createEmptyCoord(tempPiece)
    for row in range(len(tempPiece)):
        for col in range(len(tempPiece[0])):
            newRow = ( topLeftCoord[0] + row)
            newCol = ( topLeftCoord[1] + col)
            tempPieceCoord[row][col] = [newRow,newCol] 
    app.fallingCoord = tempPieceCoord
    app.fallingPiece = tempPiece
    if not fallingPieceIsLegal(app, tempPieceCoord):
        app.fallingCoord = originalCoord
        app.fallingPiece = originalPiece

#calls all of our drawing functions
def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "orange")
    drawBoard(app, canvas)
    #only temporary to see if drawFallinPiece work
    drawFallingPiece(app, canvas)
    drawScore(app,canvas)
    if app.isGameOver == True:
        drawGameOver(app, canvas)

#sets out widths and heights for our tetris game
def playTetris():
    heightVar1, widthVar1, sizeOfCell, theMargin = gameDimensions()
    runApp(width = ((widthVar1 * sizeOfCell) + 2 * theMargin), 
    height = ((heightVar1 * sizeOfCell) + 2 * theMargin))



#from: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

#set all possible shapes as boolean value 2D lists
def genStartPieces():
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]]
    startPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    pColors = [ "red", "yellow", "magenta", "pink", "cyan", "green", "orange" ]
    return (startPieces,pColors)

#start a new piece at the top of the board 
def newFallingPiece(app):
    randomIndex = random.randint(0, len(app.startPieces) - 1)
    # set type of piece and color for the falling piece
    app.fallingPiece = app.startPieces[randomIndex]
    app.fallingColor = app.pieceColors[randomIndex]
    #assign coordinates of the pieces relative to the board coordinate.
    rowsBoard = (len(app.board))
    colsBoard = (len((app.board)[0]))
    rowsFallPiece = len(app.fallingPiece)
    colsFallPiece = len(app.fallingPiece[0])
    fallPieceCoord = createEmptyCoord(app.fallingPiece)
    for row in range(rowsFallPiece):
        for col in range(colsFallPiece):
            rowPieces = row
            colPieces = (colsBoard//2 - colsFallPiece//2) + col
            pieces = [rowPieces,colPieces]
            fallPieceCoord[row][col] = pieces
    app.fallingCoord = fallPieceCoord

#when the piece reaches the bottom of the current board, whether that be block 
# pieces or just the bare bottom, we place that piece and 
# restart with a new piece
def placeFallingPiece(app):
    rowsFallPiece = len(app.fallingPiece)
    colsFallPiece = len(app.fallingPiece[0])
    for rows in range(rowsFallPiece):
        for cols in range(colsFallPiece):
            if app.fallingPiece[rows][cols] == True:
                (row,col) = app.fallingCoord[rows][cols]
                (x0, y0, x1, y1) = getCellBounds(app, row,col)
                app.board[row][col] = app.fallingColor

#finds a full row of blocks
def findFullRowsIndexes(app, board):
    List=[]
    for rows in range(app.rows):
        if app.emptyColor not in board[rows]:
            List.append(rows)
    return List
#removes that row of full block 
def removeFullRows(app):
    fullRowIndex = findFullRowsIndexes(app,app.board)
    score = len(fullRowIndex)**2
    if len(fullRowIndex) > 0:
        for index in fullRowIndex:
            # remove full rows
            tempBoard = copy.deepcopy(app.board)
            for row in range(index):
                tempBoard[(row+1)] = app.board[row]
                for col in range(app.cols):
                    if row == 0:
                        app.board[row][col] = app.emptyColor
            app.board = tempBoard
        app.score += score

#the tertis piece moves if all conditions are met
def takeStep(app):
    if movingFallingPiece(app, +1, 0) == False:
        placeFallingPiece(app)
        newFallingPiece(app)
        removeFullRows(app)
        if fallingPieceIsLegal(app, app.fallingCoord) != True:
            app.isGameOver = True

#if the game isn't over we continue
def timerFired(app):
    if app.isGameOver != True:
        return takeStep(app)
    

def drawScore(app, canvas):
    canvas.create_text(app.width/2, app.margin/2,
                       text=f'Score: {app.score}',
                       fill='blue')


def drawFallingPiece(app, canvas):
    rowsFallPiece = len(app.fallingPiece)
    colsFallPiece = len(app.fallingPiece[0])
    for rows in range(rowsFallPiece):
        for cols in range(colsFallPiece):
            if app.fallingPiece[rows][cols] == True:
                (row,col) = app.fallingCoord[rows][cols]
                (x0, y0, x1, y1) = getCellBounds(app, row,col)
                canvas.create_rectangle(x0, y0, x1, y1, fill=app.fallingColor)

def drawGameOver(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text='Game over!',
                           font='Calibri 30 bold', fill='white')
    canvas.create_text(app.width/2, app.height/2+40,
                           text='Press r to restart!',
                           font='Calibri 24', fill='grey')
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col)
                                    
def drawCell(app, canvas, cellRow, cellCol):
    (x0, y0, x1, y1) = getCellBounds(app, cellRow, cellCol)
    canvas.create_rectangle(x0, y0, x1, y1, fill = app.board[cellRow][cellCol], 
                            outline = "black")
    

#################################################
# Test Functions
#################################################

def main():
    playTetris()

if __name__ == '__main__':
    main()
