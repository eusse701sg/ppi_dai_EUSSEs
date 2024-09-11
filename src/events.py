#Importar librerias necesarias
import pandas as pd
import os

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
            'organizador', 'costo_inscripcion', 'estado', 'logo'
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
        'logo': logo
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
    # Modifica los valores correspondientes al revento con el id especificado
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