import flet as ft
from flet import Page, Container, Row, Image
from content import read_policy_text, register_user, authenticate_user, change_password, current_user, get_current_user, set_current_user


def create_header_row(page: Page): #Crear encabezado
    # Botones encabezado

    contact_button = ft.ElevatedButton( #Boton contactame
        text="Contáctame",
        width=130,
        height=50,
        bgcolor="grey",
        color="black",
        on_click=lambda e: navigate_to_page(page, "contact") #Navega a la pagina contacto
    )
    who_button = ft.ElevatedButton( #Boton quién soy
        text="Quién soy",
        width=150,
        height=50,
        bgcolor="grey",
        color="black",
        on_click=lambda e: navigate_to_page(page, "who") #Navega a la pagina Quién soy
    )
    policy_button = ft.ElevatedButton( #Boton politica de privacidad
        text="Política de Privacidad",
        width=200,
        height=50,
        bgcolor="grey",
        color="black",
        on_click=lambda e: navigate_to_page(page, "policy") #Navega a la páginca politica de privacidad
    )
    comunity_button = ft.PopupMenuButton( #Boton Comunidad
        content=ft.Text("Comunidad"),    
        menu_position="UNDER",
        width=100,    
        padding=10,        
        items=[
            ft.PopupMenuItem(text="Torneos", on_click=lambda _: navigate_to_page(page, "tournaments")), #Boton torneos
            ft.PopupMenuItem(text="Eventos", on_click=lambda _: navigate_to_page(page, "events")) #boton eventos
        ],
    )

    current_user = get_current_user()
    if current_user: #Botones y Encabezado SI hay un usuario activo

        profile_button = ft.ElevatedButton( #Boton Mi perfil
            text="Mi perfil",
            width=130,
            height=50,
            bgcolor="grey",
            color="black",
            on_click=lambda e: navigate_to_page(page, "profile") #navega a pagina mi Perfil
        )
        logout_button = ft.ElevatedButton( #Boton cerrar sesión        
            text="Cerrar sesión",
            width=150,
            height=50,
            bgcolor="black",
            color="white",
            on_click=lambda e: logout(page) #Llama la funcion cerrar sesión            
        )

        #Encabezado si hay un usuario activo
        controls = [comunity_button,contact_button, who_button, policy_button, profile_button, logout_button]

    else: #Botones y Encabezado si NO hay un usuario activo
        login_button = ft.ElevatedButton( #boton iniciar sesión
            text="Iniciar sesión",
            width=150,
            height=50,
            bgcolor="black",
            color="white",
            on_click=lambda e: navigate_to_page(page, "login") #navega a pagina inicar sesión
        )
        register_button = ft.ElevatedButton( #boton registrarme
            text="Registrarme",
            width=180,
            height=50,
            bgcolor="blue",
            color="white",
            on_click=lambda e: navigate_to_page(page, "register") #navega a pagina registrarme
        )

        #Encabezado si no hay un usuario activo
        controls = [comunity_button,contact_button, who_button, policy_button, login_button, register_button]

    # Crear fila con logo y los botones (Encabezado completo)
    header_row = ft.Row( #Crea fila horizontal
        controls=[ #Elementos contenidos
            ft.Image(src="assets/Logo.jpg", width=200, height=80), #Logo de la app
            ft.Row( #Nueva fila horizontal dentro de la fila principal
                controls=controls, #Botones
                spacing=15 #Espaciado entre botones
            ),
        ],
        alignment="spaceBetween" #Espacio entre el logo y los botones       
    )
      
    # Crear contenedor para la barra fija
    header_container = ft.Container( #Crea contenedor
        content=ft.Column(
            controls=[
                header_row, #Añade cabecera               
            ],
            spacing=10 
        ),
        padding=10, #Espaciado entre los bordes
        height=100, #Altura
        bgcolor="white", #Color de fondo
        alignment=ft.alignment.top_center, #Alineamiento
        border=ft.border.all(2, "black"), #Borde
    )

    return header_container #Retorna el encabezado completo


