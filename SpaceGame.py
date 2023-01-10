import pygame as pg # Импорт библиотеки Pygame как pg для удобства
import time # Импорт встроенной библиотеки Python время
from additionaly import * # Импорт доп настроек из отдельного модуля
from random import randint # Рандом
pg.font.init() # Конструктор текстов Pygame
pg.init()
# Дополнительно цвета и шрифты
Blue_C = (0, 255, 225) 
Laser_C = (187, 4, 4)
Border_C = (19, 0, 163)

simple_font = pg.font.Font(None, 35)
big_font = pg.font.Font(None, 60)
# Для первой мини игры
C_WALLS = (217, 217, 217)
dark = (0, 0, 0) # Чёрный цвет
mini_player_images = [pg.transform.scale(pg.image.load('images/astronaut_c3.png'), (40, 90)), # Персонаж
                    pg.transform.scale(pg.image.load('images/astronaut_c2.png'), (40, 90)),
                    pg.transform.scale(pg.image.load('images/astronaut_c1.png'), (40, 90))]

def game_timer(ticks, over_time): # Таймер для игры
    time = over_time - round(ticks/60)
    time_txt = simple_font.render('Время:'+str(time), True,(0, 190, 185))
    window.blit(time_txt, (window_width//2-50, 40))
    return time

def game_stopwatch(ticks, color, pos): # Таймер для игры
    time = round(ticks/60)
    time_txt = simple_font.render('Время:'+str(time), True,(color))
    window.blit(time_txt, (pos))
    return time

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

def print_hp(object):
    pass

class GameSpriteMini(pg.sprite.Sprite): # Класс неподвижного объекта Для мини игр
    def __init__(self, width, height, x_cord, y_cord, picture, minigame):
        super().__init__()
        
        self.image = pg.transform.scale(pg.image.load(picture), (width, height)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x_cord # Задаёт координату X
        self.rect.y = y_cord # Задаёт координату Y
        self.minigame = minigame
        if self.minigame == 'astrorun':
            self.add(all_sprites_mini_games)
        if self.minigame == 'labirint':
            self.add(all_sprites_mini_game_2)

    def draw(self): # Рисует объект на экране
        window.blit(self.image, (self.rect.x, self.rect.y))
        return window

class MiniPlayer(pg.sprite.Sprite): # Класс игрок для мини игр
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

class Wall(pg.sprite.Sprite): # Класс стена(платформа) для мини игр
    def __init__(self, **args):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([args['width'], args['height']])
        if args.get('color') != None:
            self.image.fill(args['color'])
        self.rect = self.image.get_rect()
        self.rect.x = args['x']
        self.rect.y = args['y']
        self.minigame = args['minigame']

        if self.minigame == 'astrorun':
            self.add(barriers, all_sprites_mini_games)

        if self.minigame == 'labirint':
            self.add(barriers_1, all_sprites_mini_game_2)
        if self.minigame == 'main_game':
            self.add(mg_borders, all_sprites)

class GameSprite(pg.sprite.Sprite): # Класс неподвижного объекта
    def __init__(self, width, height, x_cord, y_cord, picture, planet=False, mini_game=False):
        super().__init__()
        
        self.image = pg.transform.scale(pg.image.load(picture), (width, height)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x_cord # Задаёт координату X
        self.rect.y = y_cord # Задаёт координату Y
        self.add(all_sprites)
        self.planet = planet
        self.possible_game = True
        if self.planet:
            self.add(planets)
            if self.possible_game:
                self.mini_game = False


    def draw(self): # Рисует объект на экране
        window.blit(self.image, (self.rect.x, self.rect.y))
        return window


class Player(GameSprite): # Класс игрока
    def __init__(self, width, height, x_cord, y_cord, picture, hp, **args):
        super().__init__(width, height, x_cord, y_cord, picture)
        #self.moving_img = args['image_m']
        self.speed = 0 # Максимальная скорость от которой идут все расчёты
        self.x_speed = 0 # Перемещение по координате X
        self.y_speed = 0 # Перемещение по координате Y
        self.angle = 0 # Угол объекта
        self.angle_rotate_speed = 0 # Скорость вращения
        self.image_copy = self.image.copy() # Дополнительная картинка что бы основная не ломалась при вращении
        self.planets_touched = pg.sprite.spritecollide(self, planets, False)
        self.hp = hp
        self.mini_game = args['mini_game']
        self.collide_border = False
        all_sprites.remove(self) # Мне было лень искать другие пути

    

    def update(self): # Метод обновляющий положение персонажа
        
        if main_game:
            #if self.speed != 0:
             #   self.image = self.moving_img

            self.angle = (self.angle + self.angle_rotate_speed)%360 # Изменение угла (вращение)
        
            self.get_speed() # Метод для задания скорости в зависимости от угла
        
            new_image = pg.transform.rotate(self.image_copy, self.angle) # Создание картинки объекта после вращения
        
            old_center = self.rect.center # "Старый центр" для уравнивания объекта при вращении
        
            self.image = new_image # Замена картинки на обновлённую
            self.rect = self.image.get_rect() # Обновление квадрата персонажа
            self.rect.center = old_center # Смена координаты центра для уравнивания
        
        #self.rect.x += self.x_speed # Обновление координаты X в зависимости от скорости
        #self.rect.y += self.y_speed # Обновление координаты Y в зависимости от скорости
        # Временное решение чтобы игрок не выходил за экран

        self.planets_touched = pg.sprite.spritecollide(self, planets, False)
        if len(self.planets_touched) != 0:
            for p in self.planets_touched:
                if p.possible_game:
                    p.mini_game = True
        
        if pg.sprite.spritecollide(self, mg_borders, False):
            
            self.collide_border = True

            if self.y_speed > 0 and self.angle >= 135 and self.angle <= 225:
                self.angle = 0
                self.y_speed = 10

            elif self.y_speed < 0 and (self.angle <= 45 or self.angle >= 315):
                self.angle = 180
                self.y_speed = -10

            elif self.x_speed > 0:
                self.angle = 90
                self.x_speed = 10

            elif self.x_speed < 0:
                self.x_speed = -10
                self.angle = 270
    
    def stop_game(self):
        if len(self.planets_touched) != 0:
            for p in self.planets_touched:
                p.possible_game = False
                p.mini_game = False
                
    def return_p_cords(self):
        x = 0
        y = 0
        if len(self.planets_touched) != 0:
            x = self.planets_touched[0].rect.x  
            y = self.planets_touched[0].rect.y
        return (x, y)

    def get_speed(self): # Метод для задания скорости в зависимости от угла
        if self.angle == 0: # Если угол равен нулю то скорость по Y будет равна максимальной скорости перемещения 
            self.y_speed = -self.speed # Обе скорости отрицательны
            self.x_speed = 0

        if self.angle > 0 and self.angle <= 45: # Если угол больше нуля и меньше или равен 45
                                                # cкорость по x будет увеличиваться в зависимости от угла
            speed_x = self.speed / 45 * self.angle # Максимальная скорость делится на максимальный угол и умножается на нынещний угол
            self.x_speed = round(-speed_x) # Скорость по координате X будет отрицательной расчёты выше
            self.y_speed = round(-self.speed) # Скорость по координате Y менятся не будет будет равна максимальной

        
        if self.angle > 45 and self.angle <= 90: # Если угол выше 45 но меньше или равен 90
            speed_y = self.speed - self.speed / 45 * (self.angle-45) # Тут добавляются 2 переменные так как скорость по координате Y
                                                     # Будет уменьшаться в зависимости от угла -45 так как 90-45 = 45 или же                                                # 46-45 = 1 градус
            self.y_speed = round(-speed_y) # Также обе скорости отрицательны
            self.x_speed = round(-self.speed) # Скорость по X не изменяется и равна максимальной
        
        if self.angle > 90 and self.angle <=135: # Если угол выше 90 но меньше или равен 135
            speed_y = self.speed / 45 * (self.angle-90) # Скорость по Y будет пропорционально увеличиваться 
            self.y_speed = round(speed_y)
            self.x_speed = round(-self.speed) # Скорость по X остаётся отрицательной менятся не будет, равна максимальной
             # Скорость по Y будет положительной
        
        if self.angle > 135 and self.angle <= 180: # Если угол выше 135 но меньше или равен 180
            speed_x = self.speed - self.speed / 45 * (self.angle-135) # Скорость по X уменьшается
            self.x_speed = round(-speed_x) # Скорость по X также будет отрицательной 
            self.y_speed = round(self.speed) # Скорость по Y менятся не будет и будет равна максимальной
        
        if self.angle > 180 and self.angle <= 225: # Если угол выше 180 не меньше или равен 225
            speed_x = self.speed / 45 * (self.angle - 180) # Скорость X Будет увеличиваться
            self.x_speed = round(speed_x)
            self.y_speed = round(self.speed) # Скорость по Y будет равна максимальной
                # Обе скорости будут положительны
        
        if self.angle > 225 and self.angle <= 270: # Дальше по тому же принципу
            speed_y = self.speed - self.speed / 45 * (self.angle-225)
            self.y_speed = round(speed_y)
            self.x_speed = round(self.speed)
        
        if self.angle > 270 and self.angle <= 315:
            speed_y = self.speed / 45 * (self.angle-270)
            self.y_speed = round(-speed_y)
            self.x_speed = round(self.speed)
            
        
        if self.angle > 315 and self.angle <= 360:
            speed_x = self.speed - self.speed / 45 * (self.angle - 315)
            self.x_speed = round(speed_x)
            self.y_speed = round(-self.speed)
            
        
        # Если угол от 0 до 180 то скорость по X будет отрицательна т.е лево
        # Если угол от 180 до 0 то скорость по X будет положительная т.е. право
        # Если угол от 90 до 270 то скорость по Y будет положительна т.е низ
        # Если угол от 270 до 90 то скорость по Y будет отрицательна т.е верх
    
    def print_statistic(self): # Выводит статистику угол и скорости, игрокам не обязательно
        angle = pg.font.Font(None, 20).render('Угол:'+str(self.angle), True, (255, 255, 255)) # Создаёт объект текст и берёт переменные
        speed_x = pg.font.Font(None, 20).render('Скорость X:'+str(self.x_speed), True, (255, 255, 255)) 
        speed_y = pg.font.Font(None, 20).render('Скорость Y:'+str(self.y_speed), True, (255, 255, 255)) 
        window.blit(angle, (0, 0)) # Выводит текст на экран по координате
        window.blit(speed_x, (0, 20))
        window.blit(speed_y, (0, 40))

class LabirintPlayer(pg.sprite.Sprite):
    def __init__(self, **args):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([args['width'], args['height']])
        if args.get('color') != None:
            self.image.fill(args['color'])
        self.rect = self.image.get_rect()
        self.rect.x = args['x']
        self.rect.y = args['y']
        self.add(all_sprites_mini_game_2)
    
    def update(self, x, y):
        self.rect.center = x, y
        if pg.sprite.spritecollide(lab_player, barriers_1, False, False):
            reset_lab()
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        #return window

def create_map1(): # Функция создающая основные стены для мини игры
    # Для всех комнат
    platform1 = Wall(width=1950, height=40, x=0, y=560, color=C_WALLS, minigame='astrorun') # Объект 1 пол
    # Комната 1
    platform = Wall(width=15, height=560, x=0, y=0, color=C_WALLS, minigame='astrorun') # Объект 2 стена
    # Для всех комнат
    platform = Wall(width=15, height=410, x=685, y=150, color=C_WALLS, minigame='astrorun') # Объект 3 стена
    # Комната 1
    platform = Wall(width=210, height=20, x=15, y=440, color=C_WALLS, minigame='astrorun') # Объект 4 платформа
    platform = Wall(width=115, height=20, x=570, y=340, color=C_WALLS, minigame='astrorun') # Объект 5 платформа
    platform = Wall(width=100, height=20, x=15, y=320, color=C_WALLS, minigame='astrorun') # Объект 6 платформа
    platform = Wall(width=100, height=20, x=220, y=250, color=C_WALLS, minigame='astrorun') # Объект 7 платформа
    platform = Wall(width=100, height=20, x=430, y=400, color=C_WALLS, minigame='astrorun') # Объект 8 платформа
    # Для всех комнат
    platform = Wall(width=2080, height=20, x=15, y=0, color=C_WALLS, minigame='astrorun') # Объект 9 потолок так получилось не спрашивайте
    # Комната 1
    platform = Wall(width=95, height=20, x=75, y=135, color=C_WALLS, minigame='astrorun') # Объект 10 платформа
    platform = Wall(width=85, height=20, x=485, y=200, color=C_WALLS, minigame='astrorun') # Объект 11 платформа
    platform = Wall(width=40, height=20, x=645, y=250, color=C_WALLS, minigame='astrorun') # Объект 12 платформа
    platform = Wall(width=130, height=20, x=330, y=130, color=C_WALLS, minigame='astrorun') # Объект 13 платформа
    # Подсказка перед первой комнатой
    east = GameSpriteMini(40, 60, -300, 10, easter, 'astrorun') # А найди :)
    # Комната 2
    platform = Wall(width=500, height=20, x=700, y=150, color=C_WALLS, minigame='astrorun') # Объект 14
    platform = Wall(width=540, height=20, x=845, y=265, color=C_WALLS, minigame='astrorun') # Объект 15
    platform = Wall(width=530, height=20, x=785, y=380, color=C_WALLS, minigame='astrorun') # Объект 16
    platform1 = Wall(width=15, height=440, x=1385, y=20, color=C_WALLS, minigame='astrorun') # Объект 17 наложен под объект
    # Комната 3
    platform = Wall(width=465, height=20, x=1400, y=440, color=C_WALLS, minigame='astrorun') 
    platform = Wall(width=460, height=20, x=1470, y=320, color=C_WALLS, minigame='astrorun') 
    platform = Wall(width=115, height=20, x=1400, y=200, color=C_WALLS, minigame='astrorun') 
    platform = Wall(width=360, height=20, x=1570, y=120, color=C_WALLS, minigame='astrorun') 
    platform = Wall(width=20, height=440, x=1930, y=120, color=C_WALLS, minigame='astrorun') 
    platform = Wall(width=15, height=580, x=2080, y=20, color=C_WALLS, minigame='astrorun') 

def create_planets():
    Planet1 = GameSprite(600, 500, 1220, 900, 'images/planet1.png', True)

def reset_astrorun():
    global mini_player, platform1, platform_joke, key1, ship_part_1, timer_ticks
    all_sprites_mini_games.empty()
    barriers.empty()                    
    create_map1()
    mini_player = MiniPlayer()
    timer_ticks = 0
    platform1 = Wall(width=15, height=560, x=1385, y=20, color=C_WALLS, minigame='astrorun') 
    platform_joke = Wall(width=20, height=160, x=880, y=400, color=C_WALLS, minigame='astrorun')
    key1 = GameSpriteMini(10, 10, 870, 550, key_img, 'astrorun')
    ship_part_1 = GameSpriteMini(30, 30, 2000, 540, ship_part_1_img, 'astrorun')

def create_labirint():
    barrier = Wall(width = 700, height=10, x=0, y=0, color=Blue_C, minigame='labirint') # 1
    barrier = Wall(width = 10, height=590, x=0, y=10, color=Blue_C, minigame='labirint') # 2
    barrier = Wall(width = 690, height=10, x=10, y=590, color=Blue_C, minigame='labirint') # 3
    barrier = Wall(width = 10, height=590, x=690, y=10, color=Blue_C, minigame='labirint') # 4
    barrier = Wall(width = 10, height=90, x=290, y=10, color=Blue_C, minigame='labirint') # 5
    barrier = Wall(width = 10, height=100, x=410, y=10, color=Blue_C, minigame='labirint') # 6
    barrier = Wall(width = 70, height=10, x=290, y=100, color=Blue_C, minigame='labirint') # 7
    barrier = Wall(width = 10, height=120, x=640, y=470, color=Blue_C, minigame='labirint') # 8
    barrier = Wall(width = 440, height=10, x=210, y=145, color=Blue_C, minigame='labirint') # 9
    barrier = Wall(width = 10, height=70, x=450, y=40, color=Blue_C, minigame='labirint') # 10
    barrier = Wall(width = 150, height=10, x=545, y=40, color=Blue_C, minigame='labirint') # 11
    barrier = Wall(width = 200, height=20, x=460, y=90, color=Blue_C, minigame='labirint') # 12
    barrier = Wall(width = 110, height=10, x=580, y=420, color=Blue_C, minigame='labirint') # 13
    barrier = Wall(width = 10, height=120, x=580, y=430, color=Blue_C, minigame='labirint') # 14
    barrier = Wall(width = 220, height=10, x=360, y=540, color=Blue_C, minigame='labirint') # 15
    barrier = Wall(width = 10, height=70, x=350, y=480, color=Blue_C, minigame='labirint') # 16
    barrier = Wall(width = 70, height=10, x=280, y=480, color=Blue_C, minigame='labirint') # 17
    barrier = Wall(width = 10, height=50, x=270, y=490, color=Blue_C, minigame='labirint') # 18
    barrier = Wall(width = 10, height=25, x=310, y=565, color=Blue_C, minigame='labirint') # 19
    barrier = Wall(width = 70, height=10, x=200, y=530, color=Blue_C, minigame='labirint') # 20
    barrier = Wall(width = 10, height=100, x=150, y=490, color=Blue_C, minigame='labirint') # 21
    barrier = Wall(width = 10, height=90, x=200, y=445, color=Blue_C, minigame='labirint') # 22
    barrier = Wall(width = 80, height=10, x=120, y=445, color=Blue_C, minigame='labirint') # 23
    barrier = Wall(width = 10, height=100, x=110, y=445, color=Blue_C, minigame='labirint') # 24
    barrier = Wall(width = 10, height=160, x=60, y=385, color=Blue_C, minigame='labirint') # 25
    barrier = Wall(width = 170, height=10, x=60, y=375, color=Blue_C, minigame='labirint') # 26
    barrier = Wall(width = 210, height=10, x=60, y=320, color=Blue_C, minigame='labirint') # 27
    barrier = Wall(width = 10, height=170, x=270, y=320, color=Blue_C, minigame='labirint') # 28
    barrier = Wall(width = 310, height=10, x=10, y=260, color=Blue_C, minigame='labirint') # 29
    barrier = Wall(width = 10, height=170, x=320, y=260, color=Blue_C, minigame='labirint') # 30
    barrier = Wall(width = 130, height=10, x=330, y=420, color=Blue_C, minigame='labirint') # 31 
    barrier = Wall(width = 120, height=10, x=410, y=480, color=Blue_C, minigame='labirint') # 32 
    barrier = Wall(width = 10, height=60, x=460, y=420, color=Blue_C, minigame='labirint') # 33 
    barrier = Wall(width = 10, height=110, x=520, y=370, color=Blue_C, minigame='labirint') # 34
    barrier = Wall(width = 95, height=10, x=380, y=360, color=Blue_C, minigame='labirint') # 35
    barrier = Wall(width = 10, height=40, x=465, y=320, color=Blue_C, minigame='labirint') # 36
    barrier = Wall(width = 215, height=10, x=475, y=320, color=Blue_C, minigame='labirint') # 37
    barrier = Wall(width = 115, height=10, x=530, y=370, color=Blue_C, minigame='labirint') # 38 
    barrier = Wall(width = 90, height=10, x=330, y=310, color=Blue_C, minigame='labirint') # 39
    barrier = Wall(width = 275, height=10, x=415, y=260, color=Blue_C, minigame='labirint') # 40
    barrier = Wall(width = 10, height=65, x=415, y=195, color=Blue_C, minigame='labirint') # 41 
    barrier = Wall(width = 10, height=90, x=250, y=10, color=Blue_C, minigame='labirint') # 42
    barrier = Wall(width = 365, height=10, x=50, y=195, color=Blue_C, minigame='labirint') # 43
    barrier = Wall(width = 10, height=105, x=200, y=50, color=Blue_C, minigame='labirint') # 44
    barrier = Wall(width = 55, height=10, x=150, y=50, color=Blue_C, minigame='labirint') # 45
    barrier = Wall(width = 10, height=50, x=140, y=10, color=Blue_C, minigame='labirint') # 46
    barrier = Wall(width = 10, height=145, x=50, y=50, color=Blue_C, minigame='labirint') # 47
    barrier = Wall(width = 80, height=10, x=60, y=95, color=Blue_C, minigame='labirint') # 48
    barrier = Wall(width = 100, height=10, x=100, y=145, color=Blue_C, minigame='labirint') # 49
    barrier = Wall(width = 180, height=10, x=465, y=200, color=Blue_C, minigame='labirint') # 50
    barrier = Wall(width = 10, height=45, x=530, y=155, color=Blue_C, minigame='labirint') # 51
    barrier = Wall(width = 50, height=10, x=10, y=480, color=Blue_C, minigame='labirint') # 52
    barrier = Wall(width = 10, height=45, x=650, y=110, color=Blue_C, minigame='labirint') # 53

def reset_lab():
    global pause, lab_attemps
    lab_attemps -= 1
    pause = True
    lab_player.rect.x = 350
    lab_player.rect.y = 45

def print_attemps(attemps):
    lab_attemps_txt = simple_font.render('Попыток:'+str(attemps), True, (255, 255, 255))
    window.blit(lab_attemps_txt, (10, 10))

def print_rules_lab():
    lab_game_rules1 = simple_font.render('Правило простое|', True, (250, 0, 200))
    lab_game_rules1_pos = (10, 90)
    lab_game_rules2 = simple_font.render('Проведи лазер мышкой к части корабля|', True, (250, 0, 200))
    lab_game_rules2_pos = (10, 110)
    lab_game_rules3 = simple_font.render('Не задевай дорожки платы|', True, (250, 0, 200))
    lab_game_rules3_pos = (10, 130)
    hint_lab_txt = simple_font.render('Нажми на лазер для игры', True, (250, 0, 200))
    hint_lab_pos = (230, 70)
    window.blit(lab_game_rules1, lab_game_rules1_pos)
    window.blit(lab_game_rules2, lab_game_rules2_pos)
    window.blit(lab_game_rules3, lab_game_rules3_pos)
    window.blit(hint_lab_txt, hint_lab_pos)

def create_border():
    border = Wall(width = 7000, height=20, x=0, y=5000, color=Border_C, minigame='main_game')
    border = Wall(width = 20, height=5000, x=7000, y=0, color=Border_C, minigame='main_game')
    border = Wall(width = 7000, height=20, x=0, y=0, color=Border_C, minigame='main_game')
    border = Wall(width = 20, height=5000, x=0, y=0, color=Border_C, minigame='main_game')
    
# Лабиринт
lab_attemps = 3

pause_text = big_font.render('ПАУЗА', True, (5, 175, 0))
pause_pos = (window_width//2-90, window_height//2-50)

barriers_1 = pg.sprite.Group()
all_sprites_mini_game_2 = pg.sprite.Group()

lab_player = LabirintPlayer(width=20, height=20, color=Laser_C, x=350, y=45)


create_labirint()

labirint_background = pg.transform.scale(pg.image.load(labirint_back),(window_width, window_height))

labirint = False

window = pg.display.set_mode((window_width, window_height))
clock = pg.time.Clock()
run = True

pause = True

ship_part_3 = GameSpriteMini(20, 20, 660, 560, ship_part_3_img, 'labirint')

lab_win = False
lab_lose = False

possible_game_lab = True

timer_ticks = 0

score = 0

total_time = 0

# Подсказка
hint1 = simple_font.render('Нажмите на E чтобы начать квест', True, (202, 4, 161))
hint2 = simple_font.render('Данный квест пройден', True, (202, 4, 161))

planets = pg.sprite.Group()    

barriers = pg.sprite.Group() # Группа для проверки столкновений
all_sprites_mini_games = pg.sprite.Group() # Группа все объекты

mini_player = MiniPlayer() # Игрок
# Мини игра
timer_ticks = 0 
seconds = timer_ticks//60

right_bound = window_width//2 + 50
left_bound = window_width//2 - 50

mini_game_1 = False

win_game_1 = False
lose_game_1 = False

create_map1()
platform1 = Wall(width=15, height=560, x=1385, y=20, color=C_WALLS, minigame='astrorun') 
platform_joke = Wall(width=20, height=160, x=880, y=400, color=C_WALLS, minigame='astrorun')
key1 = GameSpriteMini(10, 10, 870, 550, key_img, minigame='astrorun')
ship_part_1 = GameSpriteMini(30, 30, 2000, 540, ship_part_1_img, minigame='astrorun')

# Все спрайты основная игра
all_sprites = pg.sprite.Group()
# Планеты
planets = pg.sprite.Group()    
# Границы основная игра
mg_borders = pg.sprite.Group()
create_border()

# Дальше основы, создание окна
window = pg.display.set_mode((window_width, window_height))
pg.display.set_caption('Cosmo Quest')
create_planets()
# Задний фон
back = pg.transform.scale(pg.image.load(background),(window_width, window_height))
shift1 = 0
shift2 = 0
# Создание игрока
player = Player(player_width, player_height, player_x, player_y, player_img, 5, mini_game='main_game')
parts = 0 # Количество собранных частей двигателя
score_parts = 0 # Очки за части двигателя
total_score = 0 # Очки за мини игры
# Создаёт игровой таймер
clock = pg.time.Clock()
# Переменная для запуска игрового цикла, флажок
run = True
# Переменные для запуска мини игр - основной игры
main_game = False
# Игровой цикл
x_hint, y_hint = 0, 0

while run:
    # Обработчик событий
    if not main_game and not mini_game_1 and not labirint:
        # Проверка на мини игры

        for e in pg.event.get():
            # Обрабатывает выход из игры
            if e.type == pg.QUIT:
                run = False # Меняет флажок для завершения цикла
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_1:
                    main_game = True
                    labirint = False
                    mini_game_1 = False
                
                if e.key == pg.K_2:
                    main_game = False
                    labirint = False
                    mini_game_1 = True
                if e.key == pg.K_3:
                    main_game = False
                    labirint = True
                    mini_game_1 = False
                elif e.key == pg.K_ESCAPE:
                    run = False

        window.fill((0, 0, 0))        
    
    # Обновление экрана               
    pg.display.update()
    
    if main_game:
        pg.mouse.set_visible(False)
        for e in pg.event.get():
            
            # Обрабатывает выход из игры
            if e.type == pg.QUIT:
                run = False # Меняет флажок для завершения цикла
            
            # Обрабатчик нажатий на клавиши
            if e.type == pg.KEYDOWN: # Если клавиша нажата  
            
                # Если клавиша стрелочка влево
                if e.key == pg.K_LEFT or e.key == pg.K_a:
                    player.angle_rotate_speed = 2 # Скорость вращения влево равна * градусов 
            
                # Если клавиша стрелочка вправо
                elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                    player.angle_rotate_speed = -2 # Скорость вращения влево равна * градусов 
                
                # Если клавиша стрелочка вправо
                    # Будет отключено но не выведено если клавиша стрелочка вверх

                elif e.key == pg.K_UP or e.key == pg.K_w:
                    player.speed = player_speed # Изменить максимальную скорость на * единиц

                if e.key == pg.K_2:
                    main_game = False
                    mini_game_1 = True
                
                
                elif e.key == pg.K_ESCAPE:
                    run = False

                if e.key == pg.K_r:
                    for obj in all_sprites:
                        obj.kill()
                    player.angle = 0
                    player.speed_x, player.speed_y = 0, 0
                    create_planets()
                    create_border()
                    win_game_1 = False
                    lose_game_1 = False
                    planets.possible_game = True
                    

                elif e.key == pg.K_e:
                    for i in range(len(planets)):
                        if planets.sprites()[i].mini_game != False:
                            if i == 0:
                                main_game = False
                                mini_game_1 = True

            # Если клавиши более не нажаты
            elif e.type == pg.KEYUP:
            
                # Скорость вращения влево меняется на 0
            
                if e.key == pg.K_LEFT or e.key == pg.K_a:
                    if player.angle_rotate_speed > 0:
                        player.angle_rotate_speed = 0
            
                # Скорость вращение вправо меняется на 0
                elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                    if player.angle_rotate_speed < 0:
                        player.angle_rotate_speed = 0
            
                # Максимальная скорость равна 0
                elif e.key == pg.K_UP or e.key == pg.K_w:
                    player.speed = 0
    
        # Вызов функций обновления
        all_sprites.update()
        player.update()
        
        # Перемещение всех объектов по отношению к игроку
        for s in all_sprites:
            s.rect.x -= player.x_speed
            s.rect.y -= player.y_speed
            

        # Отображение фона
        shift1 -= player.x_speed
        shift2 -= player.y_speed
        local_shift_x = shift1 % window_width
        local_shift_y = shift2 % window_height

        window.blit(back, (local_shift_x, local_shift_y))

        if local_shift_x != 0:
            window.blit(back, (local_shift_x - window_width, local_shift_y))
        if local_shift_y != 0:
            window.blit(back, (local_shift_x-window_width, local_shift_y-window_height))
        
        if local_shift_y != 0 or local_shift_x != 0:
            window.blit(back, (local_shift_x, local_shift_y-window_height))
  
        # Отображение статистики
        player.print_statistic()
        # Рисует все объекты
        all_sprites.draw(window)  
        player.draw()
        
        if len(player.planets_touched) != 0:
            x_hint, y_hint = player.return_p_cords()
            if player.planets_touched[0].possible_game:
                window.blit(hint1, (x_hint, y_hint))
            else:
                window.blit(hint2, (x_hint, y_hint))
        # Показывает количество кадров на данный момент
    elif mini_game_1 and not main_game and not labirint:
        if win_game_1 or lose_game_1:
            main_game = True
            player.stop_game()

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
                
                elif e.key == pg.K_1:
                    mini_game_1 = False
                    main_game = True
                
                elif e.key == pg.K_r:
                    reset_astrorun()
                    
                    
                
                elif e.key == pg.K_ESCAPE:
                    run = False

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
            reset_astrorun()

        pg.display.update()
        mini_player.update()
        window.fill((0, 0, 0))
        all_sprites_mini_games.draw(window)
        
        if mini_player.rect.y > window_height or game_timer(timer_ticks, 25) <= 0:
            lose_game_1 = True
            reset_astrorun()   
        
        timer_ticks+=1

    elif labirint and not main_game and not mini_game_1:
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
            elif e.type == pg.MOUSEMOTION:
                if not pause:
                    x, y = e.pos
                    lab_player.update(x, y)

            elif e.type == pg.MOUSEBUTTONDOWN and possible_game_lab:
                if pg.Rect.collidepoint(lab_player.rect, e.pos):
                    pause = False

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    run = False
                if e.key == pg.K_1:
                    main_game = True
                    labirint = False
                    mini_game_1 = False

        pg.display.update()
        
        if pause:
            window.fill((0, 191, 255))
            window.blit(pause_text, pause_pos)
            print_rules_lab()
            lab_player.draw()
            pg.mouse.set_visible(True)
            timer_ticks = 0

        if not pause and not lab_win and not lab_lose:
            pg.mouse.set_visible(False)
        
        if lab_attemps <= 0:
            lab_lose = True
            possible_game_lab = False

        if not pause:
            window.blit(labirint_background, (0, 0))
            all_sprites_mini_game_2.draw(window)
            timer_ticks += 1
            total_time = game_stopwatch(timer_ticks, (255, 20, 147), (10, 50))
        
        if pg.sprite.collide_rect(lab_player, ship_part_3):
            lab_win = True

            if total_time <= 50:
                score += 20

            elif total_time > 50 or total_time <= 80:
                score += 10
            
        print_attemps(lab_attemps)

    print_fps()
    # Вертикальная синхронизация (ограничение FPS)
    clock.tick(60)
