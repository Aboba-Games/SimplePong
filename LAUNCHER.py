import pygame
import random
import time

#window
FPS = 70
WIDTH = 900
HEIGHT = 600
SPEED = 10

def printing(window, text, font, size, color, x, y):
    fontName = pygame.font.match_font(font)
    fontSize = pygame.font.Font(fontName, size)
    textSurface = fontSize.render(text, True, color)
    text_rect = textSurface.get_rect()
    text_rect.center = (x, y)
    window.blit(textSurface, text_rect)

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (25,255,0)
GRAY = (128, 128, 128)
VIOLET = (126, 8, 236)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREEN = (0,128,0)
CYAN = (0, 255, 255)
LIGHTGRAY = (211, 211, 211)
NAVY = (0, 0, 128)
MEDIUMSLATEBLUE = (123, 104, 238)
SKYBLUE = (0, 191, 255)
HONEYDEW = (240, 255, 240)
SNOW = (255, 250, 250)
IVORY = (255, 255, 240)
YELLOWGREEN = (154, 205, 50)
DARKGREEN = (0, 100, 0)
INDIGO = (75, 0, 130)

#player(platform) and objects
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platImg,(200,20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT-20)
    
    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speedx = -SPEED
        if keys[pygame.K_d]:
            self.speedx = SPEED
        self.rect.x += self.speedx  

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0     

class Circle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image = pygame.transform.scale(circleImg,(20,20))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2-10)
        self.speedx = random.randint(-3,3)
        if self.speedx == 0:
            self.speedx = 2
        self.speedy = random.randint(3,7)

    def update(self):
        if self.rect.right > WIDTH:
            self.speedx = -self.speedx
            ballSound.play()
            

        if self.rect.left < 0:
            self.speedx = -self.speedx
            ballSound.play()
            

        if self.rect.top < 0:
            self.speedy = -self.speedy
            ballSound.play()

        if self.rect.bottom > player.rect.top:
            if player.rect.x < self.rect.x < player.rect.x+30:
                ballSound.play()
                self.speedy = -self.speedy
                self.speedx = random.randint(-3,-1)
            elif player.rect.x+30 < self.rect.x < player.rect.x+60:
                ballSound.play()
                self.speedy = -self.speedy
                self.speedx = random.randint(-6,-1)
            elif player.rect.x+60 < self.rect.x < player.rect.x+90:
                ballSound.play()
                self.speedy = -self.speedy
                self.speedx = random.randint(1,3)
            elif player.rect.x+90 < self.rect.x < player.rect.x+120:
                ballSound.play()
                self.speedy = -self.speedy
                self.speedx = random.randint(3,6)
            elif player.rect.x+120 < self.rect.x < player.rect.x+150:
                ballSound.play()
                self.speedy = -self.speedy
                self.speedx = 6

        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((43,43))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 2
        # self.image = pygame.transform.scale(blockImg,(43,43))
        self.updTx()
    def updTx(self):
        self.image = pygame.transform.scale(blockImg[self.hp-1],(43,43))
        
class Bonus(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,25))
        self.image.fill(LIME)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT+1)
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.speedy = 5
        self.rect.y += self.speedy
        if self.rect.top>HEIGHT:
            self.kill()

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SimplePong')
clock = pygame.time.Clock()

#textures and design
platImg = pygame.image.load('player.jpg').convert()
blockImg =[ pygame.image.load('brick.jpg').convert(), pygame.image.load('block.jpg').convert()]
circleImg = pygame.image.load('circle.jpg').convert()
pygame.display.set_icon(pygame.image.load('icon.svg'))
mainbg = pygame.image.load('mainBg.jpg').convert()
mainbg = pygame.transform.scale(mainbg,(WIDTH, HEIGHT))
mainbg_rect = mainbg.get_rect()
bglv = pygame.image.load('bglv.jpg').convert()
bglv = pygame.transform.scale(bglv,(WIDTH, HEIGHT))
bglv_rect = bglv.get_rect()
menubg = pygame.image.load('menuBg.jpg').convert()
menubg = pygame.transform.scale(menubg, (WIDTH, HEIGHT))
menubg_rect = menubg.get_rect()

ballSound = pygame.mixer.Sound('ball.mp3')
ballSound.set_volume(0.3)

