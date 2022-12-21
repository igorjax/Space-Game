import pygame as pg # Импорт библиотеки Pygame как pg для удобства
import time # Импорт встроенной библиотеки Python время
from additionaly import * # Импорт доп настроек из отдельного модуля
pg.font.init() # Конструктор текстов Pygame

def print_fps(): # Выводит количество фпс на экран
    fps = pg.font.Font(None, 30).render(str(round(clock.get_fps())), True,(0,255,0))
    window.blit(fps, (670, 0))

class GameSprite(pg.sprite.Sprite): # Класс неподвижного объекта
    def __init__(self, width, height, x_cord, y_cord, picture):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(picture), (width, height)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x_cord # Задаёт координату X
        self.rect.y = y_cord # Задаёт координату Y
    
    def draw(self): # Рисует объект на экране
        window.blit(self.image, (self.rect.x, self.rect.y))
        return window

class Player(GameSprite): # Класс игрока
    def __init__(self, width, height, x_cord, y_cord, picture):
        super().__init__(width, height, x_cord, y_cord, picture)
        self.speed = 0 # Максимальная скорость от которой идут все расчёты
        self.x_speed = 0 # Перемещение по координате X
        self.y_speed = 0 # Перемещение по координате Y
        self.angle = 0 # Угол объекта
        self.angle_rotate_speed = 0 # Скорость вращения
        self.image_copy = self.image.copy() # Дополнительная картинка что бы основная не ломалась при вращении

    def update(self): # Метод обновляющий положение персонажа
        
        self.angle = (self.angle + self.angle_rotate_speed)%360 # Изменение угла (вращение)
        
        new_image = pg.transform.rotate(self.image_copy, self.angle) # Создание картинки объекта после вращения
        
        old_center = self.rect.center # "Старый центр" для уравнивания объекта при вращении
        
        self.image = new_image # Замена картинки на обновлённую
        self.rect = self.image.get_rect() # Обновление квадрата персонажа
        self.rect.center = old_center # Смена координаты центра для уравнивания
        
        self.get_speed() # Метод для задания скорости в зависимости от угла

        self.rect.x += self.x_speed # Обновление координаты X в зависимости от скорости
        self.rect.y += self.y_speed # Обновление координаты Y в зависимости от скорости

        # Временное решение чтобы игрок не выходил за экран
        if self.rect.x < 0: 
            self.rect.x = 700
        
        elif self.rect.x>700:
            self.rect.x = 0
        
        if self.rect.y < 0:
            self.rect.y = 700
        
        elif self.rect.y > 700:
            self.rect.y = 0
    
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
# Дальше основы создание окна
window = pg.display.set_mode((window_width, window_height))
# Задний фон, скоро будет изменено
back_gr = GameSprite(window_width, window_height, 0, 0, background)
# Создание игрока
player = Player(player_width, player_heght, player_x, player_y, player_texture)
# Создаёт игровой таймер
clock = pg.time.Clock()
# Переменная для запуска игрового цикла, флажок
run = True
# Игровой цикл
while run:
    # Обработчик событий
    for e in pg.event.get():
        # Обрабатывает выход
        if e.type == pg.QUIT:
            run = False # Меняет флажок для завершения цикла
        # Обрабатчик нажатий на клавиши
        elif e.type == pg.KEYDOWN: # Если клавиша нажата  
            # Если клавиша стрелочка влево
            if e.key == pg.K_LEFT:
                player.angle_rotate_speed = 3 # Скорость вращения влево равна 5 градусов 
            # Если клавиша стрелочка вправо
            elif e.key == pg.K_RIGHT:
                player.angle_rotate_speed = -3 # Скорость вращение вправо равна 5 градусов
            # Будет отключено но не выведено если клавиша стрелочка вверх
            elif e.key == pg.K_UP:
                player.speed = 5 # Изменить максимальную скорость на 5 единиц
        # Если клавиши более не нажаты
        elif e.type == pg.KEYUP:
            # Скорость вращения влево меняется на 0
            if e.key == pg.K_LEFT:
                if player.angle_rotate_speed > 0:
                    player.angle_rotate_speed = 0
            # Скорость вращение вправо меняется на 0
            elif e.key == pg.K_RIGHT:
                if player.angle_rotate_speed < 0:
                    player.angle_rotate_speed = 0
            # Максимальная скорость равна 0
            elif e.key == pg.K_UP:
                player.speed = 0
    # Обновление экрана               
    pg.display.update()
    # Вызов функции обновление игрока
    player.update()
    # Отрисовка заднего фона
    back_gr.draw()
    # Отображение статистики
    #player.print_statistic()
    # Рисует игрока
    player.draw()
    # Показывает количество кадров на данный момент
    print_fps()
    # Вертикальная синхронизация
    clock.tick(60)
