import pygame
import random
import math
import os
import time
import sys
"""
ball coordinates : 
    width : 32
    height : 32

pad coordinates :
    width : 10
    height : 64
"""
"""
dim stored as width, height in that order
"""
running = True
screen_size = (810,560)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("PONG !!!!")

clock = pygame.time.Clock()

ball_cod = [screen_size[0]/2,random.randint(20,300)]
ball_dim = [10,10]

pad1_cod = [0,screen_size[1]/2 -  50]
pad2_cod = [screen_size[0]-10,screen_size[1]/2 - 50]

touch_cod = [0,0]
    
x_comp = 5
y_comp = 3
ai_hit = False
start = False

ball_color = [204,204,204]
color = color2= [255,0,0]

player1_score = player2_score = _rally = 0

top = random.randint(0,20)
bottom = random.randint(25,64)

pygame.font.init()
pygame.mixer.init()

game_font = pygame.font.SysFont('Times New Roman',50)
title_font = pygame.font.Font(os.path.dirname(os.path.abspath(__file__))+"/res/ka1.ttf",40)

loose_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__))+"/res/sounds/lose.wav")
hit_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__))+"/res/sounds/hit.wav")
#wallHit_sound = pygame.mixer.Sound(os.path.dirname(os.path.abspath(__file__))+"\\res\\sounds\\wall_hit.wav")


play_with_ai = False
running = False
### start screen +++++
title = title_font.render("PONG",False,[255,255,0])
start_message = title_font.render("hit a for ai", False, [255, 0, 255])

 
dis_winner = None

