import pygame
import os
import random
#import time

WIDTH, HEIGHT = 600, 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling fruits")

RED = (255, 0, 0)
WHITE = (255, 255, 255)
FPS = 60
FRUIT_IMAGE_WIDTH, FRUIT_IMAGE_HEIGHT = 55, 40
GLUTTONY_IMAGE_WIDTH, GLUTTONY_IMAGE_HEIGHT = 50.9, 70
#POSSIBLE_X_SPAWN = [element for element in range(1, 600) if element%60]
POSSIBLE_X_SPAWN = [10,65,120,175,230,285,340]
POSSIBLE_Y_SPAWN = [-300,-240,-180,-120,-60,0,60]
POSSIBLE_BOMB_Y_SPAWN = [-330, -270, -210, -150, -90, -30, 30]
GLUTTONY_Y_SPAWN = 649.9
GLUTTONY_X_SPAWN = 265
GLUTTONY_VEL = 8

GLUTTONY_ATE = pygame.USEREVENT + 1
FRUIT_HAS_FALLEN = pygame.USEREVENT + 2
BOMB_DAMAGED_GLUTTONY = pygame.USEREVENT + 3
BOMB_TO_CLOSE_TO_FRUIT = pygame.USEREVENT + 4
BOMB_OUT_OF_BOARD = pygame.USEREVENT + 5

ZERO_IMAGE = pygame.image.load(os.path.join('0.png'))
ONE_IMAGE = pygame.image.load(os.path.join('1.png'))
TWO_IMAGE = pygame.image.load(os.path.join('2.png'))
THREE_IMAGE = pygame.image.load(os.path.join('3.png'))
FOUR_IMAGE = pygame.image.load(os.path.join('4.png'))
FIFE_IMAGE = pygame.image.load(os.path.join('5.png'))
SIX_IMAGE = pygame.image.load(os.path.join('6.png'))
SEVEN_IMAGE = pygame.image.load(os.path.join('7.png'))
EIGHT_IMAGE = pygame.image.load(os.path.join('8.png'))
NINE_IMAGE = pygame.image.load(os.path.join('9.png'))
number_dictionary = {0:ZERO_IMAGE, 1:ONE_IMAGE, 2:TWO_IMAGE, 3:THREE_IMAGE, 4:FOUR_IMAGE, 5:FIFE_IMAGE, 
                6:SIX_IMAGE, 7:SEVEN_IMAGE, 8:EIGHT_IMAGE, 9:NINE_IMAGE}
scaled_numbers_list = [pygame.transform.scale(value, (FRUIT_IMAGE_WIDTH, FRUIT_IMAGE_HEIGHT)) for value in number_dictionary.values()]
scaled_numbers_dictionary = {0:scaled_numbers_list[0], 1:scaled_numbers_list[1], 2:scaled_numbers_list[2], 3:scaled_numbers_list[3], 4:scaled_numbers_list[4],
                             5:scaled_numbers_list[5], 6:scaled_numbers_list[6], 7:scaled_numbers_list[7], 8:scaled_numbers_list[8], 9:scaled_numbers_list[9]}
HEART_IMAGE = pygame.image.load(os.path.join('heart.png'))
HEART = pygame.transform.scale(HEART_IMAGE, (FRUIT_IMAGE_WIDTH, FRUIT_IMAGE_HEIGHT))
APPLE_IMAGE = pygame.image.load(os.path.join('apple.png'))
APPLE = pygame.transform.scale(APPLE_IMAGE, (FRUIT_IMAGE_WIDTH, FRUIT_IMAGE_HEIGHT))
BOMB_IMAGE = pygame.image.load(os.path.join('bomb.png'))
BOMB = pygame.transform.scale(BOMB_IMAGE, (FRUIT_IMAGE_WIDTH, FRUIT_IMAGE_HEIGHT))
GLUTTONY_IMAGE = pygame.image.load(os.path.join('icons8-pacman-48.png'))
GLUTTONY = pygame.transform.rotate(pygame.transform.scale(GLUTTONY_IMAGE, (GLUTTONY_IMAGE_WIDTH, GLUTTONY_IMAGE_HEIGHT)), 90)
#list_fruit_images = [APPLE, LEMON]


