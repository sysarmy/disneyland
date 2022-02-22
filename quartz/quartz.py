#!/usr/bin/env python3

from icmplib import ping
import json
import logging
import requests
from requests.structures import CaseInsensitiveDict
from pathlib import Path
import configparser
import argparse
import sys
import subprocess
import shlex
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

CONFIG_DIR = Path.home()/'.config'
CONFIG_FILE = CONFIG_DIR/'quartz.conf'
DEFAULT_API_KEY = 'XXXXXX'
DEFAULT_URL = 'https://xxxxxxxx'
DEFAULT_ISP = 'Nombre del ISP (Fibertel, Telecentro, etc.)'
LOGGER = logging.getLogger("quartz")

def loglevel_validator(v):
    """Validate selected log level. Return v.upper() or raise an error."""
    if v.upper() not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
        raise argparse.ArgumentTypeError(
            'Log level must be a valid Python log level. See -h for details.'
        )
    else:
        return v.upper()


def setup_logging(log_level):
    logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=log_level, format=logformat)

def generate_config():
    if not CONFIG_DIR.exists():
        LOGGER.info(f'Creando {CONFIG_DIR} ya que no existe.')
        CONFIG_DIR.mkdir()
    if not CONFIG_FILE.exists():
        config = configparser.ConfigParser()
        config['quartz'] = {}
        config['quartz']['api_key'] = DEFAULT_API_KEY
        config['quartz']['url'] = DEFAULT_URL
        config['quartz']['isp'] = DEFAULT_ISP
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        LOGGER.info(f'Creando {CONFIG_FILE} ya que no existe.')
        LOGGER.warning(
            f'{CONFIG_FILE} se creó con valores dummy. ' 
            'Corregir con el isp, url y api_key correctos.'
        )
        return True
    return False

def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        if (
        config['quartz']['api_key'] == DEFAULT_API_KEY or
        config['quartz']['url'] == DEFAULT_URL or
        config['quartz']['isp'] == DEFAULT_ISP
        ):
            LOGGER.error(f'El archivo {CONFIG_FILE} tiene valores dummy.')
            if os.environ.get('EXECUTION_ENV') == "DOCKER":
                LOGGER.error(f'Revisá haber pasado las variables de entorno correctas al docker run.')
            sys.exit(1)
    except KeyError:
        LOGGER.error(f'El archivo {CONFIG_FILE} es inválido (está vacío?).')
        sys.exit(2)
    return config

def ping_host(hostname):
    if os.geteuid() == 0:
        host = ping(hostname, count=3, privileged=True)
        return {
                'anchor': hostname.split('.')[0],
                'min_rtt': host.min_rtt,
                'max_rtt': host.max_rtt,
                'jitter': host.jitter,
                'packet_loss': host.packet_loss
        }
    else:
        p = subprocess.Popen(
            shlex.split(f'ping -c3 {hostname}'),
            stdout=subprocess.PIPE
        )
        output = p.stdout.read()
        for line in output.decode('utf-8').split('\n'):
            if 'packets transmitted' in line:
                transmitted = line
            if line.startswith('rtt min'):
                rtt = line
        packet_loss = float(transmitted.split(',')[2].split('%')[0].strip())
        min_rtt, _, max_rtt, jitter = map(
            float, rtt.split('=')[1].strip().split(' ')[0].split('/')
        )
        return {
                'anchor': hostname.split('.')[0],
                'min_rtt': min_rtt,
                'max_rtt': max_rtt,
                'jitter': jitter,
                'packet_loss': packet_loss
        }
                
def run(config, args):
    response = {
        "id": config['quartz']['api_key'].split('-')[0], 
        "isp": config['quartz']['isp'], 
        'measurements': []
    }
    hosts = [
        'fr-sxb-as8839.anchors.atlas.ripe.net',
        'us-mia-as15133.anchors.atlas.ripe.net',
        'us-qas-as15169.anchors.atlas.ripe.net',
        'br-sao-as16509.anchors.atlas.ripe.net',
        'au-syd-as16509.anchors.atlas.ripe.net',
        'fr-lio-as41405.anchors.atlas.ripe.net',
        'uy-mvd-as28000.anchors.atlas.ripe.net'
    ]
    # tirarle ping a 3 anchors US,EU,APAC
    # buildear el json
    if args.parallel:
        max_workers = len(hosts)
    else:
        max_workers=1
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ping = {
            executor.submit(ping_host, hostname): hostname for hostname in hosts
        }
        for future in as_completed(future_to_ping):
            try:
                response['measurements'].append(future.result())
            except Exception as exc:
                logger.error(f'Se rompió todo MAL. {exc}')
    url = config['quartz']['url']
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["api_key"] = config['quartz']['api_key']
    LOGGER.info(f'Subiendo datos a {url}.')
    LOGGER.debug(f' Datos a subir: {response}')
    if not args.read_only:
        resp = requests.post(url, headers=headers, data=json.dumps(response))
        LOGGER.info(f'Datos subidos. Status code: {resp.status_code}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f'Quartz')
    parser.add_argument(
        '-l', '--log-level',
        metavar='level',
        type=loglevel_validator,
        default='INFO',
        help='El log level. Puede ser cualquiera de los niveles estándares ' +
        'de Python: CRITICAL, ERROR, WARNING, INFO, DEBUG.'
    )
    parser.add_argument(
        '-s', '--silent',
        action='store_true',
        help='No generar logs. Útil para correr desde cron.'
    )
    parser.add_argument(
        '-p', '--parallel',
        action='store_true',
        help='Ejecuta las mediciones en paralelo. Time is money!'
    )
    parser.add_argument(
        '-r', '--read-only',
        action='store_true',
        help='No sube datos. Útil para debuggear qué se subiría.'
    )
    args = parser.parse_args()
    if args.silent:
        args.log_level = 'ERROR'
    setup_logging(args.log_level)
    if generate_config():
        sys.exit(0)
    config = read_config()
    run(config, args)
