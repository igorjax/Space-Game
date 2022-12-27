import pygame as pg # Импорт библиотеки Pygame как pg для удобства
import time # Импорт встроенной библиотеки Python время
from additionaly import * # Импорт доп настроек из отдельного модуля
pg.font.init() # Конструктор текстов Pygame

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
        self.add(barriers, all_sprites_mini_games)

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


class Player(GameSprite): # Класс игрока
    def __init__(self, width, height, x_cord, y_cord, picture, **args):
        super().__init__(width, height, x_cord, y_cord, picture)
        #self.moving_img = args['image_m']
        self.speed = 0 # Максимальная скорость от которой идут все расчёты
        self.x_speed = 0 # Перемещение по координате X
        self.y_speed = 0 # Перемещение по координате Y
        self.angle = 0 # Угол объекта
        self.angle_rotate_speed = 0 # Скорость вращения
        self.image_copy = self.image.copy() # Дополнительная картинка что бы основная не ломалась при вращении
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
    
    def get_speed(self): # Метод для задания скорости в зависимости от угла
        if self.angle == 0: # Если угол равен нулю то скорость по Y будет равна максимальной скорости перемещения 
            self.y_speed = -self.speed # Обе скорости отрицательны
            self.x_speed = 0

        if self.angle > 0 and self.angle <= 45: # Если угол больше нуля и меньше или равен 45
                                                # cкорость по x будет увеличиваться в зависимости от угла
            speed_x = self.speed / 45 * self.angle # Максимальная скорость делится на максимальный угол и умножается на нынещний угол
            self.x_speed = -speed_x # Скорость по координате X будет отрицательной расчёты выше
            self.y_speed = -self.speed # Скорость по координате Y менятся не будет будет равна максимальной

        
        if self.angle > 45 and self.angle <= 90: # Если угол выше 45 но меньше или равен 90
            speed_y = self.speed - self.speed / 45 * (self.angle-45) # Тут добавляются 2 переменные так как скорость по координате Y
                                                                     # Будет уменьшаться в зависимости от угла -45 так как 90-45 = 45 или же 
                                                                     # 46-45 = 1 градус
            self.y_speed = -speed_y # Также обе скорости отрицательны
            self.x_speed = -self.speed # Скорость по X не изменяется и равна максимальной
        
        if self.angle > 90 and self.angle <=135: # Если угол выше 90 но меньше или равен 135
            speed_y = self.speed / 45 * (self.angle-90) # Скорость по Y будет пропорционально увеличиваться 
            self.x_speed = -self.speed # Скорость по X остаётся отрицательной менятся не будет, равна максимальной
            self.y_speed = speed_y # Скорость по Y будет положительной
        
        if self.angle > 135 and self.angle <= 180: # Если угол выше 135 но меньше или равен 180
            speed_x = self.speed - self.speed / 45 * (self.angle-135) # Скорость по X уменьшается
            self.x_speed = -speed_x # Скорость по X также будет отрицательной 
            self.y_speed = self.speed # Скорость по Y менятся не будет и будет равна максимальной
        
        if self.angle > 180 and self.angle <= 225: # Если угол выше 180 не меньше или равен 225
            speed_x = self.speed / 45 * (self.angle - 180) # Скорость X Будет увеличиваться
            self.y_speed = self.speed # Скорость по Y будет равна максимальной
            self.x_speed = speed_x # Обе скорости будут положительны
        
        if self.angle > 225 and self.angle <= 270: # Дальше по тому же принципу
            speed_y = self.speed - self.speed / 45 * (self.angle-225)
            self.y_speed = speed_y
            self.x_speed = self.speed
        
        if self.angle > 270 and self.angle <= 315:
            speed_y = self.speed / 45 * (self.angle-270)
            self.x_speed = self.speed
            self.y_speed = -speed_y
        
        if self.angle > 315 and self.angle <= 360:
            speed_x = self.speed - self.speed / 45 * (self.angle - 315)
            self.y_speed = -self.speed
            self.x_speed = speed_x
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

def create_map1(): # Функция создающая основные стены для мини игры
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
platform1 = Wall(width=15, height=560, x=1385, y=20, color=C_WALLS) 
platform_joke = Wall(width=20, height=160, x=880, y=400, color=C_WALLS)
key1 = GameSpriteMini(10, 10, 870, 550, key_img)
ship_part_1 = GameSpriteMini(30, 30, 2000, 540, ship_part_1_img)
                
# Все спрайты основная игра
all_sprites = pg.sprite.Group()

def create_planets():
    Planet1 = GameSprite(600, 500, 1220, 900, 'images/planet1.png')

# Дальше основы, создание окна
window = pg.display.set_mode((window_width, window_height))
create_planets()
# Задний фон
back = pg.transform.scale(pg.image.load(background),(window_width, window_height))
shift1 = 0
shift2 = 0
# Создание игрока
player = Player(player_width, player_height, player_x, player_y, player_img)
# Создаёт игровой таймер
clock = pg.time.Clock()
# Переменная для запуска игрового цикла, флажок
run = True
# Переменные для запуска мини игр - основной игры
main_game = False
# Игровой цикл
while run:
    # Обработчик событий
    if not main_game and not mini_game_1:
        for e in pg.event.get():
            # Обрабатывает выход из игры
            if e.type == pg.QUIT:
                run = False # Меняет флажок для завершения цикла
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_1:
                    main_game = True
                    mini_game_1 = False
                
                if e.key == pg.K_2:
                    main_game = False
                    mini_game_1 = True
                elif e.key == pg.K_ESCAPE:
                    run = False

        window.fill((0, 0, 0))        
    
    # Обновление экрана               
    pg.display.update()
    
    if main_game:
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
                s.rect.y -= player.y_speed
                s.rect.x -= player.x_speed
        
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
        
        if local_shift_y != 0 and local_shift_x != 0:
            window.blit(back, (local_shift_x, local_shift_y-window_height))
  
        # Отображение статистики
       # player.print_statistic()
        # Рисует все объекты
        all_sprites.draw(window)  
        player.draw()
        # Показывает количество кадров на данный момент
    elif mini_game_1 and main_game != True:

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
                    all_sprites_mini_games.empty()
                    barriers.empty()                    
                    create_map1()
                    mini_player = MiniPlayer()
                    timer_ticks = 0
                    platform1 = Wall(width=15, height=560, x=1385, y=20, color=C_WALLS) 
                    platform_joke = Wall(width=20, height=160, x=880, y=400, color=C_WALLS)
                    key1 = GameSpriteMini(10, 10, 870, 550, key_img)
                    ship_part_1 = GameSpriteMini(30, 30, 2000, 540, ship_part_1_img)
                    
                    
                
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
            #mini_game_1 = False

        pg.display.update()
        mini_player.update()
        window.fill((0, 0, 0))
        all_sprites_mini_games.draw(window)
        if game_timer(timer_ticks, 25) <= 0:
            lose_game_1 = False
            #mini_game_1 = False       
        timer_ticks+=1

    print_fps()
    # Вертикальная синхронизация
    clock.tick(60)
