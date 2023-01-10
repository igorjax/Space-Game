import pygame as pg # Импорт библиотеки Pygame как pg для удобства
import time # Импорт встроенной библиотеки Python время
from additionaly import * # Импорт доп настроек из отдельного модуля
pg.font.init() # Конструктор текстов Pygame

Blue_C = (0, 255, 225) 
Laser_C = (187, 4, 4)

simple_font = pg.font.Font(None, 35)
big_font = pg.font.Font(None, 60)
mini_font=pg.font.Font(None,20)

def game_timer(ticks, over_time, color, pos): # Таймер для игры
    time = over_time - round(ticks/60)
    time_txt = simple_font.render('Время:'+str(time), True, color)
    window.blit(time_txt, (pos))
    return time

def game_stopwatch(ticks, color, pos): # Таймер для игры
    time = round(ticks/60)
    time_txt = simple_font.render('Время:'+str(time), True,(color))
    window.blit(time_txt, (pos))
    return time

class GameSpriteMini(pg.sprite.Sprite): # Класс неподвижного объекта Для мини игр
    def __init__(self, width, height, x_cord, y_cord, picture, minigame):
        super().__init__()
        
        self.image = pg.transform.scale(pg.image.load(picture), (width, height)) # Создаёт текстуру персонажу
        self.rect = self.image.get_rect() # Задаёт квадрат
        self.rect.x = x_cord # Задаёт координату X
        self.rect.y = y_cord # Задаёт координату Y
        self.minigame = minigame
        if self.minigame == 'labirint':
            self.add(all_sprites_mini_game_2)

    def draw(self): # Рисует объект на экране
        window.blit(self.image, (self.rect.x, self.rect.y))
        return window

class Wall(pg.sprite.Sprite):
    def __init__(self, **args):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([args['width'], args['height']])
        if args.get('color') != None:
            self.image.fill(args['color'])
        self.rect = self.image.get_rect()
        self.rect.x = args['x']
        self.rect.y = args['y']
        self.mini_game = args['minigame']
        if self.mini_game == 'labirint':
            self.add(barriers_1, all_sprites_mini_game_2)

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
            reset()
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        #return window

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

def reset():
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
    
lab_attemps = 3

pause_text = big_font.render('ПАУЗА', True, (5, 175, 0))
pause_pos = (window_width//2-90, window_height//2-50)

barriers_1 = pg.sprite.Group()
all_sprites_mini_game_2 = pg.sprite.Group()

lab_player = LabirintPlayer(width=20, height=20, color=Laser_C, x=350, y=45)


create_labirint()

labirint_background = pg.transform.scale(pg.image.load(labirint_back),(window_width, window_height))

labrirint = True

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

while run:
    if labrirint:
        
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
        clock.tick(60)