def draw_window(gluttony, apples_in_game, gluttony_health_points, gluttony_score):
    WIN.fill(WHITE)        
    blit_score(gluttony_score)
    for fruit in apples_in_game:
        WIN.blit(APPLE, (fruit.x, fruit.y))
    for bomb in bombs_in_game:
        WIN.blit(BOMB, (bomb.x, bomb.y))
    for i in range(gluttony_health_points):
        WIN.blit(HEART, (535 - i*65, 10))
    WIN.blit(GLUTTONY, (gluttony.x, gluttony.y))
    pygame.display.update()

def blit_score(gluttony_score):
    if gluttony_score < 10:
        for i in str(gluttony_score):
            WIN.blit(scaled_numbers_dictionary[int(i)], (0,0))
    elif gluttony_score > 10 and gluttony_score < 100:
        WIN.blit(scaled_numbers_dictionary[int(str(gluttony_score)[0])], (0,0))
        for i in str(gluttony_score)[1]:
            WIN.blit(scaled_numbers_dictionary[int(i)], (40,0))
    elif gluttony_score > 100 and gluttony_score < 1000:
        WIN.blit(scaled_numbers_dictionary[int(str(gluttony_score)[0])], (0,0))
        for i in str(gluttony_score)[1]:
            WIN.blit(scaled_numbers_dictionary[int(i)], (40,0))
        for i in str(gluttony_score)[2]:
            WIN.blit(scaled_numbers_dictionary[int(i)], (80,0))

def falling_fruits(apples_in_game, fruit_vel):
    for fruit in apples_in_game:
        fruit.y += fruit_vel

def falling_bombs(bombs_in_game, fruit_vel):
    for bomb in bombs_in_game:
        bomb.y += fruit_vel

def handle_gluttony_movement(key_pressed, gluttony):
    if key_pressed[pygame.K_a] and gluttony.x - GLUTTONY_VEL > 0:
        gluttony.x -= GLUTTONY_VEL
    elif key_pressed[pygame.K_d] and gluttony.x + GLUTTONY_VEL + GLUTTONY_IMAGE_HEIGHT < WIDTH:
        gluttony.x += GLUTTONY_VEL


def create_bombs(avaliable_bomb_x_spawn, avaliable_bomb_y_spawn, max_bombs):
    if len(avaliable_bomb_y_spawn) == 0:
            avaliable_bomb_y_spawn += POSSIBLE_Y_SPAWN
    if len(avaliable_bomb_x_spawn) == 0:
        avaliable_bomb_x_spawn += POSSIBLE_X_SPAWN
    if len(bombs_in_game) < max_bombs:
        bomb_x_spawn = random.choice(avaliable_bomb_x_spawn)
        bomb_y_spawn = random.choice(avaliable_bomb_y_spawn)
        bomb = pygame.Rect(bomb_x_spawn, bomb_y_spawn, FRUIT_IMAGE_WIDTH, FRUIT_IMAGE_HEIGHT)
        bombs_in_game.append(bomb)

def create_fruits(avaliable_x_spawn, avaliable_y_spawn, max_fruits):
    if len(avaliable_y_spawn) == 0:
            avaliable_y_spawn += POSSIBLE_Y_SPAWN
    if len(avaliable_x_spawn) == 0:
        avaliable_x_spawn += POSSIBLE_X_SPAWN
    if len(apples_in_game) < max_fruits:
        fruit_x_spawn = random.choice(avaliable_x_spawn)
        fruit_y_spawn = random.choice(avaliable_y_spawn)
        apple = pygame.Rect(fruit_x_spawn, fruit_y_spawn, FRUIT_IMAGE_WIDTH, FRUIT_IMAGE_HEIGHT)
        avaliable_y_spawn.remove(fruit_y_spawn)
        avaliable_x_spawn.remove(fruit_x_spawn)
        apples_in_game.append(apple)            

