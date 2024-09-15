# Importar librerías necesarias
import flet as ft
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import time
import os
from PIL import Image as PILImage
from flet import Page, Image
from geopy.geocoders import Nominatim
from pyproj import CRS
import numpy as np
import json
# Importar funciones necesarias de events.py
from events import load_events, add_event, modify_event, inscribe_user, uninscribe_user, get_user_events
# Importar funciones necesarias de content.py
from content import read_privacy_policy, register_user, authenticate_user, change_password, get_current_user, set_current_user, save_profile_picture, save_event_logo

# Función para crear el encabezado de la aplicación
def create_header_row(page: Page):
    """Crea el encabezado dependiendo si hay o no un usuario activo.

    Args:
        page (Page): Objeto `Page` que representa la página principal de la aplicación.
        
    Returns:
        ft.Container: Contenedor con el encabezado
    """   
    
    # Boton Logo
    logo_button = ft.GestureDetector(
        # Objeto 'Image' que contiene la ruta al logo, el ancho y el largo
        content=ft.Image(src="LogoSportex.PNG", width=200, height=80),
        # Al clickear llama la función navigate_to_page que redirige a la página home/inicio
        on_tap=lambda e: navigate_to_page(page, "home") 
    )

    # Boton Inicio
    home_button = ft.ElevatedButton(
        # Propiedades como texto, ancho, largo, color de fondo, color de letra
        text="Inicio",
        width=130,
        height=50,
        bgcolor="grey",
        color="black",
        # Al clickear llama la función navigate_to_page que redirige a la página home/inicio
        on_click=lambda e: navigate_to_page(page, "home")
    )

    # Boton contactame
    contact_button = ft.ElevatedButton( 
        # Propiedades como texto, ancho, largo, color de fondo, color de letra
        text="Contáctame",
        width=130,
        height=50,
        bgcolor="grey",
        color="black",
        # Al clickear llama la función navigate_to_page que redirige a la página Contáctame
        on_click=lambda e: navigate_to_page(page, "contact") 
    )

    # Boton quién soy
    who_button = ft.ElevatedButton( 
        # Propiedades como texto, ancho, largo, color de fondo, color de letra
        text="Quién soy",
        width=150,
        height=50,
        bgcolor="grey",
        color="black",
        # Al clickear llama la función navigate_to_page que redirige a la página Quién soy
        on_click=lambda e: navigate_to_page(page, "who") 
    )

    # Boton Eventos
    events_button = ft.ElevatedButton(
        # Propiedades como texto, ancho, largo, color de fondo, color de letra
        text="Eventos",
        width=130,
        height=50,
        bgcolor="grey",
        color="black",
        # Al clickear llama la función navigate_to_page que redirige a la página Eventos
        on_click=lambda e: navigate_to_page(page, "events") 
    )

    # Boton Mi perfil
    profile_button = ft.ElevatedButton(
        # Propiedades como texto, ancho, largo, color de fondo, color de letra
        text="Mi perfil",
        width=130,
        height=50,
        bgcolor="grey",
        color="black",
        # Al clickear llama la función navigate_to_page que redirige a la página Mi perfil
        on_click=lambda e: navigate_to_page(page, "profile") 
    )

    # Boton cerrar sesión 
    logout_button = ft.ElevatedButton( 
        # Propiedades como texto, ancho, largo, color de fondo, color de letra      
        text="Cerrar sesión",
        width=150,
        height=50,
        bgcolor="black",
        color="white",
        # Llama la funcion cerrar sesión  
        on_click=lambda e: logout(page)          
    )

    # Boton iniciar sesión
    login_button = ft.ElevatedButton(
        # Propiedades como texto, ancho, largo, color de fondo, color de letra   
        text="Iniciar sesión",
        width=150,
        height=50,
        bgcolor="black",
        color="white",
        # Al clickear llama la función navigate_to_page que redirige a la página Iniciar sesión
        on_click=lambda e: navigate_to_page(page, "login") 
    )

    # Boton registrarme
    register_button = ft.ElevatedButton(
        # Propiedades como texto, ancho, largo, color de fondo, color de letra   
        text="Registrarme",
        width=180,
        height=50,
        bgcolor="blue",
        color="white",
        # Al clickear llama la función navigate_to_page que redirige a la página Registrarme
        on_click=lambda e: navigate_to_page(page, "register")
    )  

    # Llama a la función get_current_user de content.py para determinar si hay un usuario activo o no
    current_user = get_current_user()

    # Botones SI hay un usuario activo
    if current_user:               
        controls = [home_button, events_button, contact_button, who_button, profile_button, logout_button]

    # Botones si NO hay un usuario activo
    else: 
        controls = [home_button, events_button, contact_button, who_button, login_button, register_button]

    
    # Encabezado completo con logo y botones
    # Crear fila horizontal tipo Row
    header_row = ft.Row(
        #Contenido
        controls=[
            #Boton de logo             
            logo_button,
            # Otra fila horizontal tipo Row que está adentro del Row principal
            ft.Row( 
                # Contenido (botones)
                controls=controls, 
                # Espaciado entre botones
                spacing=15 
            ),
        ],
        # Espaciado entre el logo y los botones
        alignment="spaceBetween"       
    )
      
    # Crear contenedor para el encabezado
    header_container = ft.Container(
        content=ft.Column(
            controls=[
                # Añade cabecera
                header_row,               
            ],
            spacing=10 
        ),
        # Espaciado entre los bordes
        padding=10,
        # Altura
        height=100,
        # Color de fondo
        bgcolor="white", 
        # Alineamiento arriba en el centro
        alignment=ft.alignment.top_center,
        # Bordeado tamaño 2, color negro
        border=ft.border.all(2, "black"), 
    )

    # Retorna el encabezado completo
    return header_container 

