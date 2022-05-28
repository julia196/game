import pygame
import math
import random
import threading
import _thread as thread
import time
import pyganim
 
# Define some colors
COLOR =  "#888888"
ANIMATION_DELAY = 5
ANIMATION_STAY_UNIT = [('unit/0.png', ANIMATION_DELAY)]
ANIMATION_STAY_ENEMY = [('enemy/0.png', ANIMATION_DELAY)]
ANIMATION_STAY_JUMPER = [('jumper/0.png', ANIMATION_DELAY)]
ANIMATION_RIGHT_UNIT = [('unit/r1.png'),
            ('unit/r2.png'),
            ('unit/r3.png'),
            ('unit/r4.png'),
            ('unit/r5.png')]

ANIMATION_FIGHT_UNIT  = [('unit/f1.png'),
                   ('unit/f2.png'),
                   ('unit/f3.png'),
                   ('unit/f4.png'),
                   ('unit/f5.png')]

ANIMATION_LEFT_ENEMY = [('enemy/l1.png'),
            ('enemy/l2.png'),
            ('enemy/l3.png'),
            ('enemy/l4.png'),]

ANIMATION_FIGHT_ENEMY  = [('enemy/f1.png'),
                   ('enemy/f2.png'),
                   ('enemy/f3.png'),
                   ('enemy/f4.png'),]

ANIMATION_RIGHT_JUMPER = [('jumper/r1.png'),
            ('jumper/r2.png'),
            ('jumper/r3.png')]

ANIMATION_FIGHT_JUMPER = [('jumper/f1.png'),
                          ('jumper/f2.png'),
                          ('jumper/f3.png')]

scr_w = 1920
scr_h = 1002
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = [scr_w, scr_h]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")


background_image = pygame.image.load("ground.png").convert()

pos1 = pygame.mouse.get_pos()
x1_mouse = pos1[0]
y1_mouse = pos1[1]
####################

class Wall(pygame.sprite.Sprite):
    def __init__(self, width=50, height=50):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = pygame.image.load('grass.png').convert()
        #self.image.set_colorkey(white)
        self.rect = self.image.get_rect()

class Ground(pygame.sprite.Sprite):
    def __init__(self, width=20, height=20):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = pygame.image.load('ground1.png').convert()
        #self.image.fill((0,0,0))
        self.rect = self.image.get_rect()

class HealthLine():
    def __init__(self, x_line, y_line, h=2, w=20):
        self.h = h
        self.w = w
        self.x_line = x_line
        self.y_line = y_line
        
    def draww(self):
        pygame.draw.rect(screen,(0,255,0),[self.x_line, self.y_line, self.w, self.h])

    def move(self, x_new):
        self.x_line = x_new

class Unit(pygame.sprite.Sprite):
    def __init__(self, friend, x_unit, y_unit):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'Unit'
        self.x_unit = x_unit
        self.y_unit = y_unit
        self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load('unit/0.png').convert_alpha()
        #self.image.set_colorkey(Color(COLOR))
        self.rect = self.image.get_rect()
        ###ДВИЖЕНИЕ ВПРАВО###
        boltAnim = []
        for anim in ANIMATION_RIGHT_UNIT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight_UNIT = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight_UNIT.play()

        ###АТАКА###
        boltAnim = []
        for anim in ANIMATION_FIGHT_UNIT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimFight_UNIT = pyganim.PygAnimation(boltAnim)
        self.boltAnimFight_UNIT.play()
        
        self.speed = 1.5
        self.health = 100
        self.attack = -10
        #self.hl = HealthLine(x_unit, y_unit+21)

    def move(self):
        self.rect.x += self.speed
        self.boltAnimRight_UNIT.blit(self.image, (0, 0))
##        self.rect.y += 0
        #self.hl.move(self.rect.x)

    def damage(self, enemy):
        enemy.health += self.attack

