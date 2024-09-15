#Importar librerias necesarias
import pandas as pd
import os
import json

# Ruta en la que se guardan los eventos tipo csv
csv_path = 'data/events.csv'

# Función para cargar los eventos
def load_events():
    """
    Función para cargar los eventos.

    Returns:
        df (DataFrame)              
    """     
    # Si existe el csv con los eventos
    if os.path.exists(csv_path):
        # Leer csv
        df = pd.read_csv(csv_path)
        # Retornar dataframe
        return df

    # Si no existe el csv, crear uno nuevo con los indices de los eventos
    else:
        # Indices
        columns = [
            'id', 'nombre', 'tipo_deporte', 'fecha', 'hora',
            'lugar', 'ciudad', 'latitud', 'longitud',
            'descripcion', 'modalidad_participacion', 'capacidad',
            'organizador', 'costo_inscripcion', 'estado', 'logo',
            'inscritos', 'usuarios_inscritos'
        ]
        # Convertir a dataframe
        df = pd.DataFrame(columns=columns)
        # Convertir a csv
        df.to_csv(csv_path, index=False)
        return df

# Función para añadir un evento nuevo
def add_event(event_id, name, sport_type, date, time, place, city, latitude, longitude, description, participation_mode, capacity, organizer, registration_fee, status, logo):
    """
    Función para modificar un evento existente en una base de datos de eventos almacenada en un archivo CSV.

    Args:
        event_id (int): Identificador único del evento que se desea modificar.
        name (str): Nuevo nombre del evento.
        sport_type (str): Tipo de deporte que se realizará en el evento.
        date (str): Nueva fecha del evento (formato YYYY-MM-DD).
        time (str): Nueva hora de inicio del evento (formato HH:MM).
        place (str): Nuevo lugar donde se llevará a cabo el evento.
        city (str): Nueva ciudad donde se realizará el evento.
        latitude (float): Nueva coordenada de latitud del lugar del evento.
        longitude (float): Nueva coordenada de longitud del lugar del evento.
        description (str): Nueva descripción del evento, proporcionando detalles adicionales.
        participation_mode (str): Nueva modalidad de participación (por ejemplo, 'presencial', 'virtual').
        capacity (int): Nueva capacidad máxima de participantes permitidos.
        registration_fee (str): Nuevo costo de inscripción (por ejemplo, 'Gratis' o 'Pago').
        status (str): Nuevo estado del evento (por ejemplo, 'Abierto', 'Cerrado', 'En curso').
        logo (str): Nueva ruta del archivo de la imagen del logo del evento.    

    Returns:
        None: La función no retorna ningún valor. Simplemente modifica el evento existente y guarda los cambios en el archivo CSV.
    """

    # Llama la función load_events para cargar los eventos actuales
    df = load_events()
    # Se define un nuevo evento con los parámetros diligenciados en la función
    new_event = {
        'id': event_id,
        'nombre': name,
        'tipo_deporte': sport_type,
        'fecha': date,
        'hora': time,
        'lugar': place,
        'ciudad': city,
        'latitud': latitude,
        'longitud': longitude,        
        'descripcion': description,
        'modalidad_participacion': participation_mode,
        'capacidad': capacity,
        'organizador': organizer,
        'costo_inscripcion': registration_fee,  
        'estado': status,      
        'logo': logo,
        'inscritos': 0, # Se inicializa en 0 inscritos
        'usuarios_inscritos': json.dumps([]) # Lista vacía como string JSON
    }
    # Añade al final del dataframe el nuevo evento
    df.loc[len(df)] = new_event

    # Guardar en archivo csv
    df.to_csv(csv_path, index=False)

# Función para modificar un evento existente
def modify_event(event_id, name, sport_type, date, time, place, city, latitude, longitude, description, participation_mode, capacity, registration_fee, status, logo):
    """
    Función para modificar un evento existente en una base de datos de eventos almacenada en un archivo CSV.

    Args:
        event_id (int): Identificador único del evento que se desea modificar.
        name (str): Nuevo nombre del evento.
        sport_type (str): Tipo de deporte que se realizará en el evento.
        date (str): Nueva fecha del evento (formato YYYY-MM-DD).
        time (str): Nueva hora de inicio del evento (formato HH:MM).
        place (str): Nuevo lugar donde se llevará a cabo el evento.
        city (str): Nueva ciudad donde se realizará el evento.
        latitude (float): Nueva coordenada de latitud del lugar del evento.
        longitude (float): Nueva coordenada de longitud del lugar del evento.
        description (str): Nueva descripción del evento, proporcionando detalles adicionales.
        participation_mode (str): Nueva modalidad de participación.
        capacity (int): Nueva capacidad máxima de participantes permitidos.
        registration_fee (str): Nuevo costo de inscripción (por ejemplo, 'Gratis' o 'Pago').
        status (str): Nuevo estado del evento (por ejemplo, 'Abierto', 'Finalizado', 'En curso').
        logo (str): Nueva ruta del archivo de la imagen del logo del evento.

    Returns:
        None: La función no retorna ningún valor. Simplemente modifica el evento existente y guarda los cambios en el archivo CSV.
    """

    # Llama la función load_events para obtener el dataframe con todos los eventos
    df = load_events()
    # Modifica los valores correspondientes al evento con el id especificado
    df.loc[df['id'] == event_id, 'nombre'] = name
    df.loc[df['id'] == event_id, 'tipo_deporte'] = sport_type
    df.loc[df['id'] == event_id, 'fecha'] = date
    df.loc[df['id'] == event_id, 'hora'] = time
    df.loc[df['id'] == event_id, 'lugar'] = place
    df.loc[df['id'] == event_id, 'ciudad'] = city
    df.loc[df['id'] == event_id, 'latitud'] = latitude
    df.loc[df['id'] == event_id, 'longitud'] = longitude
    df.loc[df['id'] == event_id, 'descripcion'] = description
    df.loc[df['id'] == event_id, 'modalidad_participacion'] = participation_mode
    df.loc[df['id'] == event_id, 'capacidad'] = capacity
    df.loc[df['id'] == event_id, 'costo_inscripcion'] = registration_fee
    df.loc[df['id'] == event_id, 'estado'] = status
    df.loc[df['id'] == event_id, 'logo'] = logo

    # Guardar los cambios en el archivo csv
    df.to_csv(csv_path, index=False)

