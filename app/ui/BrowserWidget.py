from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import webbrowser

class BrowserWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        url_layout = BoxLayout(size_hint_y=None, height=40)
        self.url_input = TextInput(multiline=False, hint_text='Introducir URL')
        go_button = Button(text='Ir', size_hint_x=0.2)
        go_button.bind(on_press=self.load_url)
        url_layout.add_widget(self.url_input)
        url_layout.add_widget(go_button)
        
        self.info_label = Label(text='Haga clic en "Ir" para abrir en el navegador predeterminado')
        
        # Agregar widgets al layout
        self.add_widget(url_layout)
        self.add_widget(self.info_label)
    
    def load_url(self, instance=None):
        url = self.url_input.text
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            webbrowser.open(url)
            self.info_label.text = f'Abriendo: {url}'
        except Exception as e:
            self.info_label.text = f'Error al abrir URL: {str(e)}'