buttonSound = pygame.mixer.Sound('button.mp3')
buttonSound.set_volume(0.3)

win = pygame.mixer.Sound('win.mp3')
win.set_volume(0.3)
lose = pygame.mixer.Sound('fail.mp3')
lose.set_volume(0.3)


#objects
player = Platform()
circle = Circle()
sprites = pygame.sprite.Group()
circles = pygame.sprite.Group()
blocks = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
circles.add(circle)
sprites.add(player)
sprites.add(circle)

levels = [
    ['####################',
     ' # # # # # # # # # #'],

    ['####################',
     '# #### ### ### ### #'],

    ['### # # #### # # ###',
     '## ## ## ## ## ## ##'],

    ['#### #### #### #####',
     '#### #### #### #####'],

    [' # # # # # # # # # #',
     '# # # # # # # # # # '],

    ['# ## ## ## ## ## # #',
     ' # # # # # # # # # #'],

    ['### ### ## ## ## ###',
     ' # # # ####### # # #'],

    ['######## ### #######',
     '######## # # #######'],

    ['## ## #### #### ####',
     '#### # ### ### # ###'],

    ['####################',
     '####################'],

    ['########## #########',
     '## ### # ### # ### #'],

    ]


level = 0
for i in range(20):
    for j in range(len(levels[level])):
        if levels[level][j][i] == '#':
            block = Block(i*45, j*45)
            sprites.add(block)
            blocks.add(block)

