import sys
import pygame
from player import player
from main_menu import main_menu
from key_bindings import key_bindings
from debris import debris
import math

class game():
    
    def __init__(self):
        """Main running function"""
        self.windowx = 640
        self.windowy = 800
        pygame.init()
        self.clock = pygame.time.Clock()
        self.set_up_screen()
        self.time_since_last_frame = 0.0
        self.enemy_text = open("enemies.txt").readlines()
        self.enemy_data = self.interp_enemies(self.enemy_text)
        self.debris_list = []
        self.player = player()
        self.distance = 0
        self.worldspeed = 1 #distance per ms for river image movement
        self.riverimg = pygame.image.load("img/riverproxy.png").convert()
        self.landimgl = pygame.image.load("img/landproxy.png").convert()
        #self.landimgr = pygame.image.load("img/landproxy.png").convert()
        self.landimgr = pygame.transform.rotate(self.landimgl, 180)
        self.key_bindings = key_bindings()
        self.screen_rect = pygame.Rect(0,0,self.windowx,self.windowy)
        self.player_killed = False

    def interp_enemies(self, enemy_txt):
        """translate enemies.txt input into a list of tuples"""
        new_data = []
        for entry in enemy_txt:
            someline = entry.split(',')
            #print someline
            new_data.append([int(someline[0]), someline[1], int(someline[2]), int(someline[3])]) #2D Array!
        #Some test code:
        #for en in new_data:
            #print "At time %i, spawn a %s at position (%i, %i)"%(en[0], en[1], en[2], en[3])
        return new_data

    def run(self):
        """Begin running the game"""
        the_menu = main_menu(self)
        the_menu.run(self.screen)
        self.clock.tick()
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.time_since_last_frame = float(self.clock.tick(60))

    def set_up_screen(self):
        """Initialize the window"""
        self.screen = pygame.display.set_mode((self.windowx, self.windowy))
        pygame.display.set_caption("A Game With Koi Fish, Bears, Debris, and DRAGON MODE!!!!111!!!11!!!!1one")
        pygame.mouse.set_visible(0)
    
    def draw(self):
        """Draw all the things!"""
        #Currently, the setup is up to two images dealing with the scrolling river
        riverrect = self.riverimg.get_rect()
        landrectl = self.landimgl.get_rect()
        landrectr = self.landimgr.get_rect()
        ydisp = (self.distance/2)%riverrect.height
        self.screen.blit(self.riverimg, pygame.Rect(0, ydisp, self.windowx, self.windowy))
        self.screen.blit(self.riverimg, pygame.Rect(0, ydisp - riverrect.height, self.windowx, self.windowy))
        self.screen.blit(self.landimgl, pygame.Rect(0, ydisp, self.windowx, self.windowy))
        self.screen.blit(self.landimgl, pygame.Rect(0, ydisp - landrectl.height, self.windowx, self.windowy))
        self.screen.blit(self.landimgr, pygame.Rect(self.windowx - 160, ydisp, self.windowx, self.windowy))
        self.screen.blit(self.landimgr, pygame.Rect(self.windowx - 160, ydisp - landrectr.height, self.windowx, self.windowy))
        self.player.draw(self.screen)
        for e in self.debris_list:
            e.draw(self.screen)
        
    def update(self):
        """Update every frame"""
        self.distance += self.time_since_last_frame * self.worldspeed
        #think about using clock.tick(60) to have a consistent frame rate across different machines
        #^^^See run(self)
        projectiles = self.player.update(self.time_since_last_frame)
        #After updating the player, let's deal with enemies
        #1. Check for enemies we need to add
        for enemy in self.enemy_data:
            if self.distance > enemy[0]:
                #Create the enemy, add it to self.enemies
                #print "It's been %i ms, time to spawn an enemy!"%self.distance
                if enemy[1] == "debris":
                    rdyenemy = debris(enemy[2],-math.pi/2)
                    self.debris_list.append(rdyenemy)
                else:
                    print "INVALID ENEMY!"
                    exit_game()
                #Remove from data
                self.enemy_data.remove(enemy)
        #2. Update Enemies
        for en in self.debris_list:
            en.update(self.time_since_last_frame)
        #3. Remove Enemies that are off screen
        for en in self.debris_list:
            if not(self.screen_rect.colliderect(en.rect)):
                self.debris_list.remove(en)
                #print "killing enemy!"
        #COLLISION
        self.handle_collision(projectiles)
    
    def handle_collision(self, projectiles):
        for i, trash in enumerate(self.debris_list):
            if self.player.rect.colliderect(trash.rect):
                self.player_killed = True
            for bullet in projectiles:
                if bullet.rect.colliderect(trash.rect):
                    self.debris_list.pop(i)

    def handle_events(self):
        """Handle events (such as key presses)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game() #If close button clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.activate_menu()
		#KOI CONTROLS (pardon the intrusion)
				#movement
                if event.key in self.key_bindings.up:
                    self.player.moving[0] = True
                if event.key in self.key_bindings.down:
                    self.player.moving[1] = True
                if event.key in self.key_bindings.left:
                    self.player.moving[2] = True
                if event.key in self.key_bindings.right:
                    self.player.moving[3] = True
				#abilities
                if event.key in self.key_bindings.barrel_left:
                    self.player.barrel[0] = True
                if event.key in self.key_bindings.barrel_right:
                    self.player.barrel[1] = True
                if event.key in self.key_bindings.shoot:
                    self.player.shoot = True
                if event.key in self.key_bindings.dragon:
                    self.player.dragon = True
            if event.type == pygame.KEYUP:
				#cancelling movement
                if event.key in self.key_bindings.up:
                    self.player.moving[0] = False
                if event.key in self.key_bindings.down:
                    self.player.moving[1] = False
                if event.key in self.key_bindings.left:
                    self.player.moving[2] = False
                if event.key in self.key_bindings.right:
                    self.player.moving[3] = False
				#cancelling abilities
                if event.key in self.key_bindings.barrel_left:
                    self.player.barrel[0] = True
                if event.key in self.key_bindings.barrel_right:
                    self.player.barrel[1] = True
                if event.key in self.key_bindings.shoot:
                    self.player.shoot = False

    def activate_menu(self):
        m = main_menu(self)
        m.run(self.screen)
                    
    def exit_game(self):
        """Exit the game"""
        pygame.quit()
        sys.exit()
 
