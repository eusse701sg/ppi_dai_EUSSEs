# Importar librerías, framework de flet, sus métodos y objetos
import flet as ft
import pandas as pd
import time
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from PIL import Image as PILImage
import time
from flet import Page, Container, Row, Image, Checkbox
# Importar funciones necesarias de events.py
from events import load_events, add_event
# Importar funciones necesarias de content.py
from content import read_privacy_policy, register_user, authenticate_user, change_password, get_current_user, set_current_user, save_profile_picture, save_event_logo



# Crear encabezado
def create_header_row(page: Page):
    # Botones encabezado

    # Boton Logo
    logo_button = ft.GestureDetector(
        content=ft.Image(src="LogoSportex.PNG", width=200, height=80),
        on_tap=lambda e: navigate_to_page(page, "home")  # Redirige a la página de inicio
    )

    # Boton Inicio
    home_button = ft.ElevatedButton(
        text="Inicio",
        width=130,
        height=50,
        bgcolor="grey",
        color="black",
        # Navega a la página de inicio
        on_click=lambda e: navigate_to_page(page, "home")
    )

    # Boton contactame
    contact_button = ft.ElevatedButton( 
        text="Contáctame",
        width=130,
        height=50,
        bgcolor="grey",
        color="black",
        # Navega a la pagina contacto
        on_click=lambda e: navigate_to_page(page, "contact") 
    )

    # Boton quién soy
    who_button = ft.ElevatedButton( 
        text="Quién soy",
        width=150,
        height=50,
        bgcolor="grey",
        color="black",
        # Navega a la pagina Quién soy
        on_click=lambda e: navigate_to_page(page, "who") 
    )


    # Boton Eventos
    events_button = ft.ElevatedButton(
        text="Eventos",
        width=130,
        height=50,
        bgcolor="grey",
        color="black",
        # Navega a pagina Eventos
        on_click=lambda e: navigate_to_page(page, "events") 
    )

    current_user = get_current_user()
    # Botones y Encabezado SI hay un usuario activo
    if current_user: 
        
        # Boton Mi perfil
        profile_button = ft.ElevatedButton(
            text="Mi perfil",
            width=130,
            height=50,
            bgcolor="grey",
            color="black",
            # Navega a pagina mi Perfil
            on_click=lambda e: navigate_to_page(page, "profile") 
        )

        # Boton cerrar sesión 
        logout_button = ft.ElevatedButton(       
            text="Cerrar sesión",
            width=150,
            height=50,
            bgcolor="black",
            color="white",
            # Llama la funcion cerrar sesión  
            on_click=lambda e: logout(page)          
        )

        # Encabezado si hay un usuario activo
        controls = [home_button, events_button, contact_button, who_button, profile_button, logout_button]

    # Botones y Encabezado si NO hay un usuario activo
    else: 
        # Boton iniciar sesión
        login_button = ft.ElevatedButton( 
            text="Iniciar sesión",
            width=150,
            height=50,
            bgcolor="black",
            color="white",
            # Navega a pagina inicar sesión
            on_click=lambda e: navigate_to_page(page, "login") 
        )

        # Boton registrarme
        register_button = ft.ElevatedButton( 
            text="Registrarme",
            width=180,
            height=50,
            bgcolor="blue",
            color="white",
            # Navega a pagina registrarme
            on_click=lambda e: navigate_to_page(page, "register")
        )

        # Encabezado si no hay un usuario activo
        controls = [home_button, events_button, contact_button, who_button, login_button, register_button]

    # Crear fila con logo y los botones (Encabezado completo)

    # Crea fila horizontal
    header_row = ft.Row(
        # Elementos contenidos
        controls=[
            #Boton de logo             
            logo_button,
            # Nueva fila horizontal dentro de la fila principal
            ft.Row( 
                # Botones
                controls=controls, 
                # Espaciado entre botones
                spacing=15 
            ),
        ],
        # Espacio entre el logo y los botones 
        alignment="spaceBetween"       
    )
      
    # Crear contenedor para la barra fija

    # Crea contenedor
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
        # Alineamiento
        alignment=ft.alignment.top_center,
        # Borde
        border=ft.border.all(2, "black"), 
    )
    # Retorna el encabezado completo
    return header_container 