class Jumper(pygame.sprite.Sprite):
    def __init__(self, friend, x_jumper, y_jumper):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'Jumper'
        self.x_jumper = x_jumper
        self.y_jumper = y_jumper
        self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load('jumper/0.png').convert()
        self.rect = self.image.get_rect()
        
        ###ДВИЖЕНИЕ ВПРАВО###
        boltAnim = []
        for anim in ANIMATION_RIGHT_JUMPER:
            boltAnim.append((anim, 1.9))
        self.boltAnimRight_JUMPER = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight_JUMPER.play()

         ###АТАКА###
        boltAnim = []
        for anim in ANIMATION_FIGHT_JUMPER:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimFight_JUMPER = pyganim.PygAnimation(boltAnim)
        self.boltAnimFight_JUMPER.play()
        
        self.speed = 20
        self.health = 20
        self.attack = -50
        self.dx = 1
        self.sleep = 0

    def move(self):
##        self.dx += 1
        #print(self.dx)
        
##            print(self.sleep)
        if self.sleep != 0:
            ct = time.time()
            #print(math.floor(self.sleep), math.floor(ct))
            if math.floor(ct) - math.floor(self.sleep) > 1:
                self.sleep = 0
                self.dx = 0
        else:
            self.rect.x += self.speed
            self.dx += 1
            #print(self.dx)
            if self.dx % 3 == 0:
                self.sleep = time.time()
        self.boltAnimRight_JUMPER.blit(self.image, (0, 0))
        

    def damage(self, enemy):
        enemy.health += self.attack

class Enemy(pygame.sprite.Sprite):
    def __init__(self, friend, x_enemy, y_enemy):
        self.name = 'Enemy'
        pygame.sprite.Sprite.__init__(self)
        self.x_enemy = x_enemy
        self.y_enemy = y_enemy
        self.image = pygame.Surface((20, 20))
        self.image = pygame.image.load('enemy/0.png').convert()
        self.rect = self.image.get_rect()
        
        ###ДВИЖЕНИЕ ВЛЕВО###
        boltAnim = []
        for anim in ANIMATION_LEFT_ENEMY:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft_ENEMY = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft_ENEMY.play()

        ###АТАКА###
        boltAnim = []
        for anim in ANIMATION_FIGHT_ENEMY:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimFight_ENEMY = pyganim.PygAnimation(boltAnim)
        self.boltAnimFight_ENEMY.play()
        
        self.speed = 1.5
        self.health = 100
        self.attack = -10 
        
    def move(self):
        self.rect.x -= self.speed
        self.boltAnimLeft_ENEMY.blit(self.image, (0, 0))
        self.rect.y += 0

    def damage(self, unit):
        unit.health += self.attack

def battle(unit, enemy, health = 20):
    while unit.health > 0:
        #pygame.draw.rect(screen,(0,255,0),[unit.rect.x, unit.rect.y + 21, health, 2])
        try:
          unit.boltAnimFight_JUMPER.blit(unit.image, (0, 0))
        except:
            unit.boltAnimFight_UNIT.blit(unit.image, (0, 0))
        unit.damage(enemy)
        enemy.damage(unit)
        enemy.boltAnimFight_ENEMY.blit(enemy.image, (0, 0))
        #print(unit.health, enemy.health)
        time.sleep(0.5)
        health -= 2
    all_sprites_list.remove(unit)
    all_sprites_list.remove(enemy)
    all_sprites.remove(unit)
    all_sprites.remove(enemy)
    all_attack.clear()

####################

block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
all_players = []
all_enemys = []
all_grounds = []
all_lines = []
all_sprites = pygame.sprite.Group()
all_attack = {}

wall = Wall()
wall1 = Wall()

wall.rect.x = -10
wall1.rect.x = 0
wall.rect.y = -2
wall1.rect.y = 801

#unit.rect.x = 101 #((x_mouse-0) // 20) * 20 #101 
#unit.rect.y = 501 #((y_mouse-0) // 20) * 20 #501

block_list.add(wall)
block_list.add(wall1)
all_sprites_list.add(wall)
all_sprites_list.add(wall1)

y0 = 0
for x in range(96):
    x0 = 1
    for y in range(50):
        ground = Ground()
        ground.rect.x = x * 20
        ground.rect.y = y * 20 
        x0 += 1
        all_grounds.append(ground)
        all_sprites.add(ground)

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

