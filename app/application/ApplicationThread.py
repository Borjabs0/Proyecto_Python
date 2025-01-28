import threading  
import subprocess  
import os  
from typing import Dict, Optional  

class ApplicationThread:  
    def __init__(self):  
        self.running_apps: Dict[str, subprocess.Popen] = {}  
        self.app_threads: Dict[str, threading.Thread] = {}  

        self.app_paths = {  
            'vscode': r'C:\Users\borja\AppData\Local\Programs\Microsoft VS Code\Code.exe',
            'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',  
            'explorer': r'explorer.exe',  
            'notepad': r'notepad.exe'  

        }  

    def _run_application(self, app_name: str, app_path: str, args: Optional[list] = None):  
        """  
        Método interno para ejecutar una aplicación  
        """  
        try:  
            if args is None:  
                args = []  

            expanded_path = os.path.expandvars(app_path)  

            process = subprocess.Popen([expanded_path] + args,   
                                     stdout=subprocess.PIPE,  
                                     stderr=subprocess.PIPE)  

            self.running_apps[app_name] = process  

            process.wait()  

            if app_name in self.running_apps:  
                del self.running_apps[app_name]  
            if app_name in self.app_threads:  
                del self.app_threads[app_name]  

        except Exception as e:  
            print(f"Error al ejecutar {app_name}: {str(e)}")  

    def launch_application(self, app_name: str, custom_path: str = None, args: list = None):  
        """  
        Lanza una aplicación en un nuevo hilo  
        """  
        app_path = custom_path if custom_path else self.app_paths.get(app_name.lower())  

        if not app_path:  
            raise ValueError(f"No se encontró la ruta para la aplicación: {app_name}")  

        thread = threading.Thread(  
            target=self._run_application,  
            args=(app_name, app_path, args),  
            name=f"Thread-{app_name}"  
        )  
        thread.daemon = True  

        self.app_threads[app_name] = thread  
        thread.start()  

    def kill_application(self, app_name: str):  
        """  
        Termina una aplicación en ejecución  
        """  
        if app_name in self.running_apps:  
            try:  
                self.running_apps[app_name].terminate()  
                del self.running_apps[app_name]  
                if app_name in self.app_threads:  
                    del self.app_threads[app_name]  
                return True  
            except Exception as e:  
                print(f"Error al terminar {app_name}: {str(e)}")  
                return False  
        return False  

    def get_running_apps(self):  
        """  
        Retorna una lista de aplicaciones en ejecución  
        """  
        return list(self.running_apps.keys())  

    def kill_all_applications(self):  
        """  
        Termina todas las aplicaciones en ejecución  
        """  
        for app_name in list(self.running_apps.keys()):  
            self.kill_application(app_name)  