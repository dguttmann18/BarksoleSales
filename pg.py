# import pygame module in this program
import pygame
import sys
 
# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

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
user_text = ''
 
# create a text surface object,
# on which text is drawn on it.
text = font2.render('FRANCHISE TURNOVER REPORT', True, white, blue)
txtDocketNumber = font1.render('       DOCKET NUMBER:', True, white, blue)
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
input_rect = pygame.Rect(450, 80, 140, 32)
textRect = text.get_rect()
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
 
# infinite loop
while True:
 
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
                user_text = user_text[:-1]

            # Check for ENTER
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                print(user_text) 
  
            # Unicode standard is used for string
            # formation
            else:
                user_text += event.unicode
                      
    
        # Draws the surface object to the screen.

        pygame.draw.rect(display_surface, black, input_rect)
  
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        
        # render at position stated in arguments
        display_surface.blit(text_surface, (450, 90))
        
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)
        
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()
        
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)
        pygame.display.update()