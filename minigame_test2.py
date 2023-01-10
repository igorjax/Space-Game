import pygame as pg # Импорт библиотеки Pygame как pg для удобства
import time # Импорт встроенной библиотеки Python время
from additionaly import * # Импорт доп настроек из отдельного модуля
pg.font.init() # Конструктор текстов Pygame
big_font = pg.font.Font(None, 60)
simple_font = pg.font.Font(None, 35)
mini_font=pg.font.Font(None,20)
def print_fps(): # Выводит количество фпс на экран
    fps = simple_font.render(str(round(clock.get_fps())), True,(0,255,0))
    window.blit(fps, (670, 0))

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

class GameSprite(pg.sprite.Sprite): # Класс неподвижного объекта
    def __init__(self, width, height, x_cord, y_cord, picture, minigame=None):
        super().__init__()
        
        self.image = pg.transform.scale(pg.image.load(picture), (width, height)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x_cord # Задаёт координату X
        self.rect.y = y_cord # Задаёт координату Y
        self.minigame = minigame
        if self.minigame == None:
            self.add(all_sprites)

        if self.minigame == 'meteorsbetween':
            self.add(all_sprites_met_game)
            self.add(meteors_mini)
            
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
        self.game = args['game']
        all_sprites.remove(self) # Мне было лень искать другие пути
    
    
    def update(self): # Метод обновляющий положение персонажа
        
        if self.game != 'main_game':

            #if self.speed != 0:
             #   self.image = self.moving_img

            self.angle = (self.angle + self.angle_rotate_speed)%360 # Изменение угла (вращение)
        
            self.get_speed() # Метод для задания скорости в зависимости от угла
        
            new_image = pg.transform.rotate(self.image_copy, self.angle) # Создание картинки объекта после вращения
        
            old_center = self.rect.center # "Старый центр" для уравнивания объекта при вращении
        
            self.image = new_image # Замена картинки на обновлённую
            self.rect = self.image.get_rect() # Обновление квадрата персонажа
            self.rect.center = old_center # Смена координаты центра для уравнивания
        
            if not main_game and self.minigame != 'main_game':
                self.rect.x += self.x_speed # Обновление координаты X в зависимости от скорости
                self.rect.y += self.y_speed # Обновление координаты Y в зависимости от скорости
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
    global pause, lab_attemps
    lab_attemps -= 1
    pause = True
    mini_player_meteors.rect.x = 610
    mini_player_meteors.rect.y = 30

def print_attemps(attemps):
    lab_attemps_txt = simple_font.render('Попыток:'+str(attemps), True, (255, 255, 255))
    window.blit(lab_attemps_txt, (10, 10))

def print_hint():
    hint_txt=mini_font.render('Чтобы покинуть мини игру выйдите за пределы карты',True,(255,255,255))
    window.blit(hint_txt,(10,35))

meteor_attemps=5
all_sprites = pg.sprite.Group()
all_sprites_met_game = pg.sprite.Group()
meteors_mini = pg.sprite.Group()
window = pg.display.set_mode((window_width, window_height))
# Задний фон
back = pg.transform.scale(pg.image.load(background),(window_width, window_height))
shift1 = 0
shift2 = 0
# Создание игрока
mini_player_meteors = Player(50,55,610,30 , player_img, game='meteorsbetween')

lose=big_font.render('Вы проиграли', True, (255,255,255))
win=big_font.render('Вы выиграли',True,(255,255,255))

create_asteroids()
pause = True
pause_text = big_font.render('ПАУЗА', True, (5, 175, 0))
pause_pos = (window_width//2-50, window_height//2-50)

ship_part_2= GameSprite(75,55,310,280,ship_part_2_img)
# Создаёт игровой таймер
clock = pg.time.Clock()
# Переменная для запуска игрового цикла, флажок
run = True
# Переменные для запуска мини игр - основной игры
main_game = False
meteors_bet_game = False
win_game_1 = False
lose_game_1 = False

while run:
    if win_game_1 != False or lose_game_1 != False:
        pass
    # Обработчик событий
    if not main_game and not meteors_bet_game:
        for e in pg.event.get():
            # Обрабатывает выход из игры
            if e.type == pg.QUIT:
                run = False # Меняет флажок для завершения цикла
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_4:
                    main_game = False
                    meteors_bet_game = True
                
                if e.key == pg.K_2:
                    main_game = False
                    mini_game_1 = True
                elif e.key == pg.K_ESCAPE:
                    run = False

        window.fill((0, 0, 0)) 
    if meteor_attemps <= 0:
        lose_game_1 = True   
        window.blit(lose,(230,260))  
        meteors_bet_game=False

    if win_game_1:
        window.blit(win,(230,260))
    
    # Обновление экрана               
    pg.display.update()
    
    if meteors_bet_game:
        for e in pg.event.get():
            
            # Обрабатывает выход из игры
            if e.type == pg.QUIT:
                run = False # Меняет флажок для завершения цикла
            
            # Обрабатчик нажатий на клавиши
            if e.type == pg.KEYDOWN: # Если клавиша нажата  
            
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

                if e.key == pg.K_2:
                    main_game = False
                    mini_game_1 = True
                
                elif e.key == pg.K_ESCAPE:
                    run = False

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
                reset_meteors_game()
                
        if pg.sprite.collide_rect(mini_player_meteors,ship_part_2):
            win_game_1=True
            window.blit(win,(230,260))



        

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

    print_fps()
    # Вертикальная синхронизация
    clock.tick(60)