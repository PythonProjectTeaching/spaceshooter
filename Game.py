import turtle
import math
import random

# Thiết lập cửa sổ trò chơi
wn = turtle.Screen()
wn.bgcolor("grey")
wn.title("Space Shooter")

# Đăng ký ảnh asset
turtle.register_shape('ship_p.gif')
turtle.register_shape('ship_e.gif')

# Vẽ người chơi
player = turtle.Turtle(shape='ship_p.gif')
player.color("blue")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player.shapesize(30)

playerspeed = 15

# Di chuyển người chơi sang trái
def move_left():
    x = player.xcor() - playerspeed
    x = max(x, -280)
    player.setx(x)

# Di chuyển người chơi sang phải
def move_right():
    x = player.xcor() + playerspeed
    x = min(x, 280)
    player.setx(x)

# Điểm số
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-280, 260)
score_string = "Score: {}".format(str(score))
score_pen.write(score_string, False, align="left", font=("sans-serif", 14, "normal"))
score_pen.hideturtle()



# Bắn đạn
def fire_bullet():
    global bulletstate
    bulletstate = "fire"
    x = player.xcor()
    y = player.ycor() + 15
    for bullet in bullet_pool:
        if not bullet.isvisible():
            bullet.setposition(x, y)
            bullet.showturtle()
            break

# Tạo ra đạn
bullet_pool = []
bullet_count = 5
bulletspeed = 30
for _ in range(bullet_count):
    bullet = turtle.Turtle()
    bullet.color("yellow")
    bullet.shape("triangle")
    bullet.penup()
    bullet.speed(0)
    bullet.setheading(90)
    bullet.shapesize(0.5, 0.5)
    bullet.hideturtle()
    bullet_pool.append(bullet)

bulletstate = "ready"

# Tạo ra nhiều kẻ thù
enemies = []
number_of_enemies = 3

for _ in range(number_of_enemies):
    enemy = turtle.Turtle(shape = "ship_e.gif")
    enemy.setheading(180)
    enemy.color("red")
    enemy.penup()
    enemy.speed(0)
    enemy.setposition(random.randint(-200, 200), random.randint(100, 250))
    enemies.append(enemy)

enemyspeed = 2

# Lấy đạn từ object pool
def get_bullet_from_pool():
    for bullet in bullet_pool:
        if not bullet.isvisible():
            return bullet
    return None

# Kiểm tra xem hai đối tượng có va chạm không
def is_collision(t1, t2):
    distance_squared = (t1.xcor() - t2.xcor())**2 + (t1.ycor() - t2.ycor())**2
    return distance_squared < 225  # Sử dụng bình phương 15 (bán kính) để so sánh

# Liên kết phím
wn.listen()
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")

# Vòng lặp trò chơi
while True:
    # Di chuyển kẻ thù
    for enemy in enemies:
        x = enemy.xcor() + enemyspeed
        enemy.setx(x)

        # Kiểm tra xem kẻ thù đã chạm tường hay chưa
        if abs(enemy.xcor()) > 280:
            y = enemy.ycor() - 40
            enemy.sety(y)
            enemyspeed *= -1

        # Kiểm tra xem kẻ thù đã va chạm với người chơi hay chưa
        if is_collision(player, enemy):
            player.hideturtle()
            for e in enemies:
                e.hideturtle()
            print("Game Over")
            break

        # Kiểm tra xem đạn đã va chạm với kẻ thù hay chưa
        for bullet in bullet_pool:
            if bullet.isvisible() and is_collision(bullet, enemy):
                bullet.hideturtle()
                bulletstate = "ready"
                bullet.setposition(0, -400)
                enemy.setposition(random.randint(-200, 200), random.randint(100, 250))
                score += 999
                score_string = "Score: %s" % score
                score_pen.clear()
                score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

    # Di chuyển đạn
    for bullet in bullet_pool:
        if bullet.isvisible():
            y = bullet.ycor() + bulletspeed
            bullet.sety(y)

            # Kiểm tra xem đạn đã ra khỏi màn hình hay chưa
            if bullet.ycor() > 275:
                bullet.hideturtle()
    # Kiểm tra nút space để bắn đạn mới
    if bulletstate == "ready":
        wn.onkeypress(fire_bullet, "space")
    else:
        wn.onkeyrelease(lambda: None, "space")
    
    wn.update()

wn.mainloop()
