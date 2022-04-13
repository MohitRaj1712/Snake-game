# The Snake (CUT AND GLUE GAME)

import pygame
import pygame_widgets
from pygame_widgets.button import Button
import random

# initialize the game
pygame.init()

# GAME_CONSTANTS
GAME_FOLDER = 'D:/Snake_Game

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 700

FPS = 30

BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
DARK_RED = pygame.Color(136, 0, 21)
ORANGE = pygame.Color(255, 127, 0)
BLUE = pygame.Color(0, 0, 255)

# create the game window
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('The SNAKE')

# snake
snake = pygame.image.load(GAME_FOLDER + 'snake.jpg')

# tiles
tiles = []
for i in range(24):
    temp = pygame.image.load(GAME_FOLDER + 'snake_' + str(i) + '.png')
    tiles.append((temp, temp.get_rect(), i))

tile_index = 0
random.shuffle(tiles)

#tile_map
tile_map = [[0,1,2,3,4,5],[6,7,8,9,10,11],[12,13,14,15,16,17],[18,19,20,21,22,23]]

def fx_left():
    global tile_index
    if tile_index < 14:
        tile_index += 1


def fx_right():
    global tile_index
    if tile_index > 0:
        tile_index -= 1


# left and the right buttons
bttn_left = Button(win=display_surface, x=90, y=WINDOW_HEIGHT - 100, width=50, height=50, text='<<', inactiveColour=RED, hoverColour=ORANGE, pressedColour=DARK_RED, onClick=fx_left)
bttn_right = Button(win=display_surface, x=WINDOW_WIDTH - 140, y=WINDOW_HEIGHT - 100, width=50, height=50, text='>>', inactiveColour=RED, hoverColour=ORANGE, pressedColour=DARK_RED, onClick=fx_right)

#cut and glue
cut = pygame.image.load(GAME_FOLDER + 'cut.png')
cut_rect = cut.get_rect()
cut_copy = cut.copy()
glue = pygame.image.load(GAME_FOLDER + 'glue.png')
glue_rect = glue.get_rect()
glue_copy = glue.copy()

#sounds
loss = pygame.mixer.Sound(GAME_FOLDER + 'loss.wav')
pickup = pygame.mixer.Sound(GAME_FOLDER + 'pickup.wav')

#game_values
mouse_icon = None
clipboard = None
time = 60*2
lives = 5
timer = FPS
game_status = 1

#game fonts and texts
game_font_big = pygame.font.Font(GAME_FOLDER + 'SunnyspellsRegular.otf', 60)
game_font = pygame.font.Font(GAME_FOLDER + 'SunnyspellsRegular.otf', 40)

game_title = game_font_big.render('THE SNAKE', True, RED)
game_title_rect = game_title.get_rect()
game_title_rect.centerx = WINDOW_WIDTH//2
game_title_rect.top = 10

game_lives = game_font.render('Lives: ' + str(lives), True, RED)
game_lives_rect = game_lives.get_rect()
game_lives_rect.left = 50
game_lives_rect.top = 10

game_time = game_font.render('Time: ' + str(time), True, RED)
game_time_rect = game_time.get_rect()
game_time_rect.right = WINDOW_WIDTH -50
game_time_rect.top = 10

game_over_win = game_font_big.render('GAME OVER, You WIN!!!', True, RED)
game_over_loss = game_font_big.render('GAME OVER, You LOSE!!!', True, RED)
game_over = game_over_win
game_over_rect = game_over.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

game_replay_or_quit = game_font.render('Press r to replay, q to quit.', True, BLUE)
game_replay_or_quit_rect = game_replay_or_quit.get_rect()
game_replay_or_quit_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 60)


