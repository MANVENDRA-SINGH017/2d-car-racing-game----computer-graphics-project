import turtle
import random

# Screen setup
wn = turtle.Screen()
wn.title("Real Car Game")
wn.bgcolor("black")
wn.setup(width=600, height=700)
wn.tracer(0)

# Register car images
wn.register_shape("player.gif")
wn.register_shape("enemy.gif")

# Lanes
lanes = [-150, -50, 50, 150]
current_lane = 2

# Road borders
border = turtle.Turtle()
border.speed(0)
border.color("white")
border.penup()
border.goto(-200, -350)
border.pendown()
border.goto(-200, 350)
border.penup()
border.goto(200, -350)
border.pendown()
border.goto(200, 350)
border.hideturtle()

# Moving lane dashes
lane_dashes = []
for x in [-100, 0, 100]:
    for i in range(10):
        dash = turtle.Turtle()
        dash.shape("square")
        dash.color("gray")
        dash.shapesize(stretch_wid=1, stretch_len=0.2)
        dash.penup()
        dash.goto(x, i * 80 - 350)
        lane_dashes.append(dash)

# Player car
player = turtle.Turtle()
player.shape("player.gif")
player.penup()
player.goto(lanes[current_lane], -300)

# Enemy cars
enemies = []
for i in range(4):
    enemy = turtle.Turtle()
    enemy.shape("enemy.gif")
    enemy.penup()
    enemy.goto(random.choice(lanes), random.randint(100, 500))
    enemies.append(enemy)

# Score display
score = 0
score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 300)

# Game over display (separate)
game_over_display = turtle.Turtle()
game_over_display.color("white")
game_over_display.penup()
game_over_display.hideturtle()

def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Arial", 16, "bold"))

update_score()

# Controls
def move_left():
    global current_lane
    if current_lane > 0:
        current_lane -= 1
        player.goto(lanes[current_lane], -300)

def move_right():
    global current_lane
    if current_lane < len(lanes) - 1:
        current_lane += 1
        player.goto(lanes[current_lane], -300)

def enable_controls():
    wn.listen()
    wn.onkey(move_left, "Left")
    wn.onkey(move_right, "Right")

def disable_controls():
    wn.onkey(None, "Left")
    wn.onkey(None, "Right")

enable_controls()

# Collision
def is_collision(t1, t2):
    return t1.distance(t2) < 25

# Speeds
enemy_speed = 4
road_speed = 6

# Restart function
def restart_game():
    global score, enemy_speed, current_lane

    score = 0
    enemy_speed = 4
    current_lane = 2

    update_score()
    game_over_display.clear()

    # Reset player
    player.goto(lanes[current_lane], -300)

    # Reset enemies
    for enemy in enemies:
        enemy.goto(random.choice(lanes), random.randint(100, 500))

    enable_controls()
    game_loop()

# Game loop
def game_loop():
    global score, enemy_speed

    # Move road
    for dash in lane_dashes:
        dash.sety(dash.ycor() - road_speed)
        if dash.ycor() < -350:
            dash.sety(350)

    # Move enemies
    for enemy in enemies:
        enemy.sety(enemy.ycor() - enemy_speed)

        if enemy.ycor() < -350:
            enemy.goto(random.choice(lanes), random.randint(300, 600))
            score += 10
            update_score()

        # Collision
        if is_collision(player, enemy):
            game_over_display.goto(0, 0)
            game_over_display.write("GAME OVER\nPress R to Restart",
                                    align="center",
                                    font=("Arial", 20, "bold"))

            disable_controls()
            wn.onkey(restart_game, "r")
            return

    enemy_speed += 0.002

    wn.update()
    wn.ontimer(game_loop, 16)

# Start game
game_loop()
wn.mainloop()