import pygame as pg # Импорт библиотеки Pygame как pg для удобства
import time # Импорт встроенной библиотеки Python время
from additionaly import * # Импорт доп настроек из отдельного модуля
pg.font.init() # Конструктор текстов Pygame

C_WALLS = (217, 217, 217)

mini_player_images = [pg.transform.scale(pg.image.load('images/astronaut_c3.png'), (40, 90)),
                    pg.transform.scale(pg.image.load('images/astronaut_c2.png'), (40, 90)),
                    pg.transform.scale(pg.image.load('images/astronaut_c1.png'), (40, 90))]
#main_font = pg.font.SysFont()
simple_font = pg.font.Font(None, 35)
def print_fps(): # Выводит количество фпс на экран
    fps = simple_font.render(str(round(clock.get_fps())), True,(0,255,0))
    window.blit(fps, (670, 0))

def game_timer(ticks, over_time):
    time = 25 - round(ticks/60)
    time_txt = simple_font.render('Время:'+str(time), True,(0, 190, 185))
    window.blit(time_txt, (window_width//2-50, 40))
    return time

def print_cords(obj): # Показывает на экране расположение объекта по отношению к экрану
    obj_x = obj.rect.x
    obj_y = obj.rect.y
    obj_x_t = simple_font.render(str(obj_x), True, (0, 255, 255))
    obj_y_t = simple_font.render(str(obj_y), True, (0, 255, 255))
    window.blit(obj_x_t, (0, 90))
    window.blit(obj_y_t, (0, 120))

dark = (0, 0, 0)
class GameSpriteMini(pg.sprite.Sprite): # Класс неподвижного объекта Для мини игр
    def __init__(self, width, height, x_cord, y_cord, picture):
        super().__init__()
        
        self.image = pg.transform.scale(pg.image.load(picture), (width, height)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x_cord # Задаёт координату X
        self.rect.y = y_cord # Задаёт координату Y
        self.add(all_sprites_mini_games)

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

        self.add(all_sprites_mini_games)

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
                
                self.counter = 3
                self.walk = not self.walk
            
            else:
                self.counter -= 1
        else:
            if self.direction == 'right':
                self.image = (mini_player_images)[2]
            else:
                self.image = pg.transform.flip((mini_player_images)[2], True, False)
        
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
        self.add(barriers, all_sprites_mini_games)

def create_map1():
    # Для всех комнат
    platform1 = Wall(width=1950, height=40, x=0, y=560, color=C_WALLS) # Объект 1 пол
    # Комната 1
    platform = Wall(width=15, height=560, x=0, y=0, color=C_WALLS) # Объект 2 стена
    # Для всех комнат
    platform = Wall(width=15, height=410, x=685, y=150, color=C_WALLS) # Объект 3 стена
    # Комната 1
    platform = Wall(width=210, height=20, x=15, y=440, color=C_WALLS) # Объект 4 платформа
    platform = Wall(width=115, height=20, x=570, y=340, color=C_WALLS) # Объект 5 платформа
    platform = Wall(width=100, height=20, x=15, y=320, color=C_WALLS) # Объект 6 платформа
    platform = Wall(width=100, height=20, x=220, y=250, color=C_WALLS) # Объект 7 платформа
    platform = Wall(width=100, height=20, x=430, y=400, color=C_WALLS) # Объект 8 платформа
    # Для всех комнат
    platform = Wall(width=2080, height=20, x=15, y=0, color=C_WALLS) # Объект 9 потолок так получилось не спрашивайте
    # Комната 1
    platform = Wall(width=95, height=20, x=75, y=135, color=C_WALLS) # Объект 10 платформа
    platform = Wall(width=85, height=20, x=485, y=200, color=C_WALLS) # Объект 11 платформа
    platform = Wall(width=40, height=20, x=645, y=250, color=C_WALLS) # Объект 12 платформа
    platform = Wall(width=130, height=20, x=330, y=130, color=C_WALLS) # Объект 13 платформа
    # Подсказка перед первой комнатой
    east = GameSpriteMini(40, 60, -300, 10, easter) # А найди :)
    # Комната 2
    platform = Wall(width=500, height=20, x=700, y=150, color=C_WALLS) # Объект 14
    platform = Wall(width=540, height=20, x=845, y=265, color=C_WALLS) # Объект 15
    platform = Wall(width=530, height=20, x=785, y=380, color=C_WALLS) # Объект 16
    platform1 = Wall(width=15, height=440, x=1385, y=20, color=C_WALLS) # Объект 17 наложен под объект
    # Комната 3
    platform = Wall(width=465, height=20, x=1400, y=440, color=C_WALLS) 
    platform = Wall(width=460, height=20, x=1470, y=320, color=C_WALLS) 
    platform = Wall(width=115, height=20, x=1400, y=200, color=C_WALLS) 
    platform = Wall(width=360, height=20, x=1570, y=120, color=C_WALLS) 
    platform = Wall(width=20, height=440, x=1930, y=120, color=C_WALLS) 
    platform = Wall(width=15, height=580, x=2080, y=20, color=C_WALLS) 

barriers = pg.sprite.Group()
all_sprites_mini_games = pg.sprite.Group()
mini_player = MiniPlayer()

main_game = False
window = pg.display.set_mode((window_width, window_height))
clock = pg.time.Clock()
timer_ticks = 0 
seconds = timer_ticks//60
run = True

create_map1()
platform1 = Wall(width=15, height=560, x=1385, y=20, color=C_WALLS) 
platform_joke = Wall(width=20, height=160, x=880, y=400, color=C_WALLS)
key1 = GameSpriteMini(10, 10, 870, 550, key_img)
ship_part_1 = GameSpriteMini(30, 30, 2000, 540, ship_part_1_img)


right_bound = window_width//2 + 50
left_bound = window_width//2 - 50

win_game_1 = False
lose_game_1 = False


while run:
    if win_game_1 != False or lose_game_1 != False:
        run = False
    else:
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
                elif e.key == pg.K_r:
                    all_sprites_mini_games.empty()
                    barriers.empty()                    
                    create_map1()
                    mini_player = MiniPlayer()
                    timer_ticks = 0
                    platform1 = Wall(width=15, height=560, x=1385, y=20, color=C_WALLS) 
                    platform_joke = Wall(width=20, height=160, x=880, y=400, color=C_WALLS)
                    key1 = GameSpriteMini(10, 10, 870, 550, key_img)
                    ship_part_1 = GameSpriteMini(30, 30, 2000, 540, ship_part_1_img)

            elif e.type == pg.KEYUP:
                if e.key == pg.K_LEFT or e.key == pg.K_a:
                    if mini_player.x_speed < 0:
                        mini_player.x_speed = 0

                elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                    if mini_player.x_speed > 0:
                        mini_player.x_speed = 0

        if (mini_player.rect.x > right_bound and mini_player.x_speed > 0) or (mini_player.rect.x < left_bound and mini_player.x_speed < 0):
            for s in all_sprites_mini_games:
                s.rect.x -= mini_player.x_speed
    
        if pg.sprite.collide_rect(mini_player, key1):
            all_sprites_mini_games.remove(key1) 
            barriers, all_sprites_mini_games.remove(platform_joke, platform1)
        
        if pg.sprite.collide_rect(mini_player, ship_part_1):
            win_game_1 = True


        pg.display.update()
        mini_player.update()
        window.fill((0, 0, 0))
        all_sprites_mini_games.draw(window)
        print_fps()
        game_time = game_timer(timer_ticks, 25) 
        if game_time <= 0:
            lose_game_1 = False

        timer_ticks+=1
        clock.tick(60)
