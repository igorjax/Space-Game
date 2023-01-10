import pygame as pg # Импорт библиотеки Pygame как pg для удобства
import time # Импорт встроенной библиотеки Python время
from additionaly import * # Импорт доп настроек из отдельного модуля
import random # Рандом

pg.mixer.init()
pg.font.init() # Конструктор текстов Pygame
pg.init()
# Дополнительно цвета и шрифты
Blue_C = (0, 255, 225) 
Laser_C = (187, 4, 4)
Border_C = (19, 0, 163)
Dark_C = (0, 0, 0)

simple_font = pg.font.Font(None, 35)
big_font = pg.font.Font(None, 60)
appetit_font = pg.font.SysFont('Appetite', 50)
mini_font=pg.font.Font(None,20)
# Для первой мини игры
C_WALLS = (217, 217, 217)
dark = (0, 0, 0) # Чёрный цвет
win_s = pg.mixer.Sound('sounds/win_sound.ogg')
jump_s = pg.mixer.Sound('sounds/jump.ogg')
fire_s = pg.mixer.Sound('sounds/fire.ogg')
lose_s = pg.mixer.Sound('sounds/death.ogg')
hit_t_s = pg.mixer.Sound('sounds/hit_target.ogg')
meteor_crush_s = pg.mixer.Sound('sounds/meteor_death.ogg')


mini_player_images = [pg.transform.scale(pg.image.load('images/astronaut_c3.png'), (40, 90)), # Персонаж
                    pg.transform.scale(pg.image.load('images/astronaut_c2.png'), (40, 90)),
                    pg.transform.scale(pg.image.load('images/astronaut_c1.png'), (40, 90))]

player_slow_move = [pg.transform.scale(pg.image.load(player_slow_move_img), (player_width, player_height)),
                    pg.transform.scale(pg.image.load(player_slow_move_1_img), (player_width, player_height)),
                    pg.transform.scale(pg.image.load(player_slow_move_2_img), (player_width, player_height))]

player_fast_move = [pg.transform.scale(pg.image.load(player_fast_move_img), (player_width, player_height)),
                    pg.transform.scale(pg.image.load(player_fast_move_1_img), (player_width, player_height)),
                    pg.transform.scale(pg.image.load(player_fast_move_2_img), (player_width, player_height))]

player_shooter_imgs = [pg.transform.scale(pg.image.load(player_fast_move_img), (shooter_p_w, shooter_p_h)),
                    pg.transform.scale(pg.image.load(player_fast_move_1_img), (shooter_p_w, shooter_p_h)),
                    pg.transform.scale(pg.image.load(player_fast_move_2_img), (shooter_p_w, shooter_p_h))]

def print_parts(p_amount, pos):
    parts_txt = simple_font.render('Части двигателя:'+str(p_amount), True, (255, 255, 255))
    window.blit(parts_txt, (pos))

def print_lives(l_amount, pos):
    lives_txt = simple_font.render('Жизни:'+str(lifes), True, (255, 255, 255))
    window.blit(lives_txt, (pos))

def create_hp(hp_amount, pos):
    pos_x, pos_y = pos
    for i in range(hp_amount):
        hp = HP(70, 50, pos_x, pos_y, hp_img)
        pos_x += 20

