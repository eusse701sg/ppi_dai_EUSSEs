#Importar librerias necesarias
import pandas as pd
import os
import geopandas as gdp
import folium
import geopy

def load_events():
    # Si existe el csv con los eventos
    if os.path.exists('events.csv'):
        df = pd.read_csv('events.csv')
        return df

    # Si no existe el csv, crear uno nuevo con 2 eventos base
    else:
        events = {
            'id': [1,2],
            'nombre': ['Sustentacion Aplicación','Torneo Facultades UNAL MED'],
            'tipo_deporte': ['Desarrollo de Software', 'Fútbol'],
            'fecha': ['2024-09-02', '2024-09-05'],
            'hora': ['13:00','15:00'],
            'lugar': ['Facultad de Minas','Universidad Nacional Sede Medellin'],
            'ciudad': ['Medellin', 'Medellin'],
            'latitud': [6.274735919691621, 6.276041317998357],
            'longitud': [-75.59260007551988, -75.58972311540006],            
            'descripcion': ['Sustentación de la aplicación Sportex en el aula de clase', 'Torneo de Futbol entre todas las facultades de la UnalMed'],
            'modalidad_participacion': ['Individual','Equipos'],
            'capacidad': [20, 8],
            'organizador': ['seusse', 'seusse'],
            'costo_inscripcion': ['Gratis', 'Gratis'],            
            'logo': ['assets/uploads/events/logos/event_1.png', 'assets/uploads/events/logos/event_2.png']
        }
        df = pd.DataFrame(events)
        df.to_csv('events.csv', index= False)
        return df

def add_event(event_id, name, sport_type, date, time, place, city, latitude, longitude, description, participation_mode, capacity, organizer, registration_fee, logo):
    df = load_events()
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
        'logo': logo
    }
    df.loc[len(df)] = new_event

    # Guardar en archivo csv
    df.to_csv('events.csv', index=False)

