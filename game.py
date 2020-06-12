import pygame
import random
import math
from pygame import mixer


#Initialize pygame
pygame.init()


#Create the screen,we can give size as we want in ()
screen = pygame.display.set_mode((800,600))

#Change the title and icon of the output window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

playerImg =  pygame.image.load('battleship.png')
playerX= 370
playerY=480
playerX_change =0   #to change the position of ship


enemyImg =[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemy=6


#enemy
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,200))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

#bullet
#Ready - bullet can't be seen
#fire - we can see the bullet moving
bulletImg =  pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change =0
bulletY_change =2
bullet_state="ready"

score_value=0
font = pygame.font.Font('freesansbold.ttf',32)

textX=10
textY=10

over_font = pygame.font.Font('freesansbold.ttf',64)

mixer.music.load('background.wav')
mixer.music.play(-1)

def show_score(x,y):
    score = font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))
    

#background = pygame.image.load('space.jpg')


def player(x,y):
    screen.blit(playerImg,(x,y))    #blit is used to draw an image on the screen
                #image      #x&y co-ordinates
#Game loop = Which will run program continuously until we press close button
#pygame.event.get()= used to get any event in the program

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    d = math.sqrt((math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2)))

    if d<27:
        return True


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #QUIT means when we close the program
            running = False

        #If key is pressed on keyboard, check if its right or left

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5

            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            
            if event.key== pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    bulletX=playerX
                    bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            playerX_change = 0

        

    screen.fill((50,100,190))
    #screen.blit(background,(0,0))
    
    playerX += playerX_change
    
    #this if elif decides the boundry of the ship, 0<boundry<736
    if playerX<0:
        playerX=0
    elif playerX>736:
        playerX=736

    for i in range(num_of_enemy):
        if enemyY[i]>420:
            for j in range(num_of_enemy):
                enemyY[j]=2000

            game_over_text()
            break

        enemyX[i]+=enemyX_change[i]

        if enemyX[i]<0:
            enemyX_change[i]=0.2
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>736:
            enemyX_change[i]=-0.2
            enemyY[i]+=enemyY_change[i]

        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY=480
            bullet_state="ready"
            score_value+=1   
            enemyX[i]= random.randint(0,736)
            enemyY[i]=random.randint(50,200)

        enemy(enemyX[i],enemyY[i],i)


    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        bullet(bulletX,bulletY)
        bulletY-=bulletY_change    

    
    
    player(playerX,playerY)    #we called this fun here because we want to run it all the time while game is on
    show_score(textX,textY)
    
    pygame.display.update()