from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from random import randint


class SnakeGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.food = (15, 15)
        self.score = 0
        self.over = False

        self.board = Widget(
            size_hint=(1, 0.68),
            pos_hint={"x": 0, "top": 0.9}
        )
        self.add_widget(self.board)

        self.label = Label(
            text="SCORE: 0",
            font_size="24sp",
            size_hint=(1, 0.1),
            pos_hint={"top": 1}
        )
        self.add_widget(self.label)

        self.make_button("UP", 0.38, 0.19, self.up)
        self.make_button("DOWN", 0.38, 0.02, self.down)
        self.make_button("LEFT", 0.03, 0.02, self.left)
        self.make_button("RIGHT", 0.73, 0.02, self.right)

        Clock.schedule_interval(self.update, 0.15)
        self.draw()

    def make_button(self, text, x, y, func):
        b = Button(
            text=text,
            size_hint=(0.24, 0.13),
            pos_hint={"x": x, "y": y},
            font_size="18sp"
        )
        b.bind(on_press=func)
        self.add_widget(b)

    def up(self, *a):
        if self.direction != (0, -1):
            self.direction = (0, 1)

    def down(self, *a):
        if self.direction != (0, 1):
            self.direction = (0, -1)

    def left(self, *a):
        if self.direction != (1, 0):
            self.direction = (-1, 0)

    def right(self, *a):
        if self.direction != (-1, 0):
            self.direction = (1, 0)

    def update(self, dt):
        if self.over:
            return

        x, y = self.snake[0]
        dx, dy = self.direction
        head = (x + dx, y + dy)

        if (
            head[0] < 0 or head[0] >= 20
            or head[1] < 0 or head[1] >= 20
            or head in self.snake[:-1]
        ):
            self.over = True
            self.label.text = "GAME OVER! SCORE: " + str(self.score)
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.score += 1
            self.label.text = "SCORE: " + str(self.score)
            self.food = (randint(0, 19), randint(0, 19))
        else:
            self.snake.pop()

        self.draw()

    def draw(self):
        self.board.canvas.clear()

        w = self.board.width / 20
        h = self.board.height / 20

        with self.board.canvas:
            Color(0.08, 0.08, 0.08)
            Rectangle(pos=self.board.pos, size=self.board.size)

            Color(0.1, 0.9, 0.2)
            for x, y in self.snake:
                Rectangle(
                    pos=(self.board.x + x*w, self.board.y + y*h),
                    size=(w-2, h-2)
                )

            Color(1, 0.1, 0.1)
            Rectangle(
                pos=(
                    self.board.x + self.food[0]*w,
                    self.board.y + self.food[1]*h
                ),
                size=(w-2, h-2)
            )


class SnakeApp(App):
    def build(self):
        return SnakeGame()


SnakeApp().run()
