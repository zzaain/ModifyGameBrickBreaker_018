import tkinter as tk
import random
import winsound


class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, -1]
        self.speed = 11
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='#fff200', outline='#ff3838', width=3)
        super(Ball, self).__init__(canvas, item)
        self.trail = []

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
            try:
                winsound.Beep(800, 50)
            except:
                pass
        if coords[1] <= 0:
            self.direction[1] *= -1
            try:
                winsound.Beep(800, 50)
            except:
                pass
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed

        cx = (coords[0] + coords[2]) * 0.5
        cy = (coords[1] + coords[3]) * 0.5
        fire_colors = ['#ff3838', '#ff9f1a', '#fffa65', '#ff4d4d']
        r = random.randint(4, 9)
        flame = self.canvas.create_oval(
            cx - r + random.randint(-3, 3),
            cy - r + random.randint(-3, 3),
            cx + r + random.randint(-3, 3),
            cy + r + random.randint(-3, 3),
            fill=random.choice(fire_colors), outline=''
        )
        self.canvas.tag_lower(flame, self.item)
        self.trail.append(flame)

        if len(self.trail) > 10:
            old_flame = self.trail.pop(0)
            self.canvas.delete(old_flame)

        self.move(x, y)

    def clear_trail(self):
        for t in self.trail:
            self.canvas.delete(t)
        self.trail.clear()

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[1] *= -1
            try:
                winsound.Beep(600, 60)
            except:
                pass
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1
            try:
                winsound.Beep(600, 60)
            except:
                pass

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()
class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 110
        self.height = 18
        self.ball = None

        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='', outline='')
        super(Paddle, self).__init__(canvas, item)

        self.car_parts = []
        body = canvas.create_rectangle(x - 55, y - 4, x + 55, y + 8,
                                       fill='#dcdde1', outline='#7f8fa6', width=1)
        cabin = canvas.create_polygon(x - 32, y - 4, x - 18, y - 15,
                                      x + 22, y - 15, x + 36, y - 4,
                                      fill='#2f3640', outline='#dcdde1', width=2)
        headlight = canvas.create_rectangle(x + 48, y - 2, x + 55, y + 3, fill='#00a8ff', outline='')
        taillight = canvas.create_rectangle(x - 55, y - 2, x - 48, y + 3, fill='#e84118', outline='')
        wheel_l = canvas.create_oval(x - 42, y + 2, x - 24, y + 16, fill='#1e272e', outline='#7f8fa6', width=2)
        rim_l = canvas.create_oval(x - 36, y + 6, x - 30, y + 12, fill='#f5f6fa', outline='')
        wheel_r = canvas.create_oval(x + 24, y + 2, x + 42, y + 16, fill='#1e272e', outline='#7f8fa6', width=2)
        rim_r = canvas.create_oval(x + 30, y + 6, x + 36, y + 12, fill='#f5f6fa', outline='')
        
        logo_circle = canvas.create_oval(x - 6, y - 3, x + 6, y + 7, outline='#2f3640', fill='#f5f6fa', width=1)
        star1 = canvas.create_line(x, y - 3, x, y + 2, fill='#2f3640', width=1)
        star2 = canvas.create_line(x, y + 2, x - 4, y + 5, fill='#2f3640', width=1)
        star3 = canvas.create_line(x, y + 2, x + 4, y + 5, fill='#2f3640', width=1)

        self.car_parts = [body, cabin, headlight, taillight, wheel_l, rim_l, wheel_r, rim_r, logo_circle, star1, star2, star3]

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            for part in self.car_parts:
                self.canvas.move(part, offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)