import psutil  
import threading  
import time  
import matplotlib.pyplot 

class StatsCollector:  
    def __init__(self, queue):  
        self.queue = queue  
        self.net_io_counters = psutil.net_io_counters()  
        self.prev_bytes_sent = self.net_io_counters.bytes_sent  
        self.prev_bytes_recv = self.net_io_counters.bytes_recv  
        self._stop_event = threading.Event()  

    def start_collecting(self, running):  
        while not self._stop_event.is_set():  
            # Recolectar CPU  
            self.collect_cpu()  
            # Recolectar Memoria  
            self.collect_memory()  
            # Recolectar Disco  
            self.collect_disk() 
            # Recolectar Red  
            self.collect_network()  
            # Esperar antes de la siguiente actualización  
            time.sleep(1)  

    def stop(self):  
        self._stop_event.set()  

    def collect_cpu(self):  
        try:  
            cpu_percent = psutil.cpu_percent(interval=None)  
            self.queue.put({  
                'type': 'cpu',  
                'value': cpu_percent  
            })  
        except Exception as e:  
            print(f"Error collecting CPU stats: {e}")  

    def collect_memory(self):  
        try:  
            memory = psutil.virtual_memory()  
            self.queue.put({  
                'type': 'memory',  
                'percent': memory.percent,  
                'used': memory.used / (1024 * 1024 * 1024),  
                'total': memory.total / (1024 * 1024 * 1024)  
            })  
        except Exception as e:  
            print(f"Error collecting memory stats: {e}")  

    def collect_disk(self):  
        try:  
            disk = psutil.disk_usage('/')  
            self.queue.put({  
                'type': 'disk',  
                'percent': disk.percent,  
                'used': disk.used / (1024 * 1024 * 1024),  
                'total': disk.total / (1024 * 1024 * 1024)  
            })  
        except Exception as e:  
            print(f"Error collecting disk stats: {e}")  

    def collect_network(self):  
        try:  
            net_io = psutil.net_io_counters()  
            bytes_sent = net_io.bytes_sent  
            bytes_recv = net_io.bytes_recv  

            sent_speed = (bytes_sent - self.prev_bytes_sent) / 1024  
            recv_speed = (bytes_recv - self.prev_bytes_recv) / 1024  

            self.prev_bytes_sent = bytes_sent  
            self.prev_bytes_recv = bytes_recv  

            self.queue.put({  
                'type': 'network',  
                'sent_speed': sent_speed,  
                'recv_speed': recv_speed  
            })  
        except Exception as e:  
            print(f"Error collecting network stats: {e}")  