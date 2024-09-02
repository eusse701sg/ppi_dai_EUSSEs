#Importar librerías necesarias
import os
from PIL import Image
from events import load_events

#Base de datos con Correo, Contraseña, Usuario, Nombres, Apellidos
USERS_DB_FILE = "users_db.txt"
current_user = None

#Definir usuario actual
def set_current_user(user): 
    global current_user
    current_user = user

#Obtener usuario actual
def get_current_user():
    return current_user
   

#Funcion para verificar en la base de datos si existe un usuario, retorna true o false
def user_exists(email: str, username: str) -> bool:
    if not os.path.exists(USERS_DB_FILE):
        return False 
    #Abrir archivo de bases de datos
    with open(USERS_DB_FILE, "r") as file: 
        for line in file:
            data = line.strip().split(",")
            # Comprobar que la línea tiene el número esperado de campos
            if len(data) < 5:
                continue
            # Buscar si el email o el usuario están en alguna linea
            if data[0] == email or data[2] == username:
                #Existe usuario
                return True
    #No existe usuario
    return False

# Función para leer el archivo de políticas de privacidad
def read_privacy_policy():
    try:
        with open("privacy_policy.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Política de privacidad no disponible."


# Función para registrar usuario
def register_user(email: str, password: str, username: str, names: str, lastnames: str):
    if user_exists(email, username):
        # Ya existe usuario y no se puede registrar
        return False
    with open(USERS_DB_FILE, "a") as file:
        # Registra datos del usuario en la base de datos
        file.write(f"{email},{password},{username},{names},{lastnames}\n")
    return True

# Funcion para autenticar usuario (usada para validar credenciales), retorna los datos
def authenticate_user(email_or_username: str, password: str):
    if not os.path.exists(USERS_DB_FILE):
        return None
    with open(USERS_DB_FILE, "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) < 5:
                continue
            # Verifica autenticacion exitosa
            if (data[0] == email_or_username or data[2] == email_or_username) and data[1] == password:
                return {"email": data[0], "password": data[1], "username": data[2], "names": data[3], "lastnames": data[4]}
    return None

# Función para cambiar contraseña
def change_password(old_password, new_password):
    # Almacena lineas del archivo
    users=[]
    password_changed = False

    # Abrir archivo bases de datos
    with open(USERS_DB_FILE, "r") as file: 
        for line in file:
            # Divide la linea en partes
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
    #Obtener usuario actual
    current_user = get_current_user()
    if current_user is None:
        return False
    
    # Crear el nombre del archivo para la imagen de perfil
    username = current_user["username"]
    new_file_name = f"{username}_profile.png"
    
    # Definir la ruta de destino en la carpeta assets
    destination_path = os.path.join("assets/uploads/profile", new_file_name)

    try:
        # Abrir la imagen seleccionada
        with Image.open(file_path) as img:
            # Redimensionar la imagen a un tamaño estándar (por ejemplo, 200x200 píxeles)
            img = img.resize((200, 200))
            
            # Guardar la imagen en formato PNG
            img.save(destination_path, "PNG")
        
        return True
    except Exception as e:
        print(f"Error al guardar la imagen de perfil: {e}")
        return False
    
def save_event_logo(file_path):
    events = load_events()    
    next_id = max(events['id']) + 1 if len(events) > 0 else 1
    new_file_name = f"event_{next_id}.png"

    destination_path = os.path.join("assets/uploads/events/logos", new_file_name)

    try:
        # Abrir la imagen seleccionada
        with Image.open(file_path) as img:                      
            # Guardar la imagen en formato PNG
            img.save(destination_path, "PNG")
        
        return destination_path
    except Exception as e:
        print(f"Error al guardar logo de evento: {e}")
        return None 