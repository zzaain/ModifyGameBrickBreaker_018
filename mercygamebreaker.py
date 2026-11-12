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