# Funcion para navegar a una pagina
def navigate_to_page(page: Page, page_name: str):
    # Limpiar los controles actuales
    page.controls.clear() 
    content = []

    # Pagina Contactame    
    if page_name == "contact": 
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
            with open("who_am_i.txt", "r", encoding="utf-8") as file: 
                who_am_i_text = file.read()
        # Si no encuentra el txt        
        except FileNotFoundError: 
            who_am_i_text = "Descripción no disponible."
        
        content = [
            ft.Container(
                content=ft.Text("Quién soy", size=30, text_align="center"),
                padding=10
            ),
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
        # Formulario de registro
        email_field = ft.TextField(label="Correo Electrónico", width=300)
        # Campo contraseña oculto
        password_field = ft.TextField(label="Contraseña", width=300, password=True) 
        username_field = ft.TextField(label="Nombre de Usuario", width=300)
        names_field = ft.TextField(label="Nombres", width=300)
        lastnames_field = ft.TextField(label="Apellidos", width=300)
        
        # Checkbox para aceptar las políticas de privacidad
        privacy_checkbox = ft.Checkbox(label="Acepto las políticas de privacidad", width=300, value=False)

        # Botón para registrar, inicialmente deshabilitado
        register_button = ft.ElevatedButton(
            content=ft.Container(
                content=ft.Text(value="Registrar", size=22)
            ),            
            on_click=lambda e: handle_register(e), disabled=True,
            height=60,
            width=180,
            color="white",
            bgcolor="blue"
        )

        # Actualizar estado del botón basado en el checkbox
        def toggle_resgister_button(e):
            register_button.disabled = not privacy_checkbox.value
            page.update()

        privacy_checkbox.on_change = toggle_resgister_button

        #Validar campos
        def validate_fields():
            fields = [email_field,password_field, username_field, names_field, lastnames_field]
            return all(field.value.strip() != "" for field in fields)

        # Funcion para el manejo del registro
        def handle_register(e):
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
            if register_user(email, password, username, names, lastnames):
                # Aviso para registro exitoso
                page.show_snack_bar(ft.SnackBar(  
                    content=ft.Text("Registro exitoso.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))
            else:
                # Aviso para registro fallido
                page.show_snack_bar(ft.SnackBar( 
                    content=ft.Text("Error: El correo o nombre de usuario ya está registrado", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))
        def show_privacy_policy(_):
            dialog = ft.AlertDialog(
                modal = True,
                title = ft.Text("Política de Privacidad"),
                content = ft.Container(
                    content = ft.ListView(
                        controls=[ft.Text(read_privacy_policy(), size=14)],
                        expand=True,
                        auto_scroll=False
                    ),
                    height=400,
                    width=400,                    
                ),
                actions=[
                    ft.TextButton("Cerrar", on_click=lambda _: close_dialog(dialog))
                ]
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
        
        def close_dialog(dialog):
            dialog.open= False
            page.update()

        # Abrir politicas de privacidad 
        privacy_link = ft.TextButton("Políticas de privacidad")
        privacy_link.on_click = show_privacy_policy

        # Contenido de la página de registro        
        content = [
            ft.Container(
                content=ft.Text("Registrarme", size=30, text_align="center"),
                padding=10,
                alignment=ft.alignment.top_center                
            ),
            # Contenedor para el formulario
            ft.Container( 
                content=ft.Column(
                    controls=[
                        email_field,
                        password_field,
                        username_field,
                        names_field,
                        lastnames_field,
                        ft.Row(controls=[privacy_checkbox, privacy_link],alignment="center"),
                        register_button                        
                    ],
                    alignment="center",
                    spacing=20,
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
            email_or_username = email_or_username_field.value
            password = password_field.value   
            # Llama la funcion authenticate_user de content.py para validar credenciales         
            user = authenticate_user(email_or_username, password)
            
            # Credenciales correctas
            if user: 
                # Actualiza al usuario actual
                set_current_user(user) 
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Inicio de sesión exitoso.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000
                ))
                # Actualiza a pagina de Inicio
                navigate_to_page(page, "home")

            # Credenciales erróneas
            else:
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Error: Credenciales incorrectas", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))
        
        content = [
            ft.Container(
                content=ft.Text("Iniciar sesión", size=30, text_align="center"),
                padding=10
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        email_or_username_field,
                        password_field,
                        # Boton iniciar sesión
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
        # Obtener usuario actual 
        current_user = get_current_user() 

        if current_user is None:
            navigate_to_page(page, "login")
            return
        
        # Funcion para cambiar contraseña    
        def handle_password_change(e): 
            # Contraseña vieja
            old_password = old_password_field.value   
            # Contraseña nueva
            new_password = new_password_field.value 
            
            # Llama funcion cambiar contraseña de content.py
            if change_password(old_password, new_password): 
                # Contraseña cambiada
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Contraseña cambiada exitosamente.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))
            else:
                # Error cambiando contraseña
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Error: Contraseña antigua incorrecta", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                )) 

        def handle_profile_picture_change(e: ft.FilePickerResultEvent):
            if not e.files or len(e.files) == 0:
                return
            
            file_path = e.files[0].path
            file_name = e.files[0].name

            # Verificar que archivo es una imagen
            valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".jfif", ".avif"]
            file_extensions = os.path.splitext(file_name)[1].lower()

            if file_extensions not in valid_extensions:
                page.show_snack_bar(ft.SnackBar(
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
                    content=ft.Text("El archivo seleccionado no es una imagen válida.", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))      


            if save_profile_picture(file_path):
                update_profile_picture(file_path)
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Foto de perfil cambiada con éxito.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))      
            else:
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Error al guardar la imagen de perfil.", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))            

        def update_profile_picture(file_path):
            profile_picture.src = file_path
            page.update()

        def load_user_events():
            events = load_events()
            user_events = events[events['organizador'] == current_user['username']]
            return user_events
        
        def delete_event(event_id):
            events = load_events()
            events = events[events['id'] != event_id]
            events.to_csv('events.csv', index=False)
            update_user_events()
            page.show_snack_bar(ft.SnackBar(
                content=ft.Text("Evento eliminado exitosamente.", size=20, color="white"),
                bgcolor="lightgreen",
                duration=3000
            ))
        
        def update_user_events():
            user_events = load_user_events()
            user_events_column.controls.clear()
            for _, event in user_events.iterrows():
                event_row = ft.Row([
                    ft.Text(event['nombre'], size=16),
                    ft.Text(event['fecha'], size=14),
                    ft.ElevatedButton("Eliminar evento", on_click=lambda _, eid=event['id']: delete_event(eid))
                ])
                user_events_column.controls.append(event_row)
            page.update()

        user_events_column = ft.Column([], scroll=ft.ScrollMode.AUTO, height=300)
        update_user_events()

        file_picker = ft.FilePicker(on_result=handle_profile_picture_change)
        page.overlay.append(file_picker)

        #Cargar foto de perfil
        profile_picture_path = os.path.join("assets/uploads/profile", f"{current_user['username']}_profile.png")
        if os.path.exists(profile_picture_path):
            profile_picture_path = os.path.join("assets/uploads/profile", f"{current_user['username']}_profile.png")

        else:
            profile_picture_path = os.path.join("assets", "Foto_usuario_defecto.jpg")

        #Foto de perfil
        profile_picture = ft.Image(
            src=profile_picture_path,
            width=200,
            height=200,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(100),
        )

        #Mostrar datos del usuario en campos
        email_field = ft.TextField(label="Correo Electrónico", value=current_user["email"], width=300, read_only=True)
        username_field = ft.TextField(label="Nombre de Usuario", value=current_user["username"], width=300, read_only=True)
        names_field = ft.TextField(label="Nombres", value=current_user["names"], width=300, read_only=True)
        lastnames_field = ft.TextField(label="Apellidos", value=current_user["lastnames"], width=300, read_only=True)        
        old_password_field = ft.TextField(label="Contraseña Antigua", width=300, password=True)
        new_password_field = ft.TextField(label="Contraseña Nueva", width=300, password=True)
        



        content = [
            ft.Row([
                ft.Column([
                    profile_picture,
                    ft.ElevatedButton("Cambiar foto de perfil", on_click=lambda _: file_picker.pick_files(allow_multiple=False)),
                    ft.Divider(),
                    ft.Text("Mis eventos creados", size=20, weight=ft.FontWeight.BOLD),
                    user_events_column 
                ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START),
                ft.VerticalDivider(width=100),                
                ft.Column(
                    controls=[
                        ft.Text("Mi perfil", size=30, text_align="center", weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                        email_field,
                        username_field,
                        names_field,
                        lastnames_field,
                        ft.Text("Cambiar contraseña"),
                        old_password_field,
                        new_password_field,
                        #Boton para cambiar contraseña
                        ft.ElevatedButton("Cambiar Contraseña", on_click=handle_password_change),                                            
                    ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.START),
                ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START   
            )
        ]

    # Pagina de inicio    
    elif page_name == "home":
        
        user=get_current_user()

        title = ft.Text(
            "     Únete a la Mejor Comunidad\nDeportiva en Linea",
            text_align="center",
            size = 40,
            weight = ft.FontWeight.W_900,
            color = ft.colors.BLACK
        )

        title2 = ft.Text(
            "Bienvenido de nuevo!",
            text_align="center",
            size = 40,
            weight = ft.FontWeight.W_900,
            color = ft.colors.BLACK
        )
        
        descriptions = ft.Text( 
            "Participa en Eventos Deportivos cerca de ti🏅📅\nObserva resultados y gráficos en tiempo real📊⏱️\nGana increíbles recompensas por convertirte en ganador🏆🎉",
            text_align="center",
            size=25
            
        )        
        
        descriptions2 = ft.Text( 
            "Proximamente Inicio mejorado para usuarios registrados",
            text_align="center",
            size=25
            
        )   

        register_button = ft.ElevatedButton(
            content=ft.Container( 
                ft.Text(value="Registrarme", size=23)                
            ),          
            width=200,
            height=70,
            bgcolor="blue",
            color="white",          
            # Navega a pagina registrarme
            on_click=lambda e: navigate_to_page(page, "register")
        )

        logo=ft.Image(src="LogoSportexCompleto.PNG", width=450, height=450)
        
        if user:
            content=[
                ft.Row(
                    [
                        ft.Column(
                            [
                                title2,                           
                                descriptions2,                                                                               
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
        else:
                        content=[
                ft.Row(
                    [
                        ft.Column(
                            [
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
    
    #Pagina de eventos
    elif page_name == "events":

        events = load_events()
        current_user = get_current_user()

        def create_event_card(event):
            return ft.GestureDetector(
                on_tap=lambda _: show_event_details(event),
                content=ft.Card(
                    content=ft.Container(
                        bgcolor=ft.colors.BLUE_200,
                        border=ft.border.all(2, ft.colors.BLACK),
                        padding=5,
                        content=ft.Column([
                            ft.Image(src=event['logo'], width=200, height=200, fit=ft.ImageFit.COVER),
                            ft.Container(
                                content=ft.Text(event['nombre'], size=14, weight=ft.FontWeight.BOLD),
                                margin=ft.margin.only(top=5, bottom=5),
                                                                
                            ),
                            ft.Text(f"{event['fecha']} - {event['hora']}", size=12),
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
                        ]),
                        width=200,
                        height=250
                    ),
                )
            )

        def show_event_details(event):
            def close_dialog(_):
                dialog.open = False
                page.update()

            dialog = ft.AlertDialog(
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
                             
                        ]),
                    ]),                  
                    ft.Text("Detalles:",size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Descripción: {event['descripcion']}"),
                    ft.Text(f"Tipo de deporte: {event['tipo_deporte']}"),
                    ft.Text(f"Modalidad de participación: {event['modalidad_participacion']}"),
                    ft.Text(f"Capacidad: {event['capacidad']}"),                    
                    ft.Text(f"Costo de inscripción: {event['costo_inscripcion']}"),                    
                    ft.TextButton(f"Ver ubicación en Google Maps", on_click=lambda _: page.launch_url(f"https://www.google.com/maps?q={event['latitud']},{event['longitud']}"))
                    
                ], scroll=ft.ScrollMode.AUTO, height=400),
                actions=[
                    ft.TextButton("Cerrar", on_click=close_dialog),
                ],
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

        event_grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=200,
            child_aspect_ratio=0.55,  # Ajustado para una mejor proporción
            spacing=10,
            run_spacing=10,
        )

        for event in events.to_dict('records'):
            event_grid.controls.append(create_event_card(event))

        current_user=get_current_user()
        if current_user:
            create_event_button = ft.ElevatedButton(
                text="Crear Evento",
                width=130,
                height=50,
                bgcolor="blue",
                color="white",
                # Navega a pagina mi Perfil
                on_click=lambda e: navigate_to_page(page, "create_event") 
        )
        
            content = [
                ft.Text("Eventos", size=30, weight=ft.FontWeight.BOLD),
                create_event_button,
                event_grid,
            ]
        
        else:
            content = [
                ft.Text("Eventos", size=30, weight=ft.FontWeight.BOLD),                
                event_grid,
            ]




        #al clickear un evento, sale ventana emergente con info y la posibilidad de darle en asistir
        #al darle en asistir, se guardará en el perfil los eventos que asistirá       
        # posibilidad de dirigirse al perfil del creador 
        #al crear nuevo evento llama funcion crear evento de events.py
        #pide info, guarda en csv y se actualiza la pagina para ver el nuevo evento
        #posibilidad de filtrar eventos (cercania, fecha mas cercana, individual o equipo, etc  )
        #al crear evento también se añadirá al perfil los eventos creados
        #tener encuenta la logica, no superar capacidad, mostrar primero los abiertos, etc

    #Pagina de crear eventos
    elif page_name == "create_event":
        events = load_events()
        current_user = get_current_user()

        # Obtener el próximo ID disponible
        next_id = max(events['id']) + 1 if len(events) > 0 else 1

        # Formulario
        name_field = ft.TextField(label="Nombre del evento", width=300)
        sport_types = ["Fútbol", "Baloncesto", "Tenis", "Voleibol", "Natación", "Atletismo", "Otro"]
        sport_type_dropdown = ft.Dropdown(
            label="Tipo de deporte",
            width=300,
            options=[ft.dropdown.Option(sport) for sport in sport_types]
        )        
        date_field = ft.TextField(label="Fecha (YYYY-MM-DD)", width=300)
        time_field = ft.TextField(label="Hora (HH:MM)", width=300)
        place_field = ft.TextField(label="Lugar", width=300)
        city_field = ft.TextField(label="Ciudad", width=300)
        description_field = ft.TextField(label="Descripción", width=300, multiline=True, max_lines=5)
        participation_mode = ft.Dropdown(
            label="Modalidad de participación",
            width=300,
            options=[
                ft.dropdown.Option("Individual"),
                ft.dropdown.Option("Equipos")
            ]
        )
        capacity_field = ft.TextField(label="Capacidad", width=300)
        registration_fee_field = ft.TextField(label="Costo de inscripción", width=300)
        street_field = ft.TextField(label="Dirección", width=300)
        neighborhood_field = ft.TextField(label="Barrio", width=300)
        state_field = ft.TextField(label="Estado/Provincia", width=300)
        country_field = ft.TextField(label="País", width=300)
        postal_code_field = ft.TextField(label="Código Postal", width=300)
        logo_file_path = None

        def handle_logo_change(e: ft.FilePickerResultEvent):
            global logo_file_path
            if not e.files or len(e.files) == 0:
                return
            
            file_path = e.files[0].path
            file_name = e.files[0].name     

            valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".jfif", ".avif"]
            file_extension = os.path.splitext(file_name)[1].lower()

            if file_extension not in valid_extensions:
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("El archivo seleccionado no es una imagen válida", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))
                return
            
        
            try:
                with PILImage.open(file_path) as img:                    
                    logo_file_path = file_path  # Guardar la ruta del archivo
                    page.show_snack_bar(ft.SnackBar(
                        content=ft.Text("Logo subido exitosamente", size=20, color="white"),
                        bgcolor="lightgreen",
                        duration=3000 
                    ))
            except Exception as e:
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text(f"Error al procesar la imagen: {str(e)}", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000 
                ))

        file_picker = ft.FilePicker(on_result=handle_logo_change)
        page.overlay.append(file_picker)

        logo_button = ft.ElevatedButton("Subir logo", on_click=lambda _: file_picker.pick_files(allow_multiple=False))

        def create_event(e):
                global logo_file_path
                # Validar campos
                if not all([name_field.value, sport_type_dropdown.value, date_field.value, time_field.value, 
                            place_field.value, city_field.value, description_field.value, participation_mode.value,
                            capacity_field.value, registration_fee_field.value, street_field.value, 
                            neighborhood_field.value, state_field.value, country_field.value, postal_code_field.value]):
                    page.show_snack_bar(ft.SnackBar(
                        content=ft.Text("Por favor, complete todos los campos", size=20, color="red"),
                        bgcolor="lightcoral",
                        duration=3000 
                    ))
                    return

                # Obtener coordenadas
                geolocator = Nominatim(user_agent="sportex_app")
                                
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
                    if location:
                        latitude, longitude = location.latitude, location.longitude
                    else:
                        raise Exception("No se pudo obtener la ubicación")
                except Exception as e:
                    page.show_snack_bar(ft.SnackBar(
                        content=ft.Text(f"Error al obtener coordenadas: {str(e)}", size=20, color="red"),
                        bgcolor="lightcoral",
                        duration=3000 
                    ))
                    return

                # Guardar logo
                if logo_file_path:
                    new_logo_path = save_event_logo(logo_file_path)
                    
                    if new_logo_path:
                        relative_logo_path = new_logo_path
                        page.show_snack_bar(ft.SnackBar(
                            content=ft.Text("Logo guardado con éxito.", size=20, color="white"),
                            bgcolor="lightgreen",
                            duration=3000 
                        ))
                    else:
                        page.show_snack_bar(ft.SnackBar(
                            content=ft.Text("Error al guardar logo del evento.", size=20, color="red"),
                            bgcolor="lightcoral",
                            duration=3000
                        ))
                        return
                    
                else:
                    new_logo_path = "assets/uploads/events/logos/evento_default.png"

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
                          relative_logo_path)

                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Evento creado exitosamente", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))
                time.sleep(1)
                navigate_to_page(page, "events")    
        
        create_button = ft.ElevatedButton("Crear Evento", on_click=create_event)

        content = [
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
            street_field,
            neighborhood_field,
            state_field,
            country_field,
            postal_code_field,
            logo_button,
            create_button
        ]                     


    # Añade a la pagina el encabezado y el contenido    
    page.controls.extend([create_header_row(page)] + content) 
    # Actualizar pagina
    page.update() 

# Funcion para cerrar cesión
def logout(page):
    set_current_user(None)
    page.show_snack_bar(ft.SnackBar(
        content=ft.Text("Sesión cerrada exitosamente.", size=20, color="white"),
        bgcolor="lightgreen",
        duration=3000
    ))
    navigate_to_page(page, "home")
    page.update()