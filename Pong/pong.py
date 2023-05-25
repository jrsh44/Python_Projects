from tkinter import *
import random
import time

############################
GAME_WIDTH = 1000
GAME_HEIGHT = 800
OBJ_WIDTH = 20
PADDLE_LENGTH = 100
PADDLE_COLOR = 'white'
BALL_COLOR = 'white'
TEXT_COLOR = 'white'
BACKGROUND_COLOR = 'black'
PADDLE_SPEED = 20
############################

class Paddle():
    def __init__(self,x_location):
        y = round(GAME_HEIGHT/2-PADDLE_LENGTH/2)
        self.item = gamepanel.create_rectangle(x_location, y, x_location+OBJ_WIDTH, y+PADDLE_LENGTH, fill=PADDLE_COLOR)

class Ball():
    def __init__(self):
        x = round(GAME_WIDTH/2-OBJ_WIDTH/2)
        y = round(GAME_HEIGHT/2-OBJ_WIDTH/2)
        self.item = gamepanel.create_rectangle(x, y, x+OBJ_WIDTH, y+OBJ_WIDTH, fill=BALL_COLOR, tag='ball')

def paddle_move(type,direction):
    if type == "a":
        paddle_a_coordinates = gamepanel.coords(paddle_a.item)
        if direction == 'up' and paddle_a_coordinates[1] - PADDLE_SPEED >=0:
            gamepanel.move(paddle_a.item,0,-PADDLE_SPEED)
        elif direction == 'down' and paddle_a_coordinates[3] + PADDLE_SPEED <= GAME_HEIGHT:
            gamepanel.move(paddle_a.item,0,PADDLE_SPEED)
    elif type == "b":
        paddle_b_coordinates = gamepanel.coords(paddle_b.item)
        if direction == 'up' and paddle_b_coordinates[1] - PADDLE_SPEED >=0:
            gamepanel.move(paddle_b.item,0,-PADDLE_SPEED)
        elif direction == 'down' and paddle_b_coordinates[3] + PADDLE_SPEED <= GAME_HEIGHT:
            gamepanel.move(paddle_b.item,0,PADDLE_SPEED) 
    window.update()
    

#############################

window = Tk()
window.title("Pong")
score_a = score_b = 0

#   Frame
frame = Frame(window, bg= BACKGROUND_COLOR)
frame.pack()

#   Scoreboard
scoreboard = Label(frame,text=f"Paddle A: {score_a}   Paddle B: {score_b}", font=('Consolas',30), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
scoreboard.pack()

#   Gamepad
gamepanel = Canvas(frame,bg=BACKGROUND_COLOR,width=GAME_WIDTH,height=GAME_HEIGHT)
gamepanel.pack()

#   Placing window in the center of the screen
window.update()
window_height = window.winfo_height()
window_width = window.winfo_width()
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()
x_cor = round(screen_width/2 - window_width/2)
y_cor = round(screen_height/2 - window_height/2)
window.geometry(f"{window_width}x{window_height}+{x_cor}+{y_cor}")
window.resizable(False, False)

#   Creating paddles
paddle_a = Paddle(20)
paddle_b = Paddle(GAME_WIDTH-40)

#   Creating ball + movement
ball = Ball()
xVelocity = random.randint(3,6)
yVelocity = random.randint(3,6)


#   Binds
window.bind("<w>",lambda event:paddle_move('a','up'))
window.bind("<s>",lambda event:paddle_move('a','down'))
window.bind("<Up>",lambda event:paddle_move('b','up'))
window.bind("<Down>",lambda event:paddle_move('b','down'))

#   Starting
while True:
        #   Border checking
    ball_coordinates = gamepanel.coords(ball.item)
    if (ball_coordinates[3] + yVelocity > GAME_HEIGHT and yVelocity >0) or (ball_coordinates[1] + yVelocity <= 0 and yVelocity < 0):
        yVelocity = -yVelocity

    #   Bounce checking
    if xVelocity > 0:
        paddle_cordinates = gamepanel.coords(paddle_b.item)
        if ball_coordinates[2] > paddle_cordinates[0]-4 and ball_coordinates[2] <= paddle_cordinates[0]+3 and ball_coordinates[1] < paddle_cordinates[3] and ball_coordinates[3] > paddle_cordinates[1]:
            xVelocity = -random.randint(3,5)
            if yVelocity > 0 :yVelocity = random.randint(3,5)
            if yVelocity < 0 :yVelocity = -random.randint(3,5)
    elif xVelocity < 0:
        paddle_cordinates = gamepanel.coords(paddle_a.item)
        if ball_coordinates[0] < paddle_cordinates[2]+3 and ball_coordinates[0] >= paddle_cordinates[2]-4 and ball_coordinates[1] < paddle_cordinates[3] and ball_coordinates[3] > paddle_cordinates[1]:
            xVelocity = random.randint(3,5)
            if yVelocity > 0 :yVelocity = random.randint(3,5)
            if yVelocity < 0 :yVelocity = -random.randint(3,5)

    #   Moving the ball
    gamepanel.move(ball.item,xVelocity,yVelocity)
    ball_coordinates = gamepanel.coords(ball.item)

    #   Goal checking
    if ball_coordinates[2] >= GAME_WIDTH-10 or ball_coordinates[0] <= 10:
        if ball_coordinates[2] >= GAME_WIDTH-10:
            score_a +=1
        elif ball_coordinates[0] <= 10:
            score_b +=1
        # winsound.PlaySound("Pong\\goal_sound.wav", winsound.SND_ASYNC)
        scoreboard.config(text=f"Paddle A: {score_a}   Paddle B: {score_b}")
        gamepanel.delete(ball.item)
        xVelocity = random.randint(3,5)
        yVelocity = random.randint(3,5)
        ball = Ball()

    #   Loop
    window.update()
    time.sleep(0.01)