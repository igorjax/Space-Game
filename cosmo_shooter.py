import pygame as pg
import random
import time
from additionaly import *
pg.font.init()

def print_score(score, cords):
    score_text = simple_font.render('Очки:'+str(round(score)), True, (255, 255, 255))
    window.blit(score_text, cords)

def print_fps(): # Выводит количество фпс на экран
    fps = simple_font.render(str(round(clock.get_fps())), True,(0,255,0))
    window.blit(fps, (670, 0))

def create_hp(hp_amount, pos):
    pos_x, pos_y = pos
    for i in range(hp_amount):
        hp = HP(70, 50, pos_x, pos_y, hp_img)
        pos_x += 20

simple_font = pg.font.Font(None, 35)

player_fast_move = [pg.transform.scale(pg.image.load(player_fast_move_img), (player_width, player_height)),
                    pg.transform.scale(pg.image.load(player_fast_move_1_img), (player_width, player_height)),
                    pg.transform.scale(pg.image.load(player_fast_move_2_img), (player_width, player_height))]

player_slow_move = [pg.transform.scale(pg.image.load(player_slow_move_img), (player_width, player_height)),
                    pg.transform.scale(pg.image.load(player_slow_move_1_img), (player_width, player_height)),
                    pg.transform.scale(pg.image.load(player_slow_move_2_img), (player_width, player_height))]

player_shooter_imgs = [pg.transform.scale(pg.image.load(player_fast_move_img), (shooter_p_w, shooter_p_h)),
                    pg.transform.scale(pg.image.load(player_fast_move_1_img), (shooter_p_w, shooter_p_h)),
                    pg.transform.scale(pg.image.load(player_fast_move_2_img), (shooter_p_w, shooter_p_h))]

def game_stopwatch(ticks, color, pos): # Таймер для игры
    time = round(ticks/60)
    time_txt = simple_font.render('Время:'+str(time), True,(color))
    window.blit(time_txt, (pos))
    return time

class HP(pg.sprite.Sprite):
    def __init__(self, w, h, x, y, picture):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.add(hps_group)

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
        

class GameSprite(pg.sprite.Sprite): # Класс неподвижного объекта
    def __init__(self, width, height, x_cord, y_cord, picture, planet=False, mini_game=False, minigame=None):
        super().__init__()
        
        self.image = pg.transform.scale(pg.image.load(picture), (width, height)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x_cord # Задаёт координату X
        self.rect.y = y_cord # Задаёт координату Y
        self.add(all_sprites)
        self.planet = planet
        self.minigame = minigame
        self.possible_game = True
        
        if self.planet:
            self.add(planets)
            if self.possible_game:
                self.mini_game = False

    def draw(self): # Рисует объект на экране
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite): # Класс игрока
    def __init__(self, width, height, x_cord, y_cord, picture,  **args):
        super().__init__(width, height, x_cord, y_cord, picture)
        self.speed = 0 # Максимальная скорость от которой идут все расчёты
        self.x_speed = 0 # Перемещение по координате X
        self.y_speed = 0 # Перемещение по координате Y
        self.angle = 0 # Угол объекта
        self.angle_rotate_speed = 0 # Скорость вращения
        
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
            bullet = Bullet(30, 30, x, y, player_bull_img, 7)
            self.reload_fire = True
            bullet.add(player_bullets)

    def print_reload(self):
        reload_txt = simple_font.render('Перезарядка..', True, (255, 255, 255))
        window.blit(reload_txt, (window_width-200, window_height-50))

    def update(self): # Метод обновляющий положение персонажа
        
        #if self.speed != 0:
         #   self.image = self.moving_img

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

        elif pg.sprite.spritecollide(shooter_player, enemy_bullets, True):
            hp_amount -= 1

        if self.rect.y <= 0 or self.rect.y >= window_width:
            self.kill()

def create_bonus():
    w = 40
    h = w
    x = random.randint(0, window_width-w)
    y = 0
    picture = bonus_img
    minigame = 'cosmo_shooter'
    bon = Bonus(w, h, x, y, picture, minigame)

all_sprites = pg.sprite.Group()
planets = pg.sprite.Group()

cosmo_shooter = True

hps_group = pg.sprite.Group() 

shooter_meteors = pg.sprite.Group()

enemy_bullets = pg.sprite.Group()
player_bullets = pg.sprite.Group()

enemies = pg.sprite.Group()

bonuses_shooter = pg.sprite.Group()

hp_amount = 3

shoot_score = 0

create_hp(hp_amount, (0, window_height-60))

shooter_back = pg.transform.scale(pg.image.load(shooter_back_jpg), (window_width, window_height))

shooter_player = Player(shooter_p_w, shooter_p_h, shooter_p_x,shooter_p_y, player_img, mini_game='shooter')

window = pg.display.set_mode((window_width, window_height))
clock = pg.time.Clock()

shooter_timer_ticks = 0

second_timer = 0
third_timer = 0
bonus_timer = 0

game_difficult = 'hard'

run = True

shift_shooter = 0

while run:
    if cosmo_shooter:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                run = False
        
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    run = False
                elif e.key == pg.K_LEFT or e.key == pg.K_a:
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
                    shooter_player.fire()

            elif e.type == pg.KEYUP:

                if e.key == pg.K_LEFT or e.key == pg.K_a:
                    if shooter_player.x_speed < 0:
                        shooter_player.x_speed = 0

                elif e.key == pg.K_RIGHT or e.key == pg.K_d:
                    if shooter_player.x_speed > 0:
                        shooter_player.x_speed = 0
            

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
            hp_amount -= 1

        if pg.sprite.spritecollide(shooter_player, bonuses_shooter, True):
            rand = random.randint(1, 5)
            if rand == 1:
                shoot_score *= 1.2
            else:
                hp_amount += 1

        if shoot_score >= 250:
            pass

        hps_group.draw(window)

        shooter_timer_ticks += 1


        clock.tick(60)
