from typing import Any
import pygame
from os.path import join
from random import randint, uniform



class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (screen_Width/2, screen_Height/2))
        self.direction = pygame.Vector2()
        self.speed = 350
    
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

        self.mask = pygame.mask.from_surface(self.image)
        

        

    def laser_timer(self):
        if self.can_shoot == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self. cooldown_duration:
                self.can_shoot = True


    def update(self,dt):
        
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys [pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surface, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        
        self.laser_timer()

        
class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = (randint(0, screen_Width), randint(0, screen_Height)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, pos, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
    
    
class Meteor(pygame.sprite.Sprite):


    def __init__(self, surface, pos, groups):
        super().__init__(groups)
        self.original_surface = surface
        self.image = self.original_surface
        self.rect = self.image.get_frect(center = pos)
        self.star_time = pygame.time.get_ticks()
        self.lifetime = 4000
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint (400,500)

        self.rotation_speed = randint(50,150)
        self.rotation = 0



    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.star_time >= self.lifetime:
            self.kill()

        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surface, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len((self.frames) )]
        else:
            self.kill()


def collisions():
    global running

    collided_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collided_sprites:
        running = False
        

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play() 
def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surface = font.render( "SCORE: " +  str(current_time), True, (240,240,240))
    text_rect = text_surface.get_frect(midbottom = (screen_Width/2, screen_Height - 50))
    pygame.draw.rect(screen, (240,240,240), text_rect.inflate(40,10).move(0,-7), 3, 3)
    screen.blit(text_surface, text_rect)

pygame.init()
screen_Width, screen_Height = 1280, 720
screen = pygame.display.set_mode((screen_Width, screen_Height))
running = True
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()



laser_surface = pygame.image.load(join("images", "laser.png")).convert_alpha()
meteor_surface = pygame.image.load(join("images", "meteor.png")).convert_alpha()
star_surface = pygame.image.load(join("images", "star.png")).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surface)
player = Player(all_sprites)
font = pygame.font.Font(join("images", "Oxanium-Bold.ttf"), 40)
explosion_frames = [pygame.image.load(join("images", "explosion", f'{i}.png')).convert_alpha() for i in range(21)]
laser_sound = pygame.mixer.Sound(join("audio", "laser.wav"))
laser_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound(join("audio", "explosion.wav"))
explosion_sound.set_volume(0.2)
game_music = pygame.mixer.Sound(join("audio", "game_music.wav"))
game_music.set_volume(0.2)
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 450)
game_music.play(loops = -1)


# game loop
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x,y = randint(0, screen_Width), randint(-200, -100)
            Meteor(meteor_surface, (x,y), (all_sprites, meteor_sprites))  
        
    all_sprites.update(dt)
    collisions()
    screen.fill("#3a2e3f")
    display_score()
    all_sprites.draw(screen)

    pygame.display.update()


pygame.quit()