def print_score(score, cords):
    score_text = simple_font.render('Очки:'+str(round(score)), True, (255, 255, 255))
    window.blit(score_text, cords)

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
            self.minigame = minigame

        if self.minigame == 'meteorsbetween':
            self.add(all_sprites_met_game)
            self.add(meteors_mini)

        if self.minigame == 'cosmo_shooter':
            self.add(bonuses_shooter)
        
    def draw(self): # Рисует объект на экране
        window.blit(self.image, (self.rect.x, self.rect.y))

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
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class GameSprite(pg.sprite.Sprite): # Класс неподвижного объекта
    def __init__(self, width, height, x_cord, y_cord, picture, planet=False, mini_game=False, minigame=None,meteor=False):
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
    def __init__(self, width, height, x_cord, y_cord, picture,  **args):
        super().__init__(width, height, x_cord, y_cord, picture)
        self.speed = 0 # Максимальная скорость от которой идут все расчёты
        self.x_speed = 0 # Перемещение по координате X
        self.y_speed = 0 # Перемещение по координате Y
        self.angle = 0 # Угол объекта
        self.angle_rotate_speed = 0 # Скорость вращения
        self.flying_sound = pg.mixer.Sound('sounds/flying.ogg')
        
        self.orig_img = player_slow_move[0]

        self.planets_touched = pg.sprite.spritecollide(self, planets, False)

        self.reload_fire = False

        self.timer_reload = 0

        self.mini_game = args['mini_game'] # Для использования класса для некоторых других мини игр
        
        self.timer_ticks = 0

        if self.mini_game != 'main_game':
            self.image_copy = self.image.copy() # Дополнительная картинка что бы основная не ломалась при вращении
        
        if self.mini_game == 'main_game':
        
            self.image_copy = self.orig_img.copy()

        self.count = 0 # Для анимации
        all_sprites.remove(self) # Мне было лень искать другие пути
        
    def update_shooter(self):
        self.timer_ticks += 1
        
        if self.reload_fire == True:
            self.timer_reload += 1
            self.print_reload()
            if self.timer_reload == 30:
                self.reload_fire = False
                self.timer_reload = 0


        if self.timer_ticks >= 15:
            self.timer_ticks = 0
        
        if self.count >= 3:
                self.count = 0

        if self.timer_ticks >= 10:
            self.orig_img = player_shooter_imgs[self.count]
            self.count += 1
        
        self.image = self.orig_img

        if self.rect.left <= 0:
            if self.x_speed < 0:
                self.x_speed  = 0

        if self.rect.right >= window_width:

            if self.x_speed > 0:
                self.x_speed  = 0
        
        self.rect.x += self.x_speed
    
    def fire(self): # метод для стрельбы
        if self.reload_fire != True:
            x, y = self.rect.center
            fire_s = pg.mixer.Sound('sounds/fire.ogg')
            fire_s.play()
            bullet = Bullet(30, 30, x, y, player_bull_img, 7)
            self.reload_fire = True
            bullet.add(player_bullets)

    def print_reload(self):
        reload_txt = simple_font.render('Перезарядка..', True, (255, 255, 255))
        window.blit(reload_txt, (window_width-200, window_height-50))

    def update(self): # Метод обновляющий положение персонажа и его картинку
        if self.mini_game == 'main_game':
            self.timer_ticks += 1
            if self.timer_ticks >= 11:
                self.timer_ticks = 0
            if self.count >= 3:
                self.count = 0
            if self.speed != 0:
                self.flying_sound.play()
                if self.speed < 6:
                    if self.timer_ticks >= 10:
                        self.orig_img = player_slow_move[self.count]
                        self.count += 1
                elif self.speed > 5 and self.speed <= 10:
                    if self.timer_ticks >= 10:
                        self.orig_img = player_fast_move[self.count]
                        self.count += 1
            else:
                self.orig_img = pg.transform.scale(pg.image.load(player_img), (player_width, player_height))
            self.image_copy = self.orig_img

        self.angle = (self.angle + self.angle_rotate_speed)%360 # Изменение угла (вращение)
        
        self.get_speed() # Метод для задания скорости в зависимости от угла
        
        new_image = pg.transform.rotate(self.image_copy, self.angle) # Создание картинки объекта после вращения
        
        old_center = self.rect.center # "Старый центр" для уравнивания объекта при вращении
        
        self.image = new_image # Замена картинки на обновлённую
        self.rect = self.image.get_rect() # Обновление квадрата персонажа
        self.rect.center = old_center # Смена координаты центра для уравнивания
        
        if self.mini_game != 'main_game':
            self.rect.x += self.x_speed # Обновление координаты X в зависимости от скорости
            self.rect.y += self.y_speed # Обновление координаты Y в зависимости от скорости
        
        if self.mini_game == 'main_game':
            
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

class HP(pg.sprite.Sprite):
    def __init__(self, w, h, x, y, picture):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(hps_group)

class Bullet(GameSprite): # класс отвечающий за пули
    def __init__(self, x, y, w, h, picture, speed_y, speed_x=0):
        super().__init__(x, y, w, h, picture)
        self.speed_y = -(speed_y)
        self.speed_x = speed_x 
    
    def update(self):
        global shoot_score, hp_amount 
        
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        if pg.sprite.groupcollide(player_bullets, enemies, True, True):
            shoot_score += 10
            hit_t_s.play()

        elif pg.sprite.spritecollide(shooter_player, enemy_bullets, True):
            hp_amount -= 1

        if self.rect.y <= 0 or self.rect.y >= window_width:
            self.kill()

class Bonus(GameSpriteMini):
    def __init__(self, width, height, x_cord, y_cord, picture, minigame):
        super().__init__(width, height, x_cord, y_cord, picture, minigame)
        self.y_speed = 4
        self.x_speed = -2
        self.direction = 'right'
        self.timer_ticks = 0
    
    def update(self):
        self.timer_ticks += 1
        if self.timer_ticks >= 60:

            if self.direction =='right':
                self.direction = 'left'
                
            elif self.direction == 'left':
                self.direction = 'right'
                
            self.timer_ticks = 0

        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        self.zigzag()
    
    def zigzag(self):
        
        if self.direction == 'left':
            self.x_speed = -1
        
        elif self.direction == 'right':
            self.x_speed = 1

class Enemy(pg.sprite.Sprite):
    def __init__(self, w, h, x, y, x_speed, picture, angle, direction, limit):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(picture), (w, h)) # Создаёт текстуру персонажу
        self.angle = angle
        self.image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = x # Задаёт координату X
        self.rect.y = y # Задаёт координату Y
        self.direction = direction
        self.limit = limit
        self.x_speed = x_speed
        self.timer_ticks = 0
        self.rand_timer = 10
        self.add(enemies)

    def update(self):
        self.timer_ticks += 1

        if self.timer_ticks >= self.rand_timer:
            self.fire()
            self.rand_timer = random.randint(70, 180)
            self.timer_ticks = 0
        
        if self.direction == 'left':
            if self.rect.x > self.limit:
                self.x_speed = 0
        
        elif self.direction == 'right':
            if self.rect.x < self.limit:
                self.x_speed = 0
        
        self.rect.x += self.x_speed

    def fire(self): # метод для стрельбы
       x, y = self.rect.center
       rand_speed_y = -(random.randint(4, 7))
       rand_speed_x = random.randint(-2, 2)
       bullet = Bullet(30, 30, x, y, enemy_bull_img, rand_speed_y, rand_speed_x)
       bullet.add(enemy_bullets)