def game_level(gluttony_score, max_bombs, max_fruits, fruit_vel):
    if gluttony_score < 30:
        fruit_vel += 1.5
        max_fruits += 5
        return max_fruits, fruit_vel, max_bombs
    if gluttony_score >= 30 and gluttony_score < 50:
        max_fruits += 7
        fruit_vel += 2
        max_bombs += 1
        return max_fruits, fruit_vel, max_bombs
    elif gluttony_score >= 50 and gluttony_score < 100:
        max_fruits  += 10
        max_bombs += 1
        fruit_vel += 2.5
        return max_fruits, fruit_vel, max_bombs
    elif gluttony_score >= 100:
        max_fruits += 10
        max_bombs += 2
        fruit_vel += 3
        return max_fruits, fruit_vel, max_bombs



apples_in_game = []
bombs_in_game = []

border = pygame.Rect(0,699,WIDTH,1)
gluttony = pygame.Rect(GLUTTONY_X_SPAWN, GLUTTONY_Y_SPAWN, GLUTTONY_IMAGE_WIDTH, GLUTTONY_IMAGE_HEIGHT) 
clock = pygame.time.Clock()

def main():
    fruit_vel = 0
    max_bombs = 0
    max_fruits = 0
    gluttony_score = 0
    gluttony_health_points = 3
    avaliable_y_spawn = [-300,-240,-180,-120,-60,0,60]
    avaliable_x_spawn = [10,65,120,175,230,285,340]
    avaliable_bomb_x_spawn = [10,65,120,175,230,285,340]
    avaliable_bomb_y_spawn = [-300,-240,-180,-120,-60,0,60]
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if gluttony_score < 30:
            fruit_vel = 2
            max_bombs = 0
            max_fruits = 5
        elif gluttony_score >=30 and gluttony_score < 50:
            fruit_vel = 2.5
            max_bombs = 0
            max_fruits = 7
        elif gluttony_score >= 50:
            fruit_vel = 2.5
            max_bombs = 1
            max_fruits = 7
        if gluttony_health_points >= 1:
            keys_pressed = pygame.key.get_pressed()
            create_bombs(avaliable_bomb_x_spawn, avaliable_bomb_y_spawn, max_bombs)
            create_fruits(avaliable_x_spawn, avaliable_y_spawn, max_fruits)
            handle_gluttony_movement(keys_pressed, gluttony)
            falling_fruits(apples_in_game, fruit_vel)
            falling_bombs(bombs_in_game, fruit_vel)
            #funkcja did_event_occur nie chciałą działać dlatego wrzuciłem to po prostu do main
            for fruit in apples_in_game:
                if fruit.colliderect(gluttony):
                    pygame.event.post(pygame.event.Event(GLUTTONY_ATE))
                    gluttony_score += 1
                    apples_in_game.remove(fruit)
            for fruit in apples_in_game:
                if fruit.colliderect(border):
                    pygame.event.post(pygame.event.Event(FRUIT_HAS_FALLEN))
                    gluttony_health_points -= 1
                    apples_in_game.remove(fruit)
            for bomb in bombs_in_game:
                for fruit in apples_in_game:
                    if bomb.colliderect(fruit):
                        pygame.event.post(pygame.event.Event(BOMB_TO_CLOSE_TO_FRUIT))
                        bombs_in_game.remove(bomb)
            for bomb in bombs_in_game:
                if bomb.colliderect(gluttony):
                    pygame.event.post(pygame.event.Event(BOMB_DAMAGED_GLUTTONY))
                    gluttony_health_points -= 1
                    if gluttony_score >= 5:
                        gluttony_score -=5
                    else:
                        gluttony_score = 0
                    bombs_in_game.remove(bomb)
                elif bomb.colliderect(border):
                    pygame.event.post(pygame.event.Event(BOMB_OUT_OF_BOARD))
                    bombs_in_game.remove(bomb)
            draw_window(gluttony, apples_in_game, gluttony_health_points, gluttony_score)


#Filmik na poczatku co sie dzieje w grze         
#Zrobić różne funkcje na rózne obrazy.
#Mozna zrobić rózne velocity dla różnych owoców i rózną ilosć punktóœ 
#owoce powinny przyspieszac po pewnym czasie i powinna byc mozliwa większa ilośc na ekranie



if __name__ == '__main__':
    main()