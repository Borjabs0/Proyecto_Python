import os  
import pygame  
import threading  
from kivy.uix.boxlayout import BoxLayout  
from kivy.uix.button import Button  
from kivy.uix.label import Label  
from kivy.uix.filechooser import FileChooserIconView  

class MusicThread(threading.Thread):  
    def __init__(self, callback):  
        super().__init__()  
        self.callback = callback  
        self.playing = False  
        self.current_song = None  
        pygame.mixer.init()  

    def run(self):  
        while True:  
            if self.playing and self.current_song:  
                if not pygame.mixer.music.get_busy():  
                    self.callback("Reproducción finalizada")  
                    self.playing = False  

    def play_song(self, song_path):  
        if not song_path:  
            self.callback("Error: No se seleccionó ninguna canción.")  
            return  

        try:  
            self.current_song = song_path  
            pygame.mixer.music.load(song_path)  
            pygame.mixer.music.play()  
            self.playing = True  
            self.callback(f"Reproduciendo: {os.path.basename(song_path)}")  
        except Exception as e:  
            self.callback(f"Error al reproducir: {str(e)}")  

    def pause_song(self):  
        if self.playing:  
            pygame.mixer.music.pause()  
            self.playing = False  
            self.callback("Pausado")  
        else:  
            self.callback("Error: No se está reproduciendo ninguna canción.")  

    def stop_song(self):  
        pygame.mixer.music.stop()  
        self.playing = False  
        self.callback("Detenido")  

    def is_playing(self):  
        return self.playing  