import os

USERS_DB_FILE = "users_db.txt" #Base de datos con Correo, Contraseña, Usuario, Nombres, Apellidos
current_user = None

def set_current_user(user): #Definir usuario actual
    global current_user
    current_user = user

def get_current_user(): #Obtener usuario actual
    return current_user

def read_policy_text(): #Funcion para leer archivo de politica de privacidad
    with open("privacy_policy.txt", "r") as file:
        return file.read()

def user_exists(email: str, username: str) -> bool: #Funcion para verificar en la base de datos si existe un usuario, retorna true o false
    if not os.path.exists(USERS_DB_FILE):
        return False 
    with open(USERS_DB_FILE, "r") as file: #Abrir archivo de bases de datos
        for line in file:
            data = line.strip().split(",")
            if len(data) < 5:  # Comprobar que la línea tiene el número esperado de campos
                continue
            if data[0] == email or data[2] == username: #Buscar si el email o el usuario están en alguna linea
                return True #Existe usuario
    return False #No existe usuario

def register_user(email: str, password: str, username: str, names: str, lastnames: str): #Función para registrar usuario
    if user_exists(email, username):
        return False #Ya existe usuario y no se puede registrar
    with open(USERS_DB_FILE, "a") as file:
        file.write(f"{email},{password},{username},{names},{lastnames}\n") #Registra datos del usuario en la base de datos
    return True

def authenticate_user(email_or_username: str, password: str): #Funcion para autenticar usuario (usada para validar credenciales), retorna los datos
    if not os.path.exists(USERS_DB_FILE):
        return None
    with open(USERS_DB_FILE, "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) < 5:
                continue
            if (data[0] == email_or_username or data[2] == email_or_username) and data[1] == password: #Verifica autenticacion exitosa
                return {"email": data[0], "password": data[1], "username": data[2], "names": data[3], "lastnames": data[4]}
    return None

def change_password(old_password, new_password):

    users=[] #Almacena lineas del archivo
    password_changed = False

    with open(USERS_DB_FILE, "r") as file: #Abrir archivo bases de datos
        for line in file:
            parts = line.strip().split(",") #Divide la linea en partes
            if len(parts) > 1 and parts[0] == current_user["email"] and parts[1]== old_password:
                #Contraseña antigua coincide, actualizar con la nueva contraseña
                parts[1] = new_password
                password_changed = True
            
            users.append(",".join(parts)) #Une las partes y las añade a la lista
        
        if password_changed: #Sobreescribe el archivo añadiendo las lineas actualizadas
            with open(USERS_DB_FILE, "w") as file:
                for line in users:
                    file.write(line+ "\n") 
        return password_changed

