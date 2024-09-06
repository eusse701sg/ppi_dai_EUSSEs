#Importar librerías necesarias
import os
from PIL import Image
# Importar funciones de events.py
from events import load_events

#Base de datos con Correo, Contraseña, Usuario, Nombres, Apellidos
USERS_DB_FILE = "data/users_db.txt"
# Definir usuario actual cono ninguno
current_user = None

# Función para cambiar el usuario actual
def set_current_user(user):
    """
    Cambia el usuario actualmente logeado.

    Args:
        user (str): nombre de usuario logeado
        
    Returns:
        None
    """  
    global current_user
    # Define que current_user será el usuario actual
    current_user = user

# Función para obtener usuario actual
def get_current_user():
    """
    Obtiene el usuario actual.
        
    Returns:
        current_user (str): Usuario actual
    """  
    return current_user
   
#Funcion para verificar en la base de datos si existe un usuario, retorna true o false
def user_exists(email: str, username: str) -> bool:
    """
    Verifica en la base de datos de users_db.txt si existe el usuario.

    Args:
        email (str): correo del usuario
        username (str): nombre de usuario
        
    Returns:
        True (bool): Si existe el usuario
        False (bool): Si no existe el usuario
    """  
    # Si no existe la base de datos users_db.txt
    if not os.path.exists(USERS_DB_FILE):
        return False 
    
    # Abrir archivo de bases de datos
    with open(USERS_DB_FILE, "r") as file: 
        # Iterar en cada linea
        for line in file:
            # Dividir por comas y eliminar espacios en blanco
            data = line.strip().split(",")
            # Comprobar que la línea tiene el número esperado de campos
            if len(data) < 5:
                continue
            # Buscar si el email o el usuario están en alguna linea
            if data[0].lower() == email.lower() or data[2].lower() == username.lower():
                # Existe usuario
                return True
    # No existe usuario
    return False

# Función para leer el archivo de políticas de privacidad
def read_privacy_policy():
    """
    Lee el archivo de políticas de privacidad desde la ubicación 'docs/privacy_policy.txt'.
    
    La función intenta abrir y leer el contenido del archivo de texto que contiene la política de privacidad. 
    Si el archivo no se encuentra, devuelve un mensaje de error indicando que la política de privacidad no está disponible.
    
    Returns:
        str: El contenido del archivo de políticas de privacidad como una cadena de texto. Si el archivo no existe, 
        devuelve la cadena "Política de privacidad no disponible".
    
    Exceptions:
        FileNotFoundError: Si el archivo no se encuentra en la ruta especificada, se captura la excepción y 
        se devuelve un mensaje de error amigable.
    """

    # Intenta leer el archivo 
    try:
        with open("docs/privacy_policy.txt", "r", encoding="utf-8") as file:
            return file.read()
    # Si no se puede leer el archivo
    except FileNotFoundError:
        return "Política de privacidad no disponible."

# Función para registrar usuario
def register_user(email: str, password: str, username: str, names: str, lastnames: str):
    """
    Registra un nuevo usuario en el archivo de base de datos de usuarios, siempre y cuando el usuario no exista ya.
    
    Args:
        email (str): Correo electrónico del usuario.
        password (str): Contraseña del usuario.
        username (str): Nombre de usuario elegido.
        names (str): Nombres del usuario.
        lastnames (str): Apellidos del usuario.
    
    Returns:
        bool: Devuelve `True` si el registro fue exitoso, o `False` si ya existe un usuario con el mismo correo electrónico o nombre de usuario.
    
    """
    # Llama la función user_exist para verificar si existe el usuario
    if user_exists(email, username):
        # Ya existe usuario y no se puede registrar
        return False
    with open(USERS_DB_FILE, "a") as file:
        # Registra datos del usuario en la base de datos
        file.write(f"{email},{password},{username},{names},{lastnames}\n")
    return True

