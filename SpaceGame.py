import pygame as pg
import time
from additionaly import *
pg.font.init()



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
        if self.angle == 0:
            self.y_speed = -self.speed

        elif self.angle > 0 and self.angle <= 45:
            speed_x = self.speed / 45 * self.angle
            speed_y = self.speed
            self.x_speed = -speed_x
            self.y_speed = -speed_y
        
        elif self.angle > 45 and self.angle <= 90:
            speed_y = self.speed - self.speed / 45 * (self.angle-45)
            self.y_speed = -speed_y
            self.x_speed = -self.speed
        
        elif self.angle > 90 and self.angle <=135:
            speed_y = self.speed / 45 * (self.angle-90)
            self.x_speed = -self.speed
            self.y_speed = speed_y
        
        elif self.angle > 135 and self.angle <= 180:
            speed_x = self.speed - self.speed / 45 * (self.angle-135)
            self.x_speed = -speed_x 
            self.y_speed = self.speed
        
        elif self.angle > 180 and self.angle <= 225:
            speed_x = self.speed / 45 * (self.angle - 180)
            self.y_speed = self.speed
            self.x_speed = speed_x
        
        elif self.angle > 225 and self.angle <= 270:
            speed_y = self.speed - self.speed / 45 * (self.angle-225)
            self.y_speed = speed_y
            self.x_speed = self.speed
        
        elif self.angle > 270 and self.angle <= 315:
            speed_y = self.speed / 45 * (self.angle-270)
            self.x_speed = self.speed
            self.y_speed = -speed_y
        
        elif self.angle > 315 and self.angle <= 360:
            speed_x = self.speed - self.speed / 45 * (self.angle - 315)
            self.y_speed = -self.speed
            self.x_speed = speed_x
    
    def print_statistic(self):
        angle = pg.font.Font(None, 20).render('Угол:'+str(self.angle), True, (255, 255, 255))
        speed_x = pg.font.Font(None, 20).render('Скорость X:'+str(self.x_speed), True, (255, 255, 255))
        speed_y = pg.font.Font(None, 20).render('Скорость Y:'+str(self.y_speed), True, (255, 255, 255))
        window.blit(angle, (0, 0))
        window.blit(speed_x, (0, 20))
        window.blit(speed_y, (0, 40))

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
    #player.print_statistic()
    player.draw()
    clock.tick(60)
