import pygame as pg
import time
from additionaly import *

class GameSprite(pg.sprite.Sprite):
    def __init__(self, width, height, x_cord, y_cord, picture):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x_cord
        self.rect.y = y_cord
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        return window

class Player(GameSprite):
    def __init__(self, width, height, x_cord, y_cord, picture):
        super().__init__(width, height, x_cord, y_cord, picture)
        self.speed = 0
        self.x_speed = 0
        self.y_speed = 0
        self.angle = 0
        self.angle_rotate_speed = 0
        self.image_copy = self.image.copy()

    def update(self):
        self.get_speed()
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.angle = (self.angle + self.angle_rotate_speed)%360
        new_image = pg.transform.rotate(self.image_copy, self.angle)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
    
    def get_speed(self):
        if self.angle > 0 and self.angle <=90:
            x_speed = self.speed/90*self.angle
            y_speed = self.speed - x_speed
            self.x_speed = -x_speed
            self.y_speed = -y_speed
        
        if self.angle > 90 and self.angle <=180:
            angle = self.angle - 90
            y_speed = self.speed/90*angle
            x_speed = self.speed - y_speed
            self.x_speed = -x_speed
            self.y_speed = y_speed

        
        if self.angle > 180 and self.angle <=270:
            angle = self.angle - 180
            x_speed = self.speed/90*angle
            y_speed = self.speed - x_speed
            self.x_speed = x_speed
            self.y_speed = y_speed
 
        
        if self.angle > 270 and self.angle < 360:
            angle = self.angle - 270
            y_speed = self.speed/90*angle
            x_speed = self.speed - y_speed
            self.x_speed = x_speed
            self.y_speed = -y_speed

        
        if self.angle == 0:
            self.x_speed = 0
            self.y_speed = -self.speed

window = pg.display.set_mode((window_width, window_height))

back_gr = GameSprite(window_width, window_height, 0, 0, background)

player = Player(50, 50, 500, 500, player_texture)

clock = pg.time.Clock()
run = True

while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_LEFT:
                player.angle_rotate_speed = 5
            elif e.key == pg.K_RIGHT:
                player.angle_rotate_speed = -5
            elif e.key == pg.K_UP:
                player.speed = 5
        elif e.type == pg.KEYUP:
            if e.key == pg.K_LEFT:
                if player.angle_rotate_speed > 0:
                    player.angle_rotate_speed = 0
            elif e.key == pg.K_RIGHT:
                if player.angle_rotate_speed < 0:
                    player.angle_rotate_speed = 0
            elif e.key == pg.K_UP:
                player.speed = 0
                
    pg.display.update()
    player.update()
    back_gr.draw()
    player.draw()
    clock.tick(60)