# Función para inscribir un usuario a un evento
def inscribe_user(event_id, username):
    """
    Función para inscribir un usuario a un evento.

    Args:
        event_id (int): ID del evento.
        username (str): Nombre de usuario a inscribir.

    Returns:
        bool: True si la inscripción fue exitosa, False si no.
    """
    # Cargar eventos como un dataframe
    df = load_events()
    # Asigna los indices
    event_index = df.index[df['id'] == event_id].tolist()[0]
    
    # Si la cantidad de inscritos es mayor o igual a la capacidad del evento retorna False
    if df.at[event_index, 'inscritos'] >= df.at[event_index, 'capacidad']:
        return False
    
    # Carga un json con los usuarios inscritos
    usuarios_inscritos = json.loads(df.at[event_index, 'usuarios_inscritos'])
    # Si el usuario no está en los usuarios inscritos
    if username not in usuarios_inscritos:
        # Añade el usuario a los usuarios inscritos
        usuarios_inscritos.append(username)
        # Accede a los usuarios inscritos y los convierte en una cadena de texto
        df.at[event_index, 'usuarios_inscritos'] = json.dumps(usuarios_inscritos)
        # Aumenta la cantidad de inscritos en 1
        df.at[event_index, 'inscritos'] += 1
        
        # Si los inscritos es mayor o igual a la capacidad el estado del evento pasa a "En curso"
        if df.at[event_index, 'inscritos'] >= df.at[event_index, 'capacidad']:
            df.at[event_index, 'estado'] = 'En curso'
        
        # Pasar dataframe al csv
        df.to_csv(csv_path, index=False)
        return True
    return False

# Función para desinscribir un usuario de un evento
def uninscribe_user(event_id, username):
    """
    Función para desinscribir un usuario de un evento.

    Args:
        event_id (int): ID del evento.
        username (str): Nombre de usuario a desinscribir.

    Returns:
        bool: True si la desinscripción fue exitosa, False si no.
    """
    # Carga los eventos como un dataframe
    df = load_events()
    # Especifica el indice
    event_index = df.index[df['id'] == event_id].tolist()[0]
    
    # Carga los usuarios inscritos como un json
    usuarios_inscritos = json.loads(df.at[event_index, 'usuarios_inscritos'])
    # Si el usuario está en usuarios inscritos
    if username in usuarios_inscritos:
        # Remueve el usuario de los usuarios inscritos
        usuarios_inscritos.remove(username)
        # Convierte los usuarios inscritos en una cadena de texto
        df.at[event_index, 'usuarios_inscritos'] = json.dumps(usuarios_inscritos)
        # Cambia la cantida de inscritos en -1
        df.at[event_index, 'inscritos'] -= 1
        
        # Si el estado del evento está en curso y los inscritos son menor igual a capacidad el estado se revierte a Abierto
        if df.at[event_index, 'estado'] == 'En curso' and df.at[event_index, 'inscritos'] < df.at[event_index, 'capacidad']:
            df.at[event_index, 'estado'] = 'Abierto'
        
        # Convertir dataframe al csv
        df.to_csv(csv_path, index=False)
        return True
    return False

# Función para obtener los eventos en los que un usuario está inscrito
def get_user_events(username):
    """
    Función para obtener todos los eventos en los que un usuario está inscrito.

    Args:
        username (str): Nombre de usuario.

    Returns:
        list: Lista de eventos en los que el usuario está inscrito.
    """
    # Carga los eventos como un dataframe
    df = load_events()
    # Filtra los eventos en los cuales el nombre de usuario está contenido
    user_events = df[df['usuarios_inscritos'].apply(lambda x: username in json.loads(x))]
    # Retorna una lista de eventos en los que el usuario está inscrito
    return user_events.to_dict('records')
