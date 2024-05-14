#30/4/2024 start date
#First attempt at making the game asteroid

import math
import random
import pygame

pygame.init()
pygame.font.init()

#Create window
HEIGHT = 800
WIDTH = 800
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Asteroid')
FONT = pygame.font.SysFont('Hyperspace', 25)
timer = pygame.time.Clock()
fps = 60

#Load images
large_asteroid_png = pygame.image.load('large_asteroid.png')
medium_asteroid_png = pygame.image.load('medium_asteroid.png')
small_asteroid_png = pygame.image.load('small_asteroid.png')
ship_png = pygame.image.load('ship.png')
bullet_png = pygame.image.load('bullet.png')

#declaring game global variables
score = 0
lives = 3
game_start = False
game_over = False
asteroids_generated = False
game_over_count = 0
asteroid_count = 4

#ship global variables
ship_x = WIDTH/2 - 25
ship_y = HEIGHT/2 - 25
velocityX = 0
velocityY = 0
MAX_SPEED = 10
space_counter = 0

#declaring text
new_game_text = FONT.render('New Game', 0, 'white')

#creating buttons
new_game_button = pygame.draw.rect(SCREEN, 'black', [WIDTH/2 - new_game_text.get_width()/2, HEIGHT/2, new_game_text.get_width(), new_game_text.get_height()])

class Asteroid(pygame.sprite.Sprite):
    '''Creates asteroid objects and handles their movement'''
    def __init__(self, x_pos, y_pos, size):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.size = size
        
        if self.size == 'large':
            self.image = large_asteroid_png
        elif self.size == 'medium':
            self.image = medium_asteroid_png
        elif self.size == 'small':
            self.image = small_asteroid_png
            
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        
        self.vec_asteroid = pygame.math.Vector2
        self.position = self.vec_asteroid(self.rect.x, self.rect.y)
        
        asteroid_vel_x = random.uniform(-2, 2)
        asteroid_vel_y = random.uniform(-2, 2)
        self.asteroid_vel = self.vec_asteroid(asteroid_vel_x, asteroid_vel_y)
        
    def asteroid_movement(self):
        self.position += self.asteroid_vel
        
        if self.size == 'large':
            size = 85
        elif self.size == 'medium':
            size = 50
        elif self.size == 'small':
            size = 26

        if self.position.x >= WIDTH:
            self.position.x = -size
        elif self.position.x <= -size:
            self.position.x = WIDTH
        elif self.position.y <= -size:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT + size:
            self.position.y = -size
        
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        self.x_pos = self.rect.x
        self.y_pos = self.rect.y
        
          
