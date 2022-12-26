import pygame as pg # Импорт библиотеки Pygame как pg для удобства
import time # Импорт встроенной библиотеки Python время
from additionaly import * # Импорт доп настроек из отдельного модуля
pg.font.init() # Конструктор текстов Pygame

C_WALLS = (217, 217, 217)

mini_player_images = [pg.transform.scale(pg.image.load('images/astronaut_c1.png'), (40, 90)),
                    pg.transform.scale(pg.image.load('images/astronaut_c2.png'), (40, 90)),
                    pg.transform.scale(pg.image.load('images/astronaut_c3.png'), (40, 90))]
#main_font = pg.font.SysFont()
simple_font = pg.font.Font(None, 35)
def print_fps(): # Выводит количество фпс на экран
    fps = simple_font.render(str(round(clock.get_fps())), True,(0,255,0))
    window.blit(fps, (670, 0))

def print_cords(obj): # Показывает на экране расположение объекта по отношению к экрану
    obj_x = obj.rect.x
    obj_y = obj.rect.y
    obj_x_t = simple_font.render(str(obj_x), True, (0, 255, 255))
    obj_y_t = simple_font.render(str(obj_y), True, (0, 255, 255))
    window.blit(obj_x_t, (0, 90))
    window.blit(obj_y_t, (0, 120))

dark = (0, 0, 0)
class GameSprite(pg.sprite.Sprite): # Класс неподвижного объекта
    def __init__(self, width, height, x_cord, y_cord, picture):
        super().__init__()
        
        self.image = pg.transform.scale(pg.image.load(picture), (width, height)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x_cord # Задаёт координату X
        self.rect.y = y_cord # Задаёт координату Y
        self.add(all_sprites)

    def draw(self): # Рисует объект на экране
        window.blit(self.image, (self.rect.x, self.rect.y))
        return window

class MiniPlayer(pg.sprite.Sprite):
    def __init__(self, x_speed=0, y_speed=0, x=25, y=470):
        super().__init__()
        self.image = mini_player_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.stands_on = False
        self.counter = 0
        
        self.direction = 'right'
        self.walk = True

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update_direction(self, direction):
        if self.direction != direction:
            self.direction = direction
        
    def gravitate(self):
        self.y_speed += .25
    
    def jump(self, y):
        if self.stands_on:
            self.y_speed = y
    
    def update(self):
        if self.x_speed != 0:
            if self.direction == 'right':
                self.image = (mini_player_images)[self.walk]
            elif self.direction == 'left':
                self.image = pg.transform.flip((mini_player_images)[self.walk], True, False)
            
            if self.counter == 0:
                
                self.counter = 2
                self.walk = not self.walk
            
            else:
                self.counter -= 1
        else:
            if self.direction == 'right':
                self.image = (mini_player_images)[0]
            else:
                self.image = pg.transform.flip((mini_player_images)[0], True, False)
        
        self.rect.x += self.x_speed
        
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = pg.sprite.spritecollide(self, barriers, False)
        
        if self.x_speed > 0: # идем направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # если коснулись сразу нескольких, то правый край - минимальный из возможных
        
        elif self.x_speed < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # если коснулись нескольких стен, то левый край - максимальный
        
        self.gravitate()
        self.rect.y += self.y_speed
        
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = pg.sprite.spritecollide(self, barriers, False)
        
        if self.y_speed > 0: # идем вниз
            for p in platforms_touched:
                self.y_speed = 0
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
        
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
                    self.stands_on = p
        
        elif self.y_speed < 0: # идем вверх
            self.stands_on = False # пошли наверх, значит, ни на чем уже не стоим!
        
            for p in platforms_touched:
                self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
                self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали

class Wall(pg.sprite.Sprite):
    def __init__(self, **args):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([args['width'], args['height']])
        if args.get('color') != None:
            self.image.fill(args['color'])
        self.rect = self.image.get_rect()
        self.rect.x = args['x']
        self.rect.y = args['y']
        self.add(barriers, all_sprites)

def create_map1():
    platform = Wall(width=700, height=40, x=0, y=560, color=C_WALLS)
    platform = Wall(width=15, height=560, x=0, y=0, color=C_WALLS)
    platform = Wall(width=15, height=560, x=685, y=0, color=C_WALLS)
    platform = Wall(width=210, height=20, x=15, y=440, color=C_WALLS)
    platform = Wall(width=115, height=20, x=570, y=340, color=C_WALLS)
    platform = Wall(width=100, height=20, x=15, y=320, color=C_WALLS)
    platform = Wall(width=100, height=20, x=220, y=250, color=C_WALLS)
    platform = Wall(width=100, height=20, x=430, y=400, color=C_WALLS)
    platform = Wall(width=90, height=20, x=595, y=45, color=C_WALLS)
    platform = Wall(width=95, height=20, x=75, y=135, color=C_WALLS)
    platform = Wall(width=85, height=20, x=485, y=200, color=C_WALLS)
    platform = Wall(width=40, height=20, x=645, y=250, color=C_WALLS)
    platform = Wall(width=130, height=20, x=330, y=130, color=C_WALLS)

barriers = pg.sprite.Group()
all_sprites = pg.sprite.Group()
create_map1()
mini_player = MiniPlayer()

main_game = False
window = pg.display.set_mode((window_width, window_height))
clock = pg.time.Clock()

run = True

while run:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_LEFT or e.key == pg.K_a:
                mini_player.update_direction('left')
                mini_player.x_speed = -4
                
            elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                mini_player.update_direction('right')
                mini_player.x_speed = 4
                
            elif e.key == pg.K_UP or e.key == pg.K_w:
                mini_player.jump(-8)

        elif e.type == pg.KEYUP:
            if e.key == pg.K_LEFT or e.key == pg.K_a:
                mini_player.x_speed = 0
                
            elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                mini_player.x_speed = 0

    pg.display.update()
    mini_player.update()
    window.fill((0, 0, 0))
    all_sprites.draw(window)
    mini_player.draw()
    clock.tick(60)