# Funcion para navegar a una pagina
def navigate_to_page(page: Page, page_name: str):
    """
    Navega hacia una página o sección.

    Args:
        page (Page): Objeto 'Page' que representa una página de la app, siempre debe ir este parámetro
        page_name (str): Nombre de la página

    Returns:
        None
    """
    
    def save_current_event(event_id):
        """
        Guarda en la variable global current_event el id del evento seleccionado.

        Args:
            event_id (int): id del evento a guardar            

        Returns:
            None
        """
        # Se define la variable como global
        global current_event
        # Se cambia el valor de la variable global current_event y se guarda el ID del evento seleccionado
        current_event = event_id
        # Llama a la función navigate_to_page y allí se utiliza la variable current_event
        navigate_to_page(page, "modify_event")
    
    # Limpiar los controles y contenido actual
    page.controls.clear()   
    content = []
    page.update()

    # Pagina Contactame    
    if page_name == "contact": 
        # Contenido de la página
        content = [
            ft.Container(
                content=ft.Text("Contáctame", size=30, text_align="center"),
                padding=10
            ),
            ft.Container(
                content=ft.Text("Si tienes alguna pregunta o necesitas asistencia, no dudes en ponerte en contacto conmigo.", size=25),
                padding=10
            ),            
            ft.Container(
                content=ft.Text("Correo Electrónico: santiagoegla@gmail.com", size=25),
                padding=10
            ),
            ft.Container(
                content=ft.Text("WhatsApp: +57 319-799-4175", size=25),
                padding=10
            ),
            ft.Container(
                content=ft.ElevatedButton("LinkedIn", on_click=lambda e: e.page.launch_url("https://www.linkedin.com/in/santiago-eusse-gil-638b83220/")),
                padding=10
            ),
            ft.Container(
                content=ft.ElevatedButton("GitHub App", on_click=lambda e: e.page.launch_url("https://github.com/eusse701sg/ppi_dai_EUSSEs")),
                padding=10
            )
        ]

    # Pagina quien soy    
    elif page_name == "who":
        try:
            # Lee el archivo txt quién soy y lo codifica a utf8
            with open("docs/who_am_i.txt", "r", encoding="utf-8") as file: 
                who_am_i_text = file.read()
        # Si no encuentra el txt        
        except FileNotFoundError: 
            who_am_i_text = "Descripción no disponible."
        
        # Contenido
        content = [
            # Titulo principal
            ft.Container(
                content=ft.Text("Quién soy", size=30, text_align="center"),
                padding=10
            ),
            # Txt de quién soy
            ft.Container(
                content=ft.Text(
                    who_am_i_text,
                    size=16,
                    # Texto justificado
                    text_align="justify"
                ),
                # Contenedor alineado al centro a la izquierda
                alignment=ft.alignment.center_left, 
                padding=10
            )
        ]

    # Pagina registrarme        
    elif page_name == "register":

        # Función Para le manejo del registro
        def handle_register(e):
            """
            Función para el manejo del registro.

            Args:
                e (control event): Se llama al realizar una accion como clickear un botón.

            Returns:
                None               
            """        

            # Llama la función validate_fields para verificar que todos los campos sean llenados
            # Si la funcion devuelve False, sale un aviso que pide rellenar campos faltantes
            if not validate_fields():
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Por favor, rellene todos los campos faltantes", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                )) 
                return
            
            # Asigna los valores a los campos 
            email = email_field.value
            password = password_field.value
            username = username_field.value
            names = names_field.value
            lastnames = lastnames_field.value
            
            # Llama la funcion registrar usuario de content.py
            # Si el registro es exitoso, es decir register_user retorna True
            if register_user(email, password, username, names, lastnames):
                # Llama a la función navigate_to_page y redirige a la página para iniciar sesión
                navigate_to_page(page, "login"),
                # Aviso para registro exitoso
                page.show_snack_bar(ft.SnackBar(  
                    content=ft.Text("Registro exitoso.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))
            # Si el registro no es exitoso, es decir register_user retorna False
            else:
                # Aviso para registro fallido
                page.show_snack_bar(ft.SnackBar( 
                    content=ft.Text("Error: El correo o nombre de usuario ya está registrado", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))

        # Actualizar estado del botón basado en el checkbox
        def toggle_register_button(e):
            """
            Función para actualizar el estado del botón basado en el checkbox.

            El botón está deshabilitado si el valor del checkbox es False, 
            A su vez el botón está habilitado si el valor del checkbox es True.
        
            
            Args:
                e (control event): Se llama al realizar una accion como clickear el checkbox.

            Returns:
                None               
            """     
            # El botón está deshabilitado si el valor del checkbox es False
            register_button.disabled = not privacy_checkbox.value
            # Actualiza la página
            page.update()

        #Validar campos
        def validate_fields():
            """
            Valida que todos los campos del formulario estén llenos.    

            La función verifica si los valores de los campos `email_field`, `password_field`, 
            `username_field`, `names_field` y `lastnames_field` no están vacíos después de 
            eliminar espacios en blanco al inicio y al final.

            Returns:
                bool: Retorna `True` si todos los campos tienen un valor no vacío. 
                Retorna `False` si al menos uno de los campos está vacío.
            """            
            fields = [email_field,password_field, username_field, names_field, lastnames_field]            
            return all(field.value.strip() != "" for field in fields)

        # Mostrar politicas de privacidad
        def show_privacy_policy(_):
            """
            Lee y muestra las políticas de privacidad en un objeto 'AlertDialog'.


            Args:
                Se llama al momento de clickear el botón "Politicas de privacidad"
            
            Returns:
                None
            """            

            # Crea objeto alertdialog
            dialog = ft.AlertDialog(
                modal = True,
                # Titulo
                title = ft.Text("Política de Privacidad"),
                # Contenido
                content = ft.Container(
                    content = ft.ListView(
                        # llama la función read_privacy_policy de content.py para leer el archivo
                        controls=[ft.Text(read_privacy_policy(), size=14)],
                        expand=True,
                        auto_scroll=False
                    ),
                    #Largo y ancho
                    height=400,
                    width=400,                    
                ),
                actions=[
                    # Boton cerrar que al clickear llama la función close_dialog
                    ft.TextButton("Cerrar", on_click=lambda _: close_dialog(dialog))
                ]
            )
            page.dialog = dialog
            # Abre el dialog
            dialog.open = True
            page.update()        

        # Funcion para cerrar el objeto dialog que genera show_privacy_policy
        def close_dialog(dialog):
            """
            Cierra el objeto dialog al clickear en el botón Cerrar
            """
            dialog.open= False
            page.update()

        # Formulario de registro
        email_field = ft.TextField(label="Correo Electrónico", width=300)        
        password_field = ft.TextField(label="Contraseña", width=300, password=True) #Contraseña oculta
        username_field = ft.TextField(label="Nombre de Usuario", width=300)
        names_field = ft.TextField(label="Nombres", width=300)
        lastnames_field = ft.TextField(label="Apellidos", width=300)
        
        # Checkbox para aceptar las políticas de privacidad, inicialmente desmarcado
        privacy_checkbox = ft.Checkbox(label="Acepto las políticas de privacidad", width=300, value=False)

        # Botón para registrar, inicialmente deshabilitado
        register_button = ft.ElevatedButton(
            # Propiedades como texto, largo, ancho, color de letra y color de fondo
            content=ft.Container(
                content=ft.Text(value="Registrar", size=22)
            ),
            # Al Clickear llama la función handle_register para el manejo del registro         
            on_click=lambda e: handle_register(e), disabled=True,
            height=60,
            width=180,
            color="white",
            bgcolor="blue"
        )

        # Llama la función toggle_register_button para habilitar el botón de registrar
        privacy_checkbox.on_change = toggle_register_button       
    

        # Botón para ver Políticas de privacidad
        privacy_link = ft.TextButton("Políticas de privacidad")
        # Llama la función show_privacy_policy al clickear el botón
        privacy_link.on_click = show_privacy_policy

        # Contenido de la página de registro        
        content = [
            ft.Container(
                # Titulo Registrarme
                content=ft.Text("Registrarme", size=30, text_align="center"),
                padding=10,
                alignment=ft.alignment.top_center                
            ),
            # Contenedor con el formulario
            ft.Container( 
                content=ft.Column(
                    controls=[
                        email_field,
                        password_field,
                        username_field,
                        names_field,
                        lastnames_field,
                        # Fila horizontal para poner el checkbox y el botón de políticas de privacidad juntos
                        ft.Row(controls=[privacy_checkbox, privacy_link],alignment="center"),
                        register_button                        
                    ],
                    alignment="center",
                    spacing=20,
                    # Alineamiento horizontal
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    
                ),
                padding=10                                                           
            )
        ]

    # Pagina para iniciar sesion
    elif page_name == "login": 

        ## Formulario de inicio de sesión
        # Campo correo o usuario
        email_or_username_field = ft.TextField(label="Correo Electrónico o Nombre de Usuario", width=300)
        # Campo contraseña oculta
        password_field = ft.TextField(label="Contraseña", width=300, password=True)
        

        # Funcion para el manejo del acceso
        def handle_login(e):
            """
            Función para el manejo de inicio de sesión.
            Esta función se llama al clickear en iniciar sesión luego de diligenciar las credenciales.

            Args:
                e (control event): Se llama al realizar una accion como clickear un botón.

            Returns:
                None               
            """            

            # Valor que diligenció el usuario en el campo de email o usuario
            email_or_username = email_or_username_field.value
            # Valor que diligenció el usuario en el campo de contraseña
            password = password_field.value   

            # Llama la funcion authenticate_user de content.py para validar credenciales         
            user = authenticate_user(email_or_username, password)
            
            # Si la función retorna True = Credenciales correctas
            if user: 
                # Llama la función set_current_ser de content.py
                # Actualiza la variable current user para definir el usuario actual
                set_current_user(user) 
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de inicio de sesión exitoso
                    content=ft.Text("Inicio de sesión exitoso.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000
                ))
                # Llama a la función navigate_to_page para redirigir al inicio
                navigate_to_page(page, "home")

            # Si la función retorna False = Credenciales erróneas
            else:
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de credenciales incorrectas
                    content=ft.Text("Error: Credenciales incorrectas", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))
        
        # Contenido de la página
        content = [
            ft.Container(
                # Titulo iniciar sesión
                content=ft.Text("Iniciar sesión", size=30, text_align="center"),
                padding=10
            ),
            ft.Container(
                # Contenedor con los campos de usuario y contraseña
                content=ft.Column(
                    controls=[
                        email_or_username_field,
                        password_field,
                        # Boton iniciar sesión que llama a la función handle_login
                        ft.ElevatedButton("Iniciar sesión", on_click=handle_login)
                    ],
                    alignment="center",
                    spacing=10
                ),
                padding=10
            )
        ]

    # Pagina del perfil    
    elif page_name == "profile":
        page.update()
        # Llama a la función get_current_user de content.py para obtener el usuario actual logeado.
        current_user = get_current_user() 

        # Si no hay un usuario logeado
        if current_user is None:
            # Redirige a la página Login
            navigate_to_page(page, "login")
            return
        
        # Función para mostrar los eventos en los que el usuario está inscrito
        def show_inscribed_events():
            """
            Muestra los eventos en los que el usuario actual está inscrito.

            Llama a la función `get_user_events` para obtener los eventos en los que el usuario está registrado, 
            luego muestra una lista de dichos eventos con la opción de desinscribirse de cada uno.

            Args:
                None

            Returns:
                events_list (ft.Column): Un componente de Flutter que contiene los eventos en los que 
                el usuario está inscrito, con un botón para desinscribirse de cada evento.
            """
            # Llama la función get_user_events de events.py con el username como parametro
            user_events = get_user_events(current_user['username'])

            # Inicializa la lista de eventos con un ft.Column vacío
            events_list = ft.Column([
                ft.Text("Mis eventos inscritos", size= 20, weight=ft.FontWeight.BOLD),
            ],alignment=ft.MainAxisAlignment.START)

            # Función para remover un evento de la interfaz del perfil y desinscribir de un evento
            def unsubscribe_from_event(event):
                # Llama la función uninscribe_user de events.py para desincribir al usuario
                if uninscribe_user(event['id'], current_user['username']):
                    # Remueve el evento desinscrito de la pagina de perfil
                    events_list.controls.remove(event_row)
                    page.update()
            
            # Itera sobre todos los eventos en los que está inscrito el usuario
            for event in user_events:
                # Crear un ft.Row por cada evento
                event_row = ft.Row([
                    ft.Text(event['nombre']),
                    ft.Text(f"{event['fecha']} - {event['hora']}"),
                    # Boton para desinscribir que llama la función unsuscribe_from_event
                    ft.ElevatedButton("Desinscribir", on_click=lambda _: unsubscribe_from_event(event))
                ])
                # Concatena todos los eventos en los que está inscrito el usuario
                events_list.controls.append(event_row)

            # Retorna la lista de eventos que el usuario está inscrito
            return events_list            

        # Funcion para cambiar contraseña    
        def handle_password_change(e):
            """
            Función para cambiar la contraseña.

            Args:
                e (control event): Se llama al realizar una accion como clickear un botón.

            Returns:
                None               
            """           

            # Valor ingresado por le usuario de Contraseña vieja
            old_password = old_password_field.value   
            # Valor ingresado por el usuario de Contraseña nueva
            new_password = new_password_field.value 
            
            # Llama funcion change_password de content.py para cambiar contraseña
            if change_password(old_password, new_password): 
                # Contraseña cambiada
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de contraseña cambiada con exito
                    content=ft.Text("Contraseña cambiada exitosamente.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))
            else:
                # Error cambiando contraseña
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de que la contraseña antigua es incorrecta
                    content=ft.Text("Error: Contraseña antigua incorrecta", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                )) 

        # Función para el manejo del cambio de foto de perfil
        def handle_profile_picture_change(e: ft.FilePickerResultEvent):
            """
            Función para cambiar la foto de perfil.

            Args:
                e (ft.FilePickerResultEvent): Se llama al subir archivos de imagen con file.picker.

            Returns:
                None               
            """                

            # Si elige 0 imagenes
            if not e.files or len(e.files) == 0:
                return
            
            # Dividir la ruta de la imagen en path y nombre
            file_path = e.files[0].path
            file_name = e.files[0].name

            # Verificar que archivo tiene formato de imagen
            valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".jfif", ".avif"]            
            file_extensions = os.path.splitext(file_name)[1].lower()

            # Si no cumple con los formatos requeridos
            if file_extensions not in valid_extensions:
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de que no es una imagen válida
                    content=ft.Text("El archivo seleccionado no es una imagen válida", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return
            
            try:
                # Intentar abrir el archivo como imagen
                with PILImage.open(file_path) as img:
                    # Si llega aquí, es una imagen válida
                    pass
            except Exception:
                page.show_snack_bar(ft.SnackBar(
                    # El archivo seleccionado no es una imágen válida
                    content=ft.Text("El archivo seleccionado no es una imagen válida.", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))      

            # Llama a la función save_profile_picture de content.py para guardar la foto de perfil en assets y cambiar el nombre del archivo
            if save_profile_picture(file_path):
                # Llama la función update_profile_picture para actualizar la foto de perfil según la nueva ruta
                update_profile_picture(file_path)
                page.update()
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de que la foto se cambió con exito
                    content=ft.Text("Foto de perfil cambiada con éxito.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))      
            else:
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de que hubo un error guardando la imagen
                    content=ft.Text("Error al guardar la imagen de perfil.", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))            

        # Función para actualizar foto de perfil
        def update_profile_picture(file_path):
            """
            Función para actualizar la foto de perfil.

            Args:
                file path: Recibe la ruta de la imagen
                                     
            """                

            profile_picture.src = file_path
            page.update()

        # Función para cargar todos los eventos
        def load_user_events():
            """
            Función para cargar los eventos creador por el usuario.

            Returns:
                Eventos creador por el usuario              
            """                

            # Llama la función load_events de events.py para cargar todos los eventos como un dataframe
            events = load_events()
            # Guarda en una varible unicamente los eventos creados por el usuario actual y los retorna
            user_events = events[events['organizador'] == current_user['username']]
            return user_events
        
        # Función para eliminar eventos creados por el usuario actual
        def delete_event(event_id):
            """
            Función para eliminar eventos creados por el usuario actual.

            Args:
                event id (int): identificador (id) de un evento

            Returns:
                None               
            """    

            # Llama la función load_events de events.py para cargar todos los eventos como un dataframe
            events = load_events()
            # Filtra las filas del dataframe exceptuando la fila del ID del evento que se va a eliminar
            events = events[events['id'] != event_id]
            # Guarda en el csv todos los eventos a excepción del evento a eliminar
            events.to_csv('data/events.csv', index=False)
            # LLama la función update_user_events para actualizar los eventos del usuario actual
            update_user_events()
            # Elimna el logo del evento eliminado de la carpeta "assets"
            if os.path.exists(f"assets/uploads/events/logos/event_{event_id}.png"):
                os.remove(f"assets/uploads/events/logos/event_{event_id}.png")
            page.show_snack_bar(ft.SnackBar(
                # Aviso de evento eliminado con exito
                content=ft.Text("Evento eliminado exitosamente.", size=20, color="white"),
                bgcolor="lightgreen",
                duration=3000
            )),
            # Actualiza la pagina
            page.update()
                    
        # Función para actualizar los eventos del usuario logeado (actualiza user_events_colum)
        def update_user_events():
            """
            Función para actualizar user_events_colum los eventos del usuario logeado.        

            Returns:
                None               
            """    
            # Llama la función load_user_events para tener los eventos creados por el usuario como un dataframe
            user_events = load_user_events()
            # Borrar los controles de la columna contenedora de los eventos
            user_events_column.controls.clear()
            # Itera por cada evento creado por el usuario logeado del dataframe y los muestra
            for _, event in user_events.iterrows():
                # Contenedor horizontal tipo Row con los eventos creados por el usuario
                event_row = ft.Row([
                    ft.Text(f"• {event['nombre']}", size=16),
                    ft.Text(f"({event['fecha']})", size=14),
                    ft.Text(f"({event['estado']})", size=14),
                    # Boton para eliminar un evento que llama la función delete_event con el id del evento
                    ft.ElevatedButton("Eliminar", on_click=lambda _, eid=event['id']: delete_event(eid)),
                    # Boton para modificar un evento que llama la función save_current_event para guardar el id del evento seleccionado         
                    ft.ElevatedButton("Modificar", on_click=lambda _, eid=event['id']: save_current_event(eid))
                ])
                # Añade los nuevos controles del Row creado anteriormente (contiene los eventos creados por el usuario)
                user_events_column.controls.append(event_row)
            # Actualiza la página
            page.update()


        # Columna contenedora de los eventos creados por el usuario
        user_events_column = ft.Column([], scroll=ft.ScrollMode.AUTO, height=300, alignment=ft.MainAxisAlignment.START)
        # Se llama la función update_user_events para modificar user_events_column
        update_user_events()

        # Definir file_picker para elegir una foto, es utilizado más tarde
        file_picker = ft.FilePicker(on_result=handle_profile_picture_change)
        page.overlay.append(file_picker)

        # Cargar foto de perfil actual que debe tener el formato assets/uploads/profile/nombreusuario_profile.png
        # Define la ruta requerida
        profile_picture_path = os.path.join("assets/uploads/profile", f"{current_user['username']}_profile.png")
        # Si la ruta existe
        if os.path.exists(profile_picture_path):
            # Define la misma ruta sin "assets" puesto que en main.py ya se tiene que el directorio de imágenes es assets
            profile_picture_path = os.path.join("uploads/profile", f"{current_user['username']}_profile.png")

        # Si no existe la ruta
        else:
            # Define que la ruta de la imagen será una imagen por defecto, no se pone "assets" al principio
            # puesto que en main.py ya se tiene que el directorio de imágenes es "assets"
            profile_picture_path = os.path.join("uploads/profile", "Foto_usuario_defecto.jpg")

        #Foto de perfil
        profile_picture = ft.Image(
            # Selecciona la ruta de la imagen del perfil con propiedades como ancho, largo y un borde circular
            src=profile_picture_path,
            width=200,
            height=200,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(100),
        )

        # Muestra los datos del usuario en campos accediendo a la variable curren_user que se obtuvo con la función get_current_user
        email_field = ft.TextField(label="Correo Electrónico", value=current_user["email"], width=300, read_only=True)
        username_field = ft.TextField(label="Nombre de Usuario", value=current_user["username"], width=300, read_only=True)
        names_field = ft.TextField(label="Nombres", value=current_user["names"], width=300, read_only=True)
        lastnames_field = ft.TextField(label="Apellidos", value=current_user["lastnames"], width=300, read_only=True)        
        old_password_field = ft.TextField(label="Contraseña Antigua", width=300, password=True)
        new_password_field = ft.TextField(label="Contraseña Nueva", width=300, password=True)
        
        # Contenido de la página
        content = [
            # Contenedor horizontal tipo Row
            ft.Row([
                # Contenedor vertical tipo Column dentro de Row
                ft.Column([
                    # Foto de perfil definida anteriormente
                    profile_picture,
                    # Boton para cambiar foto de perfil que llama la variable file_picker para elegir una foto
                    ft.ElevatedButton("Cambiar foto de perfil", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                    # Linea para dividir con los otros atributos
                    ft.Divider(),
                    # Texto con mis eventos creados
                    show_inscribed_events(),
                    ft.Text("Mis eventos creados", size=20, weight=ft.FontWeight.BOLD),
                    # Eventos creados definido anteriormente
                    user_events_column,                     
                ], 
                # Alineamiento de contenedor vertical tipo Colum
                alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.VerticalDivider(width=100),   
                # Segundo contenedor vertical tipo Column dentro de Row           
                ft.Column(
                    # Contenido del contenedor
                    controls=[
                        # Texto mi perfil
                        ft.Text("Mi perfil", size=30, text_align="center", weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                        # Campos con información del usuario
                        email_field,
                        username_field,
                        names_field,
                        lastnames_field,
                        ft.Text("Cambiar contraseña"),
                        old_password_field,
                        new_password_field,
                        #Boton para cambiar contraseña llama a la función handle_password_change
                        ft.ElevatedButton("Cambiar Contraseña", on_click=handle_password_change),                                            
                    ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START),
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START   
            )
        ]

    # Pagina de inicio    
    elif page_name == "home":
        
        # Llama la gunción get_current_user de content.py para obtener el usuario actual logeado
        user=get_current_user()

        # Titulo de la página para usuarios NO registrados
        title = ft.Text(
            "     Únete a la Mejor Comunidad\nDeportiva en Linea",
            text_align="center",
            size = 40,
            weight = ft.FontWeight.W_900,
            color = ft.colors.BLACK
        )

        # Titulo de la página para usuarios REGISTRADOS 
        title2 = ft.Text(
            "Bienvenido de nuevo!",
            text_align="center",
            size = 40,
            weight = ft.FontWeight.W_900,
            color = ft.colors.BLACK
        )
        
        # Texto de pequeña información bajo los titulos para usuarios NO REGISTRADOS
        descriptions = ft.Text( 
            "Participa en Eventos Deportivos cerca de ti🏅📅\nObserva resultados y gráficos en tiempo real📊⏱️\nGana increíbles recompensas por convertirte en ganador🏆🎉",
            text_align="center",
            size=25
            
        )        
        
        # Texto de pequeña información bajo lso titulos para usuario registrados
        descriptions2 = ft.Text( 
            "Proximamente Inicio mejorado para usuarios registrados",
            text_align="center",
            size=25
            
        )   

        # Boton para registrarse
        register_button = ft.ElevatedButton(
            content=ft.Container( 
                ft.Text(value="Registrarme", size=23)                
            ),          
            width=200,
            height=70,
            bgcolor="blue",
            color="white",          
            # Navega a pagina registrarme llamando la función navigate_to_page
            on_click=lambda e: navigate_to_page(page, "register")
        )

        # Definir el logo tipo ft.Image con la ruta en la que está ubicado
        logo=ft.Image(src="LogoSportexCompleto.PNG", width=450, height=450)
        
        # Si hay un usuario activo o registrado, la página tendrá el siguiente contenido
        if user:
            content=[
                ft.Row(
                    [
                        ft.Column(
                            [
                                # Titulo y descripción para usuario activo o registrado
                                title2,                           
                                descriptions2,                                                                               
                            ],
                            spacing=40,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(width=20),
                        #Logo de la página
                        ft.Container(logo, alignment=ft.alignment.center_right)                    
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY            
                )
            ]
        # Si NO hay un usuario registrado, la página tendrá el siguiente contenido    
        else:
                        content=[
                ft.Row(
                    [
                        ft.Column(
                            [
                                # Titulo, descripción y botón de registrarse para USUARIOS NO REGISTRADOS
                                title,                           
                                descriptions,
                                ft.Container(
                                    content=register_button,
                                    alignment=ft.alignment.center,
                                    width=620                                       
                                )                                                    
                            ],
                            spacing=40,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(width=20),
                        ft.Container(logo, alignment=ft.alignment.center_right)                    
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY            
                )
            ]
    
    # Pagina de eventos
    elif page_name == "events":
        
        # Llama a la función load_events de events.py para obtener los eventos actuales como un dataframe
        events = load_events()
        # Llama a la función get_current_user de content.py para obtener el usuario acutal
        current_user = get_current_user()

        # Función para crear carta de evento
        def create_event_card(event):
            """
            Crea una tarjeta de evento interactiva.

            Args:
                event (dict): Diccionario con la información del evento.

            Returns:
                ft.GestureDetector: Retorna una tarjeta que reacciona al hacer clic sobre ella.
            """    
            # Establecer color del texto del estado del evento
            if event['estado'] == "Abierto":
                status_color = ft.colors.GREEN_900
            else:
                status_color = 'red'
            
            # Crear el contenido de la tarjeta
            card_content = [
                ft.Image(src=event['logo'], width=200, height=200, fit=ft.ImageFit.COVER),
                ft.Container(
                    content=ft.Text(event['nombre'], size=14, weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(top=5, bottom=5),
                ),
                ft.Text(f"{event['fecha']} - {event['hora']}", size=12),
                ft.Text(f"Estado: {event['estado']}", size=13, color=status_color, weight=ft.FontWeight.BOLD),
                ft.Text(f"Inscritos: {event['inscritos']}", size=13, color=status_color)
            ]

            # Agregar la distancia si está disponible
            if 'distance' in event:
                distance_km = event['distance'] / 1000  # Convertir metros a kilómetros
                card_content.append(ft.Text(f"Distancia: {distance_km:.2f} km", size=12))

            # Agregar la descripción
            card_content.append(
                ft.Container(
                    content=ft.Text(
                        event['descripcion'],
                        size=12,
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    margin=ft.margin.only(top=5),
                    expand=True,
                )
            )

            # Crear y retornar el GestureDetector con la tarjeta
            return ft.GestureDetector(
                on_tap=lambda _: show_event_details(event),
                content=ft.Card(
                    content=ft.Container(
                        bgcolor=ft.colors.BLUE_200,
                        border=ft.border.all(2, ft.colors.BLACK),
                        padding=5,
                        content=ft.Column(card_content, spacing=2),
                        width=200,
                        height=280  # Aumentado para acomodar la línea de distancia
                    ),
                )
            )

        # Función para mostrar detalles de un evento
        def show_event_details(event):
            """
            Función para mostrar detalles de un evento.

            Args:
                event (dic): recibe el diccionario de un evento
            Returns:
                None              
            """  
            # Función para cerrar el dialogo generado al abrir un evento           
            def close_dialog(_):
                dialog.open = False
                page.update()

            # Función para el manejo de la inscripción desde la página de eventos
            def toggle_inscription(_):
                """
                
                Args:
                    None, es llamado al dar click en un botón que la invoca

                Returns:
                    No retorna ningun valor, solo actualiza la interfaz
                    
                """
                # Obtiene usuario logeado
                current_user = get_current_user()
                # Si hay un usuario logeado
                if current_user:
                    # Obtiene el nombre de usuario
                    username = current_user['username']
                    # Si el usuario está dentro de los usuarios inscritos de un evento
                    if username in event['usuarios_inscritos']:
                        # Llama la funcion uniscribe_user de events.py para desinscribir un usuario
                        if uninscribe_user(event['id'], username):
                            # Cambia el texto del botón de Desinscribirme a Inscribirme
                            inscription_button.text = "Inscribirme"
                            # Disminuye eventos en 1
                            event['inscritos'] -= 1     
                    # Si el usuario no está dentro de los usuarios inscritos de un evento                               
                    else:
                        # Llama la función inscribe_user de events.py para inscribir un usuario
                        if inscribe_user(event['id'], username):
                            # Cambia el texto del botón de desinscribirme a Inscribirme
                            inscription_button.text = "Desinscribirme"
                            # Aumenta los inscritos en 1
                            event['inscritos'] += 1

                    # Si los inscritos son mayor igual a la capacidad de un evento
                    if event['inscritos'] >= event['capacidad']:
                        # El estado del evento se pone en curso
                        event['estado'] = "En curso"
                        # Desactiva el botón de inscribirse
                        inscription_button.disabled = True
                    # Si el estado del evento está en curso y los inscritos son menores a la capacidad    
                    elif event['estado'] == "En curso" and event['inscritos'] < event['capacidad']:
                        # Pasa a estado abierto
                        event['estado'] = "Abierto"
                        # Activa el botón para inscribirse
                        inscription_button.disabled = False

                    # Texto que compara los inscritos respecto a la capacidad total
                    inscribed_text.value = f"Inscritos: {event['inscritos']}/{event['capacidad']}"

                    # Cierra la ventana emergente
                    close_dialog(_)
                    # Actualiza la página eventos para visualizar los cambios
                    navigate_to_page(page, "events")
                     
            # Obtiene el usuario actual
            current_user = get_current_user()

            # Si hay un usuario activo
            if current_user:
                # Si el usuario está dentro de los usuarios inscritos de un evento
                if current_user['username'] in event['usuarios_inscritos']:
                    # Crea el botón desinscribirme que al dar click llama la función toggle_inscription y se activa
                    inscription_button_text = "Desinscribirme"
                    inscription_button = ft.ElevatedButton(
                        text = inscription_button_text,
                        on_click=toggle_inscription,
                        disabled=False
                    )
                # Si el usuario NO está dentro de los usuarios inscritos de un evento    
                else:
                    # Crea el botón Inscribirme que al dar click llama la función toggle_inscription 
                    inscription_button_text = "Inscribirme"
                    inscription_button = ft.ElevatedButton(
                        text= inscription_button_text,
                        on_click = toggle_inscription,
                        # Se desactiva el botón en caso de que el estado sea diferente a abierto o los inscritos superen la capacidad
                        disabled=(event['estado'] != "Abierto" or event['inscritos'] >= event['capacidad'])
                    )
            # SI no hay un usuario activo        
            else:
                # Texto que indica que debe iniciar sesión para inscribirse
                inscription_button = ft.Text("Inicia sesión para inscribirte", color='blue', weight=ft.FontWeight.BOLD)

            # Texto para mostrar el numero de inscritos
            inscribed_text = ft.Text(f"Inscritos: {event['inscritos']}/{event['capacidad']}")

            # Crear el dialogo que se genera al abrir un evento tipo ft.AlerDialog
            dialog = ft.AlertDialog(
                # Contiene, titulo, logo y más detalles del evento
                title=ft.Text(event['nombre']),
                content=ft.Column([
                    ft.Row([
                        ft.Image(src=event['logo'], width=300, height=300, fit=ft.ImageFit.COVER),
                        ft.Column([
                            ft.Text(f"Organizador: {event['organizador']}"),
                            ft.Text(f"Fecha: {event['fecha']}"),
                            ft.Text(f"Hora: {event['hora']}"),
                            ft.Text(f"Lugar: {event['lugar']}"),
                            ft.Text(f"Ciudad: {event['ciudad']}"),
                            ft.Text(f"Estado: {event['estado']}"),
                            inscribed_text,                             
                        ]),
                    ]),                  
                    ft.Text("Detalles:",size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Descripción: {event['descripcion']}"),
                    ft.Text(f"Tipo de deporte: {event['tipo_deporte']}"),
                    ft.Text(f"Modalidad de participación: {event['modalidad_participacion']}"),
                    ft.Text(f"Capacidad: {event['capacidad']}"),                    
                    ft.Text(f"Costo de inscripción: {event['costo_inscripcion']}"),
                    # Boton para redirigir a la ubicación de google maps                    
                    ft.TextButton(f"Ver ubicación en Google Maps", on_click=lambda _: page.launch_url(f"https://www.google.com/maps?q={event['latitud']},{event['longitud']}")),
                    inscription_button,
                    
                ], scroll=ft.ScrollMode.AUTO, height=400), #Habilita el scroll
                actions=[
                    # Boton cerrar que llama la función close_dialog que cierra el ft.AlertDialog
                    ft.TextButton("Cerrar", on_click=close_dialog),
                ],
            )
            # Abre el ft.AlertDialog
            page.dialog = dialog
            dialog.open = True
            # Actualiza la página
            page.update()

        # Crear GeoDataFrame con los eventos
        gdf = gpd.GeoDataFrame(
            events,
            geometry=gpd.points_from_xy(events.longitud, events.latitud),
            crs="EPSG:4326"
        )
        
        # Función para aplicar los filtros
        def apply_filters(e):
            '''
            Aplica los filtros seleccionados a los eventos.

            Args:
                e: Evento de cambio
            '''

            # Crea una copia del Dataframe original
            filtered_gdf = gdf.copy()    
            # Crear una lista para almacenar todas las condiciones de filtro
            filter_conditions = []

            # Si se selecciona una ciudad se filtra para que solo tenga los registros correspondientes a esa ciudad y se añada a la lista
            if city_dropdown.value:
                filter_conditions.append(filtered_gdf['ciudad'] == city_dropdown.value)
            
            # Si hay un tipo de deporte se filtra para que solo contenga los registros del tipo de deporte especificado y se añada a la lista
            if sport_dropdown.value:
                filter_conditions.append(filtered_gdf['tipo_deporte'] == sport_dropdown.value)
            
            # Si el interruptor está activado, se filtra para incluir solo los eventos que tengan estado abierto y se añada a la lista
            if open_only_switch.value:
                filter_conditions.append(filtered_gdf['estado'] == 'Abierto')
            
            # Si el interruptor está activado, se filtra para incluir solo los eventos que tengan inscripción gratis y se añada a la lista
            if free_only_switch.value:
                filter_conditions.append(filtered_gdf['costo_inscripcion'] == 'Gratis')
            
            # Si se selecciona una modalidad de participación , filtra para incluir solo las entradas con esa modalidad y se añada a la lista
            if modality_dropdown.value:
                filter_conditions.append(filtered_gdf['modalidad_participacion'] == modality_dropdown.value)

            # Aplicar de una vez todos los filtros
            if filter_conditions:
                filtered_gdf = filtered_gdf.loc[np.logical_and.reduce(filter_conditions)]

            # Si el usuario proporcionó ubicación válida (latitud y longitud obtenidas)
            if user_latitude.value and user_longitude.value and distance_slider.value > 0:
                # Crear punto con latitud y longitud del usuario
                user_location = Point(float(user_longitude.value), float(user_latitude.value))
                # Crea un GeoDataFrame con la ubicación del usuario y establece el sistema de coordenadas
                user_gdf = gpd.GeoDataFrame(geometry=[user_location], crs="EPSG:4326")          

                # Determinar una proyección UTM adecuada basada en la ubicación del usuario
                utm_crs = CRS.from_proj4(f"+proj=utm +zone={int((float(user_longitude.value) + 180) / 6) + 1} +datum=WGS84 +units=m +no_defs")
                
                # Proyectar tanto la ubicación del usuario como los eventos a la proyección UTM
                user_gdf_projected = user_gdf.to_crs(utm_crs)
                filtered_gdf_projected = filtered_gdf.to_crs(utm_crs)

                # Calcular distancias en metros
                filtered_gdf_projected['distance'] = filtered_gdf_projected.geometry.distance(user_gdf_projected.iloc[0].geometry)

                # Filtrar por distancia (convertir km a metros)
                if distance_slider.value:
                    max_distance = distance_slider.value * 1000  # km to meters
                    filtered_gdf = filtered_gdf_projected[filtered_gdf_projected['distance'] <= max_distance].to_crs("EPSG:4326")                
            else:
                # Si no hay ubicación del usuario, asignar distancia infinita
                filtered_gdf['distance'] = float('inf')

            # Llama la función update_event_grid para actualizar la cuadrícula con los eventos filtrados    
            update_event_grid(filtered_gdf)

        # Función para limpiar filtros
        def clear_filters(e):
            '''
            Limpia todos los filtros aplicados

            Args:
                e: Evento de click
            '''

            # Limpia los valores actuales y los actualiza
            city_dropdown.value = None
            sport_dropdown.value = None
            open_only_switch.value = False
            free_only_switch.value = False
            modality_dropdown.value = None
            distance_slider.value = 0

            city_dropdown.update()
            sport_dropdown.update()
            open_only_switch.update()
            free_only_switch.update()
            modality_dropdown.update()
            distance_slider.update()

            # LLama la función apply_filters para aplicar filtros limmpios
            apply_filters(None)

        # Función para obtener la ubicación del usuario
        def get_location(e):
            '''
            Obtiene la ubicación del usuario basada en el pais, departamento, ciudad y barrio ingresados.

            Args:
                e: Evento de click
            '''
            # Utiliza la librería Nominatim y busca pais, departamento, ciudad y barrio
            geolocator = Nominatim(user_agent="myGeocoder")
            address = f"{neighborhood_user.value}, {city_user.value}, {state_user.value}, {country_user.value}"
            
            # Obtiene latitud y longitud
            location = geolocator.geocode(address)
            # Si se obtiene una latitud y longitud
            if location:
                # Guarda latitud y longitud como valor de los campos user_latitude y user_longitude definidos
                user_latitude.value = location.latitude
                user_longitude.value = location.longitude
                # valor que tiene Ubicación general que incluye ciudad y pais
                user_location.value = f"Ubicación: {city_user.value}, {country_user.value}."
                # Activa el slider de distancias
                distance_slider.disabled = False
            
            # SI no se obtiene latitud y longitud
            else:
                # Guarda valores vacíos               
                user_latitude.value = ""
                user_longitude.value = ""                
                user_location.value = "Ubicación: No definida"
                # Desactiva el slider de distancias
                distance_slider.disabled = True
            
            # Actualizar pagina
            apply_filters(None)
            page.update()

        # Controles de filtrado que llaman la funcion apply filters al seleccionar un valor de la lista desplegable
        city_dropdown = ft.Dropdown(
            label="Ciudad",
            options=[ft.dropdown.Option(city) for city in gdf['ciudad'].unique()],
            on_change=apply_filters
        )

        sport_dropdown = ft.Dropdown(
            label="Deporte",
            options=[ft.dropdown.Option(sport) for sport in gdf['tipo_deporte'].unique()],
            on_change=apply_filters
        )

        open_only_switch = ft.Switch(label="Solo abiertos", on_change=apply_filters)
        free_only_switch = ft.Switch(label="Solo gratis", on_change=apply_filters)

        modality_dropdown = ft.Dropdown(
            label="Modalidad",
            options=[ft.dropdown.Option(modality) for modality in gdf['modalidad_participacion'].unique()],
            on_change=apply_filters
        )

        clear_filters_button = ft.ElevatedButton(
            text="Borrar filtros",
            on_click=clear_filters
        )

        # Slider de distancia
        distance_slider = ft.Slider(
            min=0,
            max=100,
            divisions=10,
            label="{value} km",
            value=0,
            disabled=True,
            on_change=apply_filters
        )

        # Campos de ubicación que debe llenar el usuario
        country_user = ft.TextField(label="País", width=200)
        state_user = ft.TextField(label="Departamento/Estado", width=200)
        city_user = ft.TextField(label="Ciudad", width=200)
        neighborhood_user = ft.TextField(label="Barrio", width=200)
        # Se inicializa la longitud y la latiud del usuario como vacío
        user_latitude = ft.TextField(label="", read_only=True)
        user_longitude = ft.TextField(label="", read_only=True)
        user_location = ft.TextField(label="Tu ubicación", read_only=True)
        # Botón que llama la función get location para guardar la ubicación
        user_location_button = ft.ElevatedButton("Usar esta ubicación", on_click=get_location)

        # Crea un ft.GridView (Cuadricula)
        event_grid = ft.GridView(
            # Se expande para ocupar todo el espacio disponible
            expand=1,
            # Columnas de la cuadricula
            runs_count=5,
            # Tamaño máximo de cada elemento de la cuadricula
            max_extent=200,
            # Controla la relació nde aspecto (ancho/alto) de cada elemento de la cuadricula
            child_aspect_ratio=0.55,
            # Espaciado entre cada elemento de la cuadricula  
            spacing=10,
            # Espaciado vertical 
            run_spacing=10,
        )

        def update_event_grid(filtered_gdf):
            '''
            Actualiza la cuadrícula de eventos con los eventos filtrados.

            Args:
                filtered_gdf (GeoDataFrame): GeoDataFrame de eventos filtrados
            '''
            # limpiar todos los eventos de la cuadrícula
            event_grid.controls.clear()
            # Para cada evento con los filtros seleccionados crea una carta de evento
            for _, event in filtered_gdf.iterrows():
                event_dict = event.to_dict()
                if 'distance' in event_dict:
                    event_dict['distance'] = event_dict['distance']
                event_grid.controls.append(create_event_card(event_dict))
            #Actualizar la pagina
            page.update()
       
        # Llama la función get_current_user de content.py para obtener el usuario actual
        current_user=get_current_user()
        # Si hay un usuario activo podrá crear un evento
        if current_user:
            # Boton para crear evento
            create_event_button = ft.ElevatedButton(
                text="Crear Evento",
                width=130,
                height=50,
                bgcolor="blue",
                color="white",
                # Navega a pagina create_event por medio de la función navigate_to_page
                on_click=lambda e: navigate_to_page(page, "create_event") 
        )
            # Contenido si hay un usuario activo
            content = [                             
                ft.Text("Filtros", size=20, weight=ft.FontWeight.BOLD),   
                # Filtros             
                ft.Row([city_dropdown, sport_dropdown, modality_dropdown]),
                ft.Row([open_only_switch, free_only_switch, clear_filters_button]),
                ft.Text("Busca eventos cercanos a ti: Ingresa tus datos.", size=20, weight=ft.FontWeight.BOLD),                
                ft.Row([country_user, state_user, city_user, neighborhood_user, user_location_button]),
                ft.Row([user_location]),
                ft.Row([ft.Text("Distancia máxima:"), distance_slider, ft.Text("Ingresa tu ubicación para habilitar")]),
                # Boton crear evento
                ft.Row([ft.Text("Eventos", size=30, weight=ft.FontWeight.BOLD),create_event_button]),
                # Cuadricula de eventos
                event_grid,
            ]
        
        # Si no hay un usuario activo
        else:
            # El contenido será unicamente la cuadrícula
            content = [                
                ft.Text("Filtros", size=20, weight=ft.FontWeight.BOLD),
                # Filtros
                ft.Row([city_dropdown, sport_dropdown, modality_dropdown]),
                ft.Row([open_only_switch, free_only_switch, clear_filters_button]),
                ft.Text("Eventos", size=30, weight=ft.FontWeight.BOLD),                              
                event_grid
            ]

        # Inicializa la página de eventos sin filtros
        apply_filters(None)

    # Pagina de crear eventos
    elif page_name == "create_event":

        # Función para mostrar información sobre como obtener la latitud y la longitud
        def show_help_latlong(_):
            """
            Muestra información sobre como obtener latitud y longitud en un objeto 'AlertDialog'.

            Args:
                Se llama al momento de clickear el botón "¿Cómo saber latitud y longitud?"
            
            Returns:
                None
            """            

            # Crea objeto alertdialog
            dialog = ft.AlertDialog(
                modal = True,
                # Titulo
                title = ft.Text("¿Cómo saber latitud y longitud?"),
                # Contenido
                content = ft.Container(
                    width=600,
                    height=700,
                    content=ft.Column(
                        [   ft.Text("1. En tu teléfono o Computador, abre la aplicación Google Maps.\n2. Clickea o Mantén pulsada un área del mapa que no esté etiquetada para colocar ahí un marcador rojo.\n3. Verás las coordenadas en el cuadro de búsqueda.",
                                    size=14),
                            # Imagen de ejemplo
                            ft.Image(src="uploads/events/Ayuda_latitud_longitud.jpg", width=900,height=400, fit=ft.ImageFit.CONTAIN),
                            ft.Text("En la imagen podrá visualizar la latitud y la longitud separadas por coma.\nEn este caso\nLatitud: 6.261306\nLongitud: -75.575243",
                                    size=14)],
                                    # Alineamiento al comienzo (izquierda)
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment= ft.CrossAxisAlignment.START,
                                    # Permitir scroll
                                    scroll="auto",
                                    spacing=3)            
                ),
                actions=[
                    # Boton cerrar que al clickear llama la función close_dialog
                    ft.TextButton("Cerrar", on_click=lambda _: close_dialog(dialog))
                ]
            )
            page.dialog = dialog
            # Abre el dialog
            dialog.open = True
            page.update()          

        # Funcion para cerrar el objeto dialog que genera show_help_latlong
        def close_dialog(dialog):
            """
            Cierra el objeto dialog al clickear en el botón Cerrar
            """
            dialog.open= False
            page.update()


        # Llama a la función load_events de events.py para cargar los eventos actuales como un dataframe      
        events = load_events()
        # Llama la función get_current_user para obtener el usuario actual
        current_user = get_current_user()

        # Obtener el próximo ID disponible de los eventos creados ej: si hay eventos con id 1,2,3 se creará el 4
        next_id = max(events['id']) + 1 if len(events) > 0 else 1

        # Formulario para crear evento
        # Campo Nombre
        name_field = ft.TextField(label="Nombre del evento", width=300)
        # Lista con deportes a elegir
        sport_types = ["Fútbol", "Baloncesto", "Tenis", "Voleibol", "Natación", "Atletismo", "Otro"]
        # Lista desplegable para elegir un deporte entre la lista
        sport_type_dropdown = ft.Dropdown(
            label="Tipo de deporte",
            width=300,
            options=[ft.dropdown.Option(sport) for sport in sport_types]
        )
        # Campos con fecha, hora, lugar, ciudad, descripción        
        date_field = ft.TextField(label="Fecha (YYYY-MM-DD)", width=300)
        time_field = ft.TextField(label="Hora (HH:MM)", width=300)
        place_field = ft.TextField(label="Lugar", width=300)
        city_field = ft.TextField(label="Ciudad", width=300)
        description_field = ft.TextField(label="Descripción", width=300, multiline=True, max_lines=5)
        # Lista desplegable para elegir la modalidad de participación (Individual o en Equipos)
        participation_mode = ft.Dropdown(
            label="Modalidad de participación",
            width=300,
            options=[
                ft.dropdown.Option("Individual"),
                ft.dropdown.Option("Equipos")
            ]
        )
        # Campo de capacidad del evento
        capacity_field = ft.TextField(label="Capacidad", width=300)
        # Lista desplegable para elegir el costo de inscripción (Gratis o pago)
        registration_fee_field = ft.Dropdown(
            label="Costo de inscripción",
            width = 300,
            options=[
                ft.dropdown.Option("Gratis"),
                ft.dropdown.Option("Pago")
            ]
        )
        # Lista desplegable para elegir el estado del evento (Al estar recién creado solo sale opción Abierto)
        status_field = ft.Dropdown(
            label="Estado",
            width = 300,
            options=[
                ft.dropdown.Option("Abierto"),
            ]
        )

        # Campos de latitud y longitud
        latitude_field = ft.TextField(label="Latitud", width=300)
        longitude_field = ft.TextField(label="Longitud", width=300)

        # Boton para leer ayuda sobre cómo obtener la latitud y la longitud
        help_latlong_button = ft.TextButton("¿Cómo saber latitud y longitud?")
        help_latlong_button.on_click = show_help_latlong

        # Definir logo actual del evento como ninguno        
        logo_file_path = None

        # Función para cambiar el logo del evento    
        def handle_logo_change(e: ft.FilePickerResultEvent):
            """
            Función para cambiar el logo del evento.

            Args:
                FilePicker: La función es llamada al seleccionar un filepicker para subir imagenes
            Returns:
                None              
            """             
            nonlocal logo_file_path

            # Si la cantidad de imagenes es 0, hace return
            if not e.files or len(e.files) == 0:
                return
            
            # Divide la ruta en path y nombre
            file_path = e.files[0].path
            file_name = e.files[0].name     

            # Formatos validos de imágenes
            valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".jfif", ".avif"]
            # Obtiene formato del logo subido
            file_extension = os.path.splitext(file_name)[1].lower()

            # Si el formato del logo no está en la lista de formatos admitidos
            if file_extension not in valid_extensions:
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de que la imagen no es de formato válido
                    content=ft.Text("El archivo seleccionado no es una imagen válida", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return
            
            # Tratar de abrir la ruta como una imagen
            try:
                with PILImage.open(file_path) as img:   
                    # Guardar ruta del archivo                 
                    logo_file_path = file_path                    
                    page.show_snack_bar(ft.SnackBar(
                        # Aviso de que el logo se subió correctamente
                        content=ft.Text("Logo subido exitosamente", size=20, color="white"),
                        bgcolor="lightgreen",
                        duration=3000 
                    ))
            except Exception as e:
                page.show_snack_bar(ft.SnackBar(
                    # Aviso  de que no se pudo procesar imagen
                    content=ft.Text(f"Error al procesar la imagen: {str(e)}", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))

        # File picker para seleccionar una imagen que llama la función handle_logo_change
        file_picker = ft.FilePicker(on_result=handle_logo_change)
        page.overlay.append(file_picker)

        # Boton de subir logo que llama al file picker definido anteriormente
        logo_button = ft.ElevatedButton("Subir logo", on_click=lambda _: file_picker.pick_files(allow_multiple=False))

        # Función para crear evento
        def create_event(e):
            nonlocal logo_file_path
            # Validar campos llenados por el usuario
            if not all([name_field.value, sport_type_dropdown.value, date_field.value, time_field.value, 
                        place_field.value, city_field.value, description_field.value, participation_mode.value,
                        capacity_field.value, registration_fee_field.value, status_field.value,
                        latitude_field.value, longitude_field.value]):
                page.show_snack_bar(ft.SnackBar(
                    # Si no se ha llenado los campos en su totalidad, avisa que debe hacerlo
                    content=ft.Text("Por favor, complete todos los campos", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return

            try:
                # Intentar convertir el valor del campo a entero
                capacity_field.value = int(capacity_field.value)
                # Verificar si la capacidad es menor o igual a 0
                if capacity_field.value <= 0:
                    raise ValueError
            except ValueError as e:                
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de que la capacidad debe ser un número entero mayor a 0
                    content=ft.Text("La capacidad debe ser un número entero mayor a 0", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return

            try:
                # Intentar convertir el valor de latitud a float
                latitude_field.value = float(latitude_field.value)
                
                # Verificar que la latitud esté dentro del rango permitido
                if not (-90 <= latitude_field.value <= 90):
                    raise ValueError("La latitud debe estar entre -90 y 90")
                
                # Intentar convertir el valor de longitud a float
                longitude_field.value = float(longitude_field.value)
                
                # Verificar que la longitud esté dentro del rango permitido
                if not (-180 <= longitude_field.value <= 180):
                    raise ValueError("La longitud debe estar entre -180 y 180")
            
            except ValueError as e:
                # Mostrar un mensaje de error si ocurre una excepción
                error_message = str(e)
                if "could not convert string to float" in error_message:
                    error_message = "La latitud y la longitud deben ser números decimales."

                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text(error_message, size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))
                return                           

            # Guardar logo si existe un path al haber sido guardado, en caso contrario fue definido como None anteriormente
            if logo_file_path:
                # Llama la función save_event_logo de content.py que guarda ruta ej: assets\uploads\events\logos\event_1.png
                new_logo_path = save_event_logo(logo_file_path)
                
                # Si guarda el logo en assets
                if new_logo_path:
                    page.show_snack_bar(ft.SnackBar(
                        # Aviso de que se guardó el logo
                        content=ft.Text("Logo guardado con éxito.", size=20, color="white"),
                        bgcolor="lightgreen",
                        duration=3000 
                    ))
                # Si no se pudo guardar el logo
                else:
                    page.show_snack_bar(ft.SnackBar(
                        # Aviso de que hubo un error guardando el logo
                        content=ft.Text("Error al guardar logo del evento.", size=20, color="red"),
                        bgcolor="lightcoral",
                        duration=3000
                    ))
                    return
            # Si no se guardó un logo anteriormente, logo_file_path seria None    
            else:                
                # Guarda el logo del evento como una imagen default
                new_logo_path = "uploads/events/logos/evento_default.png"

            # Llama la función add_event de events.py para guardar un evento en el csv con los valores diligenciados por el usuario
            add_event(next_id, 
                        name_field.value, 
                        sport_type_dropdown.value,                         
                        date_field.value, 
                        time_field.value, 
                        place_field.value, 
                        city_field.value, 
                        latitude_field.value, 
                        longitude_field.value, 
                        description_field.value, 
                        participation_mode.value, 
                        int(capacity_field.value), 
                        current_user['username'], 
                        registration_fee_field.value, 
                        status_field.value,
                        new_logo_path)
            # Esperar 2 segundos
            time.sleep(2)
            page.show_snack_bar(ft.SnackBar(
                # Aviso de que el evento fue creado
                content=ft.Text("Evento creado exitosamente", size=20, color="white"),
                bgcolor="lightgreen",
                duration=3000 
            ))
            time.sleep(1)
            # Al terminar llama la función navigate_to_page para redirigir a la pagina "eventos"
            navigate_to_page(page, "events")    
        
        # Boton para crear evento que al ser clickeado llama la función create_event de events.py
        create_button = ft.ElevatedButton("Crear Evento", on_click=create_event)

        # Contenido de la página
        content = [
            # Campos que deben ser llenados por le usuario
            ft.Text("Crear Nuevo Evento", size=30, weight=ft.FontWeight.BOLD),
            name_field,
            sport_type_dropdown,
            date_field,
            time_field,
            place_field,
            city_field,
            description_field,
            participation_mode,
            capacity_field,
            registration_fee_field,
            status_field,
            help_latlong_button,
            latitude_field,
            longitude_field,
            logo_button,
            create_button
        ]                     

    # Pagina para modificar un evento según el ID guardado
    elif page_name == "modify_event":
        
        # Función para mostrar información sobre como obtener la latitud y la longitud
        def show_help_latlong(_):
            """
            Muestra información sobre como obtener latitud y longitud en un objeto 'AlertDialog'.

            Args:
                Se llama al momento de clickear el botón "¿Cómo saber latitud y longitud?"
            
            Returns:
                None
            """            

            # Crea objeto alertdialog
            dialog = ft.AlertDialog(
                modal = True,
                # Titulo
                title = ft.Text("¿Cómo saber latitud y longitud?"),
                # Contenido
                content = ft.Container(
                    width=600,
                    height=700,
                    content=ft.Column(
                        [   ft.Text("1. En tu teléfono o Computador, abre la aplicación Google Maps.\n2. Clickea o Mantén pulsada un área del mapa que no esté etiquetada para colocar ahí un marcador rojo.\n3. Verás las coordenadas en el cuadro de búsqueda.",
                                    size=14),
                            #Imagen de ejemplo
                            ft.Image(src="uploads/events/Ayuda_latitud_longitud.jpg", width=900,height=400, fit=ft.ImageFit.CONTAIN),
                            ft.Text("En la imagen podrá visualizar la latitud y la longitud separadas por coma.\nEn este caso\nLatitud: 6.261306\nLongitud: -75.575243",
                                    size=14)],
                                    # Alineamiento al comienzo
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment= ft.CrossAxisAlignment.START,
                                    # Permitir scroll
                                    scroll="auto",
                                    spacing=3)            
                ),
                actions=[
                    # Boton cerrar que al clickear llama la función close_dialog
                    ft.TextButton("Cerrar", on_click=lambda _: close_dialog(dialog))
                ]
            )
            page.dialog = dialog
            # Abre el dialog
            dialog.open = True
            page.update()          

        # Funcion para cerrar el objeto dialog que genera show_help_latlong
        def close_dialog(dialog):
            """
            Cierra el objeto dialog al clickear en el botón Cerrar
            """
            dialog.open= False
            page.update()

        # Llama la funcion  load_events de content.py para obtener la lista de eventos totales en un dataframe
        events = load_events()
        # Filtrar del dataframe para obtener el evento del id seleeccionado junto con todos sus valores 
        event = events[events['id'] == current_event].iloc[0]
        
        # Campos para ingresar valores del evento que además muestran el valor actual        
        name_field = ft.TextField(label="Nombre del evento", width=300, value=event['nombre'])
        # Deportes totales
        sport_types = ["Fútbol", "Baloncesto", "Tenis", "Voleibol", "Natación", "Atletismo", "Otro"]
        # Lista desplegable para elegir un deporte de lal ista
        sport_type_dropdown = ft.Dropdown(
            label="Tipo de deporte",
            width=300,
            options=[ft.dropdown.Option(sport) for sport in sport_types],
            value=event['tipo_deporte']
        )
        # Campos fecha, hora, lugar, ciudad, descripción        
        date_field = ft.TextField(label="Fecha (YYYY-MM-DD)", width=300, value=event['fecha'])
        time_field = ft.TextField(label="Hora (HH:MM)", width=300, value=event['hora'])
        place_field = ft.TextField(label="Lugar", width=300, value=event['lugar'])
        city_field = ft.TextField(label="Ciudad", width=300, value=event['ciudad'])
        description_field = ft.TextField(label="Descripción", width=300, multiline=True, max_lines=5, value=event['descripcion'])
        # Lista desplegable para elegir la modalidad de participación (Individual o en Equipos)
        participation_mode = ft.Dropdown(
            label="Modalidad de participación",
            width=300,
            options=[
                ft.dropdown.Option("Individual"),
                ft.dropdown.Option("Equipos")
            ],
            value=event['modalidad_participacion']
        )
        # Campo Capacidad del evento
        capacity_field = ft.TextField(label="Capacidad", width=300, value=int(event['capacidad']))
        # Lista desplegable para elegir el costo de la inscripción (Gratis o Pago)
        registration_fee_field = ft.Dropdown(
            label="Costo de inscripción",
            width=300,
            options=[
                ft.dropdown.Option("Gratis"),
                ft.dropdown.Option("Pago")
            ],
            value=event['costo_inscripcion']
        )
        # Lista desplegable para elegir el estado del evento deportivo (Abierto, en curso, finalizado)
        status_field = ft.Dropdown(
            label="Estado",
            width=300,
            options=[
                ft.dropdown.Option("Abierto"),
                ft.dropdown.Option("En curso"),
                ft.dropdown.Option("Finalizado"),
            ],
            value=event['estado']
        )        

        # Boton para leer ayuda sobre cómo obtener la latitud y la longitud
        help_latlong_button = ft.TextButton("¿Cómo saber latitud y longitud?")
        help_latlong_button.on_click = show_help_latlong


        # Campos Latitud y longitud
        latitude_field = ft.TextField(label="Latitud", width=300, value=event['latitud'])
        longitude_field = ft.TextField(label="Longitud", width=300, value=event['longitud'])

        # Logo actual
        current_logo = ft.Image(src=event['logo'], width=100, height=100)

        # Función para actualizar el logo
        def handle_logo_change(e: ft.FilePickerResultEvent):
            """
            Función para actualizar el logo del evento.

            Args:
                FilePicker: La función es llamada al seleccionar un filepicker para subir imagenes
            Returns:
                None              
            """   
            nonlocal current_logo

            # Si la cantidad de imagenes es 0, hace return
            if not e.files or len(e.files) == 0:
                return
            
            # Divide la ruta en path y nombre
            file_path = e.files[0].path
            file_name = e.files[0].name

            # Formatos válidos de imagenes
            valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".jfif", ".avif"]
            # Obtiene el formato del logo subido
            file_extension = os.path.splitext(file_name)[1].lower()

            # Si el formato del logo no está en la lista de formatos admitidos
            if file_extension not in valid_extensions:
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("El archivo seleccionado no es una imagen válida", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return
            
            # Tratar de abrir la ruta como imagen
            try:
                with PILImage.open(file_path) as img:
                    # Guardar ruta local del archivo en la variable current logo
                    current_logo = file_path
                    page.update()                    
                    page.show_snack_bar(ft.SnackBar(
                        # Aviso que se actualizó
                        content=ft.Text("Logo actualizado", size=20, color="white"),
                        bgcolor="lightgreen",
                        duration=3000 
                    ))                    
            except Exception as e:
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de error al procesar
                    content=ft.Text(f"Error al procesar la imagen: {str(e)}", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))

        # File picker para seleccionar una imagen que llama la función  handle_logo_change
        file_picker = ft.FilePicker(on_result=handle_logo_change)
        page.overlay.append(file_picker)

        # Boton de cambiar logo que llama al file picker definido anteriormente
        logo_button = ft.ElevatedButton("Cambiar logo", on_click=lambda _: file_picker.pick_files(allow_multiple=False))

        # Funcion para guardar el logotipo del evento
        def update_event_logo(file_path):
            """
            guarda el logotipo actualizado de un evento

            Args:
                file_path (str): Ruta del archivo de imagen del logotipo del evento.
            
            Returns:
                str | None: Devuelve la ruta relativa desde la carpeta 'uploads' donde se guardó el
                logotipo si el proceso fue exitoso, o `None` en caso de error.
            """
            # Llama la funcion  load_events para obtener la lista de eventos totales en un dataframe
            events = load_events()
            # Filtrar del dataframe para obtener todos los valores del id del evento seleccionado
            event = events[events['id'] == current_event].iloc[0]

            # Obtener el nombre del archivo existente            
            existing_logo_path = event['logo']
            existing_logo_name = os.path.basename(existing_logo_path)
            
            # Definir carpeta destino
            destination_folder = "assets/uploads/events/logos"

            # Comprobar si el logo actual es el de evento por default
            if existing_logo_name == "evento_default.png":
                # Si es el logo por defecto, genera un nuevo archivo de imagen con el id correspondiente
                new_file_name = f"event_{event['id']}.png"
                destination_path = os.path.join(destination_folder, new_file_name)

            else:
                # Si no es el logo por defecto, guarda el nuevo logo en la misma ruta para sobreescribirlo conservando el mismo nombre
                destination_path = os.path.join(destination_folder, existing_logo_name)

            # Intentar guardar el logo
            try:
                # Abrir la imagen seleccionada
                with PILImage.open(file_path) as img:
                    # Guardar la imagen en formato PNG
                    img.save(destination_path, format='PNG')

                # Ruta base que se quitará de la ruta completa
                base_path = "assets"
                # Obtener ruta relativa desde la carpeta 'uploads' removiendo la carpeta base
                relative_path = os.path.relpath(destination_path, base_path)
                # Retorna la ruta relativa desde la carpeta 'uploads"
                return relative_path
            
            # Si no se pudo guardar el logo
            except Exception as e:
                print(f"Error al guardar logo de evento: {e}")
                return None     
            
        # Función para actualizar un evento
        def update_event(e):
            """
            Actualiza el evento en el csv

            Args:
                e (EventCallable): Se llama al clickear en el botón guardar cambios
            
            Returns:
                None            
            """            
            nonlocal current_logo
            # Validar campos llenados por el usuario
            if not all([name_field.value, sport_type_dropdown.value, date_field.value, time_field.value, 
                        place_field.value, city_field.value, description_field.value, participation_mode.value,
                        capacity_field.value, registration_fee_field.value, status_field.value, latitude_field.value,
                        longitude_field.value]):
                page.show_snack_bar(ft.SnackBar(
                    # Si no se ha llenado los campos en su totalidad, avisa que debe hacerlo
                    content=ft.Text("Por favor, complete todos los campos", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return

            try:
                # Intentar convertir el valor del campo a entero
                capacity_field.value = int(capacity_field.value)
                # Verificar si la capacidad es menor o igual a 0
                if capacity_field.value <= 0:
                    raise ValueError
            except ValueError as e:                
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de que la capacidad debe ser un número entero mayor a 0
                    content=ft.Text("La capacidad debe ser un número entero mayor a 0", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return
            
            try:
                # Intentar convertir el valor de latitud a float
                latitude_field.value = float(latitude_field.value)
                
                # Verificar que la latitud esté dentro del rango permitido
                if not (-90 <= latitude_field.value <= 90):
                    raise ValueError("La latitud debe estar entre -90 y 90")
                
                # Intentar convertir el valor de longitud a float
                longitude_field.value = float(longitude_field.value)
                
                # Verificar que la longitud esté dentro del rango permitido
                if not (-180 <= longitude_field.value <= 180):
                    raise ValueError("La longitud debe estar entre -180 y 180")
            
            except ValueError as e:
                # Mostrar un mensaje de error si ocurre una excepción
                error_message = str(e)
                if "could not convert string to float" in error_message:
                    error_message = "La latitud y la longitud deben ser números decimales."

                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text(error_message, size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))
                return                                         
            
            # Verificar si se cambió el logo al modificar el evento o se dejó el mismo anterior
            logo_changed = isinstance(current_logo, str) and current_logo != event['logo']
            # Si fue cambiado
            if logo_changed:
                # Llama la función update_event_logo
                new_logo_path = update_event_logo(current_logo)

                # Si guarda el logo en assets
                if new_logo_path:
                    page.show_snack_bar(ft.SnackBar(
                        # Aviso de que se guardó el logo
                        content=ft.Text("Logo guardado con éxito.", size=20, color="white"),
                        bgcolor="lightgreen",
                        duration=3000 
                ))
            # Si no se pudo guardar el logo
                else:
                    page.show_snack_bar(ft.SnackBar(
                        # Aviso de que hubo un error guardando el logo
                        content=ft.Text("Error al guardar logo del evento.", size=20, color="red"),
                        bgcolor="lightcoral",
                        duration=3000
                    ))
                    return
            # Si no se cambió el logo al modificar el evento
            else:
                # Conservar el logo actual
                new_logo_path = event['logo']

            # Llama la función modify_event de events.py para actualizar el evento en el csv con los valores diligenciados por el usuario
            modify_event(event['id'],
                         name_field.value,
                         sport_type_dropdown.value,
                         date_field.value,
                         time_field.value,
                         place_field.value,
                         city_field.value,
                         latitude_field.value,
                         longitude_field.value,
                         description_field.value,
                         participation_mode.value,
                         int(capacity_field.value),
                         registration_fee_field.value,
                         status_field.value,
                         new_logo_path
                         )

            # Esperar 2 segundos
            time.sleep(2)
            page.show_snack_bar(ft.SnackBar(
                # Aviso de que el evento fue modificado
                content=ft.Text("Evento modificado exitosamente", size=20, color="white"),
                bgcolor="lightgreen",
                duration=3000 
            ))
            time.sleep(1)
            # Al terminar llama la función navigate_to_page para redirigir a la pagina "Perfil"
            navigate_to_page(page, "profile")

        # Boton para guardar los cambios
        save_button = ft.ElevatedButton("Guardar cambios", on_click=update_event)
        # Boton para cancelar
        cancel_button = ft.ElevatedButton("Cancelar", on_click=lambda _: navigate_to_page(page, "profile"))

        inscribed_users = json.loads(event['usuarios_inscritos'])

        participants_column = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )

        for i, usuario in enumerate(inscribed_users, start=1):
            user_row = ft.Container(
                content=ft.Row([
                    ft.Text(f"{i}. ", weight=ft.FontWeight.BOLD),
                    ft.Text(usuario)
                ]),
                bgcolor=ft.colors.BLUE_50 if i % 2 == 0 else ft.colors.WHITE,
                padding=10,
                border_radius=5
            )
            participants_column.controls.append(user_row)

        content = [
            ft.Text("Modificar Evento", size=30, weight=ft.FontWeight.BOLD),
            name_field,
            sport_type_dropdown,
            date_field,
            time_field,
            place_field,
            city_field,
            description_field,
            participation_mode,
            capacity_field,
            registration_fee_field,
            status_field,
            help_latlong_button,
            latitude_field,
            longitude_field,           
            ft.Row([current_logo, logo_button]),
            save_button,
            cancel_button,
            ft.Text("Usuarios Inscritos", size= 30, weight=ft.FontWeight.BOLD),
            participants_column
        ]

    # Añade a la pagina el encabezado y el contenido según la página en la que está ubicado
    page.controls.extend([create_header_row(page)] + content) 
    # Actualizar pagina
    page.update() 

# Funcion para cerrar cesión
def logout(page):
    # Llama la función set_current_user de content.py para definir que no hay un usuario activo
    set_current_user(None)
    page.show_snack_bar(ft.SnackBar(
        # Aviso de que se cerró sesión con exito
        content=ft.Text("Sesión cerrada exitosamente.", size=20, color="white"),
        bgcolor="lightgreen",
        duration=3000
    ))
    # Llama la función navigate_to_page para redirigir al inicio
    navigate_to_page(page, "home")
    page.update()

# Inicializar id del evento actual seleccionado
current_event = None