import pygame
import time
import random
#create initial configurations

pygame.init()
crash_sound = pygame.mixer.Sound("crash.wav")
pygame.mixer.music.load("music_play.wav")
pygame.mixer.music.play(-1)


#screen height and width
width = 800
height = 600

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_green = (0,255,0)
bright_red = (255,0,0)
block_color = (53,115,255)

car_width = 73

#Create canvas and title
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("A bit racing","Race")
#create FPS
clock = pygame.time.Clock()

pause = False
carImage = pygame.image.load("racecar.png")
gameicon = pygame.image.load("carIcon.png")

pygame.display.set_icon(gameicon)

#display the blocks dodged
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged : "+str(count),True, black)
    gameDisplay.blit(text,(0,0))

#display the car on the screen
def car(x, y):
    gameDisplay.blit(carImage,(x,y))

def crash():

    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    pauseText = pygame.font.SysFont('comicsansms', 115)
    textSurf, textRect = text_objects("You Crashed!", pauseText)
    textRect.center = ((width / 2), (height / 2))

    gameDisplay.fill(white)

    gameDisplay.blit(textSurf, textRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Play Again!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def text_objects(text, font):
    TextSurface = font.render(text, True, black)
    return TextSurface, TextSurface.get_rect()


def things(thing_x, thing_y,thing_width, thing_height,color):
    pygame.draw.rect(gameDisplay,block_color,[thing_x,thing_y, thing_width,thing_height])


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)


def unpaused():
    pygame.mixer.music.unpause()
    global pause
    pause = False


def paused():
    pygame.mixer.music.pause()

    pauseText = pygame.font.SysFont('comicsansms',115)
    textSurf, textRect = text_objects("Paused",pauseText)
    textRect.center = ((width/2), (height/2))

    gameDisplay.fill(white)

    gameDisplay.blit(textSurf, textRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Continue",150,450,100,50,green,bright_green,unpaused)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)



def quitgame():
    pygame.quit()
    quit()


def game_intro():

    intro = True
    while intro:
        for event in pygame.event.get():
            #ssprint event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont('comicsansms', 115)
        TextSurf, TextRect = text_objects("A bit racing", largeText)
        TextRect.center = (width/2, height/2)
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(15)


def game_loop():
    x = width * 0.45
    y = height * 0.8

    x_change =  0

    dodged = 0

    thing_start_x = random.randrange(0,width)
    thing_start_y = -600

    thing_speed = 7

    thing_width = 100
    thing_height = 100

    gameExit = False
    global pause

    while not gameExit:
        for event in pygame.event.get():
            #print (event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

                #Car Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_p:
                    pause = True
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    x_change = 0

        x += x_change

        #fill background with white color and display the car, dodged score
        gameDisplay.fill(white)
        things(thing_start_x,thing_start_y,thing_width,thing_height,block_color)
        thing_start_y += thing_speed
        car(x,y)
        things_dodged(dodged)

        #hadeling the screen borders
        if x > width - car_width or x < 0:
            crash()

        #Controls block appearance on the screen
        if thing_start_y > height:
            thing_start_y = 0 - thing_height
            thing_start_x = random.randrange(0,width)
            dodged += 1
            thing_speed += 1
            #thing_width += (dodged * 0.2)

        #handels collision
        if y < thing_start_y + thing_height:
            #print ('y crossover')
            if x > thing_start_x  and x < thing_start_x + thing_width or x + car_width > thing_start_x and x + car_width < thing_start_x + thing_width:
                #lprint ('x crossover')
                crash()

        #updates the complete screen
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()