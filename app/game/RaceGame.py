import random
import threading
import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Ellipse
from kivy.clock import Clock

# Clase que representa una bola en la carrera
class Ball(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 50)
        self.x = 0
        self.y = random.randint(0, 500)
        with self.canvas:
            self.ellipse = Ellipse(pos=(self.x, self.y), size=self.size)

    def move(self, distance):
        self.x += distance
        self.ellipse.pos = (self.x, self.y)

# Clase principal de la aplicación
class RaceGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.running = False

        # Layout para los botones
        button_layout = BoxLayout(size_hint=(1, 0.1))
        self.start_button = Button(text='Start Race', on_press=self.start_race)
        self.reset_button = Button(text='Reset', on_press=self.reset_race, disabled=True)
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.reset_button)

        # Etiqueta de resultado
        self.result_label = Label(text='Welcome to the Ball Race!', size_hint=(1, 0.1))

        # Layout para la carrera
        self.race_layout = Widget()

        self.add_widget(button_layout)
        self.add_widget(self.result_label)
        self.add_widget(self.race_layout)

        self.balls = []
        self.threads = []

        self.create_balls()

    def create_balls(self):
        self.race_layout.canvas.clear()
        self.balls = []
        for i in range(3):  # Crear 3 bolas
            ball = Ball()
            self.balls.append(ball)
            self.race_layout.add_widget(ball)

    def start_race(self, instance):
        self.running = True
        self.start_button.disabled = True
        self.reset_button.disabled = True
        self.result_label.text = 'The race is on!'

        self.threads = []
        for ball in self.balls:
            thread = threading.Thread(target=self.move_ball, args=(ball,))
            self.threads.append(thread)
            thread.start()

        threading.Thread(target=self.check_winner).start()

    def move_ball(self, ball):
        while ball.x < self.race_layout.width - ball.width and self.running:
            distance = random.randint(5, 15)
            Clock.schedule_once(lambda dt: ball.move(distance), 0)
            time.sleep(0.1)

    def check_winner(self):
        while self.running:
            time.sleep(0.1)
            for ball in self.balls:
                if ball.x >= self.race_layout.width - ball.width:
                    self.running = False
                    winner = self.balls.index(ball) + 1
                    self.result_label.text = f'Ball {winner} wins the race!'
                    Clock.schedule_once(lambda dt: self.enable_reset(), 0)

    def enable_reset(self):
        self.reset_button.disabled = False

    def reset_race(self, instance):
        self.create_balls()
        self.result_label.text = 'Welcome to the Ball Race!'
        self.start_button.disabled = False
        self.reset_button.disabled = True

class BallRaceApp(App):
    def build(self):
        return RaceGame()

if __name__ == '__main__':
    BallRaceApp().run()