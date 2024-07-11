import json
import requests

class CoinMarketCap:
    """
    Clase para interactuar con la API de CoinMarketCap y gestionar la configuración de la aplicación.

    Métodos:
        ObtenerConfiguracion(): Carga la configuración desde 'config/config.json'.
        ModificarConfiguracion(key: str, valor: str): Modifica un valor específico en 'config/config.json'.
        ValidarKey(): Valida la clave API almacenada en la configuración.
        ObtenerDatos(): Obtiene datos de la API de CoinMarketCap para una categoría específica.
    """

    def __init__(self):
        """
        Constructor de la clase CoinMarketCap.
        """
        pass
    
    def ObtenerConfiguracion(self):
        """
        Carga la configuración desde 'config/config.json'.
        
        Returns:
            dict: Datos cargados desde el archivo JSON de configuración.
        """
        with open('config/config.json', 'r') as archivo:
            return json.load(archivo)
        
    def ModificarConfiguracion(self, key: str, valor: str):
        """
        Modifica un valor específico en 'config/config.json'.

        Args:
            key (str): Clave del valor a modificar.
            valor (str): Nuevo valor a asignar a la clave especificada.
        """
        if key != 'Color Tema':
            # Limpieza de datos
            if valor == "" or valor == "Ingrese aquí Api Key":
                valor = ""

        with open('config/config.json', 'r') as archivo:
            datos = json.load(archivo)

        # Modificar el dato
        datos[key] = valor

        # Guardar la configuración
        with open('config/config.json', 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def ValidarKey(self):
        """
        Valida la clave API almacenada en la configuración.

        Returns:
            bool: True si la clave API es válida, False de lo contrario.
        """
        # Obtener la clave API desde la configuración
        KEY = self.ObtenerConfiguracion()['API_KEY']
        # URL de la API de CoinMarketCap
        URL = 'https://pro-api.coinmarketcap.com/v1/key/info'

        # Encabezados con la clave API
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': KEY,
        }

        # Realizar la solicitud GET
        respuesta = requests.get(url=URL, headers=headers)

        # Verificar el estado de la solicitud
        if respuesta.status_code == 200:
            return True
        else:
            return False

    def ObtenerDatos(self):
        """
        Obtiene datos de la API de CoinMarketCap para una categoría específica.

        Returns:
            tuple: (True, datos) si la solicitud fue exitosa, (False, '') de lo contrario.
        """
        # Obtener la clave API desde la configuración
        KEY = self.ObtenerConfiguracion()['API_KEY']
        
        # Verificar si la API key es válida
        if not self.ValidarKey():
            return False, ''
        
        # URL de la API
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/category"

        # Parámetros de la solicitud
        parametros = {
            "id": "605e2ce9d41eae1066535f7c"  # Reemplaza "1" con el ID de la categoría que deseas consultar
        }

        # Encabezados de la solicitud, incluyendo la clave API
        encabezados = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": KEY
        }

        # Realizar la solicitud GET
        resultado = requests.get(url=url, headers=encabezados, params=parametros)

        if not resultado.status_code == 200:
            return False, ''

        # Extracción de datos
        resultado_en_bruto = resultado.json()

        datos = resultado_en_bruto['data']

        # Extraer las cryptos
        COIN = datos['coins']

        return True, COIN
