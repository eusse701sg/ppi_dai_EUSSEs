import flet as ft
from flet import Page
from ui import navigate_to_page

def main(page: Page):
    page.title = "Sportex"
    # Habilitar scroll siempre en la página principal
    page.scroll = "always"
    # Color de fondo
    page.bgcolor = ft.colors.WHITE
    navigate_to_page(page, "home")

#Ejecutar aplicación
ft.app(target=main, assets_dir='assets')

#Para ver en la web usar view=ft.WEB_BROWSER