from pygame import *
from time import clock,sleep
from random import randint
clock = time.Clock()
 

win_width = 700
win_height = 500
 
game = True

FPS = 60

window = display.set_mode((win_width, win_height))
display.set_caption("космос")
background = transform.scale(image.load("galaxy.jpg"),(win_width, win_height))
 
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

count = 0
skipped = 0
size_h = 500
font.init()

font_littel = font.Font(None, 30)
font_big = font.Font(None,60)

finish = False

win = font_big.render('YOU WIN!!!', True, (0, 205, 0))
lose = font_big.render('YOU LOSE!!!', True, (250, 0, 0))

mixer.init() 
shoot_sound = mixer.Sound('fire.ogg')


heart1 = transform.scale(image.load("pngwing.com.png"),(45,45))
heart2 = transform.scale(image.load("pngwing.com.png"),(45,45))
heart3 = transform.scale(image.load("pngwing.com.png"),(45,45))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,player_speed, player_size_x,player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(player_size_x,player_size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
        self.speed = player_speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed  = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 10
        if key_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += 10
    def shoot(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, -15, 20, 15)
        bullets.add(bullet)
  
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global skipped
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            skipped = skipped + 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

player = Player("rocket.png",20,360,10,80,100)
ufos = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()


# hearts = sprite.Group()
# for i in range(3):
#     size_h += 50
#     heart = GameSprite("pngwing.com.png",size_h,10,0,40,35)
#     hearts.add(heart)

for i in range(2):
    asteroid = Asteroid('asteroid.png',randint(80, win_width - 80),0,randint(1,3),50,50)
    asteroids.add(asteroid)
for i in range(5):
    ufo = Enemy("ufo.png", randint(80, win_width - 80),0,randint(1,3),80,50)
    ufos.add(ufo)


while game:
    sprites_list_2 = sprite.groupcollide(ufos, bullets, True, True)
    
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()
                shoot_sound.play()
    if finish != True:

        count_text = font_littel.render('Счёт:'+ str(count), True, (255, 255, 255))
        skipped_text = font_littel.render("Пропущено: " + str(skipped), 1,(255, 255, 255))
        window.blit(background,(0, 0))


        window.blit(count_text, (20,20))
        window.blit(skipped_text, (20,50))
        ufos.draw(window)
        ufos.update()
        player.draw()
        player.update()
        bullets.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()
        # hearts.draw(window)
        
        # if skipped == 1:
        #     hearts.remove()
        # if skipped == 2:
        #     hearts.remove()

        for c in sprites_list_2:
            count += 1
            ufo = Enemy("ufo.png", randint(80, win_width - 80),0,randint(1,4),80,50)
            ufos.add(ufo)

        if count >= 10:
            finish = True
            window.blit(win, (200,200))

        if sprite.spritecollide(player, ufos, False) or skipped > 3 or sprite.spritecollide(player,asteroids, False):
            finish = True
            window.blit(lose, (200,200))
            # hearts.remove()
       
        if skipped == 0:
            window.blit(heart1, (500,50))
            window.blit(heart2, (550,50))
            window.blit(heart3, (600,50))
        if skipped == 1:
            window.blit(heart1, (500,50))
            window.blit(heart2, (550,50))

        if skipped == 2 :
            window.blit(heart1, (500,50))
            
        

        
        
       
    display.update()
    clock.tick(FPS)
