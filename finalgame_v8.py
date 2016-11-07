from __future__ import print_function

import os, sys, random, itertools, time          # for join: creates system-independent paths
import pygame
from pygame.locals import *
FPS = 40

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

WIDTH  = 1000
HEIGHT = 600
SPACESHIP_VELOCITY = 5
ASTEROID_VELOCITY = 5
BULLET_VELOCITY = 10
SMALL_ASTEROID_RELOAD   = 12
SMALL_ASTEROID_ODDS     = 22
MEDIUM_ASTEROID_RELOAD   = 18
MEDIUM_ASTEROID_ODDS     = 30
LARGE_ASTEROID_RELOAD   = 30
LARGE_ASTEROID_ODDS     = 44
COIN_RELOAD   = 12
COIN_ODDS     = 22
FIRE_RELOAD   = 100
FIRE_ODDS     = 100
ALIEN_X_VELOCITY = 5
ALIEN_Y_VELOCITY = -5
ENEMY_BULLET_VELOCITY = -10
LEVEL = 0
BOSS_Y_VELOCITY=3
def load_background(file):
    "loads an image, prepares it for play"
    file = os.path.join('data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

class SmallAsteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('asteroidsmall.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
        self.imagewhite, self.rectwhite = load_image('asteroidsmallwhite.png', BLACK)
        self.rectwhite.x = x
        self.rectwhite.y = y
        self.hp = 2
    def update(self):
        self.rect.x = self.rect.x - self.vx
        self.rectwhite.x = self.rectwhite.x - self.vx
class MediumAsteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('asteroidmedium.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
        self.imagewhite,self.rectwhite=load_image('asteroidmediumwhite.png',BLACK)
        self.rectwhite.x=x
        self.rectwhite.y=y
        self.hp=6
    def update(self):
        self.rect.x = self.rect.x - self.vx
        self.rectwhite.x=self.rectwhite.x-self.vx
class LargeAsteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('asteroidlarge.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
        self.imagewhite,self.rectwhite=load_image('asteroidlargewhite.png',BLACK)
        self.rectwhite.x=x
        self.rectwhite.y=y
        self.hp=12
    def update(self):
        self.rect.x = self.rect.x - self.vx
        self.rectwhite.x=self.rectwhite.x-self.vx
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('coin.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('fireball.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
class Bullet(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('laser2.png', WHITE)
        self.vx = BULLET_VELOCITY
        self.rect.x = xpos
        self.rect.y = ypos
        self.power=1
    def update(self):
        self.rect.x = self.rect.x + self.vx
        if self.rect.left >= WIDTH:
            self.kill()
class Strength(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bullet.png', WHITE)
        self.vx = ASTEROID_VELOCITY
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x = self.rect.x - self.vx
#class Enemy(pygame.sprite.Sprite):
 #   def __init__(self, x, y):
  #      pygame.sprite.Sprite.__init__(self)
   #     self.image, self.rect = load_image('UFO.png', WHITE)
    #    self.vx, self.vy = ALIEN_X_VELOCITY, ALIEN_Y_VELOCITY
     #   self.rect.x = x
      #  self.rect.y = y
    #def update(self):
     #   self.rect.x = self.rect.x - self.vx
      #  self.rect.y = self.rect.y - self.vy
       # if self.rect.right <= 0:
        #    self.kill()
        #elif self.rect.y + self.rect.height >= HEIGHT:
         #   self.vy = -self.vy
          #  self.rect.bottom = HEIGHT - 1
        #elif self.rect.y <= 0:
         #   self.vy = -self.vy
          #  self.rect.top = 1
class Boss(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image('boss.png',WHITE)
        self.vy=BOSS_Y_VELOCITY
        self.rect.x=x
        self.rect.y=y
        self.imagewhite,self.rectwhite=load_image('bosswhite.png',WHITE)
        self.rectwhite.x=x
        self.rectwhite.y=y
        self.hp=100
    def update(self):
        self.rect.y=self.rect.y+self.vy
        self.rectwhite.y=self.rectwhite.y+self.vy
        if self.rect.y+self.rect.height>=550:
            self.vy=-self.vy
            self.rect.bottom=549
            self.rectwhite.bottom=549
        if self.rect.y<=0:
            self.vy=-self.vy
            self.rect.top=1
            self.rectwhite.top=1
class Enemybullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect=load_image('enemybullet.png',BLACK)
        self.rect.x=x
        self.rect.y=y
        self.vx=random.randint(1,5)
        self.vy=random.randint(-5,5)
        self.imagewhite,self.rectwhite=load_image('enemybullet.png',BLACK)
        self.rectwhite.x=x
        self.rectwhite.y=y
        self.hp=3
    def update(self):
        self.rect.y=self.rect.y+self.vy
        self.rect.x=self.rect.x-self.vx
        self.rectwhite.y=self.rectwhite.y+self.vy
        self.rectwhite.x=self.rectwhite.x-self.vx

    

        #See if they can shoot back(randomly)
        


# Loads an image from a named file,
# returning a pair of type (image, rect).
def load_image(name, colorkey=None):
    path = os.path.join('data',  name)
    try:
        image = pygame.image.load(path)
    except pygame.error, message:
        print('Cannot load image: {}'.format(path))
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at( (0, 0) )
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    path = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error, message:
        print('Cannot load sound: {}', path)
        raise SystemExit, message
    return sound
def get_highscore():
    with open('highscores.txt', 'r') as f:
        a = [x.strip(',') for x in list(f)]
        b = [x.split(',') for x in a]
        #c = [int(x) for x in a]
        d = list(itertools.chain.from_iterable(b))
    return d
def get_max():
    c = get_highscore()
    c = [float(x) for x in c]
    maximum = 0
    for i in range(len(c)):
        if c[i] >= maximum:
            maximum = c[i]
    return int(float(maximum))





def main():
    pygame.init()
    window = pygame.display.set_mode( (WIDTH, HEIGHT) )
    pygame.display.set_caption('Avoid Asteroid')

    # Clock: used for creating delays in our game
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    #Background
    space_img, space_rect = load_image('space.png', RED)
    space_rect.center = (WIDTH / 2, HEIGHT / 2)
    space_vy = 0
    

    #Spaceship
    spaceship_img, spaceship_rect = load_image('spaceship.png', WHITE)
    spaceship_rect.center = (75, HEIGHT / 2)
    spaceship_vy = 0

    #Starting values
    smallasteroidreload = SMALL_ASTEROID_RELOAD
    mediumasteroidreload = MEDIUM_ASTEROID_RELOAD
    largeasteroidreload = LARGE_ASTEROID_RELOAD
    coinreload = COIN_RELOAD
    firereload = FIRE_RELOAD
    spaceshipvelocity = SPACESHIP_VELOCITY
    asteroidvelocity = ASTEROID_VELOCITY
    counter = 0
    smallasteroidreload = SMALL_ASTEROID_RELOAD   
    smallasteroidodds = SMALL_ASTEROID_ODDS     
    mediumasteroidreload = MEDIUM_ASTEROID_RELOAD   
    mediumasteroidodds = MEDIUM_ASTEROID_ODDS     
    largeasteroidreload = LARGE_ASTEROID_RELOAD
    largeasteroidodds = LARGE_ASTEROID_ODDS
    shoot = False
    count_shoot = 19
    level = LEVEL
    killing = 0
    printlevel = False
    countframe = 0
    powerup = 0
    generate_boss=0
    generate_asteroid=True
    generate_enemybullet=0
    generate_enemybullet2=False
      

    #Background image Start Page
    start_img, start_rect = load_image('asteroid4.png', RED)
    start_rect.center = (WIDTH / 2, HEIGHT / 2)
    start_vy = 0

    #Explosion
    explosion_img, explosion_rect= load_image('explosion.png', WHITE) 
    #explosion_rect.center = (xpos, ypos)
    explosion_vy = 0

    #Load Sound
    boom = load_sound('boom.wav')
    bgmusic = load_sound('music.wav')
    laser = load_sound('laser.wav')
    intense = load_sound('intense.wav')
    
    



    gameover = False
    sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    power = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    strengths = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bosses=pygame.sprite.Group()
    start = True
    highscorewritten = False

    while start == True:
        bgmusic.play()
        window.fill(BLACK)
        window.blit(start_img, start_rect.topleft)
        (x,y) = pygame.mouse.get_pos()
        text = font.render('Click One player to start', False, RED)
        text_rect = text.get_rect()
        text_rect.center= (WIDTH -150, 30)
        window.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            elif x > 340 and x < 660 and y > 200 and y < 400:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    start = False
                    break
        pygame.display.flip()
        clock.tick(FPS)
        if start == False:
            break
        
    



    music = True
    while True:
        # 1. Render the world
        if music == True:
            bgmusic.play()
        elif music == False:
            bgmusic.stop()
            intense.play()
        #Random int
        y = random.randint(0, 600)
        y2 = random.randint(0, 600)
        y3 = random.randint(0, 600)
        y4 = random.randint(0, 600)
        y5 = random.randint(0, 600)
        y6 = random.randint(0, 600)
        y7 = random.randint(0, 600)
        #Positioning
        xpos = spaceship_rect.x
        ypos = spaceship_rect.y
        explosion_rect.center = (xpos, ypos)
        window.fill(BLACK)
        window.blit( space_img, space_rect.topleft )
        smallasteroid = SmallAsteroid(1000, y)
        mediumasteroid = MediumAsteroid(1000, y2)
        largeasteroid = LargeAsteroid(1000, y3)
        coin = Coin(1000, y4)
        fire = Fire(1000, y5)
        strength = Strength(1000, y6)
        bullet = Bullet(xpos, ypos + 18)
        bullet2 = Bullet(xpos, ypos)
        bullet3 = Bullet(xpos, ypos + 30)
        #alien = Enemy(1000, 10)
        boss=Boss(500,y7)
        # Randomly generate asteroids of three different sizes/ coins
        if shoot==True:
            count_shoot += 1
            if level==0:
                if count_shoot >= 20:
                    bullets.add(Bullet(xpos,ypos+18))
                    count_shoot = 0
                if count_shoot >= 50:
                    count_shoot = 0
            if level >= 1:
                if count_shoot >= 10:
                    bullets.add(Bullet(xpos,ypos+5),Bullet(xpos,ypos+30))
                    #bullets.add(Bullet(xpos, ypos + 18))
                    count_shoot=0
                if count_shoot >= 50:
                    count_shoot = 0
        if level >= 1:
            asteroidvelocity = 15
        if generate_asteroid==True:

            if smallasteroidreload:
                smallasteroidreload = smallasteroidreload - 1
            elif not int(random.random() * smallasteroidodds):
                sprites.add(smallasteroid)
                smallasteroidreload = SMALL_ASTEROID_RELOAD

            if mediumasteroidreload:
                mediumasteroidreload = mediumasteroidreload - 1
            elif not int(random.random() * mediumasteroidodds):
                sprites.add(mediumasteroid)
                mediumasteroidreload = MEDIUM_ASTEROID_RELOAD

            if largeasteroidreload:
                largeasteroidreload = largeasteroidreload - 1
            elif not int(random.random() * largeasteroidodds):
                sprites.add(largeasteroid)
                largeasteroidreload = LARGE_ASTEROID_RELOAD

        if coinreload:
            coinreload = coinreload - 1
        elif not int(random.random() * COIN_ODDS):
            coins.add(coin)
            coinreload = COIN_RELOAD
        if firereload:
            firereload = firereload - 1
        elif not int(random.random() * FIRE_ODDS):
            power.add(fire)
            firereload = FIRE_RELOAD
        if firereload:
            firereload = firereload - 1
        elif not int(random.random() * FIRE_ODDS):
            strengths.add(strength)
            firereload = FIRE_RELOAD
        #if counter >= 5000 and counter <= 7000 or counter >= 20000 and counter <= 24000 or counter  >=50000 and counter <=56000:
         #   if len(enemies) <= 1:
          #      enemies.add(alien)
        if counter>=100000 and counter<=110000:
            generate_boss+=1
        if generate_boss==1:
            sprites.add(boss)
            bosses.add(boss)
            generate_asteroid=False
        if len(bosses)!=0:
            generate_enemybullet+=1
            #print(generate_enemybullet)
            if generate_enemybullet>=300:
                print(boss.rect.y)
                for i in range(15):
                    sprites.add(Enemybullet(500,boss.rect.y+20))
                    generate_enemybullet=0
            


        coins.draw(window)
        sprites.draw(window)
        power.draw(window)
        strengths.draw(window)
        #enemies.draw(window)
        if not gameover:
            bullets.draw(window)
            window.blit( spaceship_img, spaceship_rect.topleft )
        #Create small asteroids at time interval

        #Create score
    
        if gameover==False:
            for i in sprites:
                counter = float(counter + .1)
            text = font.render('Score: {}'.format(int(counter)), False, RED)
            text_rect = text.get_rect()
            text_rect.center= (WIDTH -100, 30)
            window.blit(text, text_rect)
            text2 = font.render('Press space to shoot', False, RED)
            text2_rect = text.get_rect()
            text2_rect.center= (WIDTH -200, 570)
            window.blit(text2, text2_rect)
            text4 = font.render('Highscore: {}'.format(get_max()), False, RED)
            text4_rect = text4.get_rect()
            text4_rect.center= (WIDTH -500, 30)
            window.blit(text4, text4_rect)

            

        if gameover:
            text = font.render('You Died!', False, RED)
            text2 = font.render('Score: {}'.format(int(counter)), False, RED)
            text3 = font.render('Press R to Restart', False, RED)
            text_rect = text.get_rect()
            text2_rect = text.get_rect()
            text3_rect = text.get_rect()
            text_rect.center= (WIDTH/2 -2, HEIGHT/2)
            text2_rect.center= (WIDTH/2 - 8, HEIGHT/2 + 30)
            text3_rect.center= (WIDTH/2 - 50, HEIGHT/2 + 60)
            window.blit(text, text_rect)
            window.blit(text2, text2_rect)
            window.blit(text3, text3_rect)
            if highscorewritten == False:
                with open('highscores.txt', 'a') as f:
                     f.write(str(counter))
                     f.write(',')
                     highscorewritten = True
        #Update spaceship rect

    # 2. Update the world
    # Detect collision
        spaceship_rect.y = spaceship_rect.y + spaceship_vy
        sprites.update()
        coins.update()
        power.update()
        bullets.update()
        strengths.update()
        enemies.update()
        for sprite in sprites:
            if sprite.rect.collidepoint(xpos, ypos+18) or sprite.rect.collidepoint(xpos+18, ypos+18):
                if gameover == False:
                    window.blit( explosion_img, explosion_rect.topleft )
                    bgmusic.stop()
                    boom.play()
                gameover = True

        for coin in coins:
            if coin.rect.colliderect(spaceship_rect):
                coin.kill()
                if not gameover:
                    counter += 1000.
        for powe in power:
            if powe.rect.colliderect(spaceship_rect):
                powe.kill()
                if spaceship_vy < 10 and spaceship_vy > -10:
                    spaceship_vy = 2 * spaceship_vy
                    spaceshipvelocity = 10
                if not gameover:
                    counter += 1000
        for bullet in bullets:
            for sprite in sprites:
                if bullet.rect.colliderect(sprite.rect):
                    bullet.kill()
                    #count_shoot = 0
                    sprite.hp= sprite.hp - bullet.power
                    window.blit(sprite.imagewhite,sprite.rectwhite)
                if sprite.hp <= 0:
                    bosses.remove(sprite)
                    sprite.kill()
                    killing = killing+1
                    if not gameover:
                        counter += 1000
        if len(bosses)==0:
            generate_asteroid=True
                #if killing == 25:
                    #level += 1
        if killing >= 20:
            #text0 = font.render('Level Up', False, RED)
            #text0_rect = text0.get_rect()
            #ext0_rect.center= (WIDTH - 800, HEIGHT - 30)
            #window.blit(text0, text0_rect)
            music = False
            #killing = 0
            if printlevel == False:
                #print('Level Up')
                printlevel = True
                    

                    
            if bullet.rect.x == WIDTH:
                bullet.kill()
        for strength in strengths:
            if strength.rect.colliderect(spaceship_rect):
                strength.kill()
                time = pygame.time.get_ticks()
                powerup = 1
                level += 1

                #bullets.add(bullet2)
                #bullets.add(bullet3)
                counter += 1000

        if powerup == 1 and pygame.time.get_ticks() >= time + 5000:
            level = 0
            powerup = 0
        #for enemy in enemies:
         #   if enemy.rect.colliderect(spaceship_rect):
         #       gameover = True
          #  for bullet in bullets:
           #     if bullet.rect.colliderect(enemy.rect):
            #        bullet.kill()
             #       enemy.kill()
              #      counter += 10000

        if counter >= 10000:
            smallasteroidodds = 11
            mediumasteroidodds = 15
            largeasteroidodds = 22
        if counter >= 10000:
            smallasteroidodds =6
            mediumasteroidodds = 8
            largeasteroidodds = 12




        ##### Detect Wall Collisions #####
        if spaceship_rect.y <= 0:
           spaceship_rect.y = spaceship_rect.y + 10
        if spaceship_rect.y >=550:
            spaceship_rect.y = spaceship_rect.y - 10

        # 3. Process user input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            ##### Processing User Input #####
            elif event.type == KEYDOWN and event.key == K_UP or \
                 event.type == KEYUP   and event.key == K_DOWN:
                spaceship_vy = spaceship_vy - spaceshipvelocity
            elif event.type == KEYDOWN and event.key == K_DOWN or \
                 event.type == KEYUP   and event.key == K_UP:
                spaceship_vy = spaceship_vy + spaceshipvelocity
            if gameover == True:
                if event.type == KEYDOWN and event.key == K_r:
                    gameover == False
                    main()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                shoot=True
            elif event.type==KEYUP and event.key==K_SPACE:
                shoot=False
                count_shoot = 19
        #countframe +=1
           #     bullets.add(bullet)
            #    laser.play()
                #to have multiple bullets: Bullet(xpos, ypos + 18)
        # 4. Delay (for a fixed time)
        pygame.display.flip()
        clock.tick(FPS)
        pass
if __name__ == '__main__':
    main()


#Make easy mode/ normal mode just changing the bullets allowed
#Make highscore
    
###### ####### ########
    
