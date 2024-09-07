# Importar librerías necesarias
import flet as ft
import pandas as pd
import time
import os
from geopy.geocoders import Nominatim
from PIL import Image as PILImage
from flet import Page, Image
# Importar funciones necesarias de events.py
from events import load_events, add_event
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

    # Limpiar los controles y contenido actual
    page.controls.clear()   
    content = []

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
        def toggle_resgister_button(e):
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
        privacy_checkbox.on_change = toggle_resgister_button       
    

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
        # Llama a la función get_current_user de content.py para obtener el usuario actual logeado.
        current_user = get_current_user() 

        # Si no hay un usuario logeado
        if current_user is None:
            # Redirige a la página Login
            navigate_to_page(page, "login")
            return
        
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
                with Image.open(file_path) as img:
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

            # Llama la función load_events de events.py para cargar todos los eventos
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

            # Llama la función load_events de events.py para cargar todos los eventos
            events = load_events()
            # Selecciona los eventos a exepción del evento a eliminar
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
            
        
        # Función para actualizar los eventos del usuario logeado
        def update_user_events():
            """
            Función para actualizar los eventos del usuario logeado.        

            Returns:
                None               
            """    
            # Llama la función load_user_events para tener los eventos creados por el usuario
            user_events = load_user_events()
            # Borrar los controles de la columna contenedora de los eventos
            user_events_column.controls.clear()
            # Itera por cada evento creado por el usuario logeado y los muestra
            for _, event in user_events.iterrows():
                # Contenedor horizontal tipo Row con los eventos creados por el usuario
                event_row = ft.Row([
                    ft.Text(event['nombre'], size=16),
                    ft.Text(event['fecha'], size=14),
                    # Boton para eliminar un evento que llama la función delete_event
                    ft.ElevatedButton("Eliminar evento", on_click=lambda _, eid=event['id']: delete_event(eid))
                ])
                # Añade los nuevos controles del Row creado anteriormente (contiene los eventos creados por el usuario)
                user_events_column.controls.append(event_row)
            # Actualiza la página
            page.update()

        # Columna contenedora de los eventos creados por el usuario
        user_events_column = ft.Column([], scroll=ft.ScrollMode.AUTO, height=300)
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
                    ft.Text("Mis eventos creados", size=20, weight=ft.FontWeight.BOLD),
                    # Eventos creados definido anteriormente
                    user_events_column 
                ], 
                # Alineamiento de contenedor vertical tipo Colum
                alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START),
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
        
        # Llama a la función load_events de events.py para obtener los eventos actuales
        events = load_events()
        # Llama a la función get_current_user de content.py para obtener el usuario acutal
        current_user = get_current_user()

        # Función para crear carta de evento
        def create_event_card(event):
            """
            Función para crear carta de evento.

            Args:
                event (dic): recibe el diccionario de un evento
            Returns:
                ft.GestureDetector: Retorna una carta que reacciona al hacer click sobre ella               
            """    
            # Establecer color del texto del estado del evento
            if event['estado']=="Abierto":
                status_color='green'
            else:
                status_color='red'
            # Crea un tipo GestureDetector            
            return ft.GestureDetector(
                # Al clickear sobre el gesture detector llama la función show_event_details
                on_tap=lambda _: show_event_details(event),
                # Contenido del gestureDetector, el primero es un ft.Card
                content=ft.Card(
                    # Contenido del ft.Card , el primero es un ft.Container con color de fondo
                    content=ft.Container(
                        bgcolor=ft.colors.BLUE_200,
                        border=ft.border.all(2, ft.colors.BLACK),
                        padding=5,
                        # Contenido del ft.Container, el primero es un ft.Column (contenedor vertical)
                        content=ft.Column([
                            # Contiene logo del evento, y nombre
                            ft.Image(src=event['logo'], width=200, height=200, fit=ft.ImageFit.COVER),
                            ft.Container(
                                content=ft.Text(event['nombre'], size=14, weight=ft.FontWeight.BOLD),
                                margin=ft.margin.only(top=5, bottom=5),
                                                                
                            ),
                            # Contiene fecha y hora del evento
                            ft.Text(f"{event['fecha']} - {event['hora']}", size=12),
                            # Contiene el estado del evento
                            ft.Text(f"Estado: {event['estado']}", size=12, color=status_color),
                            # Contiene descripción del evento
                            ft.Container(
                                content=ft.Text(
                                    event['descripcion'],
                                    size=12,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                margin=ft.margin.only(top=5),
                                expand=True,
                            ),
                        ],spacing=2),
                        width=200,
                        height=250
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
                        ]),
                    ]),                  
                    ft.Text("Detalles:",size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Descripción: {event['descripcion']}"),
                    ft.Text(f"Tipo de deporte: {event['tipo_deporte']}"),
                    ft.Text(f"Modalidad de participación: {event['modalidad_participacion']}"),
                    ft.Text(f"Capacidad: {event['capacidad']}"),                    
                    ft.Text(f"Costo de inscripción: {event['costo_inscripcion']}"),
                    # Boton para redirigir a la ubicación de google maps                    
                    ft.TextButton(f"Ver ubicación en Google Maps", on_click=lambda _: page.launch_url(f"https://www.google.com/maps?q={event['latitud']},{event['longitud']}"))
                    
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

        # Itera entre cada evento de todos los eventos y convierte a cada uno en un diccionario
        for event in events.to_dict('records'):
            # Para cada evento llama la función create_event card y crea una carta
            event_grid.controls.append(create_event_card(event))

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
                # Navega a pagina mi Perfil por medio de la función navigate_to_page
                on_click=lambda e: navigate_to_page(page, "create_event") 
        )
            # Contenido si hay un usuario activo
            content = [
                ft.Text("Eventos", size=30, weight=ft.FontWeight.BOLD),
                # Boton crear evento
                create_event_button,
                # Cuadricula de eventos
                event_grid,
            ]
        
        # Si no hay un usuario activo
        else:
            # El contenido será unicamente la cuadrícula
            content = [
                ft.Text("Eventos", size=30, weight=ft.FontWeight.BOLD),                
                event_grid,
            ]

    # Pagina de crear eventos
    elif page_name == "create_event":

        # Llama a la función load_events de events.py para cargar los eventos actuales        
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
        # Campos con Dirección, barrio, estado, país y código postal
        street_field = ft.TextField(label="Dirección", width=300)
        neighborhood_field = ft.TextField(label="Barrio", width=300)
        state_field = ft.TextField(label="Estado/Provincia", width=300)
        country_field = ft.TextField(label="País", width=300)
        postal_code_field = ft.TextField(label="Código Postal", width=300)
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
                        capacity_field.value, registration_fee_field.value, status_field.value, street_field.value, 
                        neighborhood_field.value, state_field.value, country_field.value, postal_code_field.value]):
                page.show_snack_bar(ft.SnackBar(
                    # Si no se ha llenado los campos en su totalidad, avisa que debe hacerlo
                    content=ft.Text("Por favor, complete todos los campos", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return

            # Obtener coordenadas con la librería Nominatim, geolocator y geocode
            geolocator = Nominatim(user_agent="sportex_app")

            # Intenta obtener coordenadas según calle, barrio, ciudad, estado, pais, codigo postal ingresados por el usuario              
            try:
                location = geolocator.geocode(
                    query={
                        'street': street_field.value,
                        'neighborhood': neighborhood_field.value,
                        'city': city_field.value,
                        'state': state_field.value,
                        'country': country_field.value,
                        'postal_code': postal_code_field.value
                    }
                )
                # Si obtiene coordenadas
                if location:
                    latitude, longitude = location.latitude, location.longitude
                # Si no se pudo obtener las coordenadas
                else:
                    raise Exception("No se pudo obtener la ubicación")
            except Exception as e:
                page.show_snack_bar(ft.SnackBar(
                    # Aviso de que no se pudo obtener cordenads
                    content=ft.Text(f"Error al obtener coordenadas: {str(e)}", size=20, color="red"),
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
                        latitude, 
                        longitude, 
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
            street_field,
            neighborhood_field,
            state_field,
            country_field,
            postal_code_field,
            logo_button,
            create_button
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