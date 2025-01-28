import random  
from kivy.uix.widget import Widget  
from kivy.graphics import Color, Ellipse  
from kivy.clock import Clock  

class CircleGame(Widget):  
    def __init__(self, update_status_callback, **kwargs):  
        super().__init__(**kwargs)  
        self.update_status_callback = update_status_callback  
        self.circle = None  
        self.running = False  
        self.score = 0  

    def start_game(self):  
        self.running = True  
        self.score = 0  
        self.update_status_callback("Juego iniciado: ¡Haz clic en el círculo!")  
        self.move_circle()  

    def stop_game(self):  
        self.running = False  
        self.update_status_callback(f"Juego detenido. Puntuación final: {self.score}")  

    def move_circle(self):  
        if not self.running:  
            return  

        # Eliminar el círculo anterior  
        self.canvas.clear()  

        # Dibujar un nuevo círculo en una posición aleatoria dentro del BoxLayout  
        with self.canvas:  
            Color(1, 0, 0, 1)  # Rojo  
            x = random.randint(0, int(self.width) - 50)  
            y = random.randint(0, int(self.height) - 50)  
            self.circle = Ellipse(pos=(x, y), size=(50, 50))  

        # Programar el siguiente movimiento  
        Clock.schedule_once(lambda dt: self.move_circle(), 1)  

    def on_touch_down(self, touch):  
        if self.circle:  
            # Obtener las coordenadas y el tamaño del círculo  
            x, y = self.circle.pos  
            width, height = self.circle.size  

            # Verificar si el toque está dentro del círculo  
            if x <= touch.x <= x + width and y <= touch.y <= y + height:  
                self.score += 1  
                self.update_status_callback(f"¡Clic! Puntuación: {self.score}")  
                self.move_circle()  # Mover el círculo inmediatamente después de un clic  