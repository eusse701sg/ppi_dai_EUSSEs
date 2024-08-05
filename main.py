import flet as ft
from flet import Page
from ui import navigate_to_page

def main(page: Page):
    page.title = "Sportex"
    page.scroll = "always"  # Habilitar scroll siempre en la página principal
    navigate_to_page(page, "home")

ft.app(target=main) #Ejecutar aplicación
