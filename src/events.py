#Importar librerias necesarias
import pandas as pd
import os
import geopandas as gdp

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
    Función para añadir un evento nuevo a una base de datos de eventos almacenada en un archivo CSV.

    Args:
        event_id (int): Identificador único del evento.
        name (str): Nombre del evento.
        sport_type (str): Tipo de deporte que se realizará en el evento.
        date (str): Fecha del evento (formato YYYY-MM-DD).
        time (str): Hora de inicio del evento (formato HH:MM).
        place (str): Lugar donde se llevará a cabo el evento.
        city (str): Ciudad donde se realizará el evento.
        latitude (float): Coordenada de latitud del lugar del evento.
        longitude (float): Coordenada de longitud del lugar del evento.
        description (str): Descripción del evento, proporcionando detalles adicionales.
        participation_mode (str): Modalidad de participación, puede ser 'presencial', 'virtual', etc.
        capacity (int): Número máximo de participantes permitidos.
        organizer (str): Nombre del organizador o entidad que organiza el evento.
        registration_fee (str): Costo de inscripción (Gratis o Pago)
        status (str): Estado del evento (Abierto, Cerrado: En curso, Cerrado: Finalizado)
        logo (str): Ruta de la imagen del logo del evento.

    Returns:
        None: La función no retorna ningún valor. Simplemente añade un nuevo evento al archivo CSV.
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

