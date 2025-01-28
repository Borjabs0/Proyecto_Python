import socket
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

# Configuración del servidor
HOST = '192.168.120.106'  # Escucha en la dirección especificada
PORT = 3333  # Puerto de escucha
clients = []  # Lista para almacenar los clientes conectados
server = None  # Variable global para el socket del servidor
server_thread = None  # Hilo para ejecutar el servidor

class ServerApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Área para mostrar mensajes del servidor
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.log = Label(size_hint_y=None, text_size=(self.width, None), halign='left', valign='top')
        self.log.bind(texture_size=self.log.setter('size'))
        self.scroll_view.add_widget(self.log)
        self.add_widget(self.scroll_view)

        # Botones de control del servidor
        self.control_layout = BoxLayout(size_hint=(1, 0.2), height=50)
        self.start_button = Button(text="Iniciar Servidor")
        self.stop_button = Button(text="Detener Servidor", disabled=True)
        self.control_layout.add_widget(self.start_button)
        self.control_layout.add_widget(self.stop_button)
        self.add_widget(self.control_layout)

        # Conexión de botones con funciones
        self.start_button.bind(on_press=self.start_server)
        self.stop_button.bind(on_press=self.stop_server)

    def log_message(self, message):
        self.log.text += f"{message}\n"
        self.scroll_view.scroll_y = 0

    def broadcast(self, message, client_socket):
        for client in clients:
            if client != client_socket:  # Evitar enviar el mensaje al remitente
                try:
                    client.send(message)
                except:
                    clients.remove(client)

    def handle_client(self, client_socket, client_address):
        self.log_message(f"[NUEVO CLIENTE] {client_address} conectado.")
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                self.log_message(f"[{client_address}] {message.decode('utf-8')}")
                self.broadcast(message, client_socket)
            except:
                self.log_message(f"[DESCONECTADO] {client_address} se ha desconectado.")
                clients.remove(client_socket)
                client_socket.close()
                break

    def start_server_thread(self):
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
        self.log_message(f"[INICIO] Servidor escuchando en {HOST}:{PORT}")

        while True:
            try:
                client_socket, client_address = server.accept()
                clients.append(client_socket)
                self.log_message(f"[CONECTADO] Nueva conexión desde {client_address}")

                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.start()
            except OSError:
                break

    def start_server(self, instance):
        global server_thread
        server_thread = threading.Thread(target=self.start_server_thread, daemon=True)
        server_thread.start()

        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.log_message("[INFO] Servidor iniciado.")

    def stop_server(self, instance):
        global server
        if server:
            server.close()
            server = None

        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.log_message("[INFO] Servidor detenido.")

class ServerAppApp(App):
    def build(self):
        return ServerApp()

if __name__ == "__main__":
    ServerAppApp().run()