class Meteor(pg.sprite.Sprite):
    def __init__(self, w, h, x, y, x_speed, y_speed, picture, rotate_speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(picture), (w, h)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x # Задаёт координату X
        self.rect.y = y # Задаёт координату Y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.angle_rotate_speed = rotate_speed
        self.angle = 0
        self.image_copy = self.image.copy()
        self.add(shooter_meteors)

    def update(self):
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        self.angle = self.angle = (self.angle + self.angle_rotate_speed)%360
        new_image = pg.transform.rotate(self.image_copy, self.angle)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        if self.rect.x > window_width or self.rect.right < 0:
            self.kill
        
        if self.rect.y > window_height:
            self.kill

def create_bonus():
    w = 40
    h = w
    x = random.randint(0, window_width-w)
    y = 0
    picture = bonus_img
    minigame = 'cosmo_shooter'
    bon = Bonus(w, h, x, y, picture, minigame)


def create_s_meteor():
    x = random.randint(0, window_width)
    y = 0
    if x > window_width/2:
        x_speed = -(random.randint(0, 3))
    else:
        x_speed = random.randint(0, 3)
    w = random.randint(50, 70)
    h = w
    y_speed = random.randint(3, 7)
    pic_num = random.randint(1, 3)
    rotate_speed = random.randint(1, 5)
    if pic_num == 1:
        picture = asteroid_1
    elif pic_num == 2:
        picture = asteroid_2
    else:
        picture = asteroid_3
    met = Meteor(w, h, x, y, x_speed, y_speed, picture, rotate_speed)

def create_enemy():
    direct = random.randint(1,2)
    img = random.randint(1, 2)
    if img == 1:
        picture = enemy1_img
    else:
        picture = enemy2_img

    if direct == 1:
        direction = 'right'
    else:
        direction = 'left'
    
    if direction == 'right':
        x = window_width + 70
        x_speed = -(random.randint(2, 6))
        angle = random.randint(325, 360)
        
        limit = random.randint(window_width - window_width//3, window_width-50)
        
    elif direction == 'left':
        x = -70
        x_speed = random.randint(2, 6)
        angle = random.randint(0, 45)
        limit = random.randint(50, window_width//3)

    y = random.randint(0, window_height/2)
    w = random.randint(30, 60)
    h = w
    
    Enemy(w, h, x, y, x_speed, picture, angle, direction, limit)

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
    x_cordp1 = random.randint(1200, 2000)
    y_cordp1 = random.randint(200, 2000)
    x_cordp2 = random.randint(2000, 5000)
    y_cordp2 = random.randint(2000, 4000)
    x_cordp3 = random.randint(3000, 6300)
    y_cordp3 = random.randint(300, 4400)
    Planet1 = GameSprite(600, 500, x_cordp1, y_cordp1, 'images/planet1.png', True)
    Planet2 = GameSprite(600,600,x_cordp2,y_cordp2,'images/Asteroids.png',True)
    Planet3 = GameSprite(600, 500, x_cordp3, y_cordp3, 'images/Planet2.png', True)

def create_4_planet():
    x = 0
    y = 0
    Planet4 = GameSprite(600, 600, x, y, 'images/Planet4.png', True)

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
    global pause_lab, lab_attemps
    lab_attemps -= 1
    pause_lab = True
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
    
def create_asteroids():
    asteroid=GameSpriteMini(65,65,-4,-105,asteroid_1, 'meteorsbetween')
    asteroid1=GameSpriteMini(65,65,456,109,asteroid_1, 'meteorsbetween')
    asteroid2=GameSpriteMini(65,65,54,186,asteroid_1, 'meteorsbetween')
    asteroid3=GameSpriteMini(65,65,10,358,asteroid_1, 'meteorsbetween')
    asteroid4=GameSpriteMini(65,65,246,31,asteroid_2, 'meteorsbetween')
    asteroid5=GameSpriteMini(65,65,350,200,asteroid_2, 'meteorsbetween')
    asteroid6=GameSpriteMini(65,65,170,500,asteroid_2, 'meteorsbetween')
    asteroid7=GameSpriteMini(65,65,286,340,asteroid_2, 'meteorsbetween')
    #asteroid8=GameSpriteMini(77,77,209,139,asteroid_3, 'meteorsbetween')
    asteroid9=GameSpriteMini(65,65,114,66,asteroid_3, 'meteorsbetween')
    asteroid10=GameSpriteMini(65,65,247,251,asteroid_3, 'meteorsbetween')
    asteroid11=GameSpriteMini(65,65,588,180,asteroid_1, 'meteorsbetween')
    asteroid12=GameSpriteMini(65,65,430,400,asteroid_3, 'meteorsbetween')
    
def reset_meteors_game():
    global meteor_attemps
    meteor_attemps -= 1
    mini_player_meteors.rect.x = 610
    mini_player_meteors.rect.y = 30

def print_attemps(attemps):
    lab_attemps_txt = simple_font.render('Попыток:'+str(attemps), True, (255, 255, 255))
    window.blit(lab_attemps_txt, (10, 10))

def print_hint():
    hint_txt=mini_font.render('Чтобы покинуть мини игру выйдите за пределы карты',True,(255,255,255))
    window.blit(hint_txt,(10,35))
# Звуки
pg.mixer.music.load('sounds/bg_sound.mp3')
pg.mixer.music.play()
# Планеты
planets = pg.sprite.Group()    

# Между метеорами
meteor_attemps=5
all_sprites = pg.sprite.Group()
all_sprites_met_game = pg.sprite.Group()
meteors_mini = pg.sprite.Group()
window = pg.display.set_mode((window_width, window_height))
win_game_meteors = False
lose_game_meteors = False

# Создание игрока
mini_player_meteors = Player(50,55,610,30 , player_img, mini_game='meteorsbetween')

lose=big_font.render('Вы проиграли', True, (255,255,255))
win=big_font.render('Вы выиграли',True,(255,255,255))

create_asteroids()
pause_meteors = False

ship_part_2= GameSprite(75,55,310,280,ship_part_2_img)
# Создаёт игровой таймер
clock = pg.time.Clock()
# Переменная для запуска игрового цикла, флажок
run = True

# Лабиринт
lab_attemps = 3

pause_text = big_font.render('ПАУЗА', True, (5, 175, 0))
pause_pos = (window_width//2-90, window_height//2-50)

barriers_1 = pg.sprite.Group()
all_sprites_mini_game_2 = pg.sprite.Group()

lab_player = LabirintPlayer(width=20, height=20, color=Laser_C, x=350, y=45)

create_labirint()

labirint_background = pg.transform.scale(pg.image.load(labirint_back),(window_width, window_height))


window = pg.display.set_mode((window_width, window_height))
clock = pg.time.Clock()
run = True

pause_lab = True
# Часть корабля
ship_part_3 = GameSpriteMini(20, 20, 660, 560, ship_part_3_img, 'labirint')
# Флажки победы и поражения
lab_win = False
lab_lose = False
# Возможность игры 
possible_game_lab = True
# Таймеры
timer_ticks = 0

total_time = 0

# Подсказки планеты
hint1 = simple_font.render('Нажмите на E чтобы начать квест', True, (202, 4, 161))
hint2 = simple_font.render('Данный квест пройден', True, (202, 4, 161))

barriers = pg.sprite.Group() # Группа для проверки столкновений
all_sprites_mini_games = pg.sprite.Group() # Группа все объекты мини игры astrorun

mini_player = MiniPlayer() # Игрок
# Мини игра 1 астроран
timer_ticks = 0 
seconds = timer_ticks//60
# Ограничения до начала отклонения фона
right_bound = window_width//2 + 50
left_bound = window_width//2 - 50
# Переключатели
win_game_1 = False
lose_game_1 = False
# Создание карты
create_map1()
platform1 = Wall(width=15, height=560, x=1385, y=20, color=C_WALLS, minigame='astrorun') 
platform_joke = Wall(width=20, height=160, x=880, y=400, color=C_WALLS, minigame='astrorun')
key1 = GameSpriteMini(10, 10, 870, 550, key_img, minigame='astrorun') # Ключик
ship_part_1 = GameSpriteMini(30, 30, 2000, 540, ship_part_1_img, minigame='astrorun') # Часть корабля

# Космический шутер
# Группы спрайтов
hps_group = pg.sprite.Group() 
shooter_meteors = pg.sprite.Group()
enemy_bullets = pg.sprite.Group()
player_bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
bonuses_shooter = pg.sprite.Group()
# Количество хп
hp_amount = 3
# Очки
shoot_score = 0

# Функция создающая хп на экране
create_hp(hp_amount, (0, window_height-60))
# Задний фон
shooter_back = pg.transform.scale(pg.image.load(shooter_back_jpg), (window_width, window_height))
# Игрок
shooter_player = Player(shooter_p_w, shooter_p_h, shooter_p_x,shooter_p_y, player_img, mini_game='shooter')
# Таймеры
shooter_timer_ticks = 0
second_timer = 0
third_timer = 0
bonus_timer = 0
# Отклонение фона
shift_shooter = 0
shooter_lose = False
shooter_win = False
# Подсказки шутер
shooter_rule1 = simple_font.render('Последний рывок', True, (255, 255, 255))
shooter_rule2 = simple_font.render('Набери 250 очков и больше', True, (255, 255, 255))
shooter_rule3 = simple_font.render('Слева хп, стрелять пробел', True, (255, 255, 255))
shooter_rule4 = simple_font.render('Не касайся метеоров и стреляй по инопланетянам', True, (255, 255, 255))
# Все спрайты основная игра
all_sprites = pg.sprite.Group()

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


# Меню
# Фон меню
menu_back = pg.transform.scale(pg.image.load(menu_jpg), (window_width, window_height))
# Тексты в меню игры
game_title = appetit_font.render('Cosmo Quest', True, (198, 0, 76))
#Кнопочки
game_start_btn = Wall(width=150, height=30, x=20, y=150, color=Dark_C, minigame=None)
game_start_txt = simple_font.render('Начать игру', True, (255, 255, 255))
game_diff_btn = Wall(width=250, height=30, x=20, y=200, color=Dark_C, minigame=None)
game_diff_posible = True
game_exit_btn = Wall(width=100, height=30, x=20, y=300, color=Dark_C, minigame=None)
game_exit_txt = simple_font.render('Выйти', True, (255, 255, 255))
rules_btn = Wall(width=130, height=30, x=20, y=250, color=Dark_C, minigame=None)
rules_txt = simple_font.render('Правила', True, (255, 255, 255))
# Тексты правил
rule1 = simple_font.render('После путешествия ты решил улететь домой', True, (0, 0, 0))
rule2 = simple_font.render('Но у тебя сломался варп двигатель', True, (0, 0, 0))
rule3 = simple_font.render('Вокруг тебя есть барьеры лучше их не касаться', True, (0, 0, 0))
rule4 = simple_font.render('Твоя задача пройти 4 квеста и починить двигатель', True, (0, 0, 0))
rule5 = simple_font.render('Ищи планеты или странные астероиды', True, (0, 0, 0))
rule6 = simple_font.render('Там и ждут тебя квесты', True, (0, 0, 0))
# Кнопка назад правила
back_btn = Wall(width=100, height=30, x=20, y=560, color=Dark_C, minigame=None)
back_txt = simple_font.render('Назад', True, (255, 255, 255))
# Сложность игры
game_difficult = 'normal'
# Создание игрока
player = Player(player_width, player_height, player_x, player_y, player_img, mini_game='main_game')
parts_amount = 0 # Количество собранных частей
lifes = 5 # Количество попыток на всё и про всё
score_parts = 0 # Очки за части двигателя
total_score = 0 # Очки за мини игры
# Создаёт игровой таймер
clock = pg.time.Clock()
# Переменная для запуска игрового цикла, флажок
run = True
# Переменные для запуска мини игр - основной игры
main_game = False
cosmo_shooter = False
shooter_pause = True
mini_game_1 = False
pause_minigame_1 = True
# Кнопкиии и тексты и флажки
start_minigame_btn = Wall(width=200, height=30, x=280, y=100, color=Dark_C, minigame=None)
start_minigame_txt = simple_font.render('Начать игру', True, (255, 255, 255))
mini_game_1_quest = simple_font.render('Задача: добежать за время', True, (255, 255, 255))
mini_game_1_quest_1 = simple_font.render('На уровне есть пасхалка', True, (255, 255, 255))
restart_minis_btn = Wall(width=200, height=80, x=280, y=260, color=Dark_C, minigame=None)
restart_minis_txt = simple_font.render('Сначала', True, (255, 255, 255))
restart_cosneq = simple_font.render('-1 Жизнь', True, (255, 255, 255)) 
labirint = False
meteors_bet_game = False
meteors_pause = False
rules = False
win_blit = False
win_txt = pg.font.SysFont('Current Typeface', 100).render('С победой тебя!!!', True, (255, 250, 42))
lose_txt = pg.font.SysFont('Current Typeface', 100).render('Ты проиграл:(', True, (255, 250, 42))
#  Координаты подсказки
x_hint, y_hint = 0, 0
planet4_created = False
# Игровой цикл
while run:
    if parts_amount >= 3 and not planet4_created:
        planet4_created = True
        create_4_planet()
    
    pg.display.update()
    if not main_game and not mini_game_1 and not labirint and not meteors_bet_game and not cosmo_shooter and not rules:
        # Проверка на мини игры

        for e in pg.event.get():
            # Обрабатывает выход из игры
            
            if e.type == pg.QUIT:
                run = False # Меняет флажок для завершения цикла
            
            elif e.type == pg.MOUSEBUTTONDOWN:
                
                if game_start_btn.rect.collidepoint(e.pos):
                    main_game = True

                if game_diff_posible:
                    if game_diff_btn.rect.collidepoint(e.pos):
                    
                        if game_difficult == 'normal':
                            game_difficult = 'hard'
                    
                        elif game_difficult == 'hard':
                            game_difficult = 'normal'
                
                if game_exit_btn.rect.collidepoint(e.pos):
                    run = False
                
                if rules_btn.rect.collidepoint(e.pos):

                    rules = True
            

        game_diff_txt = simple_font.render(f'Сложность: {game_difficult}', True, (255, 255, 255))
        pg.mouse.set_visible(True)
        window.blit(menu_back, (0, 0))     
        window.blit(game_title, (230, 50))   
        game_start_btn.reset()
        game_diff_btn.reset()
        game_exit_btn.reset()
        rules_btn.reset()
        window.blit(rules_txt, (25, 253))
        window.blit(game_exit_txt, (25, 303))
        window.blit(game_diff_txt, (25, 203))
        window.blit(game_start_txt,(25, 153))
    
    if rules and not main_game and not mini_game_1 and not labirint and not meteors_bet_game and not cosmo_shooter:
        for e in pg.event.get():
            # Обрабатывает выход из игры
            if e.type == pg.QUIT:
                run = False # Меняет флажок для завершения цикла

            elif e.type == pg.MOUSEBUTTONDOWN:
                
                if back_btn.rect.collidepoint(e.pos):
                    rules = False
            
            window.fill((30, 0, 187))
            back_btn.reset()
            window.blit(back_txt, (25, 563))

            window.blit(rule1, (0, 0))
            window.blit(rule2, (0, 40))
            window.blit(rule3, (0, 80))
            window.blit(rule4, (0, 120))
            window.blit(rule5, (0, 160))
            window.blit(rule6, (0, 180))
    
    if main_game and not mini_game_1 and not labirint and not meteors_bet_game and not cosmo_shooter and not rules:
        game_diff_posible = False
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
                    labirint = False
                    meteors_bet_game = False
                
                elif e.key == pg.K_ESCAPE:
                    main_game = False
                    cosmo_shooter = False
                    mini_game_1 = False
                    labirint = False
                    meteors_bet_game = False
                    rules = False
                    

                elif e.key == pg.K_e:
                    for i in range(len(planets)):
                        if planets.sprites()[i].mini_game != False:
                            
                            if i == 0:
                                meteors_bet_game = False
                                main_game = False
                                mini_game_1 = True
                                

                            elif i == 1:
                                main_game = False
                                mini_game_1 = False
                                meteors_bet_game = True
                            
                            elif i == 2:
                                main_game = False
                                mini_game_1 = False
                                meteors_bet_game = False
                                labirint = True
                            
                            elif i == 3:
                                main_game = False
                                mini_game_1 = False
                                meteors_bet_game = False
                                labirint = False
                                cosmo_shooter = True

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
        #player.print_statistic()
        # Рисует все объекты
        all_sprites.draw(window)  
        print_parts(parts_amount, (450, 550))
        print_lives(lifes, (20, 550))
        player.draw()
        
        if len(player.planets_touched) != 0:
            x_hint, y_hint = player.return_p_cords()
            if player.planets_touched[0].possible_game:
                window.blit(hint1, (x_hint, y_hint))
            else:
                window.blit(hint2, (x_hint, y_hint))


    elif mini_game_1 and not main_game and not labirint and not meteors_bet_game and not cosmo_shooter: # Пунктир 1
        for e in pg.event.get():

                if e.type == pg.QUIT:
                    run = False
                
                if pause_minigame_1:
                    if e.type == pg.MOUSEBUTTONDOWN:
                        if start_minigame_btn.rect.collidepoint(e.pos):
                            if lose_game_1 != True:
                                pause_minigame_1 = False
                        
                        elif back_btn.rect.collidepoint(e.pos):
                            main_game = True
                            mini_game_1 = False
                        
                        if lose_game_1 == True:
                            
                            if restart_minis_btn.rect.collidepoint(e.pos):
                                
                                lifes -= 1
                                lose_game_1 = False


                if not pause_minigame_1:
                    if e.type == pg.KEYDOWN:
                        
                        if e.key == pg.K_LEFT or e.key == pg.K_a:
                            mini_player.update_direction('left')
                            mini_player.x_speed = -4

                        elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                            mini_player.update_direction('right')
                            mini_player.x_speed = 4

                        elif e.key == pg.K_UP or e.key == pg.K_w:
                            jump_s.play()
                            mini_player.jump(-8)
                
                        elif e.key == pg.K_1:
                            mini_game_1 = False

                            main_game = True
                
                        elif e.key == pg.K_ESCAPE:
                            run = False

                    elif e.type == pg.KEYUP:
                        if e.key == pg.K_LEFT or e.key == pg.K_a:
                            if mini_player.x_speed < 0:
                                mini_player.x_speed = 0

                        elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                            if mini_player.x_speed > 0:
                                mini_player.x_speed = 0
                        


        if pause_minigame_1:
            pg.mouse.set_visible(True)
            window.fill((255, 42, 134))
            start_minigame_btn.reset()
            window.blit(game_start_txt, (285, 103))
            window.blit(mini_game_1_quest, (20, 150))
            window.blit(mini_game_1_quest_1, (20, 180))
            
            if lose_game_1 == True:
                restart_minis_btn.reset()
                window.blit(restart_minis_txt, (285, 263))
                window.blit(restart_cosneq, (285, 283))

            back_btn.reset()
            window.blit(back_txt, (25, 563))


        if not pause_minigame_1:
            pg.mouse.set_visible(False)
            
            if win_game_1:
                parts_amount += 1
                mini_game_1 = False
                main_game = True
                player.stop_game()

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
            
            if game_difficult == 'hard':
                if mini_player.rect.y > window_height or game_timer(timer_ticks, 25) <= 0:
                    if mini_player.rect.y > window_height:
                        lose_s.play()
                    lose_game_1 = True
                    pause_minigame_1 = True
                    reset_astrorun()   
            
            elif game_difficult == 'normal':
                if mini_player.rect.y > window_height or game_timer(timer_ticks, 40) <= 0:
                    lose_game_1 = True
                    pause_minigame_1 = True
                    reset_astrorun()   
            
            timer_ticks+=1

    elif labirint and not main_game and not mini_game_1 and not meteors_bet_game:
        if lab_win == True:
            parts_amount += 1
            labirint = False
            main_game = True
            player.stop_game()
            

        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False

            elif e.type == pg.MOUSEMOTION:
                if not pause_lab:
                    x, y = e.pos
                    lab_player.update(x, y)

            elif e.type == pg.MOUSEBUTTONDOWN :
                if possible_game_lab:
                    if pg.Rect.collidepoint(lab_player.rect, e.pos):
                        pause_lab = False
                
                if back_btn.rect.collidepoint(e.pos):
                    
                    labirint = False
                    main_game = True
                

                if lab_lose == True:
                    if restart_minis_btn.rect.collidepoint(e.pos):         
                        lifes -= 1
                        lab_attemps += 3
                        lab_lose = False
                        possible_game_lab = True

            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pause_lab = True

        pg.display.update()
        
        if pause_lab:
            window.fill((0, 191, 255))
            window.blit(pause_text, pause_pos)
            print_rules_lab()
            lab_player.draw()
            back_btn.reset()
            window.blit(back_txt, (25, 563))
            pg.mouse.set_visible(True)
            timer_ticks = 0
            
            if lab_lose == True:
                restart_minis_btn.reset()
                window.blit(restart_minis_txt, (285, 263))
                window.blit(restart_cosneq, (285, 283))

        if not pause_lab:
            pg.mouse.set_visible(False)
        
        if lab_attemps <= 0:
            lab_lose = True
            possible_game_lab = False

        if not pause_lab:
            window.blit(labirint_background, (0, 0))
            all_sprites_mini_game_2.draw(window)
            timer_ticks += 1
            
            if game_difficult == 'hard':
                if game_timer(timer_ticks, 60) <= 0:
                    lab_lose = True
                    reset_lab()
            
            elif game_difficult == 'normal':
                if game_timer(timer_ticks, 90) <= 0:
                    lab_lose = True
                    reset_lab()

        if pg.sprite.collide_rect(lab_player, ship_part_3):
                
            lab_win = True            
        
        print_attemps(lab_attemps)


    elif meteors_bet_game and not main_game and not labirint and not mini_game_1 and not cosmo_shooter:
        
        for e in pg.event.get():
            if win_game_meteors:
                meteors_bet_game = False
                parts_amount += 1
                main_game = True
                player.stop_game()
            
            # Обрабатывает выход из игры
            if e.type == pg.QUIT:
                run = False # Меняет флажок для завершения цикла
            
            # Обрабатчик нажатий на клавиши
            if e.type == pg.KEYDOWN: # Если клавиша нажата  
                if not lose_game_meteors:
                # Если клавиша стрелочка влево
                    if e.key == pg.K_LEFT or e.key == pg.K_a:
                        mini_player_meteors.angle_rotate_speed = 2 # Скорость вращения влево равна * градусов 
            
                # Если клавиша стрелочка вправо
                    elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                        mini_player_meteors.angle_rotate_speed = -2 # Скорость вращения влево равна * градусов 
            
                # Если клавиша стрелочка вправо
                    # Будет отключено но не выведено если клавиша стрелочка вверх
                
                    elif e.key == pg.K_UP or e.key == pg.K_w:
                        mini_player_meteors.speed = player_speed # Изменить максимальную скорость на * единиц
            
            elif e.type == pg.MOUSEBUTTONDOWN:
                if lose_game_meteors == True:
                    if restart_minis_btn.rect.collidepoint(e.pos):         
                        lifes -= 1
                        meteor_attemps = 5
                        lose_game_meteors = False

            # Если клавиши более не нажаты
            elif e.type == pg.KEYUP:
            
                # Скорость вращения влево меняется на 0
            
                if e.key == pg.K_LEFT or e.key == pg.K_a:
                    if mini_player_meteors.angle_rotate_speed > 0:
                        mini_player_meteors.angle_rotate_speed = 0
            
                # Скорость вращение вправо меняется на 0
                elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                    if mini_player_meteors.angle_rotate_speed < 0:
                        mini_player_meteors.angle_rotate_speed = 0
            
                # Максимальная скорость равна 0
                elif e.key == pg.K_UP or e.key == pg.K_w:
                    mini_player_meteors.speed = 0
        
        for m in meteors_mini:
            if pg.sprite.collide_rect(mini_player_meteors, m):
                meteor_crush_s.play()
                reset_meteors_game()
                
        # Вызов функций обновления
        all_sprites_met_game.update()
        mini_player_meteors.update()

        window.blit(back, (0, 0))
        
        # Отображение статистики
        # player.print_statistic()
        # Рисует все объекты
        all_sprites_met_game.draw(window)  
        ship_part_2.draw()
        mini_player_meteors.draw()
        print_attemps(meteor_attemps)
        print_hint()

                
        if pg.sprite.collide_rect(mini_player_meteors,ship_part_2):
            win_game_meteors=True
            window.blit(win,(230,260))

        if meteor_attemps <= 0:
            lose_game_meteors = True   
            window.blit(lose,(230,460))
            restart_minis_btn.reset()
            window.blit(restart_minis_txt, (285, 263))
            window.blit(restart_cosneq, (285, 283)) 
            pg.mouse.set_visible(True)
        else:
            pg.mouse.set_visible(False)

    if cosmo_shooter and not meteors_bet_game and not main_game and not labirint and not mini_game_1:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
        
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    run = False

                if not shooter_pause:
                    if e.key == pg.K_LEFT or e.key == pg.K_a:
                        if game_difficult == 'hard':
                            shooter_player.x_speed = -3
                        if game_difficult == 'normal':
                            shooter_player.x_speed = -5
                    elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                        if game_difficult == 'hard':
                            shooter_player.x_speed = 3
                        if game_difficult == 'normal':
                            shooter_player.x_speed = 5
                    elif e.key == pg.K_SPACE:
                        fire_s.play()
                        shooter_player.fire()

            elif e.type == pg.KEYUP:

                if e.key == pg.K_LEFT or e.key == pg.K_a:
                    if shooter_player.x_speed < 0:
                        shooter_player.x_speed = 0

                elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                    if shooter_player.x_speed > 0:
                        shooter_player.x_speed = 0
            
            elif e.type == pg.MOUSEBUTTONDOWN:
                if shooter_pause and not shooter_lose:
                    if start_minigame_btn.rect.collidepoint(e.pos):
                        shooter_pause = False
                if shooter_lose == True:
                    if restart_minis_btn.rect.collidepoint(e.pos):         
                        lifes -= 1
                        hp_amount = 3
                        shooter_lose = False

            
        if not shooter_pause:
            shooter_player.update_shooter()
            enemies.update()
            bonuses_shooter.update()
            player_bullets.update()
            enemy_bullets.update()
            shooter_meteors.update()
            pg.display.update()
    
            shift_shooter += 4   
    
        local_shift_y = shift_shooter % window_height

        window.blit(shooter_back, (0, local_shift_y))
    
        if local_shift_y != 0:
                window.blit(shooter_back, (0, local_shift_y-window_height))

        player_bullets.draw(window)
        bonuses_shooter.draw(window)
        enemy_bullets.draw(window)
        shooter_meteors.draw(window)
        enemies.draw(window)
        shooter_player.draw()
        print_score(shoot_score, (window_width-140, 0))

        if shooter_pause:
            pg.mouse.set_visible(True)
            start_minigame_btn.reset()
            window.blit(start_minigame_txt, (285, 103))
            window.blit(shooter_rule1, (85, 143))
            window.blit(shooter_rule2, (85, 183))
            window.blit(shooter_rule3, (85, 223))
            window.blit(shooter_rule4, (85, 263))

        if game_difficult == 'normal':
            if game_stopwatch(shooter_timer_ticks, (255, 255, 255), (0, 0)) > second_timer + 1:
                second_timer += 2
                third_timer += 1
                bonus_timer += 1
                create_s_meteor()

            if third_timer == 2:
                create_enemy()
                third_timer = 0

            if bonus_timer == 5:
                create_bonus()
                bonus_timer = 0

        elif game_difficult == 'hard':
            if game_stopwatch(shooter_timer_ticks, (255, 255, 255), (0, 0)) > second_timer + 1:
                second_timer += 2
                third_timer += 1
                bonus_timer += 1
                create_s_meteor()

            if third_timer == 2:
                create_enemy()
                third_timer = 0

            if bonus_timer == 5:
                create_bonus()
                bonus_timer = 0


        if len(hps_group) > hp_amount or hp_amount > len(hps_group):
            hps_group.empty()
            create_hp(hp_amount, (0, window_height-60))
    
        if pg.sprite.spritecollide(shooter_player, shooter_meteors, True):
            meteor_crush_s.play()
            hp_amount -= 1

        if pg.sprite.spritecollide(shooter_player, bonuses_shooter, True):
            rand = random.randint(1, 5)
            if rand == 1:
                shoot_score *= 1.2
            else:
                hp_amount += 1

        if shoot_score >= 250:
            shooter_win = True

        
        if shooter_win:
            enemies.empty()
            shooter_meteors.empty()
            bonuses_shooter.empty()
            ship_part_4 = GameSpriteMini(30, 30, 300, 540, ship_part_4_img, minigame='cosmo_shooter')
            ship_part_4.draw()
            
            if shooter_player.rect.colliderect(ship_part_4):
                labirint = False
                meteors_bet_game = False
                meteors_pause = False
                rules = False
                main_game = False
                mini_game_1 = False
                win_blit = True
                

        if len(hps_group) <= 0:
            shooter_pause = True
            shoot_score = 0
            hps_group.empty()
            enemies.empty()
            bonuses_shooter.empty()
            shooter_meteors.empty()
            shooter_lose = True
            restart_minis_btn.reset()
            window.blit(restart_minis_txt, (285, 263))
            window.blit(restart_cosneq, (285, 283))

        hps_group.draw(window)
        if not shooter_pause:
            shooter_timer_ticks += 1
            pg.mouse.set_visible(False)
    
    if win_blit == True:
        window.blit(menu_back, (0, 0))
        window.blit(win_txt, (20, 350))
        win_s.play()
    if lifes <= 0:
        window.blit(menu_back, (0, 0))
        window.blit(lose_txt, (20, 350))
    #print_fps() # Отображения кадров в реальном времени
    # (ограничение FPS)
    if parts_amount >= 2:
        player_speed = 10
    clock.tick(60)