class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = ship_png
        self.rotated_ship = self.image
        
        self.vec_ship = pygame.math.Vector2
        self.position = self.vec_ship(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center = self.position)
        self.vel = self.vec_ship(0, 0)
        self.acceleration = self.vec_ship(0, -0.15)
        self.ship_angle_speed = 0
        self.ship_angle = 0
        self.deceleration = 0.03

    def rotate_ship(self, image, angle):
        #rotates the sprite of the ship
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(self.image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        
        return rot_image
    
    def rotate_acceleration(self):
        # Rotate the acceleration vector.
        self.acceleration.rotate_ip(self.ship_angle_speed)
        self.ship_angle -= self.ship_angle_speed
        if self.ship_angle > 360:
            self.ship_angle -= 360
        elif self.ship_angle < 0:
            self.ship_angle += 360
        
    def handle_keys(self):
        if game_start and not game_over:
            keys = pygame.key.get_pressed()
            
            #handles rotating the ship, and accerlerating forwards
            if keys[pygame.K_a]:
                self.ship_angle_speed = -4
                self.rotated_ship = Player.rotate_ship(self, self.image, self.ship_angle)
                player.rotate_acceleration()
                #print('Turn left')
            elif keys[pygame.K_d]:
                self.ship_angle_speed = 4
                self.rotated_ship = Player.rotate_ship(self, self.image, self.ship_angle)
                player.rotate_acceleration()
                #print('Turn Right')
                
            if keys[pygame.K_w]:
                self.vel += self.acceleration
                #print('Move Forwards')
            elif not keys[pygame.K_w]:
                self.vel *= (1 - self.deceleration)
                
                if self.vel.length() < 0.05:
                    self.vel = pygame.math.Vector2(0, 0)
                
            #max speed
            if self.vel.length() > MAX_SPEED:
                self.vel.scale_to_length(MAX_SPEED)
                
            self.position += self.vel
            self.rect.x = self.position.x
            self.rect.y = self.position.y
            
            #handles shooting from the ship
            if keys[pygame.K_SPACE]:
                global space_counter
                #space_pressed = True
                ship_angle = self.ship_angle % 360
                
                if space_counter > 0:
                    space_counter -= 1
                    #print(space_counter)
                elif space_counter == 0:
                    space_counter = 5
                        
                    if len(sprite_list_bullets) <= 4:
                        
                        ship_center_x = player.position.x + player.rect.width / 2
                        ship_center_y = player.position.y + player.rect.height / 2
                        bullet = Bullet(ship_center_x, (ship_center_y), ship_angle)
                        sprite_list_bullets.add(bullet)
                        #print('Shoot')
                    
    def handle_window(self):
        if self.position.x >= WIDTH:
            self.position.x = -50
        elif self.position.x <= -50:
            self.position.x = WIDTH
        elif self.position.y <= -50:
            self.position.y = HEIGHT
        elif self.position.y > HEIGHT + 50:
            self.position.y = -50
            
    def ship_collision(self):
        #colliding_sprites = pygame.sprite.spritecollide(player, sprite_list_asteroids, True)
        #return colliding_sprites
        #print('player crashed!')
        asteroid_x = 0
        asteroid_y = 0
        asteroid_size = ''
        
        colliding_sprites = pygame.sprite.spritecollide(player, sprite_list_asteroids, True)
        for sprite in colliding_sprites:
            asteroid_x = sprite.x_pos
            asteroid_y = sprite.y_pos
            asteroid_size = sprite.size
        
        return colliding_sprites, asteroid_x, asteroid_y, asteroid_size
    
    def respawn(self):
        self.rect.x = 375
        self.rect.y = 375
        self.position.x = 375
        self.position.y = 375
        self.vel = pygame.math.Vector2(0, 0)
        self.acceleration = self.vec_ship(0, -0.2)
        self.ship_angle_speed = 0
        self.ship_angle = 0
        self.rotated_ship = Player.rotate_ship(self, self.image, self.ship_angle)
        player.rotate_acceleration()
                
    def draw(self, surface):
        #blit yourself at your current position
        if game_start:
            surface.blit(self.rotated_ship, (self.rect.x, self.rect.y))
            
            
class Bullet(Player, pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_png #Load bullet image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.angle = angle
        self.timer = 90
        self.first_fired = 0

        # Calculate the position of the bullet relative to the ship's center based on its angle
        bullet_angle = math.radians(360 - angle + 90 % 360)
        self.vel_x = -math.cos(bullet_angle) * self.speed
        self.vel_y = -math.sin(bullet_angle) * self.speed
        bullet_angle = math.degrees(bullet_angle)

    def update(self):
        '''moves the bullets on the screen'''
        '''currently there's a bug while adding the velocity from the ship, it's added every cycle'''
        '''this means after the bullet it fired, it will continue to gain velocity if the ship gains velocity'''
        # Move the bullet upward
        #Adds the ship velocity to the bullets velocity
        #if not self.first_fired:
        self.first_fired = True
        self.rect.x += player.vel.x
        self.rect.y += player.vel.y
        #else:
        #Moves the bullet based off it's own velocity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        #ticks the timer of each bullet
        self.timer -= 1
        
        #Bullet will disapper after 1s
        if self.rect.x >= WIDTH:
            self.rect.x = -50
        elif self.rect.x <= -50:
            self.rect.x = WIDTH
        elif self.rect.y <= -50:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT + 50:
            self.rect.y = -50
            
        if self.timer == 0:
            self.timer = 90
            self.kill()
        
    def bullet_collision(self):
        asteroid_x = 0
        asteroid_y = 0
        asteroid_size = ''
        
        colliding_bullet_sprites = pygame.sprite.groupcollide(sprite_list_asteroids, sprite_list_bullets, True, True)
        for sprite in colliding_bullet_sprites:
            asteroid_x = sprite.x_pos
            asteroid_y = sprite.y_pos
            asteroid_size = sprite.size
        
        return colliding_bullet_sprites, asteroid_x, asteroid_y, asteroid_size
    
    
def new_game():
    '''resets variables after a new game is started'''
    global score
    global lives
    global game_start
    global game_over
    global asteroids_generated
    global game_over_count
    global asteroid_count

    score = 0
    lives = 3
    game_start = False
    game_over = False
    asteroids_generated = False
    game_over_count = 0
    asteroid_count = 4
    
    sprite_list_asteroids.empty()
    
    player.respawn()


def draw_screen():
    #draw background
    SCREEN.fill('black')
    
    #draw bullets
    for bullet in sprite_list_bullets:
        SCREEN.blit(bullet.image, bullet.rect)
        
    #draw player
    if not game_over:
        player.draw(SCREEN)
      
    #draw asteroids
    for asteroid in sprite_list_asteroids:
        SCREEN.blit(asteroid.image, asteroid.rect)
        
    #create overlay text
    lives_text = FONT.render('Lives: ' + str(lives), 0, 'white')
    score_text = FONT.render('Score: ' + str(score), 0, 'white')
    #acceleration_text = FONT.render('Acceleration: ' + str(player.acceleration), 0 , 'white')
    #position_text = FONT.render('Position: ' + str(player.position), 0 , 'white')
    #velocity_text = FONT.render('Velocity: ' + str(player.vel), 0 , 'white')
    #angle_text = FONT.render('Angle: ' + str(player.ship_angle), 0 , 'white')

    #draw overlay text
    SCREEN.blit(lives_text, [8, 0])
    SCREEN.blit(score_text, [8, 30])
    #SCREEN.blit(acceleration_text, [8, 60])
    #SCREEN.blit(position_text,     [8, 90])
    #SCREEN.blit(velocity_text,     [8, 120])
    #SCREEN.blit(angle_text,        [8, 150])
        
    if not game_start:
        SCREEN.blit(new_game_text, [WIDTH/2 - new_game_text.get_width()/2, HEIGHT/2])
    elif game_over:
        SCREEN.blit(game_over_text, [WIDTH/2 - new_game_text.get_width()/2, HEIGHT/2])
           
#initialize game state
run = True

sprite_list = pygame.sprite.Group()
sprite_list_bullets = pygame.sprite.Group()
sprite_list_asteroids = pygame.sprite.Group()
player = Player(ship_x, ship_y)
sprite_list.add(player)

new_game()

#main game loop
while run:
    timer.tick(fps) #set the fps of the game window
    
    #asteroid movement
    for asteroid in sprite_list_asteroids:
        asteroid.asteroid_movement()
    
    if game_start and not game_over:
        #player movement logic
        player.handle_keys()
        player.handle_window()

        #Update sprite positions
        player.update()
        
        for asteroid in sprite_list_asteroids:
            asteroid.update()
        
        #check for the player colliding with asteroid
        colliding_asteroids, asteroid_x, asteroid_y, asteroid_size = player.ship_collision()
        
        for asteroid in colliding_asteroids:
            lives -= 1
            player.respawn() #resets the players initial position
            
            if asteroid_size == 'large':
                sprite_list_asteroids.add(Asteroid(asteroid_x + 30, asteroid_y + 30, 'medium'))
                sprite_list_asteroids.add(Asteroid(asteroid_x, asteroid_y, 'medium'))
                score += 20
            elif asteroid_size == 'medium':
                sprite_list_asteroids.add(Asteroid(asteroid_x + 20, asteroid_y + 20, 'small'))
                sprite_list_asteroids.add(Asteroid(asteroid_x, asteroid_y, 'small'))
                score += 50
            elif asteroid_size == 'small':
                score += 100
        
        #check for bullet collisions with asteroids
        for bullet in sprite_list_bullets:
            colliding_bullets, asteroid_x, asteroid_y, asteroid_size = bullet.bullet_collision()
            for bullets in colliding_bullets:
                if asteroid_size == 'large':
                    sprite_list_asteroids.add(Asteroid(asteroid_x + 20, asteroid_y + 20, 'medium'))
                    sprite_list_asteroids.add(Asteroid(asteroid_x, asteroid_y, 'medium'))
                    score += 20
                elif asteroid_size == 'medium':
                    sprite_list_asteroids.add(Asteroid(asteroid_x + 20, asteroid_y + 20, 'small'))
                    sprite_list_asteroids.add(Asteroid(asteroid_x, asteroid_y, 'small'))
                    score += 50
                elif asteroid_size == 'small':
                    score += 100
                    
        #Generate random numbers to spawn asteroids 
        if game_start == True and asteroids_generated == False:
            asteroids_generated = True
            initial_asteroid = False
            player_spawn_offset = 100
            for i in range(asteroid_count):
                test = random.randint(0, 3)
                if test == 0:
                    #places asteroids in the top section
                    random_height = random.randint(0, int(HEIGHT/2 - player_spawn_offset))
                    random_width = random.randint(0, WIDTH)
                elif test == 1:
                    #places asteroids in the bottom section
                    random_height = random.randint(int(HEIGHT/2 + player_spawn_offset), HEIGHT)
                    random_width = random.randint(0, WIDTH)
                elif test == 2:
                    #places asteroids in the left section
                    random_height = random.randint(int(HEIGHT/2 - player_spawn_offset), int(HEIGHT/2 + player_spawn_offset))
                    random_width = random.randint(0, int(WIDTH/2 - player_spawn_offset))
                elif test == 3:
                    #places asteroids in the right section
                    random_height = random.randint(int(HEIGHT/2 - player_spawn_offset), int(HEIGHT/2 + player_spawn_offset))
                    random_width = random.randint(int(WIDTH/2 + player_spawn_offset), WIDTH)
                
                sprite_list_asteroids.add(Asteroid(random_width, random_height, 'large'))

    #new level logic
    if len(sprite_list_asteroids) == 0 and game_start:
        asteroids_generated = False
        asteroid_count += 1
    
    #gameover logic
    if lives <= 0:
        game_over_count += 1
        game_over = True
        game_over_text = FONT.render('GAME OVER', 0, 'white')
        if game_over_count == 100:
            new_game()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type == pygame.K_SPACE:
            space_pressed = True
            print('Space')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if new_game_button.collidepoint(event.pos) and not game_start:
                game_start = True
    
    sprite_list.update()
    sprite_list_bullets.update()
    draw_screen()
    pygame.display.update()

pygame.QUIT