# Importar librerias necesarias
import flet as ft
from flet import Page

# Importar funciones de ui.py
from ui import navigate_to_page

def main(page: Page):
    """
    Función principal que inicializa y configura la página de la aplicación "Sportex".

    Args:
        page (Page): Objeto `Page` que representa la página principal de la aplicación.

    Returns:
        None
    """    
    # Establece el titulo de la ventana del navegador o de la ventana de windows
    page.title = "Sportex"
    # Habilitar scroll siempre en la página principal
    page.scroll = "always"
    # Color de fondo
    page.bgcolor = ft.colors.WHITE
    # Llama a la función navigate_to_page de ui.py (Redirige a la seccion home/Inicio)
    navigate_to_page(page, "home")

# Ejecutar aplicación, las imagenes estáticas se encuentran en "assets".
ft.app(target=main, assets_dir='../assets')

# Para ver en el navegador web usar "view=ft.WEB_BROWSER como parámetro de ft.app"