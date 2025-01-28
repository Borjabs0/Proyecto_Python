import threading
import requests
class WeatherThread(threading.Thread):  
    def __init__(self, callback):  
        super().__init__()  
        self.callback = callback  

    def run(self):  
        try:  
            # Usando OpenWeatherMap API  
            API_KEY = "850530a0bb411e634ebd69b94c322a14" 
            url = f"http://api.openweathermap.org/data/2.5/weather?q=Teulada&appid=850530a0bb411e634ebd69b94c322a14&units=metric"  
            response = requests.get(url)  

            if response.status_code != 200:
                raise ValueError(f"Error en la API: {response.status_code} - {response.text}")


            data = response.json()  
            temp = data['main']['temp']
            city = data['name']
            self.callback(f"Temperatura actual en {city}: {temp}°C")  
        except Exception as e:  
            self.callback(f"Error: {str(e)}")  