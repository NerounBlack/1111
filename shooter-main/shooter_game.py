#Створи власний Шутер!

from random import randint
from typing import Any
from pygame import *

from time import time as timer

wn = display.set_mode((700,500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700,500))
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
win_sound = mixer.Sound("win.mp3")
font.init()
font1 = font.Font(None,36)
font2 = font.Font(None,100)

score =0 
lose = 0

win_score = 10
lose_score = 5

class GameSprite(sprite.Sprite):
    def __init__(self,pl_image,pl_x,pl_y,size_x,size_y,pl_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.speed = pl_speed
        self.size_x = size_x 
        
    # def fill(self):
    def reset(self):
        wn.blit(self.image,(self.rect.x,self.rect.y))        
        

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        #[K_a,K_k]
        #назва списку[номер елем]
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed 
        if keys[K_d] and self.rect.x < 700 - self.size_x :
            self.rect.x += self.speed 
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20, -15)
        bullets.add(bullet)
lose = 0
class Enemy(GameSprite):
    
    def update(self):
        global lose

        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(80,620) 
            self.speed= randint(1,5)
            lose +=1
             
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

monsters = sprite.Group()
for i in range(1):
    monster = Enemy("ufo.png",randint(80,620),-50,80,50,randint(1,3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(2):
    asteroid = Enemy("asteroid.png",randint(80,620),-50,80,50,randint(1,4))
    asteroids.add(asteroid)


bossHp = 10
bullets = sprite.Group()
boss = False
bossPL = Player("Без названия (1).jpg",280,70,110,140,10)
rocket = Player("rocket.png",300,400,80,100,10)        
game = True
finish = False
num_bul = 6
cur_bul = 0
fire_bul = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if cur_bul <= num_bul and fire_bul == False:
                    fire_sound.play()
                    rocket.fire()
                    cur_bul +=1 
                
                elif cur_bul >= num_bul and fire_bul == False:
                    fire_bul = True
                    last_time = timer()
                
        
    if not finish:
        
        wn.blit(background,(0,0))
        text_score = font1.render("Рахунок: " + str(score), 1,(255,255,255))
        wn.blit(text_score,(10,20))
        text_lose = font1.render("Пропущено: " + str(lose), 1,(255,255,255))
        wn.blit(text_lose,(10,50))
        text_lose = font1.render("Пулі: " + str(cur_bul), 1,(255,255,255))
        wn.blit(text_lose,(10,80))
        
        rocket.reset()
        rocket.update()
        bullets.draw(wn)
        bullets.update()
        monsters.draw(wn)
        monsters.update()
        asteroids.draw(wn)
        asteroids.update()
        
        
        if fire_bul == True:
            now_time = timer()
            if now_time- last_time < 1 :
                reload = font1.render("почекай....", 1,(160,25,2))
                wn.blit(reload,(250,10))
            else:
                fire_bul = False
                cur_bul = 0

        collide_monster_bullet = sprite.groupcollide(monsters,bullets,True,True)
        for collide in collide_monster_bullet:
            score += 1
            monster = Enemy("ufo.png",randint(80,620),-50,80,50,randint(1,4))
            monsters.add(monster)
            
            
        collide_asteroid_bullet = sprite.groupcollide(asteroids,bullets,True,True)
        for collide in collide_asteroid_bullet:
            score += 1   
            asteroid = Enemy("asteroid.png",randint(80,620),-50,80,50,randint(1,4))
            asteroids.add(asteroid)   
        if score > 10:
            boss = True
            finish = True        
            cur_bul = 0
    elif boss:
        wn.blit(background,(0,0))
        bossPL.reset()
        rocket.reset()
        rocket.update()
        bullets.draw(wn)
        bullets.update()
    
        if fire_bul == True:
                now_time = timer()
                if now_time- last_time < 1 :
                    reload = font1.render("почекай....", 1,(160,25,2))
                    wn.blit(reload,(250,10))
                else:
                    fire_bul = False
                    cur_bul = 0
        collide_boss = sprite.spritecollide(bossPL,bullets,True)
        if collide_boss:
            bossHp -= 1    
        bossPL.rect.x += bossPL.speed
        if not (0 < bossPL.rect.x < 650):
                bossPL.speed *= -1            
        
        boss_tx = font1.render("Життя: ", 1,(255,255,255))
        wn.blit(boss_tx,(10,20))
        boss_tx = font1.render(str(bossHp), 1,(255,0,0))
        wn.blit(boss_tx,(100,20))
        text_bul = font1.render("Пулі: " + str(cur_bul), 1,(255,255,255))
        wn.blit(text_bul,(10,50))
    
    
    
    
    
    else: 
        finish = False
        lose = 0
        score = 0 
        fire_bul = False
        cur_bul = 0
        for m in monsters:
            m.kill()
        for b in bullets:
            b.kill()    
        for a in asteroids:
            a.kill()
            
        time.delay(3000)
        for i in range(2):
            monster = Enemy("ufo.png",randint(80,620),-50,80,50,randint(1,3))
            monsters.add(monster)

        for i in range(2):
            asteroid = Enemy("asteroid.png",randint(80,620),-50,80,50,randint(1,4))
            asteroids.add(asteroid)
        mixer.music.play()
    if bossHp <= 0:
        boss = True
        finish = True
        win = font2.render("YOU WIN", 1,(1,255,2))
        wn.blit(win,(200,200))
        mixer.music.stop()
    if lose >= lose_score:
        finish = True
        win = font2.render("YOU LOSE", 1,(255,2,2))
        wn.blit(win,(200,200))  
        mixer.music.stop() 
        
    clock.tick(FPS)
    display.update()