import base64
import json
import sys
import yaml

from datetime import datetime as dt
from google.oauth2 import service_account
from googleapiclient.discovery import build
from logger import getLogger

LOGGER = getLogger(__name__)


def filter_events(events_file):
    """Filtra eventos pasados

    Levanta el YAML con eventos para quedarse solamente con los eventos futuros.

    Args:
        events_file (string): path del YAML donde están los eventos.

    Returns:
        dict: diccionario formateado con todos los eventos futuros.
    """

    future_events = {}
    past_events = 0
    failed_events = 0
    failed_event_list = []

    try:
        with open(events_file, "r") as event_list:
            all_events = yaml.safe_load(event_list)
    except FileNotFoundError as e:
        LOGGER.error(f"Archivo {set_bold_text(events_file)} no encontrado.")
        sys.exit(1)

    # Chequeamos que los eventos tengan la fecha correcta y que tengan fecha futura.
    for event in all_events:
        try:
            event_date = dt.strptime(all_events[event]["desde"], "%Y-%m-%d %H:%M")
            dt.strptime(all_events[event]["hasta"], "%Y-%m-%d %H:%M")

            # Si tienen fecha futura los guardamos, sino se descartan.
            if event_date > dt.now():
                future_events[event] = get_calendar_format(all_events[event])
            else:
                past_events += 1

        except ValueError as e:
            failed_events += 1
            failed_event_list.append(event)
            LOGGER.error(
                f"Formato de fecha incorrecto para evento {set_bold_text(event)} ({e})."
            )

    LOGGER.info(
        f"Descartado {set_bold_text(past_events)} evento pasado."
        if past_events == 1
        else f"Descartados {set_bold_text(past_events)} eventos pasados."
    )

    if failed_events > 0:
        LOGGER.warning(
            f"Descartado {set_bold_text(failed_events)} evento por errores en las fechas ({failed_event_list})."
            if failed_events == 1
            else f"Descartados {set_bold_text(failed_events)} eventos por errores en las fechas ({failed_event_list})."
        )

    return future_events


def get_calendar_format(raw_event):
    """Formatea eventos para mandar a la API

    Filtra el dict creado por PyYAML al parsear el YAML con los eventos, y devuelve
    un dict con las keys y values que espera la API de Google Calendar.

    Args:
        raw_event (dict): diccionario generado por PyYAML con eventos.

    Returns:
        dict: diccionario formateado listo para mandar a la API.
    """

    event_content = {
        "summary": raw_event["titulo"],
        "location": raw_event["ubicacion"],
        "description": f"{raw_event['descripcion']}\n\nEvento creado por <a href='https://github.com/sysarmy/disneyland/tree/master/adminbirrator'>Adminbirrator</a> 🍻",
        "start": {
            "dateTime": "T".join(raw_event["desde"].split()) + ":00-03:00",
            "timeZone": "America/Argentina/Buenos_Aires",
        },
        "end": {
            "dateTime": "T".join(raw_event["hasta"].split()) + ":00-03:00",
            "timeZone": "America/Argentina/Buenos_Aires",
        },
    }

    return event_content


def get_calendar_service(creds_file):
    """Autentica con Google Calendar

    Le pega al servicio de autenticación de Google Calendar para traerse
    un servicio que pueda interactuar con el Calendar. Espera una string
    que es una base64 de las credenciales que devuelve la GCP console
    cuando se crea la service account.

    Args:
        creds_file (str): base64 del JSON que devuelve GCP console para
            la service acccount. Es un base64 no por seguridad sino por
            comodidad para crear solo una variable en el secrets de GH.

    Returns:
        googleapiclient.discovery.Resource: servicio ya autenticado
            para pegarle a la API de Calendar.
    """

    try:
        creds = service_account.Credentials.from_service_account_info(
            json.loads(base64.b64decode(creds_file).decode("utf-8")),
            scopes=["https://www.googleapis.com/auth/calendar"],
        )

        service = build("calendar", "v3", credentials=creds, cache_discovery=False)

        LOGGER.info("Autenticación exitosa con API de Google Calendar.")

        return service

    except TypeError as e:
        LOGGER.error(
            f"No se pudo autenticar con API de Google Calendar. Chequeá la variable de entorno {set_bold_text('$ADMINBIRRATOR_CREDENTIALS')} ({e})."
        )
        sys.exit(1)
    except Exception as e:
        LOGGER.error(f"No se pudo autenticar con API de Google Calendar ({e}).")
        sys.exit(1)


def parse_api_response(event_info, response, update):
    """Desglosa la API response de Calendar

    Cada vez que le pegamos a la API de Calendar nos devuelve un choclo, lo
    parseamos con información del evento en cuestión para el logger.

    Args:
        event_info (dict): diccionario con toda la información del evento enviado.
        response (JSON): respuesta de la API.
        update (bool): especifica si se le pegó a la API para updatear un evento.
    """

    if response["status"] == "confirmed":
        LOGGER.info(
            f"Evento {set_bold_text(event_info['summary'])} del día {set_bold_text(event_info['start']['dateTime'].split('T')[0])} a las {event_info['start']['dateTime'].split('T')[1][:5]}hs {'actualizado' if update else 'creado'} exitosamente."
        )
    else:
        LOGGER.error(
            f"No se pudo crear evento {set_bold_text(event_info['summary'])} T_T Error:\n{'#'*80}\n\n{response}\n\n{'#'*80}"
        )


def set_bold_text(text):
    return f"\033[1m{text}\033[0;0m"
