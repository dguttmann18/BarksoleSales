# import pygame module in this program
from asyncio.windows_events import NULL
from calendar import month
from curses import KEY_ENTER
from operator import truediv
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
from datetime import date, timedelta
import time
import sqlite3
import os
 
# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

displaySaved = False
pressedEnter = False
dateConfirmed = False
year1Confirmed = False
year2Confirmed = False
count = 0
screenNumber = 0
dateOfDocket = ""
fieldNum = 0
optionNum = 0
strokeNum = 0
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
txt = ["", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00"]
printDate = ""
printMonthDate = ""
graphYear1, graphYear2 = "", ""
numKeys = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9]

clock = pygame.time.Clock()

color_passive = pygame.Color('chartreuse4')
color = color_passive
# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
lightBlue = (0, 150, 150)
 
# assigning values to X and Y variable
X = 900
Y = 600
 
# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))
 
# set the pygame window name
pygame.display.set_caption('Show Text')
 
# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
#print(str(pygame.font.get_fonts()))
font1 = pygame.font.SysFont("consolas", 20)
font2 = pygame.font.SysFont("consolas", 35)
font3 = pygame.font.SysFont("consolas", 35)

base_font = font1

def generateGraph(year1, year2):
    conn = sqlite3.connect("BarksoleDockets.db")

    c = conn.cursor()

    c.execute("""SELECT SUBSTR(DateOfDocket, 3, 6) as Month, SUM(Shoes) + SUM(Keys) +SUM(Products) + SUM(Engraving)  + SUM(Plates) + SUM(Cleaning) + SUM(CallOuts) + SUM(Other) AS tot
                    FROM Dockets
                    WHERE LENGTH(DateOfDocket) = 8 AND SUBSTR(DateOfDocket, 5) LIKE """ + year1 + " OR SUBSTR(DateOfDocket, 5) LIKE " + year2 +
                    """ GROUP BY SUBSTR(DateOfDocket, 3, 6)
                    ORDER BY SUBSTR(DateOfDocket, 5), SUBSTR(DateOfDocket, 3, 2)""")
    d = c.fetchall()

    data = {}

    x = (year1, year2)

    for y in x:
        for i in range(12):
            s = str(i+1) + y

            if i < 9:
                s = "0" + s
            
            data[s] = 0.0

    for j in d:
        data[j[0]] = j[1]

    conn.commit()
    conn.close()

    fileGraph = open("graphData.txt", "w")
    
    fileGraph.write(year1 + "|" + year2 + "\n")
    
    for j in data:
        fileGraph.write(j + "|" + str(data[j]) + "\n")
    
    fileGraph.close()

    os.system("start excel Graphs.xlsm")


def displayMonthlyFigures():
    global printDate

    mnt = printDate[:2]
    yr = printDate[2:6]

    conn = sqlite3.connect("BarksoleDockets.db")
    c = conn.cursor()

    c.execute("SELECT * FROM dockets WHERE dateOfDocket LIKE '__" + mnt + yr + "'")

    x = c.fetchall()
    
    aFile = open("monthlyFigures.txt", "w")
    
    for row in x:
        aFile.write(row[0] + ";" + str(row[1]) + ";" + str(row[2]) + ";" + str(row[3]) + ";" + str(row[4]) + ";" + str(row[5]) + ";" + str(row[6]) + ";" + str(row[7]) + ";" + str(row[8]) + "\n")

    conn.commit()
    conn.close()

    os.system("start excel PrintMonthlySalesFigures.xlsm")

def isValidDate():
    if len(printDate) < 6:
        return False
    
    elif int(printDate[:2]) < 1 or int(printDate[:2]) > 12:
        return False
    
    else:
        return True

def setMonthDate():
    global printMonthDate

    mnt = printDate[:2]
    yr = printDate[2:6]
    
    printMonthDate = months[int(mnt) - 1] + " " + yr

def formatCurrency(curr):
    curr = curr.strip()
    curr = format(float(curr), ".2f")
    curr = curr.rjust(8)

    return curr

def fetchData():
    conn = sqlite3.connect("BarksoleDockets.db")
    c = conn.cursor()

    c.execute("SELECT * FROM dockets WHERE dateOfDocket LIKE '" + dateToNum(txt[0]) + "'")

    x = c.fetchone()
    
    if str(x) != "None":
        for i in range(1, 9):
            txt[i] = formatCurrency(str(x[i]))
    else:
        for i in range(1, 9):
            txt[i] = formatCurrency("0.00")

    conn.commit()
    conn.close()

