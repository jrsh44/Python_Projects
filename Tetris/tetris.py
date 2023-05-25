import random
import pygame
pygame.font.init()
######################

S_WIDTH = 800
S_HEIGHT = 700
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30
BG_COLOR = (0,0,0)
TEXT_COLOR = (255,255,255)
FRAME_COLOR = (255,0,0)
GRID_LINE_COLOR = (46, 48, 54)

#################################
 
S = [['.....',
      '......',
      '..00..',
      '.00...',
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
 
###################################

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 
top_left_x = (S_WIDTH-PLAY_WIDTH)//2
top_left_y = S_HEIGHT - PLAY_HEIGHT
 
####################################


class Piece(object):
    rows = 20
    columns = 10
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
 
def create_grid(locked_positions={}):
    grid = [[BG_COLOR for _ in range(10)] for _ in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
          if (j, i) in locked_positions:
                key = locked_positions[(j,i)]
                grid[i][j]=key
    return grid

def update_score(nscore):
    score = max_score()
    
    with open('Tetris\\score.txt','w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] 

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i]= (pos[0] - 2, pos[1]-4)
    
    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j]==BG_COLOR] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1]>-1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x,y = pos
        if y < 1:
            return True
    return False
 
def get_shape():
    return Piece(5, 0, random.choice(shapes))
 
def max_score():
    with open('Tetris\\score.txt','r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score
 
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('consalis',size,bold=True)
    label = font.render(text,1,color)
    xPos = top_left_x + PLAY_WIDTH/2 - label.get_width()/2
    yPos = top_left_y + PLAY_HEIGHT/2 - label.get_height()/2
    surface.blit(label, (xPos,yPos))
   
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface, GRID_LINE_COLOR, (sx, sy+i*BLOCK_SIZE), (sx+PLAY_WIDTH, sy+i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, GRID_LINE_COLOR, (sx + j*BLOCK_SIZE, sy),(sx + j*BLOCK_SIZE, sy+PLAY_HEIGHT))
         

def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if BG_COLOR not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x,y = key
            if y < ind:
                newKey = (x,y+inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans',30)
    label = font.render('Next shape', 1, TEXT_COLOR)

    sx = top_left_x+PLAY_WIDTH+50
    sy = top_left_y+PLAY_HEIGHT/2-100
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column =='0':
                pygame.draw.rect(surface, shape.color, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),0)
    surface.blit(label, (sx+10,sy-40))


 
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill(BG_COLOR)

    font = pygame.font.SysFont('comicsans',60)
    label = font.render('Tetris', 1, TEXT_COLOR)
    surface.blit(label, (top_left_x + PLAY_WIDTH/2 - label.get_width()/2, 30))

    #current score
    font = pygame.font.SysFont('comicsans',30)
    label = font.render(f'Score: {score}', 1, TEXT_COLOR)

    sx = top_left_x+PLAY_WIDTH+50
    sy = top_left_y+PLAY_HEIGHT/2 - 100

    surface.blit(label, (sx+20,sy+160))

    #max score
    label2 = font.render(f'High score: {last_score}', 1, TEXT_COLOR)
    sx = 10
    sy = top_left_y
    surface.blit(label2, (sx,sy))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*BLOCK_SIZE, top_left_y + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, FRAME_COLOR, (top_left_x, top_left_y, PLAY_WIDTH, PLAY_HEIGHT), 4)

 
def main(window):
    last_score = max_score()

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.27
    score = 0

    while run:


        level_time += clock.get_rawtime()
        fall_time += clock.get_rawtime()

        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.003


        grid = create_grid(locked_positions)
        if fall_time/1000 >= fall_speed:
            fall_time=0
            current_piece.y +=1
            if not (valid_space(current_piece, grid)) and current_piece.y >0:
                current_piece.y -=1
                change_piece = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.display.quit()
                quit()
            
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x +=1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -=1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions)*10

        draw_window(window, grid, score, last_score)  
        draw_next_shape(next_piece,window)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("YOU LOST!", 80, TEXT_COLOR, window)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            update_score(score)
    
          
def main_menu(window):
    run = True
    while run:
        window.fill(BG_COLOR)
        draw_text_middle('Press any key to play!',60,TEXT_COLOR, window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(window)

    pygame.display.quit()           

window = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
pygame.display.set_caption('Tetris')

main_menu(window)  # start game