def navigate_to_page(page: Page, page_name: str):
    page.controls.clear()  # Limpiar los controles actuales
    content = []

    if page_name == "policy": #Pagina Politica de privacidad
        policy_text = read_policy_text()
        content = [
            ft.Container(
                content=ft.Text("Política de Privacidad", size=30),
                alignment=ft.alignment.center,
                padding=10
            ),
            ft.Container(
                content=ft.Text(
                    policy_text,
                    size=16,
                    text_align="justify"
                ),
                alignment=ft.alignment.center,
                padding=10
            )
        ]
    elif page_name == "contact": #Pagina Contactame
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
    elif page_name == "who": #Pagina quien soy
        try:
            with open("who_am_i.txt", "r", encoding="utf-8") as file: #Lee el archivo txt quién soy y lo codifica a utf8
                who_am_i_text = file.read()
        except FileNotFoundError: #Si no encuentra el txt
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
                    text_align="justify" #Texto justificado
                ),
                alignment=ft.alignment.center_left, #contenedor alineado al centro a la izquierda
                padding=10
            )
        ]    
    elif page_name == "register": #Pagina registrarme
        # Formulario de registro
        email_field = ft.TextField(label="Correo Electrónico", width=300)
        password_field = ft.TextField(label="Contraseña", width=300, password=True) #Campo contraseña oculto
        username_field = ft.TextField(label="Nombre de Usuario", width=300)
        names_field = ft.TextField(label="Nombres", width=300)
        lastnames_field = ft.TextField(label="Apellidos", width=300)
        
        def handle_register(e): #Funcion para el manejo del registro
            #Asigna los valores a los campos 
            email = email_field.value
            password = password_field.value
            username = username_field.value
            names = names_field.value
            lastnames = lastnames_field.value
            
            if register_user(email, password, username, names, lastnames): #Llama la funcion registrar usuario de content.py
                page.show_snack_bar(ft.SnackBar(  #Aviso para registro exitoso
                    content=ft.Text("Registro exitoso.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))
            else:
                page.show_snack_bar(ft.SnackBar( #Aviso para registro fallido
                    content=ft.Text("Error: El correo o nombre de usuario ya está registrado", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                ))
        content = [
            ft.Container(
                content=ft.Text("Registrarme", size=30, text_align="center"),
                padding=10
            ),
            ft.Container( #Contenedor para el formulario
                content=ft.Column(
                    controls=[
                        email_field,
                        password_field,
                        username_field,
                        names_field,
                        lastnames_field,
                        ft.ElevatedButton("Registrar", on_click=handle_register) #Boton para completar registro
                    ],
                    alignment="center",
                    spacing=10
                ),
                padding=10
            )
        ]
    elif page_name == "login": #Pagina para iniciar sesion
        # Formulario de inicio de sesión
        email_or_username_field = ft.TextField(label="Correo Electrónico o Nombre de Usuario", width=300) #Campo correo o usuario
        password_field = ft.TextField(label="Contraseña", width=300, password=True) #Campo contraseña oculta
        
        def handle_login(e): #Funcion para el manejo del acceso
            email_or_username = email_or_username_field.value
            password = password_field.value            
            user = authenticate_user(email_or_username, password) #Llama la funcion authenticate_user de content.py para validar credenciales
            
            if user: #Credenciales correctas
                set_current_user(user) #Actualiza al usuario actual
                page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Inicio de sesión exitoso.", size=20, color="white"),
                    bgcolor="lightgreen",
                    duration=3000
                ))
                navigate_to_page(page, "home") #Actualiza a pagina de Inicio
            else: #Credenciales erróneas
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
                        ft.ElevatedButton("Iniciar sesión", on_click=handle_login) #Boton iniciar sesión
                    ],
                    alignment="center",
                    spacing=10
                ),
                padding=10
            )
        ]
    elif page_name == "profile": #Pagina del perfil
        current_user = get_current_user() #Obtener usuario actual

        if current_user is None:
            navigate_to_page(page, "login")
            return
        
        #Mostrar datos del usuario en campos
        email_field = ft.TextField(label="Correo Electrónico", value=current_user["email"], width=300, read_only=True)
        username_field = ft.TextField(label="Nombre de Usuario", value=current_user["username"], width=300, read_only=True)
        names_field = ft.TextField(label="Nombres", value=current_user["names"], width=300, read_only=True)
        lastnames_field = ft.TextField(label="Apellidos", value=current_user["lastnames"], width=300, read_only=True)        
        old_password_field = ft.TextField(label="Contraseña Antigua", width=300, password=True)
        new_password_field = ft.TextField(label="Contraseña Nueva", width=300, password=True)
        

        def handle_password_change(e): #Funcion para cambiar contraseña
            old_password = old_password_field.value #Contraseña vieja   
            new_password = new_password_field.value #Contraseña nueva
            
            if change_password(old_password, new_password): #Llama funcion cambiar contraseña de content.py
                page.show_snack_bar(ft.SnackBar( #Contraseña cambiada
                    content=ft.Text("Contraseña cambiada exitosamente.", size=20, color="green"),
                    bgcolor="lightgreen",
                    duration=3000 
                ))
            else:
                page.show_snack_bar(ft.SnackBar(#Error cambiando contraseña
                    content=ft.Text("Error: Contraseña antigua incorrecta", size=20, color="red"),
                    bgcolor="lightcoral",
                    duration=3000
                )) 

        content = [
            ft.Container(
                content=ft.Text("Mi perfil", size=30, text_align="center"),
                padding=10
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        email_field,
                        username_field,
                        names_field,
                        lastnames_field,
                        ft.Text("Cambiar contraseña"),
                        old_password_field,
                        new_password_field,
                        ft.ElevatedButton("Cambiar Contraseña", on_click=handle_password_change), #Boton para cambiar contraseña                        
                    ],
                    alignment="center",
                    spacing=10
                ),
                padding=10
            )
        ]
    elif page_name == "home": #Pagina de inicio
        content=[
            ft.Container(
                content=ft.Text("Inicio", size=30)
            )
        ]
    page.controls.extend([create_header_row(page)] + content) #Añade a la pagina el encabezado y el contenido
    page.update() #Actualizar pagina

def logout(page):
    set_current_user(None)
    page.show_snack_bar(ft.SnackBar(
        content=ft.Text("Sesión cerrada exitosamente.", size=20, color="white"),
        bgcolor="lightgreen",
        duration=3000
    ))
    navigate_to_page(page, "home")
    page.update()