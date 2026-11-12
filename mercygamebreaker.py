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
class Brick(GameObject):
    COLORS_FIRE = {1: '#ff5252', 2: '#ff793f', 3: '#b33939'}
    COLORS_WATER = {1: '#00d2d3', 2: '#0abde3', 3: '#2e86de'}

    def __init__(self, canvas, x, y, hits, game_instance, mode='fire'):
        self.width = 75
        self.height = 24
        self.hits = hits
        self.x = x
        self.y = y
        self.game_instance = game_instance
        self.mode = mode
        
        colors = self.COLORS_WATER if mode == 'water' else self.COLORS_FIRE
        outline_color = '#48dbfb' if mode == 'water' else '#ffb142'
        
        color = colors[hits]
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, outline=outline_color, width=2, tags='brick')
        super(Brick, self).__init__(canvas, item)

        self.decors = []
        if mode == 'fire':
            offsets = [-24, -8, 8, 24]
            for dx in offsets:
                f1 = canvas.create_polygon(x + dx - 5, y + 10, x + dx, y - 7, x + dx + 5, y + 10, fill='#ffda79', outline='')
                f2 = canvas.create_polygon(x + dx - 3, y + 10, x + dx, y - 1, x + dx + 3, y + 10, fill='#ff5252', outline='')
                self.decors.extend([f1, f2])
        else:
            offsets = [-20, 0, 20]
            for dx in offsets:
                w1 = canvas.create_oval(x + dx - 8, y - 6, x + dx + 8, y + 6, fill='#c8d6e5', outline='')
                w2 = canvas.create_oval(x + dx - 4, y - 3, x + dx + 4, y + 3, fill='#ffffff', outline='')
                self.decors.extend([w1, w2])

    def animate(self):
        for d in self.decors:
            dy = random.choice([-1, 0, 1])
            self.canvas.move(d, 0, dy)
class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        self.lives = 3
        self.score = 0
        self.width = 610
        self.height = 420
        self.canvas = tk.Canvas(self, bg='#111111',
                                width=self.width,
                                height=self.height)
        self.canvas.pack()
        self.pack()

        self.draw_race_track_background()

        self.items = {}
        self.bricks = []
        self.ball = None
        self.game_mode = 'fire'
        
        self.paddle = Paddle(self.canvas, self.width / 2, 355)
        self.items[self.paddle.item] = self.paddle

        self.create_bricks()

        self.hud_score = None
        self.hud_lives = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-22))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(22))

    def add_score(self, points):
        self.score += points
        self.update_hud()

    def draw_race_track_background(self):
        for y_pos in range(20, self.height, 40):
            self.canvas.create_line(self.width / 2, y_pos, self.width / 2, y_pos + 20, fill='#333333', width=6)
        
        for y_pos in range(0, self.height, 20):
            color_left = '#ff3838' if (y_pos // 20) % 2 == 0 else '#f5f6fa'
            color_right = '#f5f6fa' if (y_pos // 20) % 2 == 0 else '#ff3838'
            self.canvas.create_rectangle(0, y_pos, 10, y_pos + 20, fill=color_left, outline='')
            self.canvas.create_rectangle(self.width - 10, y_pos, self.width, y_pos + 20, fill=color_right, outline='')

    def update_hud(self):
        score_text = f'SCORE: {self.score}'
        lives_text = f'LIVES: {self.lives}'
        
        if self.hud_score is None:
            self.hud_score = self.draw_text(85, 22, score_text, 15, '#2ed573')
        else:
            self.canvas.itemconfig(self.hud_score, text=score_text)

        if self.hud_lives is None:
            self.hud_lives = self.draw_text(525, 22, lives_text, 15, '#ff5252')
        else:
            self.canvas.itemconfig(self.hud_lives, text=lives_text)

   def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)

def create_bricks(self):
        for b in self.bricks:
            b.delete()
        self.bricks.clear()
        
        for x in range(25, self.width - 25, 75):
            self.add_brick(x + 37.5, 55, 3, self.game_mode)
            self.add_brick(x + 37.5, 83, 2, self.game_mode)
            self.add_brick(x + 37.5, 111, 1, self.game_mode)

    def add_brick(self, x, y, hits, mode):
        brick = Brick(self.canvas, x, y, hits, self, mode)
        self.items[brick.item] = brick
        self.bricks.append(brick)

    def setup_game(self):
        self.add_ball()
        self.update_hud()
        if self.game_mode == 'fire':
            start_text = 'PRESS SPACE TO RACE (FIRE TRACK)'
            text_color = '#ffda79'
        else:
            start_text = 'PRESS SPACE TO RACE (WATER TRACK)'
            text_color = '#48dbfb'
            
        self.text = self.draw_text(305, 220, start_text, size='20', color=text_color)
        self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        if self.ball is not None:
            self.ball.clear_trail()
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 330)
        self.paddle.set_ball(self.ball)

    def draw_text(self, x, y, text, size='36', color='white'):
        font = ('Impact', size)
        return self.canvas.create_text(x, y, text=text, font=font, fill=color)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        try:
            winsound.Beep(1000, 150)
        except:
            pass
        self.game_loop()

    def game_loop(self):
        self.check_collisions()

        for brick in self.bricks:
            if brick.hits > 0:
                brick.animate()

        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.clear_trail()
            self.ball.speed = None
            self.draw_text(305, 210, 'VICTORY! RACE CHAMPION!', size='28', color='#ffda79')
            try:
                winsound.Beep(1500, 300)
            except:
                pass
        elif self.ball.get_position()[3] >= self.height:
            self.ball.clear_trail()
            self.ball.speed = None
            self.lives -= 1
            self.update_hud()
            try:
                winsound.Beep(300, 400)
            except:
                pass

            if self.lives < 0:
                if self.game_mode == 'fire':
                    self.game_mode = 'water'
                    notif_text = 'PIT STOP! SWITCH TO WATER TRACK!'
                    notif_color = '#00d2d3'
                else:
                    self.game_mode = 'fire'
                    notif_text = 'PIT STOP! SWITCH BACK TO FIRE TRACK!'
                    notif_color = '#ff5252'

                self.lives = 3
                self.create_bricks()
                self.draw_text(305, 210, notif_text, size='18', color=notif_color)
                self.after(1500, lambda: [self.canvas.delete('all'), self.restart_full()])
            else:
                self.after(1000, self.setup_game)
        else:
            self.ball.update()
            self.after(40, self.game_loop)

    def restart_full(self):
        self.canvas.delete('all')
        self.draw_race_track_background()
        self.items = {}
        self.bricks = []
        self.hud_score = None
        self.hud_lives = None
        self.paddle = Paddle(self.canvas, self.width / 2, 355)
        self.items[self.paddle.item] = self.paddle
        self.create_bricks()
        self.setup_game()

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Mercy Race Track BrickBreaker')
    game = Game(root)
    game.mainloop()