prev_time = time.time()
sw = True
winner = None
while True:
    while not running:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                pygame.quit()
        screen.fill((0,0,0))
        if time.time() - prev_time >= 0.50:
            prev_time = time.time()
            if sw == True:
                title = title_font.render("PONG", False, [255, 255, 0])
                #start_message = title_font.render("hit a to begin", False, [255, 0, 255])
                start_message = title_font.render("hit a for ai", False, [255, 0, 255])
                sw = False
            elif sw == False:
                title = title_font.render("PONG", False, [255, 0, 255])
                #start_message = title_font.render("hit a to begin", False, [255, 255, 0])
                start_message = title_font.render("hit a for ai", False, [255, 255, 0])
                sw = True
        screen.blit(title, (300,200))
        screen.blit(start_message, (225,300))
        
        pygame.display.update()
        if pygame.key.get_pressed()[pygame.K_a]:
            running = True
            play_with_ai = True
            start = True
             
    while running:
        clock.tick(60) #### this function is to set
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                pygame.quit()
        screen.fill((0,0,0))
        ####===== DRAWING ON THE SCREEN ========
        ###  ball
        pygame.draw.rect(screen,ball_color,pygame.Rect(ball_cod[0],ball_cod[1], ball_dim[0],ball_dim[1]))
        ###
        # pads
        pygame.draw.rect(screen,(0,255,0),pygame.Rect(pad1_cod[0], pad1_cod[1],10,64))
        pygame.draw.rect(screen,(0,255,0),pygame.Rect(pad2_cod[0], pad2_cod[1],10,64))

        # stats
        score = game_font.render(str(player1_score),False,(204,204,204))
        score2 = game_font.render(str(player2_score),False,(204,204,204))
        rally = game_font.render("Rally : " + str(_rally),False,(61, 61, 61))
        if x_comp > 0:
            speed = game_font.render("Speed : " + str(int(math.fabs(x_comp - 5))),False,(61, 61, 61))
        else:
            speed = game_font.render("Speed : " + str(int(math.fabs(x_comp + 5))),False,(61, 61, 61))

        screen.blit(score, (300, 10))
        screen.blit(score2,(480,10))
        screen.blit(rally,(100,500))
        screen.blit(speed,(480,500))
        #### half-line
        for i in range(12):
            pygame.draw.rect(screen,(173, 216, 230),pygame.Rect(screen_size[0]/2,i*50,12,25))
        ####=======================================


        if pygame.key.get_pressed()[pygame.K_a] or start == True:
            start = True
            #play_with_ai = True
            ball_cod[0] += x_comp
            ball_cod[1] += y_comp
            keys = pygame.key.get_pressed()
            ###=== CHECK IF BALL IS COLLIDING AGAINST THE WALL
            if ball_cod[1]+ball_dim[1]>= screen_size[1] or ball_cod[1] <= 0:
                y_comp = -y_comp
                #pygame.mixer.Sound.play(wallHit_sound)

            if (ball_cod[1]+ ball_dim[1]>= pad1_cod[1] and
                ball_cod[1] <= pad1_cod[1] + 64 and
                ball_cod[0] < pad1_cod[0] + 10 ):
                ai_hit = False


            if (ball_cod[0] + ball_dim[0] >= pad2_cod[0] and
                ball_cod[1] + ball_dim[1] >= pad2_cod[1] and
                ball_cod[1] <= pad2_cod[1]+64):
                ai_hit = True

            ###=== IF ANY PLAYER DIED===============
            if ball_cod[0] <= 0 or ball_cod[0]+ball_dim[0] >= screen_size[0]:
                pygame.mixer.Sound.play(loose_sound)
                if ball_cod[0] <= 0:
                    player2_score += 1
                elif ball_cod[0]+ball_dim[0] >= screen_size[0]:
                    player1_score += 1
                pad1_cod = [0,screen_size[1]/2 - 50]
                pad2_cod = [screen_size[0]-10,screen_size[1]/2 - 50]
                ball_cod = [screen_size[0]/2,random.randint(20,300)]
                ball_dim = [10,10]
                start = False
                x_comp = 5
                y_comp = 3
                ai_hit = False
                color = color2= [255,0,0]
                _rally = 0



            #####======= COLLISION DETECTION================
            if (ball_cod[1]+ ball_dim[1]>= pad1_cod[1] and
                ball_cod[1] <= pad1_cod[1]+64 and
                ball_cod[0] < pad1_cod[0] + 10)\
                 or \
                (ball_cod[0] + ball_dim[0] >= pad2_cod[0] and
                ball_cod[1]+ ball_dim[1]>= pad2_cod[1] and
                ball_cod[1] <= pad2_cod[1]+64) and ball_cod[0] >= pad1_cod[0]:
                x_comp = -x_comp
                touch_cod = [ball_cod[0], ball_cod[1]]
                _rally += 1
                pygame.mixer.Sound.play(hit_sound)

                ###===== INCREASE BALL_SPEED
                if _rally % 5 == 0 and _rally != 0:
                    if x_comp > 0:
                        x_comp += 1
                    else:
                        x_comp -= 1

                ###==== IF BALL IS COLLIDING WITH THE UPPER PART OF THE PAD (PLAYER_PAD)===========###
                if ball_cod[1] + ball_dim[1] >= pad1_cod[1] and ball_cod[1]  <= pad1_cod[1] + 23 and random.randint(0,1) == 1:
                    if y_comp > 0:
                        y_comp = 5
                    else:
                        y_comp = -5

                ###==== IF BALL IS COLLIDING WITH THE LOWER PART OF THE PAD (PLAYER_PAD)
                elif ball_cod[1] + ball_dim[1] >= pad1_cod[1] + 40 and ball_cod[1] <= pad1_cod[1] + 64 and random.randint(0,1) == 1:
                    color2 = [0,0,255]
                    if y_comp > 0:
                        y_comp = 5
                    else:
                        y_comp = -5
                    ball_color = [random.randint(100,255),\
                        random.randint(100,255),\
                        random.randint(100,255),]

                ####==== IF BALL COLLIDING AT ANY OTHER PART OF THE CENTRE (PLAYER_PAD)
                else:
                    if y_comp > 0:
                        y_comp = 3
                    else:
                        y_comp = -3

                ### SETTING TOP AND BOTTOM VARIABLES FOR THE AI TO HIT
                if (ball_cod[0] + ball_dim[0] >= pad2_cod[0] and
                ball_cod[1]+ ball_dim[1]>= pad2_cod[1] and
                ball_cod[1] <= pad2_cod[1]+64):
                    top = random.randint(0,20)
                    bottom = random.randint(25,64)
                ###== TOP AND BOTTOM VARIABLES JUST RANDOMIZES AT WHICH PART THE AI HAS TO HIT THE BALL
                ### NOT REALLY NECESSARY BUT IT MAKES THE AI LOOK MORE NATURAL (LIKE AS IF A REAL HUMAN IS PLAYING)

                if ((keys[pygame.K_w] or keys[pygame.K_UP])  and y_comp > 0) or\
                    ((keys[pygame.K_s] or keys[pygame.K_DOWN]) and y_comp < 0):
                        y_comp = -y_comp

            ###=== CODE THAT CONTROLS THE AI PLAYER
            if not(ball_cod[1] + ball_dim[1] >= pad2_cod[1] + top and ball_cod[1] <= pad2_cod[1] + bottom) and\
                ai_hit == False and ball_cod[0] >= screen_size[0]/(random.randint(2,3)) and play_with_ai == True:
                if ball_cod[1]+ball_dim[1] <= pad2_cod[1] + top:
                    pad2_cod[1] -= 10
                if ball_cod[1] > pad2_cod[1] + bottom:
                    pad2_cod[1] += 10
            ###======================================

            ###==== KEYBOARD INPUT ==========
            if keys[pygame.K_w]:
                pad1_cod[1] -= 8
                touch_cod[1] -= 8
            if keys[pygame.K_s]:
                pad1_cod[1] += 8
                touch_cod[1] += 8
            if pad1_cod[1] + 64 >= screen_size[1]:
                pad1_cod[1] = screen_size[1] - 64
            elif pad1_cod[1] <= 0:
                pad1_cod[1] = 0
            ###================

            ####==== check if any player has won======
            if player1_score == 5 or player2_score == 5:
                running = False
                if player1_score == 5:
                    winner = 'p1'
                elif player2_score == 5:
                    winner = 'p2'

        pygame.display.update()
    
    if winner == 'p1':
        dis_winner = title_font.render("player1 has won",False,[0,204,204])
    elif winner == 'p2':
        dis_winner = title_font.render("player2 has won",False, [51,255,255])
    #replay_note = title_font.render("hit q to start again",False, [153,255,255])
    end_note = title_font.render("hit e to end", False, [102,178,255])
    
    #### DEATH_SCREEN #############################
    while not running:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
                pygame.quit()
        screen.fill((0, 0, 0))
        #### insert your code here
        screen.blit(dis_winner,(170, 120))
        #screen.blit(replay_note,(140, 220))
        screen.blit(end_note,(220,320))
        #if pygame.key.get_pressed()[pygame.K_q]:
        #    break
        if pygame.key.get_pressed() [pygame.K_e]:
           pygame.quit()
           sys.exit()
        #######
        pygame.display.update()

