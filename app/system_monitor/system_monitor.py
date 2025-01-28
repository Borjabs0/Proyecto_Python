from kivy.uix.boxlayout import BoxLayout  
from kivy.clock import Clock  
from kivy.lang import Builder  
from kivy.properties import StringProperty  
from system_monitor.stats_collector import StatsCollector  
import threading  
from queue import Queue  
import time  

Builder.load_file('system_monitor\system_monitor.kv')  

class SystemMonitor(BoxLayout):  
    # Propiedades para actualizar la UI  
    cpu_text = StringProperty('CPU: --')  
    memory_text = StringProperty('Memoria: --')  
    disk_text = StringProperty('Disco: --')  
    network_text = StringProperty('Red: --')  

    def __init__(self, **kwargs):  
        super().__init__(**kwargs)  
        self.stats_queue = Queue()  
        self.running = True  

        # Iniciar el collector en un thread separado  
        self.stats_collector = StatsCollector(self.stats_queue)  
        self.collector_thread = threading.Thread(  
            target=self.stats_collector.start_collecting,  
            args=(self.running,)  
        )  
        self.collector_thread.daemon = True  
        self.collector_thread.start()  

        # Programar la actualización de la UI  
        Clock.schedule_interval(self.update_stats, 0.1)  

    def update_stats(self, dt):  
        try:  
            while not self.stats_queue.empty():  
                stats = self.stats_queue.get_nowait()  
                stat_type = stats.get('type')  

                if stat_type == 'cpu':  
                    self.cpu_text = f'CPU: {stats["value"]}%'  
                elif stat_type == 'memory':  
                    self.memory_text = (  
                        f'Memoria: {stats["percent"]}% '  
                        f'(Usado: {stats["used"]:.1f}GB / '  
                        f'Total: {stats["total"]:.1f}GB)'  
                    )  
                elif stat_type == 'disk':  
                    self.disk_text = (  
                        f'Disco: {stats["percent"]}% '  
                        f'(Usado: {stats["used"]:.1f}GB / '  
                        f'Total: {stats["total"]:.1f}GB)'  
                    )  
                elif stat_type == 'network':  
                    self.network_text = (  
                        f'Red: ↑ {stats["sent_speed"]:.1f} KB/s | '  
                        f'↓ {stats["recv_speed"]:.1f} KB/s'  
                    )  
        except Exception as e:  
            print(f"Error actualizando stats: {e}")  

    def stop_monitoring(self):  
        self.running = False  
        self.stats_collector.stop()  
        if self.collector_thread.is_alive():  
            self.collector_thread.join(timeout=1)


def stats_collector():
    return None


def stats_collector():
    return None


def stats_collector():
    return None