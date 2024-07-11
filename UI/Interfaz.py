from util.Backend import CoinMarketCap
import ttkbootstrap as ttk
import tkinter as tk
import threading
import time


class UI(tk.Tk):
    """
    Clase que representa la interfaz gráfica principal de la aplicación Mini Dash.

    Atributos:
        API: Instancia de CoinMarketCap para interactuar con la API de Coin Market Cap.
        style: Estilo de la interfaz gráfica.
        ApiVar: Variable de control para la entrada de la API key.
        IDVar: Variable de control para el ID del portafolio.
        HOTreload: Variable de control para el tiempo de recarga automática.
        Main: Frame principal de la interfaz.
        ConfiguracionFrame: Frame para la configuración de la aplicación.
        ColorCombobox: Combobox para seleccionar el tema de color.
        BotonGuardar: Botón para guardar la configuración.
        Contenido: Treeview para mostrar los datos de Coin Market Cap.

    Métodos:
        __init__(): Constructor de la clase, inicializa la interfaz y carga la configuración.
        Configuracion(): Configura la apariencia inicial y carga la configuración de la aplicación.
        CambiarTema(event=None): Cambia el tema de la interfaz según la selección del usuario.
        GuardarEvento(): Guarda los cambios de configuración en la API.
        Guardar(): Inicia un hilo para guardar los cambios de configuración.
        InsertarDatos(): Actualiza periódicamente los datos mostrados en la interfaz desde la API.
        UI(): Configura y muestra la interfaz gráfica.
        PestañaConfiguracion(): Configura la pestaña de configuración con los controles necesarios.
        PestañaPrincipal(): Configura la pestaña principal para mostrar los datos de Coin Market Cap.
    """

    def __init__(self):
        """
        Constructor de la clase UI.
        Inicializa la ventana principal y configura la aplicación.
        """
        super().__init__()

        # Instancia de Backend
        self.API = CoinMarketCap()

        # Cargar Configuración
        self.Configuracion()

        # Cargar la UI
        self.UI()

    def Configuracion(self):
        """
        Configura la apariencia inicial y carga la configuración de la aplicación.
        """
        self.title("Mini Dash")

        # Cargar tema de color
        self.style = ttk.Style(
            theme=self.API.ObtenerConfiguracion()['Color Tema']
        )

        # Variable para la entrada de API de configuración
        self.ApiVar = tk.StringVar()
        self.IDVar = tk.StringVar()
        self.HOTreload = tk.IntVar()

        self.IDVar.set(self.API.ObtenerConfiguracion()['ID_PORTAFOLIO'])
        self.HOTreload.set(self.API.ObtenerConfiguracion()['HOT_RELOAD'])

        # Cargar API si hay
        clave = self.API.ObtenerConfiguracion()['API_KEY']
        if clave == "":
            self.ApiVar.set("Ingrese aquí Api Key")
        else:
            self.ApiVar.set(clave)

        # Crear un proceso para cargar la tabla cada cierto tiempo
        Proceso = threading.Thread(
            target=self.InsertarDatos
        )

        Proceso.start()

    def CambiarTema(self, event=None):
        """
        Cambia el tema de la interfaz según la selección del usuario.

        Args:
            event: Evento de cambio de selección en el combobox (default: None)
        """
        Tema = self.ColorCombobox.get()
        self.style.theme_use(str(Tema))

    def GuardarEvento(self):
        """
        Guarda los cambios de configuración en la API.
        """
        try:
            self.BotonGuardar.configure(
                bootstyle='secondary-outline', state='disabled')
            time.sleep(0.5)
            # Variables a guardar
            Tema = self.ColorCombobox.get()
            ApiKey = self.ApiVar.get()
            Time = self.HOTreload.get()
            # Guardar los datos
            self.API.ModificarConfiguracion('Color Tema', Tema)
            self.API.ModificarConfiguracion('API_KEY', ApiKey)
            self.API.ModificarConfiguracion('ID_PORTAFOLIO', self.IDVar.get())
            self.API.ModificarConfiguracion('HOT_RELOAD', Time)

            self.BotonGuardar.configure(
                bootstyle='success-secondary', state='enabled')
            time.sleep(0.5)
            self.BotonGuardar.configure(bootstyle='primary', state='enabled')

        except Exception as e:
            print(f"Error al guardar: {e}")
            self.BotonGuardar.configure(
                bootstyle='danger-secondary', state='disabled')

    def Guardar(self):
        """
        Inicia un hilo para guardar los cambios de configuración.
        """
        # Iniciar un hilo para la función de guardar
        EventoGuardar = threading.Thread(target=self.GuardarEvento)
        EventoGuardar.start()

    def InsertarDatos(self):
        """
        Actualiza periódicamente los datos mostrados en la interfaz desde la API.
        """
        while True:
            DATA = self.API.ObtenerDatos()
            self.Contenido.delete(*self.Contenido.get_children())

            if DATA[0]:
                for DATOS in DATA[1]:
                    # Corrección de datos
                    quote = DATOS['quote']['USD']
                    USD = quote['price']
                    if USD is None:
                        USD_value = "N/A"
                    else:
                        USD_value = "{:.2f}".format(USD)

                    Fecha = str(DATOS['last_updated'])
                    Fecha = Fecha[:10]
                    Crypto = [DATOS['id'], DATOS['symbol'],
                              DATOS['name'], Fecha, USD_value]
                    self.Contenido.insert('', tk.END, values=Crypto)

            else:
                self.Contenido.delete(*self.Contenido.get_children())
                DATOS = ['Ve', 'a', 'Configuracion', '', '']
                self.Contenido.insert('', tk.END, values=DATOS)

            Time = self.HOTreload.get()
            time.sleep(Time)

    def UI(self):
        """
        Configura y muestra la interfaz gráfica.
        """
        # Gestor de Pestañas
        Gestor = ttk.Notebook(self, bootstyle="light")
        Gestor.pack()

        # Pestaña Principal
        self.Main = ttk.Frame(Gestor)
        self.ConfiguracionFrame = ttk.Frame(Gestor)

        # Añadirlas al Gestor
        Gestor.add(self.Main, text="Main")
        Gestor.add(self.ConfiguracionFrame, text="Configuración")

        # Cargar el contenido de las Pestañas
        self.PestañaPrincipal()
        self.PestañaConfiguracion()

    def PestañaConfiguracion(self):
        """
        Configura la pestaña de configuración con los controles necesarios.
        """
        # Listas de variables de Temas
        ColorTemas = ['vapor', 'darkly', 'morph', 'minty',
                      'superhero', 'solar', 'cosmo', 'journal']

        # Texto Api key
        TextoApi = ttk.Label(self.ConfiguracionFrame, text='Tema de color', font=(
            "Comic Sans MS", 10, "bold"))
        TextoApi.grid(row=0, column=0, padx=10, pady=10)

        # Combobox para cambiar de tema
        self.ColorCombobox = ttk.Combobox(
            self.ConfiguracionFrame, values=ColorTemas)
        self.ColorCombobox.current(ColorTemas.index(
            self.API.ObtenerConfiguracion()['Color Tema']))
        self.ColorCombobox.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
        self.ColorCombobox.bind('<<ComboboxSelected>>', self.CambiarTema)

        # Botón para guardar la configuración
        self.BotonGuardar = ttk.Button(
            self.ConfiguracionFrame, text='Guardar', bootstyle='primary', command=self.Guardar)
        self.BotonGuardar.grid(row=0, column=2, padx=10, pady=10)

        # Texto API
        TextoCoinAPI = ttk.Label(self.ConfiguracionFrame, text='CoinMarketCap API', font=(
            "Comic Sans MS", 10, "bold"))
        TextoCoinAPI.grid(row=1, column=0)

        # Entrada API
        EntradaAPIkey = ttk.Entry(
            self.ConfiguracionFrame, textvariable=self.ApiVar)
        EntradaAPIkey.grid(row=1, column=1, columnspan=2,
                           sticky='we', pady=10, padx=5)

        # Texto ID portafolio
        TextoID = ttk.Label(self.ConfiguracionFrame, text="ID Portafolio", font=(
            "Comic Sans MS", 10, "bold"))
        TextoID.grid(row=2, column=0)

        # Entrada ID
        EntradaID = ttk.Entry(self.ConfiguracionFrame, textvariable=self.IDVar)
        EntradaID.grid(row=2, column=1, columnspan=2,
                       sticky='we', pady=10, padx=5)

        # Texto SpinBox
        TextoSpinBox = ttk.Label(self.ConfiguracionFrame, text="Hot Reload Time", font=(
            "Comic Sans MS", 10, "bold"))
        TextoSpinBox.grid(row=4, column=0, padx=5, pady=5)

        # Spinbox para el tiempo de recarga automática
        SpinBoxHotReload = ttk.Spinbox(
            self.ConfiguracionFrame, from_=5, to=30, textvariable=self.HOTreload)
        SpinBoxHotReload.grid(row=4, column=1, sticky='ew',
                              columnspan=2, padx=5, pady=5)
    def PestañaPrincipal(self):
        """
        Configura la pestaña principal para mostrar los datos de Coin Market Cap.
        """
        # Texto Título
        TextoTitulo = ttk.Label(self.Main, text="Coin Market Cap", font=("Comic Sans MS", 12, "bold"))
        TextoTitulo.grid(row=0, column=0, columnspan=2)

        # Sección donde se mostrarán las divisas, etc.
        Columnas = ("ID", "Símbolo", "Nombre", "Hora de Actualización", "Precio USD")
        
        # ScrollBar
        scrollbar = ttk.Scrollbar(self.Main, orient='vertical')
        scrollbar.grid(row=1, column=1, sticky='ns')

        self.Contenido = ttk.Treeview(
            self.Main, show='headings', columns=Columnas, height=15, yscrollcommand=scrollbar.set
        )
        
        # Configurar el ScrollBar
        scrollbar.config(command=self.Contenido.yview)

        # Ajustar las columnas
        self.Contenido.column('ID', width=50, anchor=tk.CENTER)
        self.Contenido.column('Símbolo', width=100, anchor=tk.CENTER)
        self.Contenido.column('Nombre', width=100, anchor=tk.CENTER)
        self.Contenido.column('Hora de Actualización', width=100, anchor=tk.CENTER)
        self.Contenido.column('Precio USD', width=100, anchor=tk.CENTER)

        self.Contenido.heading('ID', text="ID")
        self.Contenido.heading('Símbolo', text="Símbolo")
        self.Contenido.heading('Nombre', text="Nombre")
        self.Contenido.heading('Hora de Actualización', text="Hora de Actualización")
        self.Contenido.heading('Precio USD', text="Precio USD")

        # Posicionar el TreeView
        self.Contenido.grid(row=1, column=0, sticky='nsew')

        # Configurar el peso de las filas y columnas para que se expandan
        self.Main.grid_rowconfigure(1, weight=1)
        self.Main.grid_columnconfigure(0, weight=1)