# Funcion para autenticar usuario (usada para validar credenciales), retorna los datos
def authenticate_user(email_or_username: str, password: str):
    """
    Autentica un usuario verificando su correo electrónico o nombre de usuario y su contraseña.

    La función busca en la base de datos de usuarios (archivo CSV) para validar las credenciales del usuario.
    Si las credenciales son correctas, devuelve un diccionario con los datos del usuario;
    en caso contrario, devuelve `None`.

    Args:
        email_or_username (str): Correo electrónico o nombre de usuario que se utilizará para la autenticación.
        password (str): Contraseña del usuario.

    Returns:
        dict | None: Un diccionario con los datos del usuario si la autenticación es exitosa. Contiene las claves:
            - "email": Correo electrónico del usuario.
            - "password": Contraseña del usuario (por razones de seguridad, en un sistema real esto se manejaría de otra manera).
            - "username": Nombre de usuario.
            - "names": Nombres del usuario.
            - "lastnames": Apellidos del usuario.
        Retorna `None` si las credenciales no son válidas o el archivo de usuarios no existe.
    """

    # Si no existe el archivo users_db.txt
    if not os.path.exists(USERS_DB_FILE):
        return None
    # Lee el archivo users_db.txt
    with open(USERS_DB_FILE, "r") as file:
        # Itera entre cada linea, separa por comas y elimina espacios en blanco
        for line in file:
            data = line.strip().split(",")
            if len(data) < 5:
                continue
            # Verifica autenticacion exitosa
            if (data[0].lower() == email_or_username.lower() or data[2].lower() == email_or_username.lower()) and data[1] == password:
                return {"email": data[0], "password": data[1], "username": data[2], "names": data[3], "lastnames": data[4]}
    return None

# Función para cambiar contraseña
def change_password(old_password, new_password):
    """
    Cambia la contraseña del usuario actual si la contraseña antigua es correcta.
    
    Args:
        old_password (str): La contraseña actual del usuario que se desea cambiar.
        new_password (str): La nueva contraseña que reemplazará a la anterior.

    Returns:
        bool: Devuelve `True` si la contraseña fue cambiada exitosamente, `False` si la contraseña antigua no coincide o no se pudo realizar el cambio.
    """

    # Almacena lineas del archivo
    users=[]
    password_changed = False

    # Abrir archivo bases de datos
    with open(USERS_DB_FILE, "r") as file: 
        for line in file:
            # Divide la linea por comas y borra espacios en blanco
            parts = line.strip().split(",")
            if len(parts) > 1 and parts[0] == current_user["email"] and parts[1]== old_password:
                #Contraseña antigua coincide, actualizar con la nueva contraseña
                parts[1] = new_password
                password_changed = True
            
            # Une las partes y las añade a la lista
            users.append(",".join(parts)) 
        
        # Sobreescribe el archivo añadiendo las lineas actualizadas
        if password_changed: 
            with open(USERS_DB_FILE, "w") as file:
                for line in users:
                    file.write(line+ "\n") 
        return password_changed

def save_profile_picture(file_path):
    """
    Guarda la imagen de perfil de un usuario, redimensionándola y almacenándola en una ubicación específica.

    Args:
        file_path (str): Ruta del archivo de imagen seleccionado por el usuario.

    Returns:
        bool: Devuelve `True` si la imagen se guardó correctamente, o `False` en caso de error.
    """

    # Obtener usuario actual
    current_user = get_current_user()
    # Si no hay un usuario logeado
    if current_user is None:
        return False
    
    # Crear el nombre del archivo para la imagen de perfil
    username = current_user["username"]
    new_file_name = f"{username}_profile.png"
    
    # Definir la ruta de destino en la carpeta assets
    destination_path = os.path.join("assets/uploads/profile", new_file_name)

    # Tratar de guardar la imagen
    try:
        # Abrir la imagen seleccionada
        with Image.open(file_path) as img:
            # Redimensionar la imagen a un tamaño estándar (por ejemplo, 200x200 píxeles)
            img = img.resize((200, 200))
            
            # Guardar la imagen en formato PNG
            img.save(destination_path, "PNG")
        
        return True
    # Si NO se pudo guardar la imagen
    except Exception as e:
        print(f"Error al guardar la imagen de perfil: {e}")
        return False
    
def save_event_logo(file_path):
    """
    Guarda el logotipo de un evento, asignándole un nombre basado en el siguiente ID disponible.

    Args:
        file_path (str): Ruta del archivo de imagen del logotipo del evento.

    Returns:
        str | None: Devuelve la ruta relativa desde la carpeta 'uploads' donde se guardó el
        logotipo si el proceso fue exitoso, o `None` en caso de error.
    """
    # Carga los eventos actuales llamando la función load_events
    events = load_events()
    # Define el siguiente id disponible    
    next_id = max(events['id']) + 1 if len(events) > 0 else 1
    # Cambiar el nombre del logotico
    new_file_name = f"event_{next_id}.png"

    # Guarda el nuevo nombre del logotipo en la carpeta assets
    destination_path = os.path.join("assets/uploads/events/logos", new_file_name)

    # Intenta guardar el logo
    try:
        # Abrir la imagen seleccionada
        with Image.open(file_path) as img:                      
            # Guardar la imagen en formato PNG
            img.save(destination_path, "PNG")
        
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