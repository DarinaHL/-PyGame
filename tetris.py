import pygame
import random
from random import choice

bg = pygame.image.load("bg.jpg")
bgg = pygame.image.load("bgg.jpg")
windowSurface = pygame.display.set_mode((800, 700))
windowSurface.blit(bgg, (800, 700))
musical_files = ["mega.mp3", "space.mp3", "spi.mp3", "bone.mp3", "glam.mp3",
                 "fish.mp3", "bone.mp3", "dum.mp3", "nap.mp3"]
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.load("intro.mp3")
pygame.mixer.music.play(-1)
sound1 = pygame.mixer.Sound("pong.mp3")
sound2 = pygame.mixer.Sound("lose.mp3")
good = pygame.mixer.Sound("good.mp3")
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
channel4 = pygame.mixer.Channel(3)
s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(132, 235, 254), (203, 253, 187), (89, 72, 229), (244, 255, 129),
                (252, 199, 104), (61, 90, 254), (219, 214, 248)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_pole(locked_pos=None):
    if locked_pos is None:
        locked_pos = {}
    pole = [[(0, 0, 0) for i in range(10)] for i in range(20)]
    for i in range(len(pole)):
        for j in range(len(pole[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                pole[i][j] = c
    return pole


def convert_shape_format(shape):
    positions = []
    formatte = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(formatte):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_the_middle_text(surface, text, size, color):
    font = pygame.font.SysFont("Papyrus", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2),
                         top_left_y + play_height / 2 - label.get_height() / 2))


def let_the_drawer_drawth_the_gridth(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface, (193, 135, 227), (sx, sy + i * block_size),
                         (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (193, 135, 227), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(pole, locked):
    global the_indeth
    inc = 0
    for i in range(len(pole) - 1, -1, -1):
        row = pole[i]
        if (0, 0, 0) not in row:
            inc += 1
            the_indeth = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < the_indeth:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Papyrus', 30, 30, 30)
    label = font.render('NEXT', 1, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 120
    formatte = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(formatte):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size + 30,
                                                        block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))


def update_score(score_of_the_player):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > score_of_the_player:
            f.write(str(score))
        else:
            f.write(str(score_of_the_player))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def draw_window(surface, pole, score=0, last_score=0):
    windowSurface.blit(bg, (0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('Papyrus', 60)
    label = font.render('Tetris', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 20))
    font = pygame.font.SysFont('Papyrus', 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    surface.blit(label, (sx + 20, sy + 160))
    label = font.render('Record: ' + str(last_score), 1, (255, 255, 255))
    sx = top_left_x - 200
    sy = top_left_y + 200
    surface.blit(label, (sx + 20, sy + 160))
    for i in range(len(pole)):
        for j in range(len(pole[i])):
            pygame.draw.rect(surface, pole[i][j], (top_left_x + j * block_size, top_left_y + i * block_size,
                                                   block_size, block_size), 0)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    let_the_drawer_drawth_the_gridth(surface, pole)


def main(win):
    last_score = max_score()
    locked_positions = {}
    pole = create_pole(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.25
    level_time = 0
    score = 0

    while run:
        pole = create_pole(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, pole)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    channel1.play(sound1)
                    if not (valid_space(current_piece, pole)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    channel1.play(sound1)
                    if not (valid_space(current_piece, pole)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    channel1.play(sound1)
                    if not (valid_space(current_piece, pole)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    channel1.play(sound1)
                    if not (valid_space(current_piece, pole)):
                        current_piece.rotation -= 1
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                pole[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            t = score
            score += clear_rows(pole, locked_positions) * 10
            if score != t:
                channel3.play(good)
                t = score

        draw_window(win, pole, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_the_middle_text(win, "YOU      LOSE !", 80, (255, 255, 255))
            pygame.mixer.music.stop()
            channel2.play(sound2)
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)
            pygame.mixer.music.load("intro.mp3")
            pygame.mixer.music.play(-1)


def main_menu(win):
    run = True
    pygame.mixer.music.load("intro.mp3")
    pygame.mixer.music.play(-1)
    while run:
        windowSurface.blit(bgg, (0, 0))
        draw_the_middle_text(win, 'Press any key to play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.load(choice(musical_files))
                pygame.mixer.music.play(-1)
                main(win)
    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Тетрис')
main_menu(win)
