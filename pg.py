# import pygame module in this program
import pygame
import sys
from datetime import date
import time
 
# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

dt = date.today()
print(dt)

fieldNum = 0
txt = ["", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00", "    0.00"]

clock = pygame.time.Clock()

color_passive = pygame.Color('chartreuse4')
color = color_passive
# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
 
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

base_font = font1
#txt[fieldNum] = ''
 
def drawInputScreen():
    # create a text surface object,
    # on which text is drawn on it.
    text = font2.render('FRANCHISE TURNOVER REPORT', True, white, blue)
    txtDocketNumber = font1.render('     DATE (DDMMYYYY):', True, white, blue)
    txtShoes = font1.render('SHOES/BAGS/SUITCASES:', True, white, blue)
    txtKeys = font1.render('          KEYS/LOCKS:', True, white, blue)
    txtProducts = font1.render('            PRODUCTS:', True, white, blue)
    txtEngraving = font1.render('    ENGRAVING/STAMPS:', True, white, blue)
    txtSigns = font1.render(' SIGNS/NUMBER PLATES:', True, white, blue)
    txtDryCleaning = font1.render('        DRY CLEANING:', True, white, blue)
    txtCallOuts = font1.render('           CALL-OUTS:', True, white, blue)
    txtOther = font1.render('               OTHER:', True, white, blue)
    
    # create a rectangular object for the
    # text surface object
    global input_docketNumber, textRect, cursor
    input_docketNumber = pygame.Rect(450, 80 + 50*fieldNum, 100, 32)
    textRect = text.get_rect()
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
    
    # set the center of the rectangular object.
    textRect.center = (X // 2, 20)
    lblDocketNumber.center = (300, 100)
    lblShoes.center = (300, 150)
    lblKeys.center = (300, 200)
    lblProducts.center = (300, 250)
    lblEngraving.center = (300, 300)
    lblSigns.center = (300, 350)
    lblDryCleaning.center = (300, 400)
    lblCallOuts.center = (300, 450)
    lblOther.center = (300, 500)
    
    # completely fill the surface object
    # with white color
    display_surface.fill(blue)
 
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    display_surface.blit(text, textRect)
    display_surface.blit(txtDocketNumber, lblDocketNumber)
    display_surface.blit(txtShoes, lblShoes)
    display_surface.blit(txtKeys, lblKeys)
    display_surface.blit(txtProducts, lblProducts)
    display_surface.blit(txtEngraving, lblEngraving)
    display_surface.blit(txtSigns, lblSigns)
    display_surface.blit(txtDryCleaning, lblDryCleaning)
    display_surface.blit(txtCallOuts, lblCallOuts)
    display_surface.blit(txtOther, lblOther)

drawInputScreen()
 
# infinite loop
while True:   
    global textRect, input_docketNumber, cursor

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
  
            # Check for backspace
            if event.key == pygame.K_BACKSPACE:
  
                # get text input from 0 to -1 i.e. end.
                txt[fieldNum] = txt[fieldNum][:-1]
                 
            # Check for ARROW_DOWN OR ENTER
            elif event.key == pygame.K_DOWN or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:

                if fieldNum > 0:
                    if txt[fieldNum] == "":
                        txt[fieldNum] = "0"
                
                    txt[fieldNum] = txt[fieldNum].strip()
                    txt[fieldNum] = format(float(txt[fieldNum]), ".2f")
                    txt[fieldNum] = txt[fieldNum].rjust(8)   
                
                if fieldNum + 1 < 9:
                    fieldNum += 1
                    txt[fieldNum] = txt[fieldNum].strip()

            # Check for ARROW_UP
            elif event.key == pygame.K_UP:
                '''
                while len(txt[fieldNum]) < 8:
                    txt[fieldNum] = " " + txt[fieldNum]
                '''
                if fieldNum > 0:
                    if txt[fieldNum] == "":
                        txt[fieldNum] = "0"

                    txt[fieldNum] = txt[fieldNum].strip()
                    txt[fieldNum] = format(float(txt[fieldNum]), ".2f")
                    txt[fieldNum] = txt[fieldNum].rjust(8)
                
                if fieldNum - 1 > -1:
                    fieldNum -= 1
                    txt[fieldNum] = txt[fieldNum].strip()
        

              
            # Unicode standard is used for string
            # formation
            else: 
                if len(txt[fieldNum]) < 8:
                    txt[fieldNum] += event.unicode  

        # Draws the surface object to the screen.
        drawInputScreen()
        pygame.draw.rect(display_surface, black, input_docketNumber)

        text_surface = []

        for i in range(9):
            text_surface.append(base_font.render(txt[i], True, (255, 255, 255)))
        
            # render at position stated in arguments
            display_surface.blit(text_surface[i], (450, 90 + 50*i))

        cursor.topleft = display_surface[fieldNum].topright
        pygame.draw.rect(display_surface, (255, 255, 255), cursor)
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
    
        