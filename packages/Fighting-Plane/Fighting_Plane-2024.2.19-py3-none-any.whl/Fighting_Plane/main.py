import pygame
import sys
import traceback
import myplane as mymyplne
import bullet as mybullet
import enemy as myenemy
import supply as mysupply
from pygame.locals import *
from random import *


pygame.init()
pygame.mixer.init()


bg_size=width,height=480,700
screen=pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")


background=pygame.image.load("images/background.png").convert()


BLACK=(0,0,0)
GREEN=(0,255,0)
WHITE=(255,255,255)
RED=(255,0,0)
YELLOW=(255,255,0)


pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound=pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound=pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound=pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound=pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound=pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound=pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound=pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound=pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound=pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound=pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound=pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)


def main():
    pygame.mixer.music.play(-1) 


    me=mymyplne.MyPlane(bg_size)
    mes=pygame.sprite.Group()
    mes.add(me)


    clock=pygame.time.Clock()
    enemi=pygame.sprite.Group()


   


    def add_small(a,b,num):
        for i in range(num):
            e1=myenemy.SmallEnemy(bg_size)
            a.add(e1)
            b.add(e1)
    def add_mid(a,b,num):
        for i in range(num):
            e2=myenemy.MidEnemy(bg_size)
            a.add(e2)
            b.add(e2)
    def add_big(a,b,num):
        for i in range(num):
            e3=myenemy.BigEnemy(bg_size)
            a.add(e3)
            b.add(e3)
    def add_speed(feji,add):
        for i in feji:
            i.speed+=add


    small=pygame.sprite.Group()
    add_small(small,enemi,15)


    mid=pygame.sprite.Group()
    add_mid(mid,enemi,4)


    big=pygame.sprite.Group()
    add_big(big,enemi,2)


    bullet1=[]
    bu1_i=0
    BU1_N=4
    for i in range(BU1_N):
        bullet1.append(mybullet.Bullet1(me.rect.midtop))


    bullet2=[]
    bu2_i=0
    BU2_N=8
    for i in range(BU2_N):
        bullet2.append(mybullet.Bullet2((me.rect.centerx-33,me.rect.centery)))
        bullet2.append(mybullet.Bullet2((me.rect.centerx+30,me.rect.centery)))
        
    eb=[]
    eb_i=0
    EB_N=10
    for i in range(EB_N):
        ey = list(choice([small, mid, big]))
        eb.append(mybullet.Enemy_Bullet(ey[randint(0,len(ey)-1)].rect.midbottom))
    
        
    e1_i=0
    e2_i=0
    e3_i=0
    me_i=0


    bomb_image=pygame.image.load("images\\bomb.png").convert_alpha()
    bomb_rect=bomb_image.get_rect()
    bomb_font=pygame.font.Font("font\\font.ttf",48)
    bomb_num=3

    bomb_supply=mysupply.Bomb_Supply(bg_size)
    bullet_supply=mysupply.Bullet_Supply(bg_size)
    SUPPLY=USEREVENT
    pygame.time.set_timer(SUPPLY,20000)


    SBULLET=USEREVENT+1
    shiyong=False
    

    runn=True


    qie=True
    delay=100

    score=0
    font=pygame.font.Font("font\\font.TTF",36)


    level=1


   


    reco=False
    ga_font=pygame.font.Font("font\\font.TTF",48)
    ag_image=pygame.image.load("images\\again.png").convert_alpha()
    ag_rect=ag_image.get_rect()
    ga_image=pygame.image.load("images\\gameover.png").convert_alpha()
    ga_rect=ga_image.get_rect()


    paused=False
    pause_nor=pygame.image.load("images\pause_nor.png").convert_alpha()
    pause_pressed=pygame.image.load("images\pause_pressed.png").convert_alpha()
    resume_nor=pygame.image.load("images\\resume_nor.png").convert_alpha()
    resume_pressed=pygame.image.load("images\\resume_pressed.png").convert_alpha()
    paused_rect=pause_nor.get_rect()
    paused_rect.left,paused_rect.top=width-paused_rect.width-10,10
    paused_image=pause_nor
    

    life_image=pygame.image.load("images\life.png").convert_alpha()
    life_rect=life_image.get_rect()
    life_num=10


    xing=1

    

    while runn:
        for event in pygame.event.get():
            if event.type==QUIT:
                print("score : ",score)
                pygame.quit()
                sys.exit()


            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1 and paused_rect.collidepoint(event.pos):
                    paused=not paused
                    if paused:
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                        pygame.time.set_timer(SUPPLY,0)
                    else:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        pygame.time.set_timer(SUPPLY,30000)

            elif event.type==MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        if life_num:
                            paused_image=resume_pressed
                        else:
                            paused_image=pause_pressed
                    else:
                        paused_image=pause_pressed
                else:
                    if paused:
                        if life_num:
                            paused_image=resume_nor
                        else:
                            paused_image=pause_nor
                    else:
                        paused_image=pause_nor


            elif event.type==KEYDOWN:
                if event.key==K_SPACE:
                    if bomb_num:
                        bomb_num-=1
                        for each in enemi:
                            if each.rect.bottom>0:
                                each.active=False


            elif event.type==SUPPLY:
                supply_sound.play()
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()


            elif event.type==SBULLET:
                shiyong=False
                pygame.time.set_timer(SBULLET,0)

        screen.blit(background,(0,0))


        screen.blit(paused_image,paused_rect)
                                

        if (not paused):    
            key_p=pygame.key.get_pressed()
            if key_p[K_w] or key_p[K_UP]:
                me.moveUp()
            if key_p[K_s] or key_p[K_DOWN]:
                me.moveDown()
            if key_p[K_a] or key_p[K_LEFT]:
                me.moveLeft()
            if key_p[K_d] or key_p[K_RIGHT]:
                me.moveRight()


            if not(delay%10):
                if shiyong:
                    bullets=bullet2
                    bullets[bu2_i].reset((me.rect.centerx-33,me.rect.centery))
                    bullets[bu2_i+1].reset((me.rect.centerx+30,me.rect.centery))
                    bu2_i=(bu2_i+2)%BU2_N
                else:
                    bullets=bullet1
                    bullets[bu1_i].reset(me.rect.midtop)
                    bu1_i=(bu1_i+1)%BU1_N
                ey = list(choice([small, mid, big]))
                eb[bu1_i].reset(ey[randint(0,len(ey)-1)].rect.midbottom)
                eb_i=(eb_i+1)%EB_N
                bullet_sound.play()


            for b in bullets:
                if b.active:
                    screen.blit(b.image, b.rect)
                    b.move()
                    enemy_hit=pygame.sprite.spritecollide(\
                        b,enemi,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active=False
                        for e in enemy_hit:
                            if e in mid or e in big:
                                e.hit=True
                                e.energy-=1 
                                if e.energy==0:
                                    e.active=False
                                    if e in mid:
                                        if level<6:
                                            score+=6000
                                    else:
                                        if level<6:
                                            score+=10000
                            else:
                                e.active=False
                                if level<6:
                                    score+=1000

            for b in eb:
                if b.active:
                    screen.blit(b.image, b.rect)
                    b.move()
            for each in big:
                if each.active:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit=False
                    else:
                        if qie:
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2,each.rect)


                    pygame.draw.line(screen,BLACK,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.right,each.rect.top-5),\
                                     2)
                    energy_r=each.energy/myenemy.BigEnemy.energy
                    if energy_r>0.2:
                        energy_c=GREEN
                    else:
                        energy_c=RED
                    pygame.draw.line(screen,energy_c,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.left+each.rect.width*energy_r,each.rect.top-5),\
                                     2)

                
                    if each.rect.bottom==-50:
                        enemy3_fly_sound.play()
        
                else:
                    if not(delay%3):
                        if e3_i==0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_i],each.rect)
                        e3_i=(e3_i+1)%6
                        if not(bool(e3_i)):
                            me_down_sound.stop()
                            each.reset()
                    
                
            for each in mid:
                if each.active:
                    if each.hit==False:
                        screen.blit(each.image_hit,each.rect)
                        hit=False
                    else:
                        screen.blit(each.image,each.rect)
                        each.move()


                    pygame.draw.line(screen,BLACK,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.right,each.rect.top-5),\
                                     2)
                    en_r=each.energy/myenemy.MidEnemy.energy
                    if en_r>0.2:
                        en_c=GREEN
                    else:
                        en_c=RED
                    pygame.draw.line(screen,en_c,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.left+each.rect.width*en_r,\
                                      each.rect.top-5),2)
                                 
                    
                else:
                    if not(delay%3):
                        if e2_i==0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_i],each.rect)
                        e2_i=(e2_i+1)%4
                        if e2_i==0:
                            each.reset()
            
            for each in small:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                else:
                    if not(delay%3):
                        if e1_i==0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_i],each.rect)
                        e1_i=(e1_i+1)%4
                        if e1_i==0:
                            each.reset()



            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if bomb_num<3:
                        bomb_num+=1
                    bomb_supply.active=False


            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    pygame.time.set_timer(SBULLET,18000)
                    shiyong=True
                    bullet_supply.active=False
        else:
            for b in bullets:
                if b.active:
                    screen.blit(b.image, b.rect)
                    enemy_hit=pygame.sprite.spritecollide(\
                        b,enemi,False,pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active=False
                        for e in enemy_hit:
                            if e in mid or e in big:
                                e.hit=True
                                e.energy-=1 
                                if e.energy==0:
                                    e.active=False
                                    if e in mid:
                                        if level<6:
                                            score+=6000
                                    else:
                                        if level<6:
                                            score+=10000
                            else:
                                e.active=False
                                if level<6:
                                    score+=1000
            for each in big:
                if each.active:
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit=False
                    else:
                        if qie:
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2,each.rect)


                    pygame.draw.line(screen,BLACK,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.right,each.rect.top-5),\
                                     2)
                    energy_r=each.energy/myenemy.BigEnemy.energy
                    if energy_r>0.2:
                        energy_c=GREEN
                    else:
                        energy_c=RED
                    pygame.draw.line(screen,energy_c,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.left+each.rect.width*energy_r,each.rect.top-5),\
                                     2)
            for each in mid:
                if each.active:
                    if each.hit==False:
                        screen.blit(each.image_hit,each.rect)
                        hit=False
                    else:
                        screen.blit(each.image,each.rect)


                    pygame.draw.line(screen,BLACK,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.right,each.rect.top-5),\
                                     2)
                    en_r=each.energy/myenemy.MidEnemy.energy
                    if en_r>0.2:
                        en_c=GREEN
                    else:
                        en_c=RED
                    pygame.draw.line(screen,en_c,\
                                     (each.rect.left,each.rect.top-5),\
                                     (each.rect.left+each.rect.width*en_r,\
                                      each.rect.top-5),2)
                                 
                    
                else:
                    if not(delay%3):
                        if e2_i==0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_i],each.rect)
                        e2_i=(e2_i+1)%4
                        if e2_i==0:
                            each.reset()
            for each in small:
                if each.active:
                    screen.blit(each.image,each.rect)
                else:
                    if not(delay%3):
                        if e1_i==0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_i],each.rect)
                        e1_i=(e1_i+1)%4
                        if e1_i==0:
                            each.reset()
            if bomb_supply.active:
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if bomb_num<3:
                        bomb_num+=1
                    bomb_supply.active=False


            if bullet_supply.active:
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    pygame.time.set_timer(SBULLET,18000)
                    bullet_supply.active=False 
            


        if level==1 and score>50000:
            upgrade_sound.play()
            level=2
            life_num+=1
            add_speed(small,1)
            add_small(small,enemi,3)
            add_mid(mid,enemi,2)
            add_big(big,enemi,1)
        elif level==2 and score>300000:
            upgrade_sound.play()
            level=3
            life_num+=2
            add_speed(small,1)
            add_speed(mid,1)
            add_small(small,enemi,5)
            add_mid(mid,enemi,3)
            add_big(big,enemi,2)
        elif level==3 and score>600000:
            upgrade_sound.play()
            level=4
            life_num+=3
            add_speed(small,1)
            add_speed(mid,1)
            add_small(small,enemi,5)
            add_mid(mid,enemi,3)
            add_big(big,enemi,2)
        elif level==4 and score>1000000:
            upgrade_sound.play()
            level=5
            life+=4
            add_speed(small,1)
            add_speed(mid,1)
            add_small(small,enemi,5)
            add_mid(mid,enemi,3)
            add_big(big,enemi,2)
        elif level==5 and score>2000000:
            upgrade_sound.play()
            level=6
            life_num+=5
            add_speed(small,5)
            add_speed(mid,3)
            add_speed(big,2)
        

   
        score_t=font.render("Score : %s"%str(score),True,WHITE)
        screen.blit(score_t,(10,5))
        bomb_t=bomb_font.render('x %s'%str(bomb_num),True,WHITE)
        text_rect=bomb_t.get_rect()
        life_t=font.render('x %s'%str(life_num),True,WHITE)
        life_text_rect=life_t.get_rect()
        screen.blit(bomb_image,(10,height-10-bomb_rect.height))
        screen.blit(bomb_t,(20+bomb_rect.width,height-5-text_rect.height))
        screen.blit(life_image,(width-10,width-(height-10-life_rect.height)))
        screen.blit(life_t,(width-(20+life_rect.width),width-(height+5+life_text_rect.height)))
        enemie=pygame.sprite.spritecollide(me,enemi,False,pygame.sprite.collide_mask)
        if enemie:
            me.active=False
            for e in enemie:
                e.active=False
        ebsss=pygame.sprite.spritecollide(me,eb,False,pygame.sprite.collide_mask)
        if ebsss:
            me.active=False
            for b in eb:
                b.active=False
        if me.active:
            if qie:
                screen.blit(me.image1,me.rect)
            else:
                screen.blit(me.image2,me.rect)


            pygame.draw.line(screen,BLACK,\
                             (me.rect.left,me.rect.top-5),\
                             (me.rect.right,me.rect.top-5),\
                             2)
            if life_num>5:
                en_c=GREEN
            elif life_num>3:
                en_c=YELLOW
            else:
                en_c=RED
            if life_num>=10:
                life_num=10
            else:
                life_num=life_num
            pygame.draw.line(screen,en_c,\
                             (me.rect.left,me.rect.top-5),\
                             (me.rect.left+me.rect.width*(life_num/10),\
                              me.rect.top-5),2)

            
                
        else:
            if not(delay%3):
                if me_i==0:
                    me_down_sound.play()
                screen.blit(me.destroy_images[me_i],me.rect)
                me_i=(me_i+1)%4
                if me_i==0:
                    if life_num:
                        life_num-=1
                        me.reset()
                    else:
                        pygame.mixer.music.stop()
    

                        pygame.mixer.stop()



                        pygame.time.set_timer(SUPPLY,0)
                        if not reco:
                            reco=True
                            with open('record.txt','r') as f:
                                reco_i=int(f.read())
    
    
    
                            if score>reco_i:
                                with open('record.txt','w') as f:
                                    f.write(str(score))
                        i=0
                                    
                        while True:
                            for event in pygame.event.get():
                                if event.type==QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type==MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    if ag_rect.left < pos[0] < ag_rect.right and ag_rect.top < pos[1] < ag_rect.bottom:
                                        main()
                                        exit()
                                    elif ga_rect.left < pos[0] < ga_rect.right and ga_rect.top < pos[1] < ga_rect.bottom:
                                        pygame.quit()
                                        sys.exit()
                            screen.blit(background,(0,0))
    
                            reco_score=font.render('Best : %s'%str(reco_i),True,(255,255,255))
                            screen.blit(reco_score,(50,50))
    
    
                            max_score=font.render('Your Score : %s'%str(score),True,(255,255,255))
                            max_score_rect=max_score.get_rect()
                            max_score_rect.left,max_score_rect.top=(width-max_score_rect.width)//2,height//2
                            screen.blit(max_score,max_score_rect)
                            if not i: 
                                ag_rect.left,ag_rect.top=(width-ag_rect.width)//2,(height-ag_rect.height)//2+150
                                ga_rect.left,ga_rect.top=(width-ga_rect.width)//2,(height-ga_rect.height)//2+200
                                i=1
                            screen.blit(ag_image,ag_rect)
                            screen.blit(ga_image,ga_rect)


                            pygame.display.flip()
                            clock.tick(60)
                        
        if not delay%5:
            qie=not qie


        delay-=1
        if not delay:
            delay=100
        pygame.display.flip()
        clock.tick(60)