# main game loop (life of the game)
clock = pygame.time.Clock()
running = True
while running:

    # apply the background color
    display_surface.fill(BLACK)

    # blit the snake
    display_surface.blit(snake, (10, 100))

    # draw the target grid
    target_grid_x = 690
    target_grid_y = 100
    for rows in range(4):
        for cols in range(6):
            box = (target_grid_x + cols * 100, target_grid_y + rows * 100, 100, 100) # (left,top,width,height)
            pygame.draw.rect(surface=display_surface, color=RED, rect=box, width=3)
            if not isinstance(tile_map[rows][cols], int):
                tile_map[rows][cols][1].topleft = (box[0], box[1])
                display_surface.blit(tile_map[rows][cols][0], tile_map[rows][cols][1])


    # draw the reel
    reel_grid_x = 150
    reel_grid_y = WINDOW_HEIGHT - 150
    for i in range(10):
        try:
            box = (reel_grid_x + i * 100, reel_grid_y, 100, 100)
            pygame.draw.rect(surface=display_surface, color=BLUE, rect=box, width=3)
            tiles[tile_index + i][1].topleft = (box[0], box[1])
            display_surface.blit(tiles[tile_index + i][0], tiles[tile_index + i][1])
        except:
            pass
    # read the events
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_r and game_status == 2:
                #restart
                tile_map = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 17],
                            [18, 19, 20, 21, 22, 23]]
                tiles.clear()
                for i in range(24):
                    temp = pygame.image.load(GAME_FOLDER + 'snake_' + str(i) + '.png')
                    tiles.append((temp, temp.get_rect(), i))

                tile_index = 0
                random.shuffle(tiles)

                mouse_icon = None
                clipboard = None
                time = 60 * 2
                lives = 5
                timer = FPS
                game_status = 1

                game_lives = game_font.render('Lives: ' + str(lives), True, RED)
                game_time = game_font.render('Time: ' + str(time), True, RED)

            elif ev.key == pygame.K_q:
                running = False
        elif ev.type == pygame.MOUSEMOTION:
            if ev.pos[0] >= target_grid_x and ev.pos[0] <= target_grid_x + 600 and ev.pos[1] >= target_grid_y and ev.pos[1] <= target_grid_y + 400:
                mouse_icon = 'glue'
            elif ev.pos[0] >= reel_grid_x and ev.pos[0] <= reel_grid_x + 1000 and ev.pos[1] >= reel_grid_y and ev.pos[1] <= reel_grid_y + 100:
                mouse_icon = 'cut'
            else:
                mouse_icon = None
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1 and game_status ==1:

                if mouse_icon == 'glue' :
                    if clipboard is not None:
                        col_index = (ev.pos[0]- target_grid_x)//100
                        row_index = (ev.pos[1]- target_grid_y)//100
                        if tile_map[row_index][col_index] == clipboard[2]:
                            tile_map[row_index][col_index] = clipboard
                            clipboard = None
                            glue = glue_copy.copy()
                            cut = cut_copy.copy()
                            pickup.play()
                            #extra time for a correct placement
                            time+=5
                            game_time = game_font.render('Time: ' + str(time), True, RED)
                            #check win
                            if len(tiles) == 0:
                                game_status = 2
                                game_over = game_over_win
                                pickup.play(5)
                        else:
                            loss.play()
                            lives-=1
                            game_lives = game_font.render('Lives: ' + str(lives), True, RED)
                            if lives == 0:
                                game_over = game_over_loss
                                game_status = 2

                elif mouse_icon == 'cut':
                    i = tile_index #first element of the reel
                    max = tile_index+10 # reel size is 10
                    while i < max:
                        if tiles[i][1].collidepoint(ev.pos):
                            print('clicked on tile ', i, ev.pos)
                            if clipboard is not None:
                                tiles.append(clipboard)
                            clipboard = tiles.pop(i)
                            temp = pygame.transform.scale( clipboard[0], (50,50))
                            cut.blit(temp, (35,15))
                            glue.blit(temp,(25,25))
                            break
                        i+=1

    if game_status ==1:
        timer -= 1
        if timer == 0:
            time -= 1
            game_time = game_font.render('Time: ' + str(time), True, RED)
            timer = FPS
            if time == 0:
                game_status =2
                game_over = game_over_loss

        if mouse_icon is None:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
            if mouse_icon == 'cut':
                cut_rect.center = pygame.mouse.get_pos()
                display_surface.blit(cut, cut_rect)
            elif mouse_icon == 'glue':
                glue_rect.center = pygame.mouse.get_pos()
                display_surface.blit(glue, glue_rect)

    if game_status ==2:
        display_surface.blit(game_over, game_over_rect)
        display_surface.blit(game_replay_or_quit, game_replay_or_quit_rect)

    #blit the hud
    display_surface.blit(game_title, game_title_rect)
    display_surface.blit(game_lives, game_lives_rect)
    display_surface.blit(game_time, game_time_rect)

    # refresh the pygame-widgets
    pygame_widgets.update(events)
    # refersh the display
    pygame.display.update()
    # moderates the loop iteration rate
    # makes the games run at the same speed over different cpu's
    clock.tick(FPS)

# quit the game
pygame.quit()


