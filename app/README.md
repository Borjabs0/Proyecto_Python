# Aplicación Multifuncional  

Esta aplicación es una herramienta desarrollada con Kivy, que ofrece múltiples funcionalidades como un reproductor de música, un gestor de aplicaciones, un juego interactivo, y un monitor de recursos del sistema.  

## Funcionalidades  

### 1. Juego del Círculo  
- **Objetivo**: Haz clic en el círculo rojo que aparece en la pantalla antes de que se mueva.  
- **Implementación**: Utiliza la clase `CircleGame` para manejar la lógica del juego y la interacción del usuario.  

### 2. Monitor de Recursos  
- **Funcionalidad**: Muestra el uso de CPU, memoria, red y disco en tiempo real.  
- **Propósito**: Ayuda a los usuarios a monitorear el rendimiento del sistema mientras utilizan la aplicación.  

### 3. Reproductor de Música  
- **Estado Actual**: Permite a los usuarios seleccionar archivos de música a través de un explorador de archivos. Actualmente, hay un problema con `pygame` que impide la reproducción de la canción seleccionada, que se resolverá en futuras actualizaciones.  
- **Implementación**: Utiliza `pygame.mixer` para la reproducción de audio y se ejecuta en un hilo separado para mantener la interfaz de usuario receptiva.  

### 4. Integración de Navegador Web  
- **Funcionalidad**: Lanza URLs introducidas por el usuario en el navegador predeterminado.  
- **Planes Futuros**: Integrar un navegador web completo dentro de la aplicación.  

## Detalles Técnicos  

### Hilos y Procesos  
- **Gestión de Aplicaciones**: Utiliza hilos para lanzar y gestionar aplicaciones externas, asegurando que se ejecuten de manera independiente sin bloquear la aplicación principal.  
- **Reproducción de Música**: Gestionada en un hilo separado para permitir la reproducción continua sin afectar el rendimiento de la interfaz de usuario.  

### Estructura del Código  
- **Paquetes**: El proyecto está organizado en paquetes para mejorar la modularidad y el mantenimiento.  
- **Clases Clave**:  
  - `ApplicationThread`: Gestiona el lanzamiento y la terminación de aplicaciones externas.  
  - `CircleGame`: Maneja la lógica y la interfaz del juego interactivo.  
  - `MusicThread`: Gestiona las operaciones de reproducción de música.  

## Instalación y Configuración  

1. **Requisitos**: Asegúrate de tener Python y Kivy instalados en tu sistema.  
2. **Ejecución de la Aplicación**: Ejecuta el archivo `main.py` para iniciar la aplicación.  

## Mejoras Futuras  

- **Corrección de Reproducción de Música**: Resolver el problema con `pygame` para permitir la selección y reproducción adecuada de canciones.  
- **Navegador Web Integrado**: Desarrollar un navegador dentro de la aplicación para una navegación web fluida.  

## Video: https://youtu.be/zosu_2eK9XI