marker_unit = 0
marker_start = 0
marker_jumper = 0
marker_finish = 0
level = '1'
count_enemy = 5


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            pos = pygame.mouse.get_pos()
            x2_mouse = pos[0]
            y2_mouse = pos[1]
            if event.button == 1:
                if (460 <= x2_mouse <= 500) and (821 <= y2_mouse <= 861):
                    
                    ###СОЗДАНИЕ ВРАГОВ###
                    for i in range(count_enemy):
                        enemy_x = (random.randint(1780, 1900) // 20)*20
                        enemy_y = (random.randint(221, 781) // 20)*20
                        enemy = Enemy('False', enemy_x, enemy_y)
                        enemy.rect.x = enemy_x
                        enemy.rect.y = enemy_y
                        all_sprites_list.add(enemy)
                        all_enemys.append(enemy)
                        marker_start = 1
                        marker_unit = 0
                        marker_jumper = 0
                        #print(enemy.rect.x, enemy.rect.y)
                        
                if (540 <= x2_mouse <= 580) and (821 <= y2_mouse <= 861):
                    marker_unit = 1
                    marker_jumper = 0

                if (600 <= x2_mouse <= 640) and (821 <= y2_mouse <= 861):
                    marker_jumper = 1
                    marker_unit = 0

                ###СОЗДАНИЕ ЮНИТА###
                if (200 < y2_mouse < 800) and marker_unit == 1:
                    unit_x = ((x2_mouse-0) // 20) * 20
                    unit_y = ((y2_mouse-0) // 20) * 20 + 1
                    unit = Unit('True', unit_x, unit_y)
                    unit.rect.x = unit_x
                    unit.rect.y = unit_y
                    all_sprites_list.add(unit)
                    all_players.append(unit)
                    #all_lines.append(all_players[-1].hl)
                    #print(pos)
                    #print(unit.rect.x, unit.rect.y)
                    
                ###СОЗДАНИЕ ПРЫГУНА###
                if (200 < y2_mouse < 800) and marker_jumper == 1:
                    jumper_x = ((x2_mouse-0) // 20) * 20
                    jumper_y = ((y2_mouse-0) // 20) * 20 + 1
                    jumper = Jumper('True', jumper_x, jumper_y)
                    jumper.rect.x = jumper_x
                    jumper.rect.y = jumper_y
                    all_sprites_list.add(jumper)
                    all_players.append(jumper)
                    #print(pos)
                    #print(jumper.rect.x, jumper.rect.y)
 
    # --- Game logic should go here
    pos = pygame.mouse.get_pos()
    x_mouse = pos[0]
    y_mouse = pos[1]
    #print(pos)
    x_rect = ((x_mouse-0) // 20) * 20
    y_rect = ((y_mouse-0) // 20) * 20
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    all_sprites.draw(screen)
    screen.blit(background_image, [0,0])

    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 1000
    for i in range(96):
        pygame.draw.line(screen,(47,79,79),[x1,y1],[x2,y2],1)
        x1 += 20
        x2 += 20

    x1 = 0
    x2 = 1920
    y1 = 0
    y2 = 0
    for i in range(51):
        pygame.draw.line(screen,(47,79,79),[x1,y1],[x2,y2],1)
        y1 += 20
        y2 += 20
    all_sprites_list.draw(screen)

    ###ЗЕЛЁННЫЙ КВАДРАТ###
    if 200 < y_rect < 800 and (marker_unit == 1 or marker_jumper == 1):
        pygame.draw.rect(screen,(0,255,0),[x_rect,y_rect,20,20])

    ###ПОЛОСКА ЖИЗНИ###
    if all_players:
        for l in all_lines:
            l.draww()
            #l.move()
            #pygame.draw.rect(screen,(0,255,0),[un.rect.x, un.rect.y + 21, 20, 2])


    ###КНОПКА START###
    pygame.draw.rect(screen, (161, 126, 0), (460, 821, 40, 40))
    pygame.draw.rect(screen, (217, 175, 24), (460, 821, 40, 40), 3)
    pygame.draw.polygon(screen, (217, 175, 24), [[469, 830], [469, 852], [491, 841]])

    ###КНОПКА РЫЦАРЯ###
    pygame.draw.rect(screen, (161, 126, 0), (540, 821, 40, 40))
    pygame.draw.rect(screen, (217, 175, 24), (540, 821, 40, 40), 3)
    pygame.draw.polygon(screen, (217, 175, 24), [[558, 826], [561, 826], [561, 829], [564 ,829], [564 ,845], [570, 845],
                                                 [570, 846], [569 ,846], [569, 847], [568 ,847], [568, 848], [561, 848],
                                                 [561, 856], [558 ,856], [558, 848], [551, 848], [551, 847], [550, 847],
                                                 [550, 846], [549 ,846], [549, 845], [555, 845], [555, 829], [558, 829],
                                                 [558, 826]])

    ###КНОПКА ПРЫГУНА###
    pygame.draw.rect(screen, (161, 126, 0), (600, 821, 40, 40))
    pygame.draw.rect(screen, (217, 175, 24), (600, 821, 40, 40), 3)
    pygame.draw.polygon(screen, (217, 175, 24), [[614, 826], [626, 826], [626, 836], [632, 836], [632, 852], [627, 852],
                                                 [627, 857], [623, 857], [623, 852], [617, 852], [617, 857], [613, 857],
                                                 [613, 852], [608, 852], [608, 836], [613, 836]])

    ###НАДПИСЬ УРОВНЯ###
    font = pygame.font.Font(None, 72)
    text_level0 = font.render('Уровень:', True, (0, 0, 0))
    text_level = font.render(level, True, (0, 0, 0))
    screen.blit(text_level0, (120, 80))
    screen.blit(text_level, (350, 80))

    # --- Drawing code should go here

    if marker_start == 1:
        for i in all_players:
            i.move()
        for i in all_enemys:
            i.move()
            
    if all_players or all_enemys:
        hits = pygame.sprite.groupcollide(all_players, all_enemys, False, False)
        if hits:
            #print(hits)
            for unit in hits:
                unit.speed = 0
                hits[unit][0].speed = 0
                all_attack.update({unit: hits[unit][0]})
                all_players.remove(unit)
                all_enemys.remove(hits[unit][0])
            #print(all_attack)

            for i in all_attack:
                thread.start_new_thread(battle, (i, all_attack[i]))

    if marker_start == 1:
        if not(all_enemys):
            marker_finish = 1
        else:
            for en in all_enemys:
                if en.rect.x <= 20:
                    marker_jumper = 0
                    marker_unit = 0
                    pygame.draw.rect(screen, (161, 126, 0), (400, 301, 1140, 400))
                    pygame.draw.rect(screen, (217, 175, 24), (400, 301, 1140, 400), 7)
                    
                    font = pygame.font.Font(None, 72)
                    text_lost = font.render("НЕ поздравляю, ты проиграл", True, (217, 175, 24))
                    screen.blit(text_lost, (540, 381))

                    pygame.draw.rect(screen, (217, 175, 24), (800, 541, 200, 100), 7)

                    font = pygame.font.Font(None, 72)
                    text_lost1 = font.render("блин(", True, (217, 175, 24))
                    screen.blit(text_lost1, (840, 561))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if 800 <= x_mouse <= 1000 and 541 <= y_mouse <= 641:
                                marker_start = 0
                                marker_finish = 0
                                level = '1'
                                count_enemy = 5
                                for en in all_enemys:
                                    all_sprites_list.remove(en)
                                all_enemys.clear()
                                for un in all_players:
                                    all_sprites_list.remove(un)
                                all_players.clear()
    

    ###ПЕРЕХОД НА СЛЕДУЮЩИЙ УРОВЕНЬ###
    if marker_start == 1 and marker_finish == 1:
        marker_jumper = 0
        marker_unit = 0
        pygame.draw.rect(screen, (161, 126, 0), (400, 301, 1140, 400))
        pygame.draw.rect(screen, (217, 175, 24), (400, 301, 1140, 400), 7)
        
        font = pygame.font.Font(None, 72)
        text = font.render("Поздравляю, Вы прошли уровень", True, (217, 175, 24))
        screen.blit(text, (540, 381))

        pygame.draw.rect(screen, (217, 175, 24), (800, 541, 200, 100), 7)

        font = pygame.font.Font(None, 72)
        text1 = font.render("ОК", True, (217, 175, 24))
        screen.blit(text1, (840, 561))

        for en in all_enemys:
            all_sprites_list.remove(en)
        all_enemys.clear()
        
        for un in all_players:
            all_sprites_list.remove(un)
        all_players.clear()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if 800 <= x_mouse <= 1000 and 541 <= y_mouse <= 641:
                    marker_start = 0
                    marker_finish = 0
                    level = str(1 + int(level))
                    count_enemy += 5
            
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
