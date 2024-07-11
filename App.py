"""
Cargador principal para iniciar la aplicación de interfaz de usuario.

Importa la clase UI del módulo UI.Interfaz y la inicializa para comenzar la aplicación.

Uso:
    Ejecute este script para lanzar la aplicación de interfaz de usuario.

Ejemplo:
    $ python main.py
"""

from UI.Interfaz import UI

if __name__ == "__main__":
    # Inicializa la aplicación de interfaz de usuario
    App = UI()

    # Inicia el bucle principal de la aplicación
    App.mainloop()