def writeToDataBase():
    conn = sqlite3.connect("BarksoleDockets.db")
    c = conn.cursor()


    c.execute("SELECT * FROM dockets WHERE dateOfDocket LIKE '" + dateToNum(txt[0]) + "'")

    x = c.fetchone()

    if str(x) == "None":
        c.execute("INSERT INTO dockets VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (dateToNum(txt[0]), txt[1], txt[2], txt[3], txt[4], txt[5], txt[6], txt[7], txt[8]))
    else:
        c.execute("UPDATE dockets SET Shoes = ?, Keys = ?, Products = ?, Engraving = ?, Plates = ?, Cleaning = ?, CallOuts = ?, Other = ? WHERE dateOfDocket LIKE '" + dateToNum(txt[0]) + "'", (txt[1], txt[2], txt[3], txt[4], txt[5], txt[6], txt[7], txt[8]))

    conn.commit()
    conn.close()

def resetInputScreen():
    strokeNum = 0

    txt = ["", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00"]
    fieldNum = 0

def getDate():
    today = date.today()
    today = today - timedelta(days=1)
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)

    while len(day) < 2:
        day = "0" + day

    while len(month) < 2:
        month = "0" + month

    return day + month + year

def dateToNum(date):

    dte = date.split(" ")
    day = dte[0]
    mnt = dte[1]
    yr = dte[2]
    
    mntNum = 1

    while months[mntNum-1] != mnt:
        mntNum += 1 

    mntNum = str(mntNum)
    if len(mntNum) == 1:
        mntNum = "0" + mntNum
  
    return day + mntNum + yr

def numToDate(num):
    if len(num) < 8:
        return numToDate(getDate())

    day = num[0:2]
    mnt = num[2:4]
    yr = num[4:]

    mntName = months[int(mnt)-1]

    if int(day) < 1 or (int(day) > 31) or int(mnt) < 1 or int(mnt) > 12:
        return numToDate(getDate())

    return day + " " + mntName + " " + yr


def drawInputScreen():
    global input_docketNumber, textRect, cursor, displaySaved, count, year1Confirmed, year2Confirmed, graphYear1, graphYear2
    
    if screenNumber == 0:
        txtTitle = font2.render("BARKSOLE SEA POINT RECORD MANAGER", True, white, lightBlue)
        txtLine = font1.render('----------------------------------------------------------------------------------------------------------', True, white, lightBlue)
        txtHelpText = font1.render("Please select an option below:", True, black, white)

        input_docketNumber = pygame.Rect(300, 140 + 30*optionNum, 230, 32)
        txtTitleRect = txtTitle.get_rect()
        txtLineRect = txtTitle.get_rect()
        txtLine2Rect = txtTitle.get_rect()
        txtHelpTextRect = txtHelpText.get_rect()

        #pygame.draw.rect(display_surface, white, pygame.Rect(290, 90, 500, 400),  2)
        pygame.draw.rect(display_surface, white, pygame.Rect(200, 90, 1000, 400), 2)
        pygame.draw.rect(display_surface, white, pygame.Rect(200, 105, 100, 100),  2)

        txtTitleRect.center = (X // 2, 20)
        txtLineRect.center = (100, 140)
        txtLine2Rect.center = (100, 300)
        txtHelpTextRect.center = (420, 100)

        display_surface.fill(lightBlue)

        display_surface.blit(txtTitle, txtTitleRect)
        display_surface.blit(txtLine, txtLineRect)
        display_surface.blit(txtLine, txtLine2Rect)
        display_surface.blit(txtHelpText, txtHelpTextRect)


    if screenNumber == 1:
        # create a text surface object,
        # on which text is drawn on it.
        text = font2.render('DAILY SALES INPUT', True, white, blue)
        text2 = font1.render('-----------------------------------------------------------------------------------------', True, white, blue)
        txtDocketNumber = font1.render('     DATE (DDMMYYYY):', True, white, blue)
        txtShoes = font1.render('SHOES/BAGS/SUITCASES:', True, white, blue)
        txtKeys = font1.render('          KEYS/LOCKS:', True, white, blue)
        txtProducts = font1.render('            PRODUCTS:', True, white, blue)
        txtEngraving = font1.render('    ENGRAVING/STAMPS:', True, white, blue)
        txtSigns = font1.render(' SIGNS/NUMBER PLATES:', True, white, blue)
        txtDryCleaning = font1.render('        DRY CLEANING:', True, white, blue)
        txtCallOuts = font1.render('           CALL-OUTS:', True, white, blue)
        txtOther = font1.render('               OTHER:', True, white, blue)
        txtSave = font1.render('Press <TAB> to save...', True, black, white)
        txtEsc = font1.render("Press <ESC> to return to the main menu", True, black, white)
        
        # create a rectangular object for the
        # text surface object
        input_docketNumber = pygame.Rect(450, 80 + 50*fieldNum, 100, 32)
        textRect = text.get_rect()
        text2Rect = text.get_rect()
        text3Rect = text.get_rect()
        cursor = pygame.Rect(textRect.topright, (3, textRect.height))
        lblDocketNumber = txtDocketNumber.get_rect()
        lblShoes = txtShoes.get_rect()
        lblKeys = txtKeys.get_rect()
        lblProducts = txtProducts.get_rect()
        lblEngraving = txtEngraving.get_rect()
        lblSigns = txtSigns.get_rect()
        lblDryCleaning = txtDryCleaning.get_rect()
        lblCallOuts = txtCallOuts.get_rect()
        lblOther = txtOther.get_rect()
        lblSave = txtSave.get_rect()
        lblEsc = txtEsc.get_rect()

        pygame.draw.rect(display_surface, white, pygame.Rect(290, 90, 500, 400),  2)
        
        # set the center of the rectangular object.
        textRect.center = (X // 2, 20)
        text2Rect.center = (100, 70) 
        text3Rect.center = (100, 540)
        lblDocketNumber.center = (300, 100)
        lblShoes.center = (300, 150)
        lblKeys.center = (300, 200)
        lblProducts.center = (300, 250)
        lblEngraving.center = (300, 300)
        lblSigns.center = (300, 350)
        lblDryCleaning.center = (300, 400)
        lblCallOuts.center = (300, 450)
        lblOther.center = (300, 500)
        lblSave.center = (150, 570)
        lblEsc.center = (680, 570)
        
        # completely fill the surface object
        # with white color
        display_surface.fill(blue)
    
        # copying the text surface object
        # to the display surface object
        # at the center coordinate.
        display_surface.blit(text, textRect)
        display_surface.blit(text2, text2Rect)
        display_surface.blit(text2, text3Rect)
        display_surface.blit(txtDocketNumber, lblDocketNumber)
        display_surface.blit(txtShoes, lblShoes)
        display_surface.blit(txtKeys, lblKeys)
        display_surface.blit(txtProducts, lblProducts)
        display_surface.blit(txtEngraving, lblEngraving)
        display_surface.blit(txtSigns, lblSigns)
        display_surface.blit(txtDryCleaning, lblDryCleaning)
        display_surface.blit(txtCallOuts, lblCallOuts)
        display_surface.blit(txtOther, lblOther)
        display_surface.blit(txtSave, lblSave)
        display_surface.blit(txtEsc, lblEsc)
        
        if displaySaved:
            txtSaved = font3.render("Record for " + dateOfDocket + " has been saved", True, black, white)
            lblSaved = txtSaved.get_rect()
            lblSaved.center = (450, 570)
            display_surface.blit(txtSaved, lblSaved)
        
    if screenNumber == 2:
        global printMonthDate

        text = font2.render('VIEW MONTHLY SALES', True, white, blue)
        txtLine = font1.render('-----------------------------------------------------------------------------------------------------------------------------', True, white, blue)
        txtHelp = font1.render("Please provide the month and year in the format <MMYYYY>:", True, blue, white)
        txtInput = font1.render("", True, white, black)
        txtContinue = font1.render("Press <ENTER> to continue...", True, blue, white)
        txtError = font1.render("Invalid date entered! Please provide a valid one...", True, blue, white)
        txtConfirm = font1.render("Press <ENTER> to print the Monthly Sales Report for: " + printMonthDate, True, blue, white)
        txtEsc = font1.render("Press <ESC> to return to the main menu", True, blue, white)

        textRect = text.get_rect()
        txtLineRect = txtLine.get_rect()
        txtLine2Rect = txtLine.get_rect()
        txtHelpRect = txtHelp.get_rect()
        txtInputRect = txtInput.get_rect()
        txtContinueRect = txtContinue.get_rect()
        txtConfirmRect = txtConfirm.get_rect()
        txtEscRect = txtEsc.get_rect()
        txtErrorRect = txtError.get_rect()
            
        textRect.center = (X // 2, 70)
        txtLineRect.center = (250, 140)
        txtLine2Rect.center = (250, 500)
        txtHelpRect.center = (450, 200)
        txtInputRect.center = (400, 250)
        txtContinueRect.center = (450, 330)
        txtErrorRect.center = (450, 330)
        txtConfirmRect.center = (450, 400)
        txtEscRect.center = (680, 570)

        input_docketNumber = pygame.Rect(400, 250, 70, 32)
        display_surface.fill(blue)

        display_surface.blit(text, textRect)
        display_surface.blit(txtLine, txtLineRect)
        display_surface.blit(txtLine, txtLine2Rect)
        display_surface.blit(txtHelp, txtHelpRect)
        display_surface.blit(txtInput, txtInputRect)
        display_surface.blit(txtEsc, txtEscRect)
        
        pygame.draw.rect(display_surface, black, input_docketNumber)

        x = base_font.render(printDate, True, (255, 255, 255))

        #display_surface.blit(, (450, 500))
        display_surface.blit(x, (400, 260))

        if isValidDate() and not pressedEnter:
            display_surface.blit(txtContinue, txtContinueRect)
        elif not isValidDate() and len(printDate) == 6:
            display_surface.blit(txtError, txtErrorRect)
        
        if pressedEnter:
            display_surface.blit(txtConfirm, txtConfirmRect)
    if screenNumber == 3:
        text = font2.render('VIEW GRAPH', True, white, blue)
        txtLine = font1.render('-----------------------------------------------------------------------------------------------------------------------------', True, white, blue)
        txtHelpYear1 = font1.render("Please provide a year in the format <YYYY>:", True, blue, white)
        txtInputYear1 = font1.render("", True, white, black)
        txtInputYear2 = font1.render("", True, white, black)
        txtHelpYear2 = font1.render("Please provide a year in the format <YYYY> with which to compare " + graphYear1 + ":", True, blue, white)
        txtError = font1.render("Invalid date entered! Please provide a valid one...", True, blue, white)
        txtConfirm = font1.render("Press <ENTER> to display the graph comparing " + graphYear1 + " with " + graphYear2 + "...", True, blue, white)
        txtEsc = font1.render("Press <ESC> to return to the main menu", True, blue, white)

        textRect = text.get_rect()
        txtLineRect = txtLine.get_rect()
        txtLine2Rect = txtLine.get_rect()
        txtHelpYear1Rect = txtHelpYear1.get_rect()
        txtInputYear1Rect = txtInputYear1.get_rect()
        txtInputYear2Rect = txtInputYear2.get_rect()
        txtHelpYear2Rect = txtHelpYear2.get_rect()
        txtConfirmRect = txtConfirm.get_rect()
        txtEscRect = txtEsc.get_rect()
        txtErrorRect = txtError.get_rect()
            
        textRect.center = (X // 2, 70)
        txtLineRect.center = (250, 140)
        txtLine2Rect.center = (250, 500)
        txtHelpYear1Rect.center = (450, 200)
        txtHelpYear2Rect.center = (450, 330)
        txtInputYear1Rect.center = (430, 220)
        txtInputYear2Rect.center = (430, 360)
        txtErrorRect.center = (400, 330)
        txtConfirmRect.center = (450, 450)
        txtEscRect.center = (680, 570)

        if not year1Confirmed:
            input_docketNumber = pygame.Rect(430, 220, 50, 32)
        else:
            input_docketNumber = pygame.Rect(430, 350, 50, 32)
        
        display_surface.fill(blue)

        display_surface.blit(text, textRect)
        display_surface.blit(txtLine, txtLineRect)
        display_surface.blit(txtLine, txtLine2Rect)
        display_surface.blit(txtHelpYear1, txtHelpYear1Rect)
        display_surface.blit(txtInputYear1, txtInputYear1Rect)
        display_surface.blit(txtEsc, txtEscRect)
        
        if not year1Confirmed or not year2Confirmed:
            pygame.draw.rect(display_surface, black, input_docketNumber)

        x = base_font.render(graphYear1, True, (255, 255, 255))
        display_surface.blit(x, (430, 230))
        
        if year1Confirmed:
            x = base_font.render(graphYear2, True, (255, 255, 255))
            display_surface.blit(x, (430, 360))
            #txtInputRect.center = (430, 360)
            display_surface.blit(txtInputYear2, txtInputYear2Rect)

        
        if year1Confirmed:
             display_surface.blit(txtHelpYear2, txtHelpYear2Rect)

        if year1Confirmed and year2Confirmed:
            display_surface.blit(txtConfirm, txtConfirmRect)

drawInputScreen()
 
# infinite loop
while True:   
    global textRect, input_docketNumber, cursor#, year1Confirmed, year2Confirmed, graphYear1, graphYear2

    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():
 
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
 
            # deactivates the pygame library
            pygame.quit()
 
            # quit the program.
            quit()
        
        if event.type == pygame.KEYDOWN:

            if screenNumber == 0:
                if event.key == pygame.K_DOWN:
                    if optionNum < 4:
                        optionNum += 1
                    
                    elif optionNum == 4:
                        optionNum = 0


                if event.key == pygame.K_UP:
                    if optionNum > 0:
                        optionNum -= 1
                    
                    elif optionNum == 0:
                        optionNum = 4
                
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if optionNum == 0:
                        screenNumber = 1
                    elif optionNum == 1:
                        screenNumber = 2
                    elif optionNum == 2:
                        screenNumber = 3
                        
            elif screenNumber == 1:
  
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    displaySaved = False
                    
                    # get text input from 0 to -1 i.e. end.
                    txt[fieldNum] = txt[fieldNum][:-1]
                    
                # Check for ARROW_DOWN OR ENTER
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:            
                       
                    displaySaved = False
                        
                    strokeNum = 0

                    if fieldNum > 0:
                        if txt[fieldNum] == "":
                            txt[fieldNum] = "0"
                        
                        txt[fieldNum] = txt[fieldNum].strip()
                        txt[fieldNum] = format(float(txt[fieldNum]), ".2f")
                        txt[fieldNum] = txt[fieldNum].rjust(8)
                    elif fieldNum == 0:
                            
                        if txt[0] == "":
                            txt[0] = getDate()
                            
                        txt[0] = numToDate(txt[0]) 

                        dateOfDocket = txt[0]
                        fetchData() 
                        
                    if fieldNum < 8:
                        fieldNum += 1
                        txt[fieldNum] = txt[fieldNum].strip()

                # Check for ARROW_UP
                elif event.key == pygame.K_UP:
                    displaySaved = False
                        
                    strokeNum = 0

                    if fieldNum > 0:
                        if txt[fieldNum] == "":
                            txt[fieldNum] = "0"

                        txt[fieldNum] = txt[fieldNum].strip()
                        txt[fieldNum] = format(float(txt[fieldNum]), ".2f")
                        txt[fieldNum] = txt[fieldNum].rjust(8)
                        
                    if fieldNum == 0:
                        pass
                    else:
                        fieldNum -= 1

                        if fieldNum > 1:
                            txt[fieldNum] = txt[fieldNum].strip()
                        elif fieldNum == 0:
                            txt[0] = dateToNum(txt[0])
                            dateOfDocket = txt[0]
            
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    displaySaved = False
                
                # Unicode standard is used for string
                # formation
                elif event.key in numKeys or (event.key in [pygame.K_KP_PERIOD, pygame.K_PERIOD] and txt[fieldNum].count(".") == 0):
                    if screenNumber == 1:    
                        displaySaved = False
                        strokeNum += 1

                        if strokeNum == 1:
                            txt[fieldNum] = ""

                        if len(txt[fieldNum]) < 8:
                            txt[fieldNum] += event.unicode

                # Check for TAB key pressed
                elif event.key == pygame.K_TAB:            
                    writeToDataBase()
                    displaySaved = True
                
                elif event.key == pygame.K_ESCAPE:
                    screenNumber = 0
                    optionNum = 0
                    resetInputScreen()
            
            elif screenNumber == 2:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    
                    # get text input from 0 to -1 i.e. end.
                    printDate = printDate[:-1]
                    pressedEnter = False
                    dateConfirmed = False
                
                elif event.key in numKeys:
                    strokeNum += 1

                    if strokeNum == 1:
                        printDate = ""

                    if len(printDate) < 6:
                        printDate += event.unicode
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if not dateConfirmed:
                        if isValidDate():
                            pressedEnter = True
                            setMonthDate()
                            dateConfirmed = True
                        else:
                            dateConfirmed = False
                    else:
                        displayMonthlyFigures()
                        printDate = ""
                        pressedEnter = False
                        dateConfirmed = False
                        screenNumber = 0

                elif event.key == pygame.K_ESCAPE:
                    printDate = ""
                    pressedEnter = False
                    dateConfirmed = False
                    screenNumber = 0
            
            elif screenNumber == 3:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    
                    if not year1Confirmed:
                        # get text input from 0 to -1 i.e. end.
                        graphYear1 = graphYear1[:-1]
                        year1Confirmed = False
                    elif year1Confirmed and not year2Confirmed:
                        graphYear2 = graphYear2[:-1]
                        year2Confirmed = False
                
                elif event.key in numKeys:
                    if not year1Confirmed:
                        strokeNum += 1

                        if strokeNum == 1:
                            graphYear1 = ""

                        if len(graphYear1) < 4:
                            graphYear1 += event.unicode
                    elif year1Confirmed and not year2Confirmed:
                        strokeNum += 1

                        if strokeNum == 1:
                            graphYear2 = ""

                        if len(graphYear2) < 4:
                            graphYear2 += event.unicode
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if not year1Confirmed and len(graphYear1) == 4:
                        year1Confirmed = True

                    elif year1Confirmed and not year2Confirmed and len(graphYear2) == 4 and graphYear1 != graphYear2:
                        year2Confirmed = True
                    
                    elif year1Confirmed and year2Confirmed:
                        generateGraph(graphYear1, graphYear2)
                        graphYear1 = ""
                        graphYear2 = ""
                        year1Confirmed = False
                        year2Confirmed = False
                        screenNumber = 0

                elif event.key == pygame.K_ESCAPE:
                    year1Confirmed = False
                    year2Confirmed = False
                    graphYear1 = ""
                    graphYear2 = ""
                    screenNumber = 0
                
                elif event.key == pygame.K_UP:
                    if year1Confirmed and not year2Confirmed:
                        year1Confirmed = False
                        graphYear1 = ""
                        graphYear2 = ""
                    elif year1Confirmed and year2Confirmed:
                        year2Confirmed = False
                        graphYear2 = ""


        # Draws the surface object to the screen.
        drawInputScreen()

        if screenNumber == 0:
            pygame.draw.rect(display_surface, blue, input_docketNumber)

            dailySalesInput = base_font.render("Daily Sales Input", True, white)
            monthlySales = base_font.render("View Monthly Sales", True, white)
            viewGraphs = base_font.render("View Graphs", True, white)
            sendToHeadOffice = base_font.render("Send to Head Office", True, white)
            createInvoice = base_font.render("Create Invoice", True, white)

            display_surface.blit(dailySalesInput, (300, 150 + 30*0))
            display_surface.blit(monthlySales, (300, 150 + 30*1))
            display_surface.blit(viewGraphs, (300, 150 + 30*2))
            display_surface.blit(sendToHeadOffice, (300, 150 + 30*3))
            display_surface.blit(createInvoice, (300, 150 + 30*4))
        
        if screenNumber == 1:
            pygame.draw.rect(display_surface, black, input_docketNumber)

            text_surface = []

            for i in range(9):
                text_surface.append(base_font.render(txt[i], True, (255, 255, 255)))
        
                # render at position stated in arguments
                display_surface.blit(text_surface[i], (450, 90 + 50*i))

        #cursor.topleft = display_surface[fieldNum].topright
        #pygame.draw.rect(display_surface, (255, 255, 255), cursor)
        # draw text box at fieldNum position
        #input_docketNumber = pygame.Rect(450, 80 + 50*fieldNum, 140, 32)
        
        # set width of textfield so that text cannot get
        # outside of user's text input
        #input_docketNumber.w = max(100, text_surface.get_width()+10)
        
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()
        
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)
        pygame.display.update()
    
        