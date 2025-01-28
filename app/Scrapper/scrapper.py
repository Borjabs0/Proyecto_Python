import threading
import requests
from bs4 import BeautifulSoup
import mysql.connector
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Configuración de la base de datos MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'scrapper_db'
}

# Función para configurar la conexión a la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para guardar datos en la base de datos
def guardar_datos(titulo, contenido):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = """
                INSERT INTO monitoreo_web (titulo, contenido, fecha) 
                VALUES (%s, %s, NOW())
            """
            cursor.execute(query, (titulo, contenido))
            conexion.commit()
            print("Datos guardados correctamente en la base de datos.")
        except mysql.connector.Error as e:
            print(f"Error al guardar datos: {e}")
        finally:
            cursor.close()
            conexion.close()

# Función para extraer y procesar información de la página web
def extraer_datos(url):
    try:
        print(f"Extrayendo datos de la página web {url}...")
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            sopa = BeautifulSoup(respuesta.text, 'html.parser')
            # Modifica estas líneas según la estructura de la página
            titulo = sopa.title.string if sopa.title else 'Sin título'
            contenido = sopa.get_text()[:500]  # Extrae un fragmento del contenido
            print(f"Título: {titulo}")
            guardar_datos(titulo, contenido)
        else:
            print(f"Error al acceder a la página: {respuesta.status_code}")
    except Exception as e:
        print(f"Error al extraer datos: {e}")

# Clase para ejecutar el monitoreo en un hilo separado
class ScraperThread(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.daemon = True  # Permitir que el hilo se cierre cuando termine el programa
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            extraer_datos(self.url)
            time.sleep(60)

    def detener(self):
        self.running = False

# Interfaz gráfica con Kivy
class ScraperApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.label = Label(text="Estado: Detenido")
        self.add_widget(self.label)

        self.url_input = TextInput(hint_text="Introduce la URL a monitorear")
        self.add_widget(self.url_input)

        self.iniciar_btn = Button(text="Iniciar Scraper")
        self.iniciar_btn.bind(on_press=self.iniciar_scraper)
        self.add_widget(self.iniciar_btn)

        self.detener_btn = Button(text="Detener Scraper")
        self.detener_btn.bind(on_press=self.detener_scraper)
        self.detener_btn.disabled = True
        self.add_widget(self.detener_btn)

        self.hilo_scraper = None

    def iniciar_scraper(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.label.text = "Por favor, introduce una URL válida."
            return

        if not self.hilo_scraper or not self.hilo_scraper.is_alive():
            self.hilo_scraper = ScraperThread(url)
            self.hilo_scraper.start()
            self.label.text = f"Estado: Monitoreando {url}"
            self.iniciar_btn.disabled = True
            self.detener_btn.disabled = False

    def detener_scraper(self, instance):
        if self.hilo_scraper and self.hilo_scraper.is_alive():
            self.hilo_scraper.detener()
            self.hilo_scraper.join()
            self.label.text = "Estado: Detenido"
            self.iniciar_btn.disabled = False
            self.detener_btn.disabled = True

class ScraperAppLauncher(App):
    def build(self):
        return ScraperApp()

if __name__ == '__main__':
    ScraperAppLauncher().run()