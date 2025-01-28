from asyncio import Queue
import os
import threading  
import pygame  
from threading import Thread  
import webbrowser  
from kivy.app import App  
from kivy.uix.boxlayout import BoxLayout  
from kivy.uix.gridlayout import GridLayout  
from kivy.uix.button import Button  
from kivy.uix.label import Label  
from kivy.uix.textinput import TextInput  
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem  
from kivy.clock import Clock  
from kivy.uix.filechooser import FileChooserIconView  
from application.ApplicationThread import ApplicationThread  
from utils.Enlaces import Enlaces
from music.MusicThread import MusicThread  
from game.CircleGame import CircleGame
import datetime  

from weather.WeatherThread import WeatherThread
from system_monitor.stats_collector import StatsCollector
from system_monitor.system_monitor import SystemMonitor    
from ui.BrowserWidget import BrowserWidget

class MainWindow(BoxLayout):  
    pygame.init()  
    pygame.mixer.init() 
     

    def __init__(self, **kwargs):  
        super().__init__(**kwargs)  
        self.orientation = 'vertical' 
        self.current_song = "app\\resource\\Two Steps From Hell - Victory (1).mp3"

        pygame.mixer.init()
 
        self.circle_game = CircleGame(self.update_game_status)

        self.main_layout = BoxLayout(orientation='horizontal')  
        self.create_left_panel()  
        self.create_center_panel()  
        self.create_right_panel()  
        self.add_widget(self.main_layout)  
        self.create_bottom_bar()  

        Clock.schedule_interval(self.update_time, 1)  


        self.start_weather_thread()  


        

    def create_left_panel(self):  
        left_panel = GridLayout(cols=1, size_hint_x=0.2, spacing=5, padding=5)  

        self.app_thread_manager = ApplicationThread()  
        self.enlaces = Enlaces()  

        app_buttons = {  
            "Visual Code": self.launch_vscode,  
            "Edge": self.launch_edge,  
            "Explorador de Archivos": self.launch_explorer,  
            "Notepad": self.launch_notepad  
        }  
        left_panel.add_widget(Label(text="Aplicaciones", size_hint_y=None, height=30))  
        for name, action in app_buttons.items():  
            btn = Button(text=name)  
            btn.bind(on_press=action)  
            left_panel.add_widget(btn)  

        url_buttons = {  
            "Google": self.open_google,  
            "Github": self.open_github,  
            "StackOverflow": self.open_stackoverflow  
        }  
        left_panel.add_widget(Label(text="Enlaces", size_hint_y=None, height=30))  
        for name, action in url_buttons.items():  
            btn = Button(text=name)  
            btn.bind(on_press=action)  
            left_panel.add_widget(btn)  
        self.main_layout.add_widget(left_panel)  

    def create_center_panel(self):    
        center_panel = TabbedPanel(do_default_tab=False)    

        center_panel.tab_width = 200  # Ancho de cada pestaña  
        center_panel.tab_height = 60  # Altura de cada pestaña  

        self.tab_nav = TabbedPanelItem(text="Navegador", size_hint=(1, 1))    
        nav_content = BrowserWidget()   
        self.tab_nav.add_widget(nav_content)

        self.tab_scraping = TabbedPanelItem(text="Scrapping", size_hint=(1, 1))    

        tab_resources = TabbedPanelItem(text="Monitor de Recursos", size_hint=(1, 1))    
        resource_layout = SystemMonitor()   
        tab_resources.add_widget(resource_layout)    

        self.circle_game_tab = TabbedPanelItem(text="Juego del Círculo", size_hint=(1, 1))    
        circle_game_layout = BoxLayout(orientation='vertical')    
        self.game_status_label = Label(text="Estado del juego")    
        circle_game_layout.add_widget(self.game_status_label)    
        circle_game_layout.add_widget(self.circle_game)    

        game_controls = BoxLayout(size_hint_y=None, height=50)    
        start_game_button = Button(text="Iniciar Juego", on_press=self.start_game)    
        stop_game_button = Button(text="Detener Juego", on_press=self.stop_game)    
        game_controls.add_widget(start_game_button)    
        game_controls.add_widget(stop_game_button)    
        circle_game_layout.add_widget(game_controls)  

        self.circle_game_tab.add_widget(circle_game_layout)   

        for tab in [self.tab_nav, tab_resources, self.circle_game_tab, self.tab_scraping]:    
            center_panel.add_widget(tab)    

        self.main_layout.add_widget(center_panel)      

    def create_right_panel(self):  
        right_panel = GridLayout(cols=1, size_hint_x=0.3, spacing=5, padding=5)  

        right_panel.add_widget(Label(text="[b]Chat[/b]", markup=True, size_hint_y=None, height=30))  
        right_panel.add_widget(TextInput(hint_text="Mensaje", size_hint_y=0.2))  
        right_panel.add_widget(Button(text="Enviar", size_hint_y=None, height=40))  

        self.music_status_label = Label(text="Reproductor de música", size_hint_y=None, height=30)  
        right_panel.add_widget(self.music_status_label)  

        music_controls = BoxLayout(size_hint_y=None, height=40)  
        play_button = Button(text="Play", on_press=self.play_music)  
        pause_button = Button(text="Pause", on_press=self.pause_music)  
        stop_button = Button(text="Stop", on_press=self.stop_music)  
        for btn in [play_button, pause_button, stop_button]:  
            music_controls.add_widget(btn)  
        right_panel.add_widget(music_controls)  

        self.file_chooser = FileChooserIconView(filters=['*.mp3'], size_hint_y=0.3, path="C:\\Users\\borja\\Music")  
        self.file_chooser.bind(on_selection=self.select_song)  
        right_panel.add_widget(self.file_chooser)  

        self.music_thread = MusicThread(self.update_music_status)  
        self.music_thread.start() 

        self.main_layout.add_widget(right_panel)  

    def create_bottom_bar(self):  
        bottom_bar = GridLayout(cols=3, size_hint_y=0.1)  
        self.unread_emails_label = Label(text="Correos sin leer")  
        self.temperature_label = Label(text="Temperatura local")  
        self.time_label = Label(text="Fecha y Hora")  
        for widget in [self.unread_emails_label, self.temperature_label, self.time_label]:  
            bottom_bar.add_widget(widget)  
        self.add_widget(bottom_bar)    
        
    def update_time(self, dt):  
        now = datetime.datetime.now()  
        day_of_week = now.strftime("%A")  
        time_str = now.strftime("%H:%M:%S")  
        date_str = now.strftime("%d/%m/%Y")  
        self.time_label.text = f"{day_of_week}, {date_str} - {time_str}" 
        
    def start_weather_thread(self):  
            self.weather_thread = WeatherThread(self.update_temp_label)  
            self.weather_thread.start()  

    def update_temp_label(self, temp):  
        # Actualizar la etiqueta de temperatura  
        self.temperature_label.text = temp  

    def start_search(self, instance):  
        query = self.url_input.text  
        if query:  
            webbrowser.open(f"https://www.google.com/search?q={query}")  


    def update_results(self, text):  
        self.search_result_label.text = text  

    def select_song(self, file_chooser , selection):  
         if selection:  
           self.current_song = selection[0]  
           self.music_status_label.text = f"Seleccionado: {os.path.basename(self.current_song)}"  
         else:  
           self.music_status_label.text = "No se seleccionó ninguna canción"  

    def play_music(self, instance):  
         if self.current_song:  
           self.music_thread.play_song(self.current_song)
           self.music_status_label.text = f"Reproduciendo: {os.path.basename(self.current_song)}"  
         else:  
           self.music_status_label.text = "Seleccione una canción válida primero"  

    def pause_music(self, instance):  
         self.music_thread.pause_song()
         self.music_status_label.text = "Pausado"  

    def stop_music(self, instance):  
         self.music_thread.stop_song  
         self.music_status_label.text = "Detenido"    

    def launch_vscode(self, instance):  
        self.app_thread_manager.launch_application('vscode')  

    def launch_edge(self, instance):  
        self.app_thread_manager.launch_application('edge')  

    def launch_explorer(self, instance):  
        self.app_thread_manager.launch_application('explorer')  

    def launch_notepad(self, instance):  
        self.app_thread_manager.launch_application('notepad')  

    def open_google(self, instance):  
        self.enlaces.abrir_google()  

    def open_github(self, instance):  
        self.enlaces.abrir_github()  

    def open_stackoverflow(self, instance):  
        self.enlaces.abrir_stackoverflow()  

    def show_resource_monitor(self, instance):  
        if not hasattr(self, 'stats_queue'):  
            self.stats_queue = Queue()  

        if not hasattr(self, 'stats_collector_thread'):  
            self.stats_collector = StatsCollector(self.stats_queue)  
            self.stats_collector_thread = threading.Thread(  
                target=self.stats_collector.start_collecting,  
                args=(True,)  
            )  
            self.stats_collector_thread.daemon = True  
            self.stats_collector_thread.start()  

            Clock.schedule_interval(self.update_resource_status, 1)  
        else:  
            self.stats_collector.stop()  
            self.stats_collector_thread.join(timeout=1)
              
            del self.stats_collector_thread  
            del self.stats_collector  

    def start_game(self, instance):  
            """Inicia el juego de clic en el círculo."""  
            self.circle_game.start_game()  

    def stop_game(self, instance):  
            """Detiene el juego de clic en el círculo."""  
            self.circle_game.stop_game()  

    def update_game_status(self, status):  
            """Actualiza el estado del juego en la interfaz."""  
            self.game_status_label.text = status  

    def update_music_status(self, data):  
        self.music_status_label.text = data 