import os
import sys

from datetime import datetime as dt
from googleapiclient import errors as googleErrors
from helpers import (
    filter_events,
    get_calendar_service,
    parse_api_response,
    set_bold_text,
)
from logger import getLogger


def check_existing_events(yaml_future_events, calendar_future_events, api_service):
    """Chequea si tiene que crear, updatear, o ignorar eventos del YAML.

    The truth of the milanesa, descarga eventos ya registrados en el
    Calendar y los cruza contra los eventos del YAML, para descartar la
    creación de eventos duplicados (que ya estén en Calendar con el mismo
    nombre y la misma fecha) y para actualizaciones (que estén el mismo
    día pero diferente hora de inicio).

    Args:
        yaml_future_events (dict): diccionario con todos los eventos futuros.
        api_service (googleapiclient.discovery.Resource): servicio ya
            autenticado para pegarle a la API de calendar.

    Returns:
        new_events (dict): eventos nuevos para crear.
        updated_events (dict): eventos que se van a actualizar.
    """

    duplicated_events = 0

    new_events = {}
    updated_events = {}

    if len(calendar_future_events) == 0:
        return yaml_future_events, updated_events

    for event in yaml_future_events:

        yaml_event = yaml_future_events[event]
        is_new_event = True

        for set_event in calendar_future_events:
            calendar_event = {
                key: set_event[key]
                for key in ["summary", "location", "description", "start", "end"]
            }

            # Si el evento del YAML tiene los mismos campos, marcamos como duplicado.
            if yaml_event == calendar_event:
                duplicated_events += 1
                is_new_event = False
                break
            # Si el evento del YAML tiene mismo título y fecha pero diferente contenido,
            # lo updateamos.
            elif (
                # Mismo título
                yaml_event["summary"] == calendar_event["summary"]
                and yaml_event["start"]["dateTime"][:10]
                # Mismo día de inicio
                == calendar_event["start"]["dateTime"][:10]
                and (
                    yaml_event["location"]
                    != calendar_event["location"]  # Diferente ubicación
                    or yaml_event["description"]
                    != calendar_event["description"]  # Diferente descripción
                    or yaml_event["start"]["dateTime"]
                    # Diferente hora de inicio
                    != calendar_event["start"]["dateTime"]
                    or yaml_event["end"]["dateTime"]
                    # Diferente fecha/hora de fin
                    != calendar_event["end"]["dateTime"]
                )
            ):
                updated_events[event] = {
                    **{"id": set_event["id"]}, **yaml_event}
                is_new_event = False
                break
        # Sino, no se actualiza el flag y queda como evento nuevo.
        if is_new_event:
            new_events[event] = yaml_future_events[event]

    if duplicated_events > 0:
        LOGGER.info(
            f"Descartado {set_bold_text(duplicated_events)} evento futuro por ya estar registrado en el Calendar."
            if duplicated_events == 1
            else f"Descartados {set_bold_text(duplicated_events)} eventos futuros por ya estar registrados en el Calendar."
        )

    return new_events, updated_events


def get_calendar_future_events(api_service):
    """Se trae todos los eventos del calendario de Sysarmy.

    Args:
        api_service (googleapiclient.discovery.Resource): servicio ya autenticado para
            pegarle a la API de calendar.

    Returns:
        list: lista de diccionarios con los eventos futuros ya registrados en el Calendar.
    """

    page_token = None
    future_set_events = []

    while True:
        try:
            set_events = (
                api_service.events()
                .list(calendarId=ADMINBIRRATOR_CALENDAR_ID, pageToken=page_token)
                .execute()
            )
        except TypeError as e:
            LOGGER.error(
                f"Calendar ID incorrecto. Chequear variable de entorno {set_bold_text('$ADMINBIRRATOR_CALENDAR_ID')}. {e}"
            )
            sys.exit(1)
        except googleErrors.HttpError as e:
            LOGGER.error(
                f"Calendar ID incorrecto. Chequeá bien las fechas y que la service account tenga acceso al calendar seteado en {set_bold_text('$ADMINBIRRATOR_CALENDAR_ID')} ({e})."
            )
            sys.exit(1)
        # La idea general es crear eventos nuevos y updatear los ya existentes,
        # así que solo nos quedamos con los eventos futuros.
        for event in set_events["items"]:
            try:
                event_start_date = dt.strptime(
                    event["start"]["dateTime"][:19],
                    "%Y-%m-%dT%H:%M:%S",
                )
            except KeyError:
                event_start_date = dt.strptime(
                    event["start"]["date"][:19],
                    "%Y-%m-%d",
                )
            if event_start_date > dt.now():
                future_set_events.append(event)

        # La misma response de la API te da un token para la próx page, creo
        # que te trae de a 25 eventos por default. Habría que jugar para ver
        # si puede traer solo los futuros que son los que nos interesan.
        page_token = set_events.get("nextPageToken")

        if not page_token:
            break

    return future_set_events


def create_event(event, api_service, update=False):
    """Le pega a la API de Calendar y crea o actualiza un evento

    Args:
        event (dict): diccionario con el formato listo para pegarle a la API.
        api_service (googleapiclient.discovery.Resource): servicio ya autenticado
            para pegarle a la API de calendar.
        update (bool, optional): establece si se está actualizando un evento.
            Está en False por defecto.
    """

    try:
        if update:
            response = (
                api_service.events()
                .update(
                    calendarId=ADMINBIRRATOR_CALENDAR_ID,
                    eventId=event["id"],
                    body={key: event[key] for key in event if key != "id"},
                )
                .execute()
            )
        else:
            response = (
                api_service.events()
                .insert(calendarId=ADMINBIRRATOR_CALENDAR_ID, body=event)
                .execute()
            )
        parse_api_response(event, response, update)
    except TypeError as e:
        LOGGER.error(
            f"Calendar ID incorrecto. Chequear variable de entorno {set_bold_text('$ADMINBIRRATOR_CALENDAR_ID')}. {e}"
        )
        sys.exit(1)
    except googleErrors.HttpError as e:
        LOGGER.error(
            f"Calendar ID incorrecto. Chequeá bien las fechas y que la service account tenga acceso al calendar seteado en {set_bold_text('$ADMINBIRRATOR_CALENDAR_ID')} ({e})."
        )
        sys.exit(1)


def clean_orphans(yaml_future_events, api_service):
    """Elimina eventos futuros que no estén en el YAML

    Se fija que todos los eventos que aparecen registrados en el Calendar
    estén con el mismo nombre y fechas que en el YAML, y sino los borra.

    Args:
        yaml_future_events (dict): eventos futuros en el YAML.
        api_service (googleapiclient.discovery.Resource): servicio ya autenticado
            para pegarle a la API de calendar.
    """

    calendar_future_events = get_calendar_future_events(api_service)

    LOGGER.info("Buscando eventos huérfanos no registrados en el YAML...")

    events_to_delete = []

    for calendar_event in calendar_future_events:

        event_exists = False

        calendar_future_event = {
            "id": calendar_event["id"],
            "summary": calendar_event["summary"],
            "startDateTime": calendar_event["start"]["dateTime"],
            "endDateTime": calendar_event["end"]["dateTime"],
        }

        for yaml_event in yaml_future_events:

            event = yaml_future_events[yaml_event]

            if (
                event["summary"] == calendar_future_event["summary"]
                and event["start"]["dateTime"] == calendar_future_event["startDateTime"]
                and event["end"]["dateTime"] == calendar_future_event["endDateTime"]
            ):
                event_exists = True
                break

        if not event_exists:
            events_to_delete.append(calendar_future_event)

    if len(events_to_delete) == 0:
        LOGGER.info(
            "No se encontraron eventos huérfanos a eliminar del Calendar.")

    if len(events_to_delete) > 0:
        LOGGER.warning(
            f"Detectado {set_bold_text(len(events_to_delete))} evento huérfano que será eliminado del Calendar."
            if len(events_to_delete) == 1
            else f"Detectados {set_bold_text(len(events_to_delete))} eventos huérfanos que serán eliminados del Calendar."
        )

        for event in events_to_delete:
            LOGGER.warning(
                f"Eliminando evento {set_bold_text(event['summary'])} del {set_bold_text(event['startDateTime'][:10])} a las {event['startDateTime'][11:16]}hs..."
            )
            api_service.events().delete(
                calendarId=ADMINBIRRATOR_CALENDAR_ID, eventId=event["id"]
            ).execute()


if __name__ == "__main__":

    LOGGER = getLogger("main")

    LOGGER.info(
        """Comenzando ejecución...
        
         _       _           _       _     _                _
        / \   __| |_ __ ___ (_)_ __ | |__ (_)_ __ _ __ __ _| |_ ___  _ __
       / _ \ / _` | '_ ` _ \| | '_ \| '_ \| | '__| '__/ _` | __/ _ \| '__|
      / ___ \ (_| | | | | | | | | | | |_) | | |  | | | (_| | || (_) | |
     /_/   \_\__,_|_| |_| |_|_|_| |_|_.__/|_|_|  |_|  \__,_|\__\___/|_|
    """
    )

    ADMINBIRRATOR_CALENDAR_ID = os.getenv("ADMINBIRRATOR_CALENDAR_ID")
    SERVICE = get_calendar_service(os.environ.get("ADMINBIRRATOR_CREDENTIALS"))

    yaml_future_events = filter_events("adminbirrator/events.yaml")
    calendar_future_events = get_calendar_future_events(SERVICE)

    if len(yaml_future_events) == 0:
        LOGGER.info("No se crearon ni actualizaron eventos.")
    else:

        new_events, updated_events = check_existing_events(
            yaml_future_events, calendar_future_events, SERVICE
        )

        if len(updated_events) > 0:
            LOGGER.info(
                f"Actualizando {set_bold_text(len(updated_events))} evento creado en el calendario..."
                if len(updated_events) == 1
                else f"Actualizando {set_bold_text(len(updated_events))} eventos creados en el calendario..."
            )
            for event in updated_events:
                LOGGER.info(f"Actualizando evento {set_bold_text(event)}...")
                create_event(updated_events[event], SERVICE, update=True)
        else:
            LOGGER.info("No se actualizaron eventos existentes.")

        if len(new_events) > 0:
            LOGGER.info(
                f"Creando {set_bold_text(len(new_events))} evento nuevo en el calendario..."
                if len(new_events) == 1
                else f"Creando {set_bold_text(len(new_events))} eventos nuevos en el calendario..."
            )
            for event in new_events:
                LOGGER.info(f"Creando evento {set_bold_text(event)}...")
                create_event(new_events[event], SERVICE)
        else:
            LOGGER.info("No se crearon nuevos eventos.")

    clean_orphans(yaml_future_events, SERVICE)

    LOGGER.info(
        """Ejecución finalizada.
    
    🤖 My job here is done ¯\_(ツ)_/¯
    🤖 Owner root@sysarmy.com
    """
    )