playerScore = 0
state = 3 #0  - game is going on, 1 - level has ended. 2 - game has ended

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if state != 0:
                    buttonSound.play()
                    run = False
            if event.key == pygame.K_c:
                if state != 0 and state != 3 and state != 5:
                    buttonSound.play()
                    state = 0
            if event.key == pygame.K_ESCAPE:
                if state!=1 and state!=2 and state!=3 and state != 4 and state != 5:
                    buttonSound.play()
                    state = 4
            if event.key == pygame.K_e:
                if state != 0 and state != 1 and state != 4 and state != 2 and state != 5:
                    buttonSound.play()
                    state = 0
            if event.key == pygame.K_m:
                if state != 0:
                    buttonSound.play()
                    state = 3
                    level = 0
                    playerScore = 0
                    for i in range(20):
                        for j in range(len(levels[level])):
                            if levels[level][j][i] == '#':
                                block = Block(i*45, j*45)
                                sprites.add(block)
                                blocks.add(block)
                    circle.rect.center = (WIDTH//2, HEIGHT//2)
                    player.rect.center = (WIDTH//2, HEIGHT-20)
            if event.key == pygame.K_r:
                if state != 0:
                    buttonSound.play()
                    state = 0
                    level = 0
                    playerScore = 0
                    for i in range(20):
                        for j in range(len(levels[level])):
                            if levels[level][j][i] == '#':
                                block = Block(i*45, j*45)
                                sprites.add(block)
                                blocks.add(block)
                    circle.rect.center = (WIDTH//2, HEIGHT//2)

    hitsbonuses = pygame.sprite.spritecollide(player, bonuses, True)
    for bonus in hitsbonuses:
        if hitsbonuses:
            num = random.choice([1,2,3])
            if num == 1:
                playerScore += 10
            elif num ==  2:
                player.speedx+=2
                actionStart = time.time()
                if time.time()<actionStart+15:
                    SPEED = 20
                else:
                    SPEED = 10
            elif num == 3:
                 bonusCircle = Circle()
                 sprites.add(bonusCircle)
                 circles.add(bonusCircle)

    hitsblocks = pygame.sprite.groupcollide(blocks, circles, False, False)
    if hitsblocks:
        circle.speedy = -circle.speedy
        for hit in hitsblocks:
            ballSound.play()
            hit.hp-=1
            hit.updTx()
            if hit.hp < 1: 
                hit.kill()               
                playerScore+=1
                if random.random()<0.9:
                    bonus = Bonus(hit.rect.x, hit.rect.y)
                    sprites.add(bonus)
                    bonuses.add(bonus)

    if len(blocks.sprites()) == 0:
        level+=1
        if level >= len(levels):
            state = 5 #end
        elif state!=2:
            state = 1 #level passed
            for i in range(20):
                for j in range(len(levels[level])):
                    if levels[level][j][i] == '#':
                        block = Block(i*45, j*45)
                        sprites.add(block)
                        blocks.add(block)
            circle.rect.center = (WIDTH//2, HEIGHT//2)

    if circle.rect.y > HEIGHT:
        state = 2

    if state == 0:
        window.blit(mainbg, mainbg_rect)
        sprites.draw(window)
        sprites.update()
        printing(window, 'Score: '+str(playerScore), 'Sheriff', 30, GREEN, 60, HEIGHT-70)
        printing(window, 'Level: '+str(level), 'Sheriff', 30, GREEN, 840, HEIGHT-70)
        pygame.display.flip()
    elif state == 1:
        window.blit(bglv, bglv_rect)
        printing(window, "You've passed the level!", 'Arial', 30, VIOLET, WIDTH//2, HEIGHT//2-20)
        printing(window, '|C|Continue', 'Arial', 25, BLUE, WIDTH//2, HEIGHT//2+80)
        printing(window, '|M|Exit to Main Menu', 'Arial', 25, ORANGE, WIDTH//2, HEIGHT//2+110)
        printing(window, '|Q|Exit to Desktop', 'Arial', 25, RED, WIDTH//2, HEIGHT//2+140)
        pygame.display.flip()
        win.play()
    elif state == 2:
        window.blit(bglv, bglv_rect)
        printing(window, "You've lost!", 'Arial', 40, VIOLET, WIDTH//2, HEIGHT//2-50)
        printing(window, '|R|Restart', 'Arial', 25, BLUE, WIDTH//2, HEIGHT//2+20)
        printing(window, '|M|Exit to Main Menu', 'Arial', 25, ORANGE, WIDTH//2, HEIGHT//2+50)
        printing(window, '|Q|Exit to Desktop', 'Arial', 25, RED, WIDTH//2, HEIGHT//2+80)
        pygame.display.flip()
        lose.play()
    elif state == 3:
        window.blit(menubg, menubg_rect)
        printing(window, 'SimplePong', 'Sheriff', 40, GRAY, WIDTH//2, HEIGHT//2)
        printing(window, 'Version: 1.0', 'Sheriff', 20, YELLOW, WIDTH//2, HEIGHT/2-20)
        printing(window, '|E|Play', 'Sheriff', 30, GREEN, WIDTH//2, HEIGHT//2+80)
        printing(window, '|Q|Exit', 'Sheriff', 30, RED, WIDTH//2, HEIGHT//2+120)
        printing(window, 'Aboba Games??', 'Arial', 25, GRAY, 90, 12)
        printing(window, 'Updated: 04/30/22', 'Arial', 25, GRAY, 790, 12)
        printing(window, 'All Rights Reserved!??', 'Sheriff', 25, LIGHTGRAY, WIDTH//2, 580)
        pygame.display.flip()
    elif state == 4:
        window.blit(menubg, menubg_rect)
        printing(window, 'Pause', 'Sheriff', 40, GRAY, WIDTH//2, HEIGHT//2-50)
        printing(window, '|C|Continue', 'Sheriff', 30, GREEN, WIDTH//2, HEIGHT//2+20)
        printing(window, '|M|Exit to Main Menu', 'Sheriff', 30, ORANGE, WIDTH//2, HEIGHT//2+50)
        printing(window, '|Q|Exit to Desktop', 'Sheriff', 30, RED, WIDTH//2, HEIGHT//2+80)
        pygame.display.flip()
    elif state == 5:
        window.blit(menubg, menubg_rect)
        printing(window, "Congratulations! You've won the game!", 'Arial', 40, VIOLET, WIDTH//2, HEIGHT//2-50)
        printing(window, '|R|Restart', 'Arial', 25, BLUE, WIDTH//2, HEIGHT//2+20)
        printing(window, '|M|Exit to Main Menu', 'Arial', 25, ORANGE, WIDTH//2, HEIGHT//2+50)
        printing(window, '|Q|Exit to Desktop', 'Arial', 25, RED, WIDTH//2, HEIGHT//2+80)
        printing(window, 'For more games you can visit our github: https://github.com/Aboba-Games', 'Arial', 20, SKYBLUE, WIDTH//2, HEIGHT//2+160)
        pygame.display.flip()
        win.play()
        
pygame.quit()
